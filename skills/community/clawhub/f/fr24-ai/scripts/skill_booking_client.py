#!/usr/bin/env python3
"""预订 CLI：parse-passengers / verify / order（对齐 fr_newapi_flight_mcp 流程）。"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
for p in (_ROOT, _SCRIPTS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from config import (  # noqa: E402
    BOOKING_CONTEXT_FILE,
    PASSENGERS_FILE,
    PENDING_PAYLOAD_FILE,
    booking_config_required_envelope,
    is_newapi_configured,
)
from booking_format import (  # noqa: E402
    format_order_data,
    format_verify_data,
    wrap_order,
    wrap_verify,
)
from booking_guidance import (  # noqa: E402
    PASSENGER_CONFIRM_PHRASE,
    passenger_confirmation_required_payload,
    passenger_not_confirmed_payload,
    passenger_required_payload,
    order_not_confirmed_payload,
)
from newapi_client import booking, pricing  # noqa: E402
from output_export import (  # noqa: E402
    failure_envelope,
    passengers_agent_only,
    passengers_user_view,
    wrap_config_required,
    wrap_envelope,
)
from passenger_display import build_contact_display, build_passenger_display, format_display_message  # noqa: E402
from pax_info_parser import parse_passengers_and_contact  # noqa: E402


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_parse_passengers(text: str) -> dict:
    if not is_newapi_configured():
        return wrap_config_required(
            "parse-passengers",
            booking_config_required_envelope("parse-passengers", step="booking"),
        )
    passengers, contact, raw_mappings, contact_raw, err = parse_passengers_and_contact(text)
    if err:
        return failure_envelope(
            "parse-passengers",
            err,
            agent_only={**passenger_required_payload(), "error": err},
        )
    if not contact:
        return failure_envelope("parse-passengers", "请补充联系人：姓名、手机、邮箱")

    p_disp = build_passenger_display(passengers, raw_mappings=raw_mappings)
    c_disp = build_contact_display(contact, raw=contact_raw)
    msg = format_display_message(p_disp, c_disp)
    preview = passenger_confirmation_required_payload(
        passenger_display=p_disp,
        contact_display=c_disp,
        display_message=msg,
    )
    preview["success"] = True
    preview["passengers"] = passengers
    preview["agentContact"] = contact
    preview["passengerRawMappings"] = raw_mappings
    preview["contactRaw"] = contact_raw
    preview["confirmPhrase"] = PASSENGER_CONFIRM_PHRASE

    _save_json(
        PASSENGERS_FILE,
        {
            "passengers": passengers,
            "agentContact": contact,
            "passengerRawMappings": raw_mappings,
            "contactRaw": contact_raw,
        },
    )

    return wrap_envelope(
        action="parse-passengers",
        status="success",
        user_view=passengers_user_view(preview),
        agent_only=passengers_agent_only(preview),
        message=msg,
    )


def cmd_verify(args: argparse.Namespace) -> dict:
    if not is_newapi_configured():
        return wrap_config_required("verify", booking_config_required_envelope("verify", step="verify"))

    if not args.passenger_confirmed:
        payload = passenger_not_confirmed_payload()
        return failure_envelope("verify", payload["message"], agent_only=payload)

    ctx = _load_json(Path(args.context_file))
    pax_file = Path(args.passengers_file)
    pax_data = _load_json(pax_file)
    passengers = pax_data.get("passengers") or []
    agent_contact = pax_data.get("agentContact") or {}
    if not passengers or not agent_contact:
        return failure_envelope(
            "verify",
            "请先完成乘客信息核对（parse-passengers）。",
            agent_only={"detail": "passengers.json 缺少 passengers 或 agentContact"},
        )

    offer_id = args.offer_id or (ctx.get("selectedOffer") or {}).get("offerId")
    if not offer_id:
        return failure_envelope(
            "verify",
            "请先选择直飞或中转报价后再校验。",
            agent_only={"detail": "缺少 offer_id / selectedOffer"},
        )

    payload = ctx.get("searchPayload") or _load_json(Path(args.payload_file))
    adult = payload.get("adultNum", 1)
    child = payload.get("childNum", 0)
    infant = payload.get("infantNum", 0)

    raw = pricing(
        offer_id=offer_id,
        adult_num=adult,
        child_num=child,
        infant_num=infant,
        series_trace_id=ctx.get("traceId"),
        series_rs_time=ctx.get("processingTime"),
    )
    fmt = format_verify_data(
        raw,
        passengers=passengers,
        agent_contact=agent_contact,
        passenger_raw_mappings=pax_data.get("passengerRawMappings"),
        contact_raw=pax_data.get("contactRaw"),
        selected_offer=ctx.get("selectedOffer"),
    )
    if fmt.get("success"):
        ctx["verifyOfferId"] = fmt.get("verifyOfferId")
        ctx["verifyResult"] = fmt
        _save_json(Path(args.context_file), ctx)

    return wrap_verify(fmt)


def cmd_order(args: argparse.Namespace) -> dict:
    if not is_newapi_configured():
        return wrap_config_required("order", booking_config_required_envelope("order", step="order"))
    if not args.user_confirmed:
        payload = order_not_confirmed_payload(verify_offer_id=args.verify_offer_id)
        return failure_envelope("order", payload["message"], agent_only=payload)

    pax_data = _load_json(Path(args.passengers_file))
    passengers = pax_data.get("passengers") or []
    agent_contact = pax_data.get("agentContact") or {}
    if not passengers or not agent_contact:
        return failure_envelope(
            "order",
            "请先完成乘客信息核对（parse-passengers）。",
            agent_only={"detail": "缺少 passengers 或 agentContact"},
        )

    ctx_path = Path(args.context_file)
    verify_id = args.verify_offer_id
    if not verify_id and ctx_path.exists():
        verify_id = _load_json(ctx_path).get("verifyOfferId")
    if not verify_id:
        return failure_envelope(
            "order",
            "请先完成校验（verify）后再生单。",
            agent_only={"detail": "缺少 verify_offer_id"},
        )

    partner = args.partner_order_no or f"SKILL-{int(time.time())}"
    raw = booking(
        offer_id=verify_id,
        passengers=passengers,
        agent_contact=agent_contact,
        partner_order_no=partner,
    )
    return wrap_order(format_order_data(raw))


def main() -> int:
    parser = argparse.ArgumentParser(description="fr24-ai booking client")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_parse = sub.add_parser("parse-passengers", help="解析乘客自然语言并生成核对表")
    p_parse.add_argument("--text", required=True)

    p_verify = sub.add_parser("verify", help="校验报价（须 passenger-confirmed）")
    p_verify.add_argument("--offer-id", default="")
    p_verify.add_argument("--context-file", default=str(BOOKING_CONTEXT_FILE))
    p_verify.add_argument("--payload-file", default=str(PENDING_PAYLOAD_FILE))
    p_verify.add_argument("--passengers-file", default=str(PASSENGERS_FILE))
    p_verify.add_argument(
        "--passenger-confirmed",
        action="store_true",
        help=f"用户已回复「{PASSENGER_CONFIRM_PHRASE}」",
    )

    p_order = sub.add_parser("order", help="生单（须 user-confirmed）")
    p_order.add_argument("--verify-offer-id", default="")
    p_order.add_argument("--context-file", default=str(BOOKING_CONTEXT_FILE))
    p_order.add_argument("--passengers-file", default=str(PASSENGERS_FILE))
    p_order.add_argument("--partner-order-no", default="")
    p_order.add_argument("--user-confirmed", action="store_true", help="用户已回复「确认生单」")

    args = parser.parse_args()
    if args.cmd == "parse-passengers":
        out = cmd_parse_passengers(args.text)
    elif args.cmd == "verify":
        out = cmd_verify(args)
    else:
        out = cmd_order(args)

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("status") == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
