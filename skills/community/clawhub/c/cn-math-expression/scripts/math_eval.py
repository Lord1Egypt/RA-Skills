#!/usr/bin/env python3
import argparse, json, sys, math

SAFE_NAMES = {
    "abs": abs, "round": round, "min": min, "max": max, "pow": pow,
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "log": math.log, "log10": math.log10, "pi": math.pi, "e": math.e,
    "floor": math.floor, "ceil": math.ceil,
}

def safe_eval(expr):
    return eval(expr, {"__builtins__": {}}, SAFE_NAMES)

def main():
    parser = argparse.ArgumentParser(description="Math Expression Evaluator")
    parser.add_argument("--expr", required=True)
    args = parser.parse_args()
    try:
        result = safe_eval(args.expr)
        print(json.dumps({"expression": args.expr, "result": result}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
