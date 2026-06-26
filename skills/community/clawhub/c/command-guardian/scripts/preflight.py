import argparse
import json
import sys

from guardlib import preflight_report


def format_text(report):
    lines = [f"Risk: {report['risk']}"]
    lines.append("Why:")
    for reason in report["reasons"] or ["no major risk signals detected"]:
        lines.append(f"- {reason}")
    if report.get("safer_commands"):
        lines.append("")
        lines.append("Safer commands:")
        for item in report["safer_commands"]:
            lines.append(f"- {item}")
    lines.append("")
    lines.append("Safer rewrite:")
    for item in report["safer_actions"] or ["no safer rewrite suggested"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Rollback:")
    for item in report["rollback"] or ["no rollback guidance needed"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append(f"Need approval: {'yes' if report['need_approval'] else 'no'}")
    return "\n".join(lines)


def load_command(args):
    if args.command:
        return args.command
    if args.command_file:
        with open(args.command_file, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("Provide --command, --command-file, or pipe a command on stdin.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command")
    parser.add_argument("--command-file")
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--allowed-root", action="append", dest="allowed_roots")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    command = load_command(args)
    report = preflight_report(command, args.cwd, args.allowed_roots or [])
    if args.format == "text":
        print(format_text(report))
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
