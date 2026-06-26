#!/usr/bin/env python3
"""Temperature Converter."""
import argparse
import json
import sys

def c_to_f(c): return c * 9/5 + 32
def f_to_c(f): return (f - 32) * 5/9
def c_to_k(c): return c + 273.15
def k_to_c(k): return k - 273.15
def f_to_k(f): return c_to_k(f_to_c(f))
def k_to_f(k): return c_to_f(k_to_c(k))

def main():
    parser = argparse.ArgumentParser(description="Temperature Converter")
    parser.add_argument("--value", type=float, required=True, help="Temperature value")
    parser.add_argument("--from", dest="from_unit", choices=["C","F","K"], required=True)
    parser.add_argument("--to", dest="to_unit", choices=["C","F","K"], required=True)
    args = parser.parse_args()
    
    # Convert
    converters = {
        ("C","F"): c_to_f, ("F","C"): f_to_c,
        ("C","K"): c_to_k, ("K","C"): k_to_c,
        ("F","K"): f_to_k, ("K","F"): k_to_f,
    }
    
    if args.from_unit == args.to_unit:
        result = args.value
    else:
        result = converters[(args.from_unit, args.to_unit)](args.value)
    
    result = round(result, 2)
    
    # All conversions
    all_results = {}
    for unit in ["C","F","K"]:
        if unit == args.from_unit:
            all_results[unit] = round(args.value, 2)
        else:
            all_results[unit] = round(converters.get((args.from_unit, unit), lambda x: x)(args.value), 2)
    
    print(json.dumps({
        "input": f"{args.value}{args.from_unit}",
        "output": f"{result}{args.to_unit}",
        "all_units": all_results,
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
