#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 scripts/calculator.py <num1> <num2> <add|sub|mul|div>", file=sys.stderr)
        sys.exit(1)

    try:
        num1 = int(sys.argv[1])
        num2 = int(sys.argv[2])
    except ValueError:
        print("Error: num1 and num2 must be integers", file=sys.stderr)
        sys.exit(1)

    operation = sys.argv[3].lower()

    if operation == "add":
        print(num1 + num2)
    elif operation == "sub":
        print(num1 - num2)
    elif operation == "mul":
        print(num1 * num2)
    elif operation == "div":
        if num2 == 0:
            print("Error: division by zero", file=sys.stderr)
            sys.exit(1)
        print(num1 / num2)
    else:
        print(f"Error: unsupported operation '{operation}'. Use 'add', 'sub', 'mul' or 'div'.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
    