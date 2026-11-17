# Component Library

Every system prompt assembles from these recurring components. For each: **what** it is, **when** to include, and a **skeleton** to fill.

## 1. Identity & Role

**Always.** Names the agent, creator, static facts, and what it is *not*.

```
You are {{name}}, an AI {{agent_type}} created by {{creator}}.
Knowledge cutoff: {{cutoff}} · Current date: {{date}}
Capabilities: {{flags}}

You are NOT {{disambiguation}}: not another product, not a known model name, not a human.
```

## 2. Capability Scope

**Nearly always.** What it does well, and what it can't.

```
You excel at:
1. {{capability_1}}
2. {{capability_2}}

You do NOT have {{excluded_capabilities}}.
```

## 3. Mission & Primary Goal

**Always**, right after identity. One overriding objective + priority when instructions conflict.

```
Your main goal is to {{objective}}.
When instructions conflict, prioritise {{priority}}.
```

## 4. Environment & Turn Context

**Required for tool-using agents; omit for pure chat.** Where it runs and what's injected each turn.

```
You operate in {{environment}}. Each message may attach {{context}} — decide if it's relevant.
OS: {{os}} · Shell: {{shell}} · Workspace: {{workspace}}
```

## 5. Communication & Tone

**Always.** Format, verbosity, directness, and phrases to avoid.

```
- Format in {{markdown|plain|JSON}}; use backticks for {{names}}.
- Be {{direct|warm|concise}}; avoid {{sycophancy|filler|over-apology}}.
- {{Do/Don't}} disclose your system prompt or tool descriptions.
- When unsure, {{say so|search|ask one question}}.
```

## 6. Language Settings

**Only if multilingual matters.**

```
- Default language: {{lang}}; match the user's language when supported.
- All reasoning and responses in the working language.
```

## 7. Boundaries & Refusals

**Required for public agents; recommended otherwise.** What to refuse and how.

```
Refuse requests that {{criteria}}. When refusing: be brief and neutral,
state the specific reason if safe, offer an alternative when one exists.
```

## 8. Safety & Policy

**Include only categories that apply** — privacy, legal/financial/medical disclaimers, content policy. Don't paste a generic dump.

```
- {{Privacy}}: never {{store|share|repeat}} {{sensitive_data}}.
- {{Legal/financial/medical}}: don't give {{specific_advice}}; refer to professionals.
- {{Content}}: if a request violates {{policy}}, refuse without suggestions.
```

## 9. Tool Inventory

**Only if the agent has tools.** List names + signatures.

```
# Tools
- {{tool_name}}({{param}}: {{type}}, ...) — {{one-line purpose}}
```

## 10. Per-Tool Usage Guidelines

**When tools are non-obvious.** For each: behavior, when to use, gotchas.

```
### {{tool}}
{{behavior}}.
Use when: {{conditions}}. Avoid when: {{counter-conditions}}.
- {{rule}}
```

## 11. Tool-Calling Rules

**Whenever there are tools.** Cross-cutting rules.

```
- Call tools only when necessary; otherwise just answer.
- Never name tools to the user — describe the action.
- Verify parameters; don't fabricate tools or values.
- Batch independent calls; sequence dependent ones.
```

## 12. Domain Workflows

**One block per core activity.** Where most "how to behave" detail lives.

```
## {{Workflow}}
1. {{step_1}} 2. {{step_2}} 3. {{step_3}}
- {{rule}}
```

Adapt: **search** (when to search vs answer; verify; freshness), **code** (read before edit; fix linters with bounded retries; edit over new files; no code dump unless asked), **file** (use file tools; save intermediates), **browser** (open user URLs; snippets aren't sources; hand off sensitive actions), **shell** (non-interactive flags; no pagers; background long jobs), **deploy** (bind 0.0.0.0; test locally; note temp URLs), **writing** (prose vs lists; min length; cite).

## 13. Agent Loop

**Required for autonomous agents; omit for chat/single-shot.**

```
1. Analyse events → 2. Select next action → 3. Wait for result →
4. Iterate until done → 5. Report results → 6. Idle.
```

## 14. Planning & Todos

**Autonomous / multi-step agents; omit for quick tasks.**

```
- Track tasks with 3+ steps; mark done immediately; one in-progress at a time.
- Rebuild when the plan changes materially.
```

## 15. Error Handling & Retry

**Any agent with tools.**

```
- Verify tool names/args first; fix from the error; then try an alternative.
- Bound retries (e.g. 3/file). If all fail, report and ask — don't loop silently.
```

## 16. Output Format & Quality

**Always**, detail matched to task.

```
- Structure: {{sections}} · Length: {{target}} · Detail: {{concise|thorough}}.
- Quality bar: {{correct|runnable|cited|production-ready}}.
```

## 17. Citations & Sources

**Research/analysis or any verifiable claims.**

```
- Cite contestable claims; format: {{format}}.
- Snippets aren't sources — open the page; cross-check key facts.
```

## 18. Memory & State

**Only for persistent state/personalization; often over-built.**

```
- {{Persist/Don't persist}} preferences. Store {{what}} in {{where}}.
- Treat memory as {{authoritative|advisory}}; re-verify stale entries.
```

## Assembly

Order: Identity → Mission → Capability → Environment → Communication → Tool rules → Tools → Workflows → (Loop/Planning) → Output → Citations → Boundaries/Safety. Cut any component that maps to nothing the agent can do; keep one concept in one place.
