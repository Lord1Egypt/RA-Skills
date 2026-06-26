#!/usr/bin/env python3
import argparse, json, sys, re

def validate_id18(id18):
    if len(id18) != 18:
        return False
    # Check birth date
    try:
        from datetime import datetime
        y, m, d = int(id18[6:10]), int(id18[10:12]), int(id18[12:14])
        datetime(y, m, d)
    except:
        return False
    # Check code
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    checkcodes = "10X98765432"
    total = sum(int(id18[i]) * factors[i] for i in range(17))
    return checkcodes[total % 11] == id18[17]

def validate_id15(id15):
    if len(id15) != 15:
        return False
    try:
        from datetime import datetime
        y, m, d = int("19" + id15[6:8]), int(id15[8:10]), int(id15[10:12])
        datetime(y, m, d)
        return True
    except:
        return False

def parse_id(idno):
    if len(idno) == 18 and validate_id18(idno):
        region = idno[:6]
        gender_code = int(idno[16])
        y, m, d = idno[6:10], idno[10:12], idno[12:14]
    elif len(idno) == 15 and validate_id15(idno):
        region = idno[:6]
        gender_code = int(idno[14])
        y, m, d = "19" + idno[6:8], idno[8:10], idno[10:12]
    else:
        return None
    return {"region": region, "birthday": f"{y}-{m}-{d}", "gender": "男" if gender_code % 2 == 1 else "女"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    result = parse_id(args.id)
    if result:
        print(json.dumps({"valid": True, **result}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"valid": False, "error": "Invalid Chinese ID"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
