---
name: decompose-plan
version: 1.0.0
description: |
  Forces M2.7 to produce an explicit structured plan before writing code.
  This makes Tree-of-Thought reasoning explicit instead of implicit, which
  is how Sonnet's extended thinking mode works. Captures sub-problems, APIs
  involved with version requirements, risks, and implementation order.
triggers:
  - any task expected to produce > 100 lines of code
  - any multi-file task (touching 2+ files)
  - any task mentioning "build", "implement", "design", "architect"
  - any task where decomposition could prevent wasted generation
tools:
  - llm
inputs:
  - task: user request (string)
  - rag_context: relevant retrieved context (string, optional)
  - specialist_prompt: domain-tuned system prompt (string, optional)
  - force_schema: if true, fail if output doesn't match schema
outputs:
  - plan:
      sub_problems: list of {title, description, depends_on}
      apis: list of {name, version_requirement, purpose}
      risks: list of {risk, mitigation, severity}
      files_affected: list of {path, change_type}
      order: ordered list of sub_problem titles
      estimated_loc: integer
metadata:
  openclaw:
    category: coding
    tags:
      - coding
      - planning
      - tree-of-thought
      - decomposition
    requires_openclaw: ">=2026.3.31"
    env_vars:
      - OPENCLAW_LLM_ENDPOINT
---

# Decompose and Plan

## The problem this solves

Local models generate code reactively — they start typing the moment they
see the task. This works for trivial tasks but produces mediocre output for
anything complex. Sonnet's "extended thinking" mode is essentially a forced
decomposition pass before generation.

We can replicate this behavior with M2.7 by requiring it to fill out a
structured plan template before any code is written. The act of filling the
template is the reasoning step.

## The planning prompt

```
You are planning the implementation of the following task. Your job is NOT
to write code yet — only to plan.

Task: {task}

{rag_context_if_any}

Produce a plan in the following exact JSON structure:

```json
{
  "sub_problems": [
    {
      "title": "short title",
      "description": "one paragraph describing what must be done",
      "depends_on": ["title of prior sub_problem"] or []
    }
  ],
  "apis": [
    {
      "name": "Framework.API.name",
      "version_requirement": "iOS 18+" or "Python 3.11+" or "none",
      "purpose": "why this API is needed"
    }
  ],
  "risks": [
    {
      "risk": "specific thing that could go wrong",
      "mitigation": "how to avoid or handle it",
      "severity": "high" | "medium" | "low"
    }
  ],
  "files_affected": [
    {
      "path": "relative/path/to/file.ext",
      "change_type": "create" | "modify" | "delete"
    }
  ],
  "order": ["sub_problem title", "sub_problem title", ...],
  "estimated_loc": integer
}
```

Requirements:
1. Break the task into 2-6 sub_problems. Fewer is better if possible.
2. List ALL APIs you will use, including their version requirements.
   If using iOS/Swift APIs, check iOS 26 deprecations.
3. Identify at least 2 risks. "No risks" is never acceptable — be critical.
4. File list must be complete — no files added later during implementation.
5. Order must be a valid topological sort of sub_problems based on depends_on.
6. Estimated LOC should be realistic. If > 500, flag for decomposition into
   smaller tasks.

Output ONLY the JSON. No explanation, no preamble, no markdown fences.
```

## Execution

```python
async def decompose_plan(task, rag_context=None, specialist_prompt=None,
                        force_schema=True):
    prompt = PLANNING_PROMPT.format(
        task=task,
        rag_context_if_any=f"\nRelevant context:\n{rag_context}\n" if rag_context else ""
    )

    system = specialist_prompt or "You are a senior engineer planning code."

    response = await llm.generate(
        prompt=prompt,
        model="m27-jangtq-crack",
        system=system,
        temperature=0.2,  # low temp for structured output
        max_tokens=2000
    )

    # Parse JSON
    try:
        plan = json.loads(response.strip().strip("`").strip("json").strip())
    except json.JSONDecodeError:
        # Try to extract JSON from response
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            plan = json.loads(match.group())
        else:
            if force_schema:
                raise PlanSchemaError("Model did not produce valid JSON")
            return {"error": "parse_failed", "raw": response}

    # Validate schema
    required_keys = {"sub_problems", "apis", "risks", "files_affected",
                     "order", "estimated_loc"}
    missing = required_keys - set(plan.keys())
    if missing and force_schema:
        raise PlanSchemaError(f"Missing keys: {missing}")

    # Validate order is topological
    if not _is_valid_topological(plan["sub_problems"], plan["order"]):
        raise PlanSchemaError("order is not a valid topological sort")

    # Flag if estimated_loc too large
    if plan["estimated_loc"] > 500:
        plan["warning"] = "Task may be too large — consider decomposing further"

    return plan


def _is_valid_topological(sub_problems, order):
    title_to_deps = {sp["title"]: set(sp.get("depends_on", [])) for sp in sub_problems}
    seen = set()
    for title in order:
        if title_to_deps[title] - seen:
            return False
        seen.add(title)
    return True
```

## Using the plan downstream

The plan becomes part of the context for code generation. Inject it like:

```
You have planned this task as follows:

{plan_as_readable_text}

Implement ONLY the sub_problem "{current_sub_problem}" now.
Do not attempt sub_problems that come later in the order.
```

This keeps the generation focused on one concern at a time and leverages
the decomposition to prevent the model from trying to write everything at
once.

## Why force the schema

Without schema enforcement, M2.7 tends to produce prose plans that are easy
to generate but hard to use programmatically. Structured JSON forces the
model to commit to specifics: exact file paths, exact API versions, exact
risk factors. Vagueness becomes syntactically impossible.

## When to skip this skill

For tasks where decomposition adds no value:
- Single-line fixes ("rename this variable")
- Trivial format conversions ("convert this JSON to CSV")
- Questions rather than implementation requests
- Tasks under 30 lines of expected output

The orchestrator handles this triage — decompose-plan is only invoked when
it will add value.

## Output usage

The parent orchestrator stores the plan in `task.scratchpad["plan"]`.
Subsequent steps (generation, build-feedback, reflection) read from this
plan rather than re-deriving what the task is about.

For iOS tasks specifically, the plan's `apis` section feeds into:
- RAG query expansion (retrieve docs for those specific APIs)
- Build feedback (validate those APIs are actually available at target iOS version)
- Reflection checklist (verify those APIs are used correctly)

## Failure modes

If M2.7 can't produce a valid plan after 2 retries, escalate to `claude-handoff`.
This is a strong signal that the task is outside local capability — if the
model can't even plan it, it certainly can't implement it.
