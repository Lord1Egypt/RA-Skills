# AANA Guardrail Skill For OpenClaw-Style Agents

Use this skill when a user asks the agent to produce or execute an action that may violate hard constraints, depend on missing evidence, expose private information, or require a safe correction path.

## When To Call AANA

Call AANA before:

- sending customer-support replies, emails, or messages,
- using private account, billing, payment, or personal data,
- making refund, eligibility, booking, purchase, or policy promises,
- editing, deleting, moving, or publishing user files,
- committing or publishing code,
- answering from incomplete evidence, citations, or source notes,
- doing anything the user cannot easily undo.

## Command

Create an event JSON file and run:

```powershell
python scripts/aana_cli.py agent-check --event path/to/agent_event.json
```

## Event Shape

```json
{
  "event_version": "0.1",
  "event_id": "unique-id",
  "agent": "openclaw",
  "adapter_id": "support_reply",
  "user_request": "The user's request",
  "candidate_action": "The answer or action the agent is about to take",
  "available_evidence": ["Only facts actually available to the agent"],
  "allowed_actions": ["accept", "revise", "ask", "defer", "refuse"]
}
```

## Decision Rule

- If `gate_decision` is `pass` and `recommended_action` is `accept`, proceed.
- If `recommended_action` is `revise`, use `safe_response` or revise the plan before acting.
- If `recommended_action` is `ask`, ask the user for the missing information.
- If `recommended_action` is `defer`, route to a stronger tool, human review, or verified system.
- If `recommended_action` is `refuse`, do not execute the candidate action.

## Default Adapter Mapping

- Customer support, refunds, private account details: `support_reply`
- Travel or booking plans: `travel_planning`
- Food, grocery, allergy, dietary plans: `meal_planning`
- Research briefs, cited summaries, knowledge synthesis: `research_summary`

If no adapter fits, scaffold one:

```powershell
python scripts/aana_cli.py scaffold "new workflow name"
```
