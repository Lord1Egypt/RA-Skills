"""Generate task_suite.yaml from an existing SKILL.md.

Strategy:
1. Parse SKILL.md frontmatter (name, description, triggers)
2. Extract key sections:
   - "When to Use" scenarios -> positive test tasks
   - "When NOT to Use" -> negative test tasks (should reject/redirect)
   - <example> tags -> expected-output positive tests
   - <anti-example> tags -> negative tests
   - CLI/Usage sections -> command format tests
3. For each extracted scenario, generate a task with appropriate judge
4. Calibrate: filter out tasks that a null-skill (empty context) would pass

Judge selection logic:
- Scenario mentions specific keywords/outputs -> ContainsJudge
- Scenario involves quality/style assessment -> LLMRubricJudge
- Scenario has structured output -> PytestJudge (if test script can be generated)
"""

import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class GeneratedTask:
    """A single test task in a task suite."""

    id: str
    description: str
    prompt: str
    judge: dict  # {type, expected/rubric/test_file, pass_threshold}
    timeout_seconds: int = 120
    source: str = ""  # Which part of SKILL.md this came from


def generate_task_suite(skill_path: Path, mock: bool = False) -> dict:
    """Main entry: read SKILL.md, generate task_suite.yaml content.

    Args:
        skill_path: Path to the skill directory (containing SKILL.md).
        mock: If True, skip any LLM-based calibration.

    Returns:
        A dict representing the task_suite.yaml content.
    """
    skill_md_path = skill_path / "SKILL.md"
    if not skill_md_path.exists():
        raise FileNotFoundError(f"No SKILL.md found at {skill_md_path}")

    skill_md = skill_md_path.read_text()
    frontmatter, body = parse_frontmatter(skill_md)

    tasks: list[GeneratedTask] = []

    # Strategy 1: From description/triggers
    tasks.extend(generate_trigger_tasks(frontmatter))

    # Strategy 2: From "When to Use" section
    tasks.extend(generate_when_to_use_tasks(body, frontmatter))

    # Strategy 3: From <example> tags
    tasks.extend(generate_example_tasks(body, frontmatter))

    # Strategy 4: From <anti-example> tags
    tasks.extend(generate_anti_example_tasks(body, frontmatter))

    # Strategy 5: From output format/CLI sections
    tasks.extend(generate_output_format_tasks(body, frontmatter))

    # Deduplicate and limit
    tasks = deduplicate_tasks(tasks)
    tasks = tasks[:10]  # Max 10 tasks per suite

    return {
        "skill_id": frontmatter.get("name", skill_path.name),
        "version": "1.0",
        "generated_by": "skill-forge",
        "tasks": [asdict(t) for t in tasks],
    }


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Split YAML frontmatter from markdown body.

    Returns:
        Tuple of (frontmatter_dict, body_string).
    """
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            return fm, parts[2]
    return {}, content


def generate_trigger_tasks(fm: dict) -> list[GeneratedTask]:
    """From description field, generate a task that tests the skill's core promise."""
    desc = fm.get("description", "")
    name = fm.get("name", "unknown")
    if not desc:
        return []

    return [
        GeneratedTask(
            id=f"{name}-core-capability",
            description="Test core capability described in skill description",
            prompt=(
                f"You are an AI assistant with this skill loaded: {name}. "
                f"{desc}\n\n"
                f"Demonstrate the primary capability described above "
                f"with a concrete example."
            ),
            judge={
                "type": "llm-rubric",
                "rubric": (
                    f"The output should demonstrate the capability described as: "
                    f"'{desc}'. Score 1.0 if the output clearly addresses the "
                    f"described use case, 0.0 if it's generic or unrelated."
                ),
                "pass_threshold": 0.7,
            },
            source="frontmatter.description",
        )
    ]


def generate_when_to_use_tasks(body: str, fm: dict) -> list[GeneratedTask]:
    """Extract 'When to Use' scenarios and create positive tests."""
    name = fm.get("name", "unknown")
    tasks: list[GeneratedTask] = []

    # Find "When to Use" or equivalent Chinese/English section headers
    when_match = re.search(
        r"##\s*(?:When to Use|使用场景|使用|用法|核心流程)\s*\n(.*?)(?=\n##|\Z)",
        body,
        re.DOTALL,
    )
    if not when_match:
        return []

    when_text = when_match.group(1)
    # Extract bullet points (-, *, or numbered)
    bullets = re.findall(r"[-*]\s+(.+)", when_text)
    if not bullets:
        # Try numbered list
        bullets = re.findall(r"\d+\.\s+(.+)", when_text)

    for i, bullet in enumerate(bullets[:3]):  # Max 3 from this source
        # Clean up markdown formatting in bullet
        clean_bullet = re.sub(r"[*_`]", "", bullet).strip()
        tasks.append(
            GeneratedTask(
                id=f"{name}-use-case-{i + 1:02d}",
                description=f"Use case: {clean_bullet[:80]}",
                prompt=(
                    f"Scenario: {clean_bullet}\n\n"
                    f"Using the {name} skill, handle this scenario "
                    f"and produce the expected output."
                ),
                judge={
                    "type": "llm-rubric",
                    "rubric": (
                        f"The output should address this use case: "
                        f"'{clean_bullet}'. Score based on relevance "
                        f"and completeness."
                    ),
                    "pass_threshold": 0.6,
                },
                source="when_to_use",
            )
        )

    return tasks


def generate_example_tasks(body: str, fm: dict) -> list[GeneratedTask]:
    """Extract <example> tags and create tests that verify similar output."""
    name = fm.get("name", "unknown")
    tasks: list[GeneratedTask] = []

    examples = re.findall(r"<example>\s*(.*?)\s*</example>", body, re.DOTALL)

    for i, example in enumerate(examples[:2]):  # Max 2 from examples
        # Extract key phrases from the example
        lines = [
            line.strip()
            for line in example.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        if not lines:
            continue

        # Use first meaningful line as the scenario description
        scenario = lines[0]
        # Extract keywords that should appear in correct output
        keywords = extract_keywords(example)

        if keywords:
            tasks.append(
                GeneratedTask(
                    id=f"{name}-example-{i + 1:02d}",
                    description=f"Matches example pattern: {scenario[:60]}",
                    prompt=(
                        f"Following the {name} skill pattern shown in this "
                        f"example:\n{example}\n\n"
                        f"Produce similar output for a comparable scenario."
                    ),
                    judge={"type": "contains", "expected": keywords[:4]},
                    source="example_tag",
                )
            )

    return tasks


def generate_anti_example_tasks(body: str, fm: dict) -> list[GeneratedTask]:
    """Extract <anti-example> tags and create tests that verify the skill avoids bad patterns."""
    name = fm.get("name", "unknown")
    tasks: list[GeneratedTask] = []

    anti_examples = re.findall(
        r"<anti-example>\s*(.*?)\s*</anti-example>", body, re.DOTALL
    )

    for i, anti in enumerate(anti_examples[:2]):
        tasks.append(
            GeneratedTask(
                id=f"{name}-anti-pattern-{i + 1:02d}",
                description="Should avoid anti-pattern described in anti-example",
                prompt=(
                    f"Using the {name} skill, handle a task correctly. "
                    f"The following is an INCORRECT approach that should "
                    f"be avoided:\n{anti}\n\n"
                    f"Provide the CORRECT approach instead."
                ),
                judge={
                    "type": "llm-rubric",
                    "rubric": (
                        f"The output should NOT follow this anti-pattern: "
                        f"'{anti[:200]}'. Score 1.0 if the output correctly "
                        f"avoids the described mistake, 0.0 if it repeats "
                        f"the anti-pattern."
                    ),
                    "pass_threshold": 0.7,
                },
                source="anti_example_tag",
            )
        )

    return tasks


def generate_output_format_tasks(body: str, fm: dict) -> list[GeneratedTask]:
    """If the skill specifies output format/artifacts, test that output matches."""
    name = fm.get("name", "unknown")
    tasks: list[GeneratedTask] = []

    # Look for "Output Artifacts" table or equivalent sections
    output_match = re.search(
        r"##\s*(?:Output|输出|Output Artifacts)\s*\n(.*?)(?=\n##|\Z)",
        body,
        re.DOTALL,
    )
    if not output_match:
        return []

    output_text = output_match.group(1)
    # Extract deliverable types from table rows
    deliverables = re.findall(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|", output_text)

    found = 0
    for request, deliverable in deliverables:
        if found >= 1:
            break
        req = request.strip().strip("-")
        deliv = deliverable.strip().strip("-")
        # Skip header/separator rows
        if not req or not deliv or "Request" in req or "---" in req:
            continue
        tasks.append(
            GeneratedTask(
                id=f"{name}-output-format",
                description=f"Output should match: {deliv[:60]}",
                prompt=(
                    f"Using the {name} skill for: {req}\n"
                    f"Produce the expected deliverable."
                ),
                judge={
                    "type": "llm-rubric",
                    "rubric": (
                        f"The output should be: {deliv}. Score based on "
                        f"format compliance and completeness."
                    ),
                    "pass_threshold": 0.6,
                },
                source="output_artifacts",
            )
        )
        found += 1

    return tasks


def extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords from example text for ContainsJudge.

    Tries quoted strings first, then falls back to distinctive CamelCase
    or long lowercase identifiers.
    """
    # Remove code blocks, URLs, common markdown
    clean = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    clean = re.sub(r"https?://\S+", "", clean)
    clean = re.sub(r"[#*`\-\u2192]", "", clean)

    # Find quoted strings first (most specific)
    quoted = re.findall(r'["\']([^"\']+)["\']', clean)
    if quoted:
        return [q for q in quoted if len(q) > 2][:4]

    # Fall back to distinctive words: CamelCase or long identifiers
    words = re.findall(r"[A-Z][a-zA-Z]+(?:\.[a-zA-Z]+)*|[a-z_]{5,}", clean)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for w in words:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return unique[:4]


def deduplicate_tasks(tasks: list[GeneratedTask]) -> list[GeneratedTask]:
    """Remove tasks with duplicate IDs."""
    seen_ids: set[str] = set()
    result: list[GeneratedTask] = []
    for t in tasks:
        if t.id not in seen_ids:
            seen_ids.add(t.id)
            result.append(t)
    return result


def write_task_suite(suite: dict, output_path: Path) -> Path:
    """Write a task suite dict to a YAML file.

    Args:
        suite: The task suite dict (from generate_task_suite).
        output_path: Directory to write task_suite.yaml into.

    Returns:
        The path to the written file.
    """
    output_path.mkdir(parents=True, exist_ok=True)
    out_file = output_path / "task_suite.yaml"
    with open(out_file, "w") as f:
        yaml.dump(
            suite,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )
    return out_file
