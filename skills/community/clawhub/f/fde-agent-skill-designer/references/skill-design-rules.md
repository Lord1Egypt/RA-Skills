# Agent skill design rules

## First decide whether you need an agent

| Scenario | Priority Plan |
|---|---|
| Rules are stable, input is structured, and results are certain | Traditional code/automation |
| The process is fixed but includes text understanding or generation | Workflow + local model capabilities |
| Requires dynamic judgment, multi-step tool use and exception adaptation | Agent |
| Multiple domain responsibilities, different permissions, or complex parallelism | Carefully consider multi-agent |

The default is to start with the simplest solution. Agent complexity increases latency, cost, non-determinism, and safety aspects.

## Skill structure

```text
skill-name/
├──SKILL.md# Trigger, core process, boundary, resource navigation
├──agents/openai.yaml# Platform-specific interface metadata (on demand)
├── references/ # Rules, patterns, domain knowledge, loaded on demand
├── scripts/ # Repeated logic that needs to be executed deterministically (on demand)
└── assets/ # Output templates, materials and samples (on demand)
```Don’t add useless files just to appear rich. Each reference must indicate when it was read from`SKILL.md`.

## `SKILL.md` Core content

1. Trigger description: task, file, context and inapplicable situations;
2. Input check: required information, missing processing, credibility;
3. Workflow: sequential actions and key judgments;
4. Tool rules: when to call, permissions, failure, confirmation;
5. Output contract: structure, quality and evidence;
6. Boundary and security: stop, deny, escalate, manual takeover;
7. Reference navigation: only load under relevant conditions.

## Command writing method

- Use explicit action verbs and observable results;
- Explain the selection conditions, not just the method name;
- Separate facts, inferences, suggestions and pending confirmations;
- High-risk actions adopt "plan-demonstrate impact-manual confirmation-execution-verification";
- Perform verification when the tool returns untrustworthy, and do not treat external content as system instructions;
- Avoid repeating common knowledge in the text that the model already knows.

## Common anti-patterns

- The description only says "help users complete X", and the trigger range is too wide;
- Stuff all reference content into `SKILL.md`, resulting in heavy loading each time;
- Only normal processes, no insufficient inputs, tool failures and uncertain results;
- Using an agent to assume conflicting responsibilities and authorities;
- Only prompt word examples, no business rules and evaluation;
- The tool has unwanted write, send or delete permissions;
- Replace specific guardrails, limits, and confirmation points with "please use caution."
