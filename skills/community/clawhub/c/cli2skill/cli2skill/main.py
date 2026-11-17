"""cli2skill — Turn any CLI into an Agent Skill."""
from __future__ import annotations
import argparse
import os
import sys
from .parser import run_help, parse_help_text, parse_subcommand_help
from .generator import generate_skill
from .mcp2skill import connect_and_extract, extract_from_config, generate_mcp_skill


def cmd_generate(args: argparse.Namespace) -> None:
    """Generate a SKILL.md for a CLI tool."""
    name = args.name or args.executable
    executable = args.executable

    # Get help text
    if args.help_file:
        with open(args.help_file, encoding="utf-8") as f:
            help_text = f.read()
    else:
        help_text = run_help(executable)

    # Parse
    meta = parse_help_text(name, help_text)

    # Enrich subcommands if requested
    if meta.commands and not args.no_subcommands and not args.help_file:
        meta = parse_subcommand_help(executable, meta)

    # Override executable path if specified
    exe = args.exe_path or executable

    # Generate
    skill_content = generate_skill(meta, executable=exe)

    # Output
    if args.output:
        out_dir = args.output
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{name}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(skill_content)
        print(f"Skill written to: {out_path}")
    else:
        print(skill_content)


def cmd_mcp(args: argparse.Namespace) -> None:
    """Extract MCP server tools and generate a skill."""
    # Resolve MCP server command
    if args.config and args.server:
        command, env = extract_from_config(args.config, args.server)
    elif args.command:
        command = args.command
        env = {}
    else:
        print("Error: provide either MCP command or --config + --server", file=sys.stderr)
        sys.exit(1)

    # Parse extra --env KEY=VALUE
    for e in args.env:
        if "=" in e:
            k, v = e.split("=", 1)
            env[k] = v

    print(f"Connecting to MCP server: {' '.join(command)}", file=sys.stderr)
    try:
        tools = connect_and_extract(command, env=env, timeout=args.timeout)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not tools:
        print("Warning: no tools extracted from MCP server", file=sys.stderr)

    print(f"Extracted {len(tools)} tools", file=sys.stderr)

    # Generate skill
    skill_content = generate_mcp_skill(
        tools,
        name=args.name,
        description=args.description,
        hint=args.hint,
    )

    # Output
    if args.output:
        os.makedirs(args.output, exist_ok=True)
        out_path = os.path.join(args.output, f"{args.name}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(skill_content)
        print(f"Skill written to: {out_path}", file=sys.stderr)
    else:
        print(skill_content)


def cmd_preview(args: argparse.Namespace) -> None:
    """Preview what --help gives us without generating."""
    help_text = run_help(args.executable)
    name = args.name or args.executable
    meta = parse_help_text(name, help_text)

    print(f"Name: {meta.name}")
    print(f"Description: {meta.description[:200]}")
    print(f"Commands: {len(meta.commands)}")
    for cmd in meta.commands:
        print(f"  - {cmd.name}: {cmd.description[:100]}")
    print(f"Global options: {len(meta.global_options)}")
    for opt in meta.global_options:
        print(f"  - {opt.flags}: {opt.description[:80]}")


def app() -> None:
    p = argparse.ArgumentParser(
        prog="cli2skill",
        description="Turn any CLI into an Agent Skill (SKILL.md)",
    )
    sub = p.add_subparsers(dest="cmd")

    # generate
    g = sub.add_parser("generate", aliases=["gen", "g"], help="Generate SKILL.md")
    g.add_argument("executable", help="CLI command to analyze")
    g.add_argument("--name", help="Skill name (default: executable name)")
    g.add_argument("--output", "-o", help="Output directory")
    g.add_argument("--exe-path", help="Full executable path for skill (e.g. 'python /path/to/tool.py')")
    g.add_argument("--help-file", help="Read --help text from file instead of running")
    g.add_argument("--no-subcommands", action="store_true", help="Skip subcommand help parsing")
    g.set_defaults(func=cmd_generate)

    # preview
    pv = sub.add_parser("preview", aliases=["p"], help="Preview parsed metadata")
    pv.add_argument("executable", help="CLI command to analyze")
    pv.add_argument("--name", help="Override name")
    pv.set_defaults(func=cmd_preview)

    # mcp
    m = sub.add_parser("mcp", aliases=["m"], help="Extract MCP server tools → SKILL.md")
    m.add_argument("command", nargs="*", help="MCP server command (e.g. 'npx tavily-mcp@latest')")
    m.add_argument("--name", required=True, help="Skill name")
    m.add_argument("--config", help="Path to Claude Code settings.json")
    m.add_argument("--server", help="MCP server name from settings.json")
    m.add_argument("--output", "-o", help="Output directory")
    m.add_argument("--description", help="Override skill description")
    m.add_argument("--hint", help="Implementation hint for the agent")
    m.add_argument("--timeout", type=int, default=30, help="Timeout in seconds (default: 30)")
    m.add_argument("--env", action="append", default=[], help="Extra env vars (KEY=VALUE), repeatable")
    m.set_defaults(func=cmd_mcp)

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    app()
