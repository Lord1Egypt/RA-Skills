#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from rapidocr_onnxruntime import RapidOCR
except Exception as e:
    print(f"Failed to import rapidocr_onnxruntime: {e}", file=sys.stderr)
    sys.exit(2)


def run_ocr(image_path: str):
    ocr = RapidOCR()
    result, elapse = ocr(image_path)
    lines = []
    if result:
        for item in result:
            text = item[1].strip()
            conf = float(item[2])
            if text:
                lines.append({"text": text, "confidence": conf})
    return {"elapsed": elapse, "lines": lines, "full_text": "\n".join(x["text"] for x in lines)}


def looks_date(s: str):
    return bool(re.fullmatch(r"\d{2,4}[/-]\d{1,2}[/-]\d{1,2}", s))


def looks_time(s: str):
    return bool(re.fullmatch(r"\d{1,2}:\d{2}:\d{2}", s))


def looks_amount(s: str):
    return bool(re.fullmatch(r"\d+(?:\.\d{1,2})", s))


def structure_transactions(lines):
    texts = [x["text"] for x in lines]
    rows = []
    current = None

    def flush():
        nonlocal current
        if current:
            rows.append(current)
            current = None

    for idx, t in enumerate(texts):
        if looks_date(t):
            flush()
            current = {
                "card_last4": "",
                "date": t,
                "time": "",
                "currency": "",
                "merchant_parts": [],
                "amount": "",
                "raw": [t],
            }
            continue
        if current is None:
            continue
        current["raw"].append(t)
        if not current["time"] and looks_time(t):
            current["time"] = t
        elif not current["currency"] and t in {"CNY", "RMB", "USD", "EUR", "HKD", "JPY"}:
            current["currency"] = t
        elif not current["amount"] and looks_amount(t):
            current["amount"] = t
        elif not current["card_last4"] and re.fullmatch(r"\d{4}", t):
            current["card_last4"] = t
        else:
            current["merchant_parts"].append(t)
    flush()

    cleaned = []
    for i, r in enumerate(rows):
        parts = []
        for p in r.get("merchant_parts", []):
            p = re.sub(r"^(卡号末四位|交易日期|时间|币别|商户名称|交易金额|Amount of|LAST card|Transaction|Currency|Merchant name|original|numbers|date|time|currency)+", "", p).strip()
            if not p:
                continue
            parts.append(p)

        merchant = "".join(parts)

        # Heuristic cleanup for spillover from next row starter brands.
        for marker in ["支付宝-", "微信支付-", "美团支付-", "云闪付-"]:
            pos_list = [m.start() for m in re.finditer(re.escape(marker), merchant)]
            if len(pos_list) >= 2:
                merchant = merchant[:pos_list[1]].strip()
                break

        # If a trailing payment-channel prefix appears after a more specific merchant fragment,
        # prefer the earlier merchant fragment.
        for marker in ["支付宝-", "微信支付-", "美团支付-", "云闪付-"]:
            pos = merchant.rfind(marker)
            if pos > 0:
                tail = merchant[pos:]
                head = merchant[:pos].strip()
                if head and (len(tail) <= 12 or tail.endswith('A') or tail.endswith('App')):
                    merchant = head
                    break

        # If merchant starts with connector noise but has later useful text, strip leading noise.
        merchant = re.sub(r'^(pp|App)+', '', merchant).strip()

        if r["date"] and (r["amount"] or merchant):
            cleaned.append({
                "card_last4": r["card_last4"],
                "date": r["date"],
                "time": r["time"],
                "currency": r["currency"],
                "merchant": merchant,
                "amount": r["amount"],
                "raw": r["raw"],
            })
    return cleaned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["raw", "transactions"])
    ap.add_argument("image")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    image = str(Path(args.image).expanduser())
    data = run_ocr(image)

    if args.mode == "raw":
        out = data
    else:
        out = {
            "transactions": structure_transactions(data["lines"]),
            "raw_text": data["full_text"],
        }

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        if args.mode == "raw":
            print(data["full_text"])
        else:
            for i, r in enumerate(out["transactions"], 1):
                print(f"[{i}] {r['date']} {r['time']} | {r['merchant']} | {r['currency']} {r['amount']} | card:{r['card_last4']}")


if __name__ == "__main__":
    main()
