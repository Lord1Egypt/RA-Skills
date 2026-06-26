import os
import json
import re

from parse_roty_input import parse_message
from match_product_and_modifiers import get_all_aliases, find_product_by_intent_or_alias, match_modifiers
from pricing_engine import determine_cost_of_each_date_catering_product
from build_payload import build_payload
from post_order import post_order
from onboard_product import upsert_product

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "allowed_users.json")


def load_allowed():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"admins": [], "vendors": []}


def handle_message(sender_id, message_text, source="telegram"):
    text = (message_text or "").strip()
    openclaw_context = (source == "openclaw") or (os.environ.get("OPENCLAW_CONTEXT") == "1")

    # onboarding
    if text.lower().startswith("roty product:"):
        ok, msg = upsert_product(
            sender_id,
            text[len("Roty product:") :].strip(),
            openclaw_context=openclaw_context,
        )
        return msg

    # order trigger
    if "roty input" in text.lower():
        allowed = load_allowed()
        if (
            not openclaw_context
            and str(sender_id) not in allowed.get("vendors", [])
            and str(sender_id) not in allowed.get("admins", [])
        ):
            return "Unauthorized: your account is not allowed to place orders. Ask an admin to add you."

        aliases = get_all_aliases()
        parsed = parse_message(text, extra_stop_aliases=aliases)

        # best-effort name guess only if parser didn't find one
        if not parsed.get("customerName"):
            m_name_before = re.search(r"(?i)rot[y]?\s*input\s+([A-Za-z ]+?)\s+\d+", text)
            if m_name_before:
                name_guess = m_name_before.group(1).strip()
                name_parts = name_guess.split()
                parsed["customerName"] = " ".join([w.capitalize() for w in name_parts[:3]])

        # remove product aliases from address if they leaked in
        if parsed.get("userAddress"):
            ua = parsed["userAddress"]
            for a in aliases:
                ua = re.sub(re.escape(a), " ", ua, flags=re.I)
            parsed["userAddress"] = " ".join(ua.split()).strip(" ,")

        if not parsed.get("userAddress"):
            return "Missing address; please provide a street number and street name."
        if not parsed.get("deliveryDates"):
            return "Missing delivery dates; please specify when to deliver (e.g., tomorrow, Mon-Fri, 28 days)."

        pref, product = find_product_by_intent_or_alias(text, parsed.get("intent"))
        if not product:
            return "Product not recognized. Please specify veg or non-veg (or use a known alias)."

        m1, m2 = match_modifiers(product, parsed.get("mod1"), parsed.get("mod2"), raw_text=text)

        per_date_costs = determine_cost_of_each_date_catering_product(
            product.get("price"),
            m1.get("additionalCost") if m1 else 0,
            m2.get("additionalCost") if m2 else 0,
            product.get("cateringDiscountStack"),
            parsed.get("deliveryDates"),
            product.get("cateringDiscountMode"),
            product.get("cateringDefaultWindowDays"),
        )
        if per_date_costs is None:
            return "Pricing error: missing price or dates."

        payload = build_payload(parsed, product, m1, m2, per_date_costs)

        dry = os.environ.get("DRY_RUN", "0")  # default LIVE
        if dry == "1":
            return "DRY_RUN: payload prepared:\n" + json.dumps(payload, indent=2)

        status, body = post_order(payload)

        if status == 200 and isinstance(body, dict) and (body.get("success") is True or body.get("cartNo")):
            cart_no = body.get("cartNo")
            return (
                "✅ Order Created\n"
                f"Cart Number: {cart_no}\n"
                f"Product: {product.get('name')}\n"
                f"Delivery dates: {payload['listOfOrderDetails'][0]['deliverySchedule']}\n"
                f"PerProductCost sent: {payload['listOfOrderDetails'][0]['perProductCost']}\n"
                f"Address: {payload['userAddress']}"
            )

        return f"POST failed: HTTP {status} - {body}"

    return "Unsupported command."


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print('Usage: python3 handle_message.py <sender_id> "<message text>" [--openclaw]')
        raise SystemExit(2)

    sid = sys.argv[1]
    txt = " ".join(sys.argv[2:])

    source = "telegram"
    if sid == "OPENCLAW" or ("--openclaw" in sys.argv):
        source = "openclaw"

    print(handle_message(sid, txt, source=source))
