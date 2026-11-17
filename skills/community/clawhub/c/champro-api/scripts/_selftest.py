#!/usr/bin/env python3
"""Offline correctness tests. No network, no credentials.

    python3 scripts/_selftest.py

The fixtures are CHAMPRO's own documented examples plus responses captured live
from the production API with a deliberately invalid key
(`assets/fixtures/auth_failures.json`). That capture is the important one: it
is the evidence that every endpoint answers an auth failure with HTTP 200, so
the tests assert the client treats those bodies as failures.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import validation  # noqa: E402
from catalog import normalise_product_info  # noqa: E402
from custom_builder import _normalise_design  # noqa: E402
from errors import extract_envelope_errors, parse_message_code  # noqa: E402
from inventory import normalise_inventory  # noqa: E402
from order_status import normalise_status  # noqa: E402
from orders import build_envelope, split_by_type, summarise_place_order  # noqa: E402
from reference import explain_error, list_shipping_methods  # noqa: E402
from schemas import CUSTOM, STOCK, Order, ShipTo  # noqa: E402
from shipping import lookup, requires_shipping_account  # noqa: E402

FIXTURES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fixtures"
)

_FAILURES: list[str] = []
_PASSES = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global _PASSES
    if condition:
        _PASSES += 1
    else:
        _FAILURES.append(f"{label}{': ' + detail if detail else ''}")


def fixture(name: str):
    with open(os.path.join(FIXTURES, f"{name}.json"), encoding="utf-8") as handle:
        return json.load(handle)


# --------------------------------------------------------------------------
# Every endpoint hides an auth failure behind HTTP 200, each in its own field.
# --------------------------------------------------------------------------


def test_auth_failures_are_detected() -> None:
    captured = fixture("auth_failures")
    for name in ("product_info", "order_status", "inventory", "place_order"):
        errors = extract_envelope_errors(captured[name], name)
        check(
            f"auth failure detected in {name}",
            bool(errors),
            "a 200 body carrying a validation error must not read as success",
        )
    check(
        "place_order auth failure carries its dotted code",
        extract_envelope_errors(captured["place_order"], "PlaceOrder")[0]["code"] == "E4.1",
    )
    # The CB read has no error channel at all; that is the point of the note.
    check("cb GetOrderInfo auth failure is an empty list", captured["cb_get_order_info"] == [])


def test_success_bodies_carry_no_errors() -> None:
    for name in ("product_info", "order_status", "inventory"):
        payload = fixture(name)
        errors = extract_envelope_errors(payload, name)
        if name == "inventory":
            # This fixture has one bad SKU among good ones: item-scoped only.
            check(
                "inventory per-SKU error is item-scoped",
                [e["scope"] for e in errors] == ["item"],
                str(errors),
            )
            check("inventory ResponseMessage 'OK' is not an error", "OK" not in str(errors))
        else:
            check(f"{name} success has no errors", not errors, str(errors))


def test_dotted_code_parsing() -> None:
    check(
        "dotted code parsed",
        parse_message_code("E2.8.3: BP62YGHBPS - Not enough Inventory.") == "E2.8.3",
    )
    check("no code in a bare message", parse_message_code("Customer validation error.") is None)


# --------------------------------------------------------------------------
# Partial success: suborders AND errors in one response.
# --------------------------------------------------------------------------


def test_partial_order_is_not_a_failure() -> None:
    summary = summarise_place_order(fixture("place_order_partial"))
    check("partial outcome classified", summary["outcome"] == "partial", summary["outcome"])
    check(
        "both suborders surfaced",
        summary["suborder_ids"] == [1212121, 1212133],
        str(summary["suborder_ids"]),
    )
    check("both inventory errors surfaced", len(summary["errors"]) == 2, str(summary["errors"]))
    check("errors scoped to the order", {e["scope"] for e in summary["errors"]} == {"order"})
    check("cost total summed", summary["cost_total"] == 43.62, str(summary["cost_total"]))


def test_outcome_classification() -> None:
    check(
        "errors with no suborders is failed",
        summarise_place_order(fixture("auth_failures")["place_order"])["outcome"] == "failed",
    )
    check(
        "no suborders and no errors is empty, not placed",
        summarise_place_order({"Orders": []})["outcome"] == "empty",
    )
    placed = {"Orders": [{"PO": "X", "SubOrders": [{"SubOrderID": 99, "SubOrderItems": []}]}]}
    check("clean response is placed", summarise_place_order(placed)["outcome"] == "placed")
    # A SubOrders entry with no id is not an order.
    idless = {"Orders": [{"PO": "X", "SubOrders": [{"SubOrderID": 0, "SubOrderItems": []}]}]}
    check("SubOrderID 0 is not an order", summarise_place_order(idless)["outcome"] == "empty")


# --------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------


def test_product_info_normalisation() -> None:
    info = normalise_product_info(fixture("product_info"))
    check("moq_custom read", info["moq_custom"] == 12)
    check("moq_stock read", info["moq_stock"] == 0)
    check("sku count", info["sku_count"] == 5)
    check("empty Color is None, not ''", info["colors"] == [], str(info["colors"]))
    check("configurations collected", info["configurations"] == ["GIRLS", "WOMENS", "YOUTH"])
    check("lead time days parsed", info["lead_times"][0]["days"] == 15)
    check("lead time charge parsed", info["lead_times"][1]["charge"] == 8.0)


def test_inventory_normalisation() -> None:
    rows = normalise_inventory(fixture("inventory"))
    first = rows[0]
    check("warehouses keyed by code", first["warehouses"] == {"IL": 532, "CA": 24, "DR": 0})
    check("total summed", first["total"] == 556)
    check("restock date kept", first["more_expected_on"] == "7/13/2025")
    check("blank restock date is None", rows[1]["more_expected_on"] is None)
    # A null quantity must not silently become 0.
    check("null quantity stays None", rows[1]["warehouses"]["DR"] is None)
    check("unreadable quantity flagged", rows[1]["has_unreadable_quantity"] is True)
    check("total ignores the unreadable one", rows[1]["total"] == 7)


def test_order_status_normalisation() -> None:
    status = normalise_status(fixture("order_status"))
    check("tracking extracted", status["tracking_numbers"] == ["772307173547"])
    check("shipped flag", status["shipped"] is True)
    check("sales id via SalesID", status["sales_id"] == "SO-2000712")
    check("package contents", len(status["shipments"][0]["items"]) == 2)
    # The field table spells it SALESID; the example spells it SalesID.
    check(
        "sales id via SALESID spelling",
        normalise_status({"SALESID": "SO-1", "Lines": []})["sales_id"] == "SO-1",
    )
    check("no lines means not shipped", normalise_status({"Lines": None})["shipped"] is False)


def test_cb_design_normalisation() -> None:
    items = _normalise_design(fixture("cb_design"))
    check("one cart item", len(items) == 1)
    check("blank team name is None", items[0]["teams"][0]["team_name"] is None)
    check("three players", len(items[0]["teams"][0]["players"]) == 3)
    check("selected lead time", items[0]["selected_lead_time"]["lead_time_id"] == "EX")
    check("empty design normalises to nothing", _normalise_design([]) == [])


# --------------------------------------------------------------------------
# Serialisation: the two order types have different legal fields.
# --------------------------------------------------------------------------


def _stock_order(**overrides) -> Order:
    data = {
        "po": "PO-1",
        "order_type": STOCK,
        "ship_to_first_name": "DOW",
        "ship_to_last_name": "JOE",
        "address": "220 STREET AVE",
        "city": "MYCITY",
        "state_code": "IL",
        "zip_code": "60007",
        "phone": "1234567890",
        "shipping_method": "UPS GROUND",
        "items": [{"sku": "BBS44ABS", "quantity": 3, "warehouse": "CA"}],
    }
    data.update(overrides)
    return Order.from_dict(data)


def _custom_order(**overrides) -> Order:
    data = {
        "po": "PO-2",
        "order_type": CUSTOM,
        "ship_to_first_name": "FIRST",
        "ship_to_last_name": "LAST",
        "address": "123 STREET AVE",
        "city": "CITY",
        "state_code": "IL",
        "zip_code": "60007",
        "phone": "1234567890",
        "lead_time": "JUICE Standard",
        "proof_file_url": "https://example.com/proof.pdf",
        "team_color": "RED",
        "items": [
            {"sku": "JSBJ8YACS", "quantity": 6, "team_name": "VALLEY", "player_name": "SCUBY", "player_number": "34"},
            {"sku": "JSBJ8YACL", "quantity": 6, "team_name": "VALLEY", "player_name": "EDNA", "player_number": "30"},
        ],
    }
    data.update(overrides)
    return Order.from_dict(data)


def test_serialisation() -> None:
    stock = _stock_order().to_payload()
    check("stock keeps ShippingMethod", stock["ShippingMethod"] == "UPS GROUND")
    check("stock line keeps Warehouse", stock["OrderItems"][0]["Warehouse"] == "CA")
    check("stock line has no roster fields", "PlayerName" not in stock["OrderItems"][0])
    check("stock has no LeadTime", "LeadTime" not in stock)
    check("IsResidential serialised as 0/1", stock["IsResidential"] == 0)

    custom = _custom_order().to_payload()
    check("custom keeps LeadTime", custom["LeadTime"] == "JUICE Standard")
    check("custom keeps ProofFileURL", custom["ProofFileURL"].endswith(".pdf"))
    check("custom line keeps roster", custom["OrderItems"][0]["PlayerNumber"] == "34")
    check("custom line has no Warehouse", "Warehouse" not in custom["OrderItems"][0])
    check("custom has no ShippingMethod", "ShippingMethod" not in custom)

    envelope = build_envelope([_stock_order()], autowarehouse=True)
    check("autowarehouse serialised", envelope["Autowarehouse"] == "YES")
    check("no key in the envelope", "APICustomerKey" not in envelope)
    check(
        "autowarehouse omitted when off",
        "Autowarehouse" not in build_envelope([_stock_order()]),
    )


def test_shipto_spelling_differs_from_order() -> None:
    ship_to = ShipTo.from_dict(
        {"first_name": "A", "last_name": "B", "address1": "1 St", "city": "C", "state": "IL", "zip": "60007"}
    ).to_payload()
    check("CB uses Zip not ZIPCode", "Zip" in ship_to and "ZIPCode" not in ship_to)
    check("CB uses Address1 not Address", "Address1" in ship_to)
    check("CB IsResidential is a string", ship_to["IsResidential"] == "false")


# --------------------------------------------------------------------------
# Validation rules
# --------------------------------------------------------------------------


def _errors(findings) -> list[str]:
    return [f["code"] for f in findings if f["severity"] == "error"]


def test_validation_moq_increments() -> None:
    info = {"JSBJ8": fixture("product_info")}
    # MOQCustom is 12 and the order totals 12: valid.
    ok = validation.validate_order(_custom_order(), product_info=info)
    check("MOQ multiple passes", "25" not in _errors(ok), str(_errors(ok)))

    # 18 exceeds the minimum but is not a multiple — code 25 is about
    # increments, not a floor.
    over = _custom_order(
        items=[
            {"sku": "JSBJ8YACS", "quantity": 12, "team_name": "V", "player_name": "A", "player_number": "1"},
            {"sku": "JSBJ8YACL", "quantity": 6, "team_name": "V", "player_name": "B", "player_number": "2"},
        ]
    )
    check("non-multiple above the minimum fails", "25" in _errors(validation.validate_order(over, product_info=info)))

    # The increment applies to the master total, so 6+6 across two lines is fine.
    check("MOQ applies to the master total, not per line", "25" not in _errors(ok))


def test_validation_unknown_sku_and_lead_time() -> None:
    info = {"JSBJ8": fixture("product_info")}
    bad_sku = _custom_order(
        items=[{"sku": "NOPE", "quantity": 12, "team_name": "V", "player_name": "A", "player_number": "1"}]
    )
    check("unknown SKU is code 08", "08" in _errors(validation.validate_order(bad_sku, product_info=info)))

    bad_lead = _custom_order(lead_time="OVERNIGHT MAGIC")
    check("unknown lead time is code 22", "22" in _errors(validation.validate_order(bad_lead, product_info=info)))


def test_validation_skips_are_visible() -> None:
    findings = validation.validate_order(_custom_order(), product_info=None)
    check(
        "catalog checks report as skipped, not passed",
        any(f["severity"] == "skipped" for f in findings),
    )


def test_validation_shipping_and_warehouse() -> None:
    third_party = _stock_order(shipping_method="UPS GROUND THIRD PARTY")
    check(
        "third-party method needs a payer account",
        any("ShippingCustomerAccount" in f["message"] for f in validation.blocking(validation.validate_order(third_party))),
    )
    with_account = _stock_order(
        shipping_method="UPS GROUND THIRD PARTY", shipping_customer_account="9999999"
    )
    check(
        "third-party method with an account passes",
        not any("ShippingCustomerAccount" in f["message"] for f in validation.blocking(validation.validate_order(with_account))),
    )

    no_warehouse = _stock_order(items=[{"sku": "BBS44ABS", "quantity": 3}])
    check("missing warehouse is code 11", "11" in _errors(validation.validate_order(no_warehouse)))
    check(
        "autowarehouse satisfies the warehouse rule",
        "11" not in _errors(validation.validate_order(no_warehouse, autowarehouse=True)),
    )
    bad_wh = _stock_order(items=[{"sku": "BBS44ABS", "quantity": 3, "warehouse": "TX"}])
    check("unknown warehouse code rejected", "11" in _errors(validation.validate_order(bad_wh)))

    bad_method = _stock_order(shipping_method="UPS SUPERFAST")
    findings = validation.validate_order(bad_method)
    check("unknown shipping method rejected", any("not in CHAMPRO" in f["message"] for f in validation.blocking(findings)))


def test_validation_mixing_and_proof() -> None:
    mixed = _stock_order(
        items=[{"sku": "BBS44ABS", "quantity": 3, "warehouse": "CA", "player_name": "AL"}]
    )
    check("roster fields on a stock order is code 07", "07" in _errors(validation.validate_order(mixed)))

    bad_proof = _custom_order(proof_file_url="https://example.com/proof.tiff")
    check("bad proof extension is code 02", "02" in _errors(validation.validate_order(bad_proof)))

    no_proof = _custom_order(proof_file_url="")
    check("missing proof is code 01", "01" in _errors(validation.validate_order(no_proof)))

    no_lead = _custom_order(lead_time="")
    check("missing lead time is code 21", "21" in _errors(validation.validate_order(no_lead)))


def test_validation_shipto() -> None:
    check("missing phone is code 24", "24" in _errors(validation.validate_order(_stock_order(phone=""))))
    check("missing city is code 24", "24" in _errors(validation.validate_order(_stock_order(city=""))))
    check("blank PO is code 17", "17" in _errors(validation.validate_order(_stock_order(po=" "))))
    check("bad order type rejected", _errors(validation.validate_order(_stock_order(order_type="BOTH"))) == ["19"])


def test_place_order_outcome_mapping() -> None:
    """The response outcome decides the exception, and therefore the exit code.

    Stubs the transport so no request leaves the process: what is under test is
    the classification, which is the part that decides whether a caller retries
    a request that may already have created orders.
    """

    import orders as orders_module  # noqa: PLC0415
    from errors import ChamproAPIError, ChamproPartialOrderError  # noqa: PLC0415

    order = {
        "po": "PO-1",
        "order_type": STOCK,
        "ship_to_first_name": "DOW",
        "ship_to_last_name": "JOE",
        "address": "220 STREET AVE",
        "city": "MYCITY",
        "state_code": "IL",
        "zip_code": "60007",
        "phone": "1234567890",
        "shipping_method": "UPS GROUND",
        "items": [{"sku": "BBS44ABS", "quantity": 3, "warehouse": "CA"}],
    }

    class _Stub:
        def __init__(self, payload):
            self.payload = payload
            self.sent_to = None

        def place_order(self, body, *, production):
            self.sent_to = "production" if production else "sandbox"
            return {**self.payload, "_environment": self.sent_to}

    original = orders_module._client
    try:
        # partial -> escalation, never a plain failure
        stub = _Stub(fixture("place_order_partial"))
        orders_module._client = lambda _creds: stub
        raised = None
        try:
            orders_module.place_order(order=order, confirm=True)
        except ChamproPartialOrderError as exc:
            raised = exc
        check("partial raises escalation", isinstance(raised, ChamproPartialOrderError))
        check("escalation carries the suborder ids", raised.result["suborder_ids"] == [1212121, 1212133])

        # failed -> api_error
        stub = _Stub(fixture("auth_failures")["place_order"])
        orders_module._client = lambda _creds: stub
        raised = None
        try:
            orders_module.place_order(order=order, confirm=True)
        except ChamproAPIError as exc:
            raised = exc
        check("failed raises api_error", isinstance(raised, ChamproAPIError))

        # empty -> escalation, because it proves nothing either way
        stub = _Stub({"Orders": []})
        orders_module._client = lambda _creds: stub
        raised = None
        try:
            orders_module.place_order(order=order, confirm=True)
        except ChamproPartialOrderError as exc:
            raised = exc
        check("empty response escalates rather than reporting success", raised is not None)

        # placed -> returns
        stub = _Stub({"Orders": [{"PO": "PO-1", "SubOrders": [{"SubOrderID": 77, "SubOrderItems": []}]}]})
        orders_module._client = lambda _creds: stub
        result = orders_module.place_order(order=order, confirm=True)
        check("clean placement returns", result["outcome"] == "placed")
        check("sandbox is the default target", stub.sent_to == "sandbox")

        # production must be opted into explicitly
        stub = _Stub({"Orders": [{"PO": "PO-1", "SubOrders": [{"SubOrderID": 78, "SubOrderItems": []}]}]})
        orders_module._client = lambda _creds: stub
        orders_module.place_order(order=order, confirm=True, production=True)
        check("production only when asked for", stub.sent_to == "production")

        # unconfirmed sends nothing at all
        stub = _Stub({"Orders": []})
        orders_module._client = lambda _creds: stub
        unconfirmed = orders_module.place_order(order=order)
        check("unconfirmed sends nothing", stub.sent_to is None)
        check("unconfirmed reports why", unconfirmed["reason"] == "unconfirmed")
    finally:
        orders_module._client = original


def test_split_mixed_cart() -> None:
    result = split_by_type(
        [
            {"sku": "BBS44ABS", "quantity": 3, "warehouse": "CA"},
            {"sku": "JSBJ8YACS", "quantity": 12, "player_name": "AL", "player_number": "7"},
        ],
        base={"po": "PO-9", "ship_to_first_name": "A"},
    )
    check("mixed cart detected", result["was_mixed"] is True)
    check("two orders produced", len(result["orders"]) == 2)
    check("PO suffixed per order", {o["po"] for o in result["orders"]} == {"PO-9-S", "PO-9-C"})
    check("types assigned", {o["order_type"] for o in result["orders"]} == {STOCK, CUSTOM})
    check(
        "an all-stock cart is not split",
        split_by_type([{"sku": "X", "quantity": 1}])["was_mixed"] is False,
    )


# --------------------------------------------------------------------------
# Reference tables
# --------------------------------------------------------------------------


def test_shipping_catalog() -> None:
    check("underscore spelling resolves", lookup("FEDEX 2 DAY")["name"] == "FEDEX_2_DAY")
    check("case-insensitive", lookup("ups ground")["name"] == "UPS GROUND")
    check("collect needs an account", requires_shipping_account("UPS GROUND COLLECT") is True)
    check("prepaid does not", requires_shipping_account("UPS GROUND") is False)
    check("unknown method returns None", lookup("TELEPORT") is None)
    listed = list_shipping_methods()
    check("all 40 published methods present", listed["count"] == 40, str(listed["count"]))
    check("billing-coupled methods flagged", len(listed["requires_shipping_account"]) == 20)
    check("filtering by carrier works", list_shipping_methods(carrier="UPS")["count"] == 18)
    check(
        "prepaid filter excludes billing-coupled methods",
        list_shipping_methods(billing_type="prepaid")["count"] == 20,
    )


def test_error_explanations() -> None:
    moq = explain_error(code="25")
    check("code 25 known", moq["known"] is True)
    check("code 25 has a remedy", "MULTIPLE" in (moq["remedy"] or ""))
    check("code 25 is not retryable", moq["retryable"] is False)

    ip = explain_error(code="15")
    check("code 15 is account level", ip["account_level"] is True)

    from_message = explain_error(message="E2.8.3: BP62YGHBPS - Not enough Inventory.")
    check("code pulled out of a message", from_message["code"] == "E2.8.3")
    check("family classified", from_message["family"] == "E2")

    check("unpadded code accepted", explain_error(code="8")["description"].startswith("SKU"))
    check("no code at all handled", explain_error()["code"] is None)


def test_every_documented_code_has_a_remedy() -> None:
    from errors import CB_MESSAGE_CODES  # noqa: PLC0415
    from reference import _REMEDIES  # noqa: PLC0415

    missing = sorted(set(CB_MESSAGE_CODES) - set(_REMEDIES))
    check("every documented code has a remedy", not missing, f"missing: {missing}")


def main() -> int:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        try:
            test()
        except Exception as exc:  # noqa: BLE001
            _FAILURES.append(f"{test.__name__} raised {type(exc).__name__}: {exc}")

    if _FAILURES:
        print(f"FAILED — {len(_FAILURES)} check(s) failed, {_PASSES} passed\n")
        for failure in _FAILURES:
            print(f"  ✗ {failure}")
        return 1
    print(f"OK — {_PASSES} checks passed across {len(tests)} tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
