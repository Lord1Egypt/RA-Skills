"""Analyze visual media + text description to extract best practice steps."""

from .mllm.base import MLLMProvider, MLLMResponse

ANALYSIS_PROMPT = """\
You are an expert at analyzing task demonstrations and extracting structured best practices.

You are given:
1. A sequence of images (frames from a video or screenshots) showing someone performing a task.
2. A text description of what the task accomplishes.

## Task Description
{description}

## Your Job

Analyze the images in order and produce a structured best practice document with the following sections:

### 1. TASK_NAME
A short, kebab-case identifier for this task (e.g., "setup-ci-cd-pipeline").

### 2. TASK_TITLE
A human-readable title (e.g., "Set Up CI/CD Pipeline with GitHub Actions").

### 3. TASK_DESCRIPTION
A one-sentence description suitable for an AI agent's skill description field.
Include trigger phrases starting with "Use when..." followed by 3-5 specific scenarios.
Aim for 20-40 words total.

### 4. TASK_EMOJI
A single emoji that represents this task.

### 5. REQUIRED_TOOLS
A JSON list of CLI tools/binaries required (e.g., ["git", "docker", "kubectl"]).

### 6. REQUIRED_ENV
A JSON list of environment variables needed (e.g., ["GITHUB_TOKEN"]).

### 7. STEPS
A detailed, numbered list of steps. For each step:
- Step number and title
- What to do (imperative instructions)
- Any commands to run (in code blocks)
- Expected outcome
- Common pitfalls to avoid

### 8. BEST_PRACTICES
A bullet list of key best practices, tips, and warnings observed from the demonstration.

### 9. SKILL_INSTRUCTIONS
Write the full body of an agent skill instruction document. This should be written as if you are instructing an AI agent on how to perform this task. Use second person ("You should..."). Include all the steps, commands, decision points, and error handling. This will become the main content of a SKILL.md file.

Respond with ONLY the structured output using the exact section headers above (### 1. TASK_NAME, etc.).
Do not include any preamble or conclusion outside these sections.
"""


def analyze_best_practice(
    provider: MLLMProvider,
    images_b64: list[str],
    description: str,
) -> MLLMResponse:
    """Send images and description to MLLM for best practice analysis.

    Args:
        provider: Configured MLLM provider.
        images_b64: Base64-encoded images (video frames or screenshots).
        description: User-provided text description of the task.

    Returns:
        MLLMResponse containing the structured analysis.
    """
    prompt = ANALYSIS_PROMPT.format(description=description)
    return provider.analyze_images(images_b64, prompt)


def parse_analysis(text: str) -> dict:
    """Parse the structured analysis text into a dictionary.

    Extracts sections by their headers and returns a dict with keys:
    task_name, task_title, task_description, task_emoji,
    required_tools, required_env, steps, best_practices, skill_instructions.
    """
    import json
    import re

    sections = {}
    section_pattern = re.compile(r"^###\s*\d+\.\s*(\w+)\s*$", re.MULTILINE)
    matches = list(section_pattern.finditer(text))

    for i, match in enumerate(matches):
        key = match.group(1).lower()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        sections[key] = content

    # Parse JSON fields
    for json_key in ("required_tools", "required_env"):
        raw = sections.get(json_key, "[]")
        json_match = re.search(r"\[.*\]", raw, re.DOTALL)
        if json_match:
            try:
                sections[json_key] = json.loads(json_match.group())
            except json.JSONDecodeError:
                sections[json_key] = []
        else:
            sections[json_key] = []

    return sections
