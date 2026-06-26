"""Generate OpenClaw-compatible SKILL.md from analyzed best practice data."""

import json
from pathlib import Path

from .config import SkillConfig


def generate_skill(
    analysis: dict,
    output_dir: str,
    skill_config: SkillConfig | None = None,
) -> str:
    """Generate an OpenClaw-compatible skill directory.

    Args:
        analysis: Parsed analysis dict from analyzer.parse_analysis().
        output_dir: Directory to create the skill in.
        skill_config: Skill generation settings.

    Returns:
        Path to the generated SKILL.md file.
    """
    if skill_config is None:
        skill_config = SkillConfig()

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    task_name = analysis.get("task_name", "generated-skill").strip()
    task_title = analysis.get("task_title", "Generated Skill").strip()
    task_description = analysis.get("task_description", "A generated skill.").strip()
    task_emoji = analysis.get("task_emoji", skill_config.default_emoji).strip()
    required_tools = analysis.get("required_tools", [])
    required_env = analysis.get("required_env", [])
    skill_instructions = analysis.get("skill_instructions", "")
    steps = analysis.get("steps", "")
    best_practices = analysis.get("best_practices", "")

    # Build metadata
    metadata: dict = {
        "openclaw": {
            "emoji": task_emoji,
            "os": skill_config.default_os,
        }
    }

    requires: dict = {}
    if required_tools:
        requires["bins"] = required_tools
    if required_env:
        requires["env"] = required_env
        metadata["openclaw"]["primaryEnv"] = required_env[0]
    if requires:
        metadata["openclaw"]["requires"] = requires

    metadata_json = json.dumps(metadata, ensure_ascii=False)

    # Build SKILL.md content
    lines = [
        "---",
        f"name: {task_name}",
        f"description: {task_description}",
        f'metadata: {metadata_json}',
        "---",
        "",
        f"# {task_title}",
        "",
    ]

    if skill_instructions:
        lines.append(skill_instructions)
    else:
        # Fallback: use steps and best_practices directly
        if steps:
            lines.append("## Steps")
            lines.append("")
            lines.append(steps)
            lines.append("")
        if best_practices:
            lines.append("## Best Practices")
            lines.append("")
            lines.append(best_practices)

    content = "\n".join(lines) + "\n"

    skill_path = out / "SKILL.md"
    skill_path.write_text(content, encoding="utf-8")

    return str(skill_path)
