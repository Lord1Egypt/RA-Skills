#!/usr/bin/env python3
"""Toolkit for .env file management.

Commands: validate, diff, template, merge, list-keys, check-missing.
"""

import argparse
import os
import re
import sys
from collections import OrderedDict


def parse_env_file(filepath):
    """Parse a .env file into an OrderedDict. Returns (vars, errors)."""
    variables = OrderedDict()
    errors = []
    if not os.path.isfile(filepath):
        return variables, [f"File not found: {filepath}"]

    with open(filepath, "r") as f:
        for lineno, raw_line in enumerate(f, 1):
            line = raw_line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Match KEY=VALUE (with optional export prefix)
            match = re.match(r'^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)', line)
            if not match:
                errors.append(f"  Line {lineno}: invalid syntax: {line[:80]}")
                continue
            key = match.group(1)
            value = match.group(2).strip()
            # Strip surrounding quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            if key in variables:
                errors.append(f"  Line {lineno}: duplicate key: {key}")
            variables[key] = value
    return variables, errors


def cmd_validate(args):
    """Validate .env file syntax and report issues."""
    filepath = args.file
    variables, errors = parse_env_file(filepath)

    print(f"Validating: {filepath}")
    print(f"Variables found: {len(variables)}")

    # Check for common issues
    warnings = []
    for key, value in variables.items():
        if not value:
            warnings.append(f"  Empty value: {key}")
        if " " in key:
            warnings.append(f"  Space in key name: '{key}'")
        if value and not value.startswith("$") and any(c in value for c in ["'", '"', "`"]):
            warnings.append(f"  Unescaped quotes in value: {key}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(e)
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(w)
    if not errors and not warnings:
        print("No issues found.")

    return 1 if errors else 0


def cmd_diff(args):
    """Show differences between two .env files."""
    vars1, err1 = parse_env_file(args.file1)
    vars2, err2 = parse_env_file(args.file2)

    if err1:
        print(f"Errors parsing {args.file1}:", file=sys.stderr)
        for e in err1:
            print(e, file=sys.stderr)
    if err2:
        print(f"Errors parsing {args.file2}:", file=sys.stderr)
        for e in err2:
            print(e, file=sys.stderr)

    keys1 = set(vars1.keys())
    keys2 = set(vars2.keys())

    only_in_1 = sorted(keys1 - keys2)
    only_in_2 = sorted(keys2 - keys1)
    common = sorted(keys1 & keys2)
    changed = [(k, vars1[k], vars2[k]) for k in common if vars1[k] != vars2[k]]

    print(f"Comparing: {args.file1} vs {args.file2}\n")

    if only_in_1:
        print(f"Only in {args.file1} ({len(only_in_1)}):")
        for k in only_in_1:
            print(f"  - {k}={vars1[k][:50]}")
        print()

    if only_in_2:
        print(f"Only in {args.file2} ({len(only_in_2)}):")
        for k in only_in_2:
            print(f"  + {k}={vars2[k][:50]}")
        print()

    if changed:
        print(f"Changed values ({len(changed)}):")
        for k, v1, v2 in changed:
            print(f"  ~ {k}")
            print(f"    - {v1[:60]}")
            print(f"    + {v2[:60]}")
        print()

    if not only_in_1 and not only_in_2 and not changed:
        print("Files are identical.")


def cmd_template(args):
    """Generate a .env.example template from a .env file."""
    variables, errors = parse_env_file(args.file)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)

    output = args.output or args.file + ".example"
    with open(output, "w") as f:
        f.write(f"# Generated from {os.path.basename(args.file)}\n")
        f.write(f"# {len(variables)} variables\n\n")
        for key, value in variables.items():
            if args.keep_values:
                f.write(f"{key}={value}\n")
            else:
                # Provide placeholder hints
                hint = ""
                lower = key.lower()
                if any(s in lower for s in ["secret", "password", "token", "key", "api"]):
                    hint = "your-secret-here"
                elif any(s in lower for s in ["url", "uri", "endpoint"]):
                    hint = "https://example.com"
                elif any(s in lower for s in ["host"]):
                    hint = "localhost"
                elif any(s in lower for s in ["port"]):
                    hint = "3000"
                elif any(s in lower for s in ["email"]):
                    hint = "user@example.com"
                elif any(s in lower for s in ["db", "database"]):
                    hint = "mydb"
                elif any(s in lower for s in ["true", "false", "enable", "disable", "debug"]):
                    hint = "false"
                f.write(f"{key}={hint}\n")

    print(f"Template written to: {output}")
    print(f"Variables: {len(variables)}")


def cmd_merge(args):
    """Merge multiple .env files (later files override earlier)."""
    merged = OrderedDict()
    sources = {}
    for filepath in args.files:
        variables, errors = parse_env_file(filepath)
        if errors:
            print(f"Warnings for {filepath}:", file=sys.stderr)
            for e in errors:
                print(e, file=sys.stderr)
        for k, v in variables.items():
            if k in merged and merged[k] != v:
                sources[k] = filepath
            merged[k] = v

    if args.output:
        with open(args.output, "w") as f:
            f.write(f"# Merged from: {', '.join(os.path.basename(p) for p in args.files)}\n\n")
            for k, v in merged.items():
                f.write(f"{k}={v}\n")
        print(f"Merged {len(merged)} variables to: {args.output}")
    else:
        for k, v in merged.items():
            print(f"{k}={v}")


def cmd_list_keys(args):
    """List all keys in a .env file."""
    variables, _ = parse_env_file(args.file)
    for key in variables:
        if args.with_values:
            print(f"{key}={variables[key]}")
        else:
            print(key)


def cmd_check_missing(args):
    """Check if all keys from a template exist in the target .env file."""
    template_vars, _ = parse_env_file(args.template)
    target_vars, _ = parse_env_file(args.target)

    template_keys = set(template_vars.keys())
    target_keys = set(target_vars.keys())

    missing = sorted(template_keys - target_keys)
    extra = sorted(target_keys - template_keys)

    print(f"Template: {args.template} ({len(template_keys)} keys)")
    print(f"Target:   {args.target} ({len(target_keys)} keys)")
    print()

    if missing:
        print(f"Missing from target ({len(missing)}):")
        for k in missing:
            print(f"  ! {k}")
        print()

    if extra and not args.strict:
        print(f"Extra in target ({len(extra)}):")
        for k in extra:
            print(f"  + {k}")
        print()

    if not missing:
        print("All template keys present in target.")
        return 0
    else:
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Toolkit for .env file management: validate, diff, template, merge, check."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # validate
    p_val = subparsers.add_parser("validate", help="Validate .env file syntax")
    p_val.add_argument("file", help="Path to .env file")

    # diff
    p_diff = subparsers.add_parser("diff", help="Diff two .env files")
    p_diff.add_argument("file1", help="First .env file")
    p_diff.add_argument("file2", help="Second .env file")

    # template
    p_tpl = subparsers.add_parser("template", help="Generate .env.example from .env")
    p_tpl.add_argument("file", help="Source .env file")
    p_tpl.add_argument("--output", "-o", help="Output file (default: <file>.example)")
    p_tpl.add_argument("--keep-values", action="store_true", help="Keep actual values instead of placeholders")

    # merge
    p_merge = subparsers.add_parser("merge", help="Merge multiple .env files")
    p_merge.add_argument("files", nargs="+", help=".env files to merge (later overrides earlier)")
    p_merge.add_argument("--output", "-o", help="Output file (default: stdout)")

    # list-keys
    p_keys = subparsers.add_parser("list-keys", help="List all keys in .env file")
    p_keys.add_argument("file", help="Path to .env file")
    p_keys.add_argument("--with-values", action="store_true", help="Show values too")

    # check-missing
    p_check = subparsers.add_parser("check-missing", help="Check target .env has all keys from template")
    p_check.add_argument("template", help="Template .env file (expected keys)")
    p_check.add_argument("target", help="Target .env file to check")
    p_check.add_argument("--strict", action="store_true", help="Only report missing, not extra")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "validate": cmd_validate,
        "diff": cmd_diff,
        "template": cmd_template,
        "merge": cmd_merge,
        "list-keys": cmd_list_keys,
        "check-missing": cmd_check_missing,
    }

    exit_code = cmd_map[args.command](args) or 0
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
