#!/usr/bin/env python3

import argparse, json, sys
import secrets
import string

def gen_pwd(length, upper=True, lower=True, digits=True, symbols=True):
    chars = ""
    if upper: chars += string.ascii_uppercase
    if lower: chars += string.ascii_lowercase
    if digits: chars += string.digits
    if symbols: chars += "!@#$%^&*"
    if not chars:
        return ""
    return "".join(secrets.choice(chars) for _ in range(length))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=16)
    parser.add_argument("--no-upper", action="store_true")
    parser.add_argument("--no-lower", action="store_true")
    parser.add_argument("--no-digits", action="store_true")
    parser.add_argument("--no-symbols", action="store_true")
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    pwds = [gen_pwd(args.length, not args.no_upper, not args.no_lower,
                     not args.no_digits, not args.no_symbols)
             for _ in range(args.count)]
    print(json.dumps({"passwords": pwds, "length": args.length},
                     ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
