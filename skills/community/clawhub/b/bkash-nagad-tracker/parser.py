#!/usr/bin/env python3
"""
parser.py — Natural language transaction parser
Handles Bengali + English + mixed input
Uses claude-haiku for cheap, fast parsing
"""

import sys
import json
import os
import re
import anthropic


def parse_with_claude(message: str) -> dict:
    """Use Claude Haiku to parse transaction from message"""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set")
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are a transaction parser for a Bangladeshi expense tracker.
Extract transaction details from this message. Handle Bengali, English, or mixed input.

Message: "{message}"

Return ONLY valid JSON with exactly these fields:
{{
  "amount": <number in taka — convert Bengali numerals if needed, null if not found>,
  "method": <"bkash" | "nagad" | "rocket" | "cash" | "other">,
  "category": <"food" | "transport" | "rent" | "utilities" | "remittance" | "medical" | "education" | "shopping" | "other">,
  "note": <2-4 word description in English>,
  "confidence": <"high" | "low">
}}

Rules:
- Bengali numerals: ০=0 ১=1 ২=2 ৩=3 ৪=4 ৫=5 ৬=6 ৭=7 ৮=8 ৯=9
- Bengali words: টাকা/তাকা=taka, বিকাশ=bkash, নগদ=nagad, রকেট=rocket
- "sent to mum/dad/bhai/apa/family/মা/বাবা/ভাই/আপা" = remittance
- "rickshaw/CNG/bus/train/Uber/রিকশা/ভাড়া" = transport
- "বাজার/grocery/super shop" = shopping or food
- "bill/বিল" with electricity/gas/water/internet = utilities
- Default method to "bkash" if unclear
- Set confidence "low" if amount is ambiguous or category unclear
- Return null for amount if no number found anywhere
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    return json.loads(raw)


def parse_simple(message: str) -> dict | None:
    """
    Fast regex-based parse for obvious patterns.
    Avoids API call for simple cases.
    Returns None if not confident.
    """

    msg = message.lower().strip()

    # Detect method
    method = "bkash"  # default
    if "nagad" in msg or "নগদ" in msg:
        method = "nagad"
    elif "rocket" in msg or "রকেট" in msg:
        method = "rocket"
    elif "cash" in msg or "নগদ টাকা" in msg:
        method = "cash"
    elif "bkash" in msg or "bikash" in msg or "বিকাশ" in msg:
        method = "bkash"

    # Extract amount — handle "500", "৳500", "500tk", "500 taka"
    amount_pattern = r"[৳৳\$]?\s*(\d+(?:\.\d+)?)\s*(?:tk|taka|টাকা|bdt)?|(\d+(?:\.\d+)?)\s*(?:tk|taka|টাকা|bdt)"
    match = re.search(amount_pattern, msg)
    if not match:
        return None

    amount_str = match.group(1) or match.group(2)
    if not amount_str:
        return None
    amount = float(amount_str)

    # Detect category
    food_words = ["food", "lunch", "dinner", "breakfast", "restaurant",
                  "খাবার", "রেস্তোরাঁ", "ভাত", "biryani", "snack", "coffee",
                  "tea", "চা", "meal", "grocery", "বাজার"]
    transport_words = ["rickshaw", "cng", "uber", "bus", "train", "ভাড়া",
                       "যাতায়াত", "taxi", "pathao", "shohoz", "রিকশা"]
    remittance_words = ["sent", "mum", "mom", "dad", "family", "bhai", "apa",
                        "মা", "বাবা", "ভাই", "আপা", "পাঠালাম", "দিলাম"]
    utilities_words = ["electricity", "gas", "water", "internet", "bill",
                       "বিল", "wasa", "desco", "dpdc"]
    rent_words = ["rent", "বাড়িভাড়া", "house"]
    medical_words = ["medicine", "doctor", "hospital", "pharmacy",
                     "ডাক্তার", "ওষুধ"]

    category = "other"
    for word in food_words:
        if word in msg:
            category = "food"
            break
    for word in transport_words:
        if word in msg:
            category = "transport"
            break
    for word in remittance_words:
        if word in msg:
            category = "remittance"
            break
    for word in utilities_words:
        if word in msg:
            category = "utilities"
            break
    for word in rent_words:
        if word in msg:
            category = "rent"
            break
    for word in medical_words:
        if word in msg:
            category = "medical"
            break

    # Extract note — words that aren't amount/method/category keywords
    skip = {"bkash", "nagad", "rocket", "cash", "taka", "tk", "bdt",
            "paid", "spent", "bought", "log", "track"}
    words = [w for w in msg.split() if w not in skip
             and not re.match(r"\d+", w)]
    note = " ".join(words[:3]) if words else category

    return {
        "amount": amount,
        "method": method,
        "category": category,
        "note": note,
        "confidence": "high"
    }


def parse_transaction(message: str) -> dict:
    """
    Main parse function.
    Try fast regex first, fall back to Claude if needed.
    """
    # Try fast parse first (no API cost)
    result = parse_simple(message)

    if result and result.get("confidence") == "high":
        return result

    # Fall back to Claude for complex/Bengali input
    try:
        return parse_with_claude(message)
    except Exception as e:
        return {
            "amount": None,
            "method": "bkash",
            "category": "other",
            "note": message[:30],
            "confidence": "low",
            "error": str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No message provided"}))
        sys.exit(1)

    message = " ".join(sys.argv[1:])
    result = parse_transaction(message)
    print(json.dumps(result, ensure_ascii=False))
