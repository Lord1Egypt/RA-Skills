"""Generate SKILL.md from a skill_spec.yaml.

Takes a structured specification (name, purpose, inputs, outputs,
quality_criteria) and produces a complete SKILL.md with frontmatter,
When to Use / When NOT to Use sections, examples, and output artifacts.
"""

import yaml
from pathlib import Path


def generate_skill_from_spec(spec: dict) -> str:
    """Generate a complete SKILL.md from a structured spec.

    Args:
        spec: Dict with keys: name, purpose, inputs, outputs,
              quality_criteria, domain_knowledge, reference_skills.

    Returns:
        A string containing the full SKILL.md content.
    """
    name = spec["name"]
    purpose = spec["purpose"]

    # Frontmatter
    frontmatter = {
        "name": name,
        "description": derive_description(purpose, spec.get("inputs", [])),
        "license": "MIT",
        "triggers": derive_triggers(name, purpose),
    }

    # Body sections
    sections: list[str] = []

    # Title and purpose
    title = name.replace("-", " ").title()
    sections.append(f"# {title}\n")
    sections.append(f"{purpose}\n")

    # When to Use
    sections.append("## When to Use\n")
    inputs = spec.get("inputs", [])
    if inputs:
        for inp in inputs:
            desc = inp.get("description", inp.get("name", "input"))
            sections.append(f"- When you have {desc}\n")
    else:
        sections.append(f"- When you need to {purpose.lower()}\n")

    # When NOT to Use
    sections.append("\n## When NOT to Use\n")
    sections.append(
        "- For general-purpose tasks not related to this skill's domain\n"
    )
    ref_skills = spec.get("reference_skills", [])
    if ref_skills:
        for ref in ref_skills[:2]:
            sections.append(
                f"- When you specifically need {ref} capabilities instead\n"
            )

    # Examples from quality_criteria (P7 behavior anchoring from prompt-hardening)
    quality = spec.get("quality_criteria", [])
    if quality:
        criteria_desc = "; ".join(
            c.get("description", c.get("name", ""))
            for c in quality[:3]
        )
        sections.append("\n<example>\n")
        sections.append(
            f"Correct usage: Apply {name} to produce output meeting "
            f"quality criteria: {criteria_desc}\n"
        )
        sections.append("reasoning: These criteria ensure the output is "
                        "usable without manual correction.\n")
        sections.append("</example>\n")
        sections.append("\n<anti-example>\n")
        sections.append(
            f"Incorrect: Producing output that violates quality criteria "
            f"({criteria_desc})\n"
        )
        sections.append("reasoning: Violating these criteria means the output "
                        "needs manual rework, defeating the purpose of the skill.\n")
        sections.append("</anti-example>\n")

    # P1 Triple reinforcement for critical constraints
    critical = spec.get("critical_constraints", [])
    if critical:
        sections.append("\n## Critical Constraints\n")
        for constraint in critical:
            sections.append(f"\nMUST: {constraint}\n")
        sections.append(
            f"\nI REPEAT: The above constraints are non-negotiable. "
            f"NEVER skip or rationalize around them.\n"
        )

    # Domain knowledge
    domain = spec.get("domain_knowledge", [])
    if domain:
        sections.append("\n## Domain Knowledge\n")
        for item in domain:
            sections.append(f"- {item}\n")

    # Output section
    outputs = spec.get("outputs", [])
    if outputs:
        sections.append("\n## Output Artifacts\n")
        sections.append("| Request | Deliverable |\n")
        sections.append("|---------|------------|\n")
        for out in outputs:
            fmt = out.get("format", "text")
            out_name = out.get("name", "output")
            sections.append(f"| {name} execution | {fmt}: {out_name} |\n")

    # Related skills
    if ref_skills:
        sections.append("\n## Related Skills\n")
        for ref in ref_skills:
            sections.append(f"- `{ref}`\n")

    # Compose final document
    fm_str = yaml.dump(
        frontmatter,
        allow_unicode=True,
        default_flow_style=False,
    )
    body = "".join(sections)
    return f"---\n{fm_str}---\n\n{body}"


def derive_description(purpose: str, inputs: list) -> str:
    """Create a concise description from purpose and inputs."""
    if inputs:
        input_hints = ", ".join(
            i.get("description", i.get("name", ""))[:30] for i in inputs[:2]
        )
        return f"{purpose}. Input: {input_hints}"
    return purpose


def derive_triggers(name: str, purpose: str) -> list[str]:
    """Generate trigger phrases from the skill name and purpose."""
    triggers = [name, name.replace("-", " ")]

    # Extract meaningful words from purpose (>3 chars, not common)
    stop_words = {
        "that", "this", "with", "from", "into", "when", "will",
        "have", "been", "more", "also", "they", "them", "than",
        "each", "make", "like", "long", "very", "just", "over",
    }
    for word in purpose.split():
        clean = word.strip(".,;:!?").lower()
        if len(clean) > 3 and clean not in stop_words:
            triggers.append(clean)

    # Deduplicate while keeping order, cap at 6
    seen: set[str] = set()
    unique: list[str] = []
    for t in triggers:
        if t.lower() not in seen:
            seen.add(t.lower())
            unique.append(t)
    return unique[:6]
