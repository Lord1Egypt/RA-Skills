import json

def clean_llm_output(content: str) -> str:
    content = content.strip()

    if content.startswith("```"):
        lines = content.split("\n")
        lines = lines[1:-1]
        content = "\n".join(lines)

    return content.strip()


def validate_tasks(tasks):
    if not isinstance(tasks, list):
        raise ValueError("Tasks must be a list")

    ids = set()

    for t in tasks:
        if not all(k in t for k in ("id", "task", "depends_on")):
            raise ValueError("Invalid task format")

        ids.add(t["id"])

    for t in tasks:
        for dep in t["depends_on"]:
            if dep not in ids:
                raise ValueError("Invalid dependency reference")