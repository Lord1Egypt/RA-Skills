"""Generate Agent Skill SKILL.md from CLIMetadata."""
from __future__ import annotations
from .parser import CLIMetadata


def generate_skill(meta: CLIMetadata, executable: str | None = None) -> str:
    """Generate SKILL.md content from parsed CLI metadata."""
    exe = executable or meta.name
    lines: list[str] = []

    # Frontmatter
    lines.append("---")
    lines.append(f"name: {meta.name}")
    desc = meta.description[:100] if meta.description else f"Agent skill for {meta.name} CLI"
    lines.append(f"description: {desc}")
    lines.append("user-invocable: false")
    lines.append(f"allowed-tools: Bash({exe} *)")
    lines.append("---")
    lines.append("")

    # Header
    lines.append(f"# {meta.name}")
    lines.append("")
    if meta.description:
        lines.append(meta.description)
        lines.append("")

    # Commands
    if meta.commands:
        lines.append("## Commands")
        lines.append("")
        lines.append("```bash")
        for cmd in meta.commands:
            # Build usage line
            usage = f"{exe} {cmd.name}"
            for arg in cmd.arguments:
                usage += f" <{arg.name}>"
            for opt in cmd.options:
                flag = opt.flags.split(",")[-1].strip().split()[0]
                if opt.default:
                    usage += f" [{flag}]"
            lines.append(usage)
        lines.append("```")
        lines.append("")

        # Detailed command descriptions
        for cmd in meta.commands:
            lines.append(f"### {cmd.name}")
            if cmd.description:
                lines.append(cmd.description)
            if cmd.arguments:
                for arg in cmd.arguments:
                    lines.append(f"- `{arg.name}`: {arg.description}")
            if cmd.options:
                for opt in cmd.options:
                    default = f" (default: {opt.default})" if opt.default else ""
                    lines.append(f"- `{opt.flags}`: {opt.description}{default}")
            lines.append("")
    else:
        # No subcommands — show global usage
        lines.append("## Usage")
        lines.append("")
        lines.append("```bash")
        usage = exe
        for opt in meta.global_options:
            flag = opt.flags.split(",")[-1].strip().split()[0]
            usage += f" [{flag}]"
        lines.append(usage)
        lines.append("```")
        lines.append("")

    # Global options
    if meta.global_options:
        lines.append("## Options")
        lines.append("")
        for opt in meta.global_options:
            default = f" (default: {opt.default})" if opt.default else ""
            lines.append(f"- `{opt.flags}`: {opt.description}{default}")
        lines.append("")

    # When to use
    lines.append("## When to use")
    lines.append(f"- {desc}")
    if meta.commands:
        cmd_names = ", ".join(f"`{c.name}`" for c in meta.commands[:5])
        lines.append(f"- Available commands: {cmd_names}")
    lines.append("")

    return "\n".join(lines)
