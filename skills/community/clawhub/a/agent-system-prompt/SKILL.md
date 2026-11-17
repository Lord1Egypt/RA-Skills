---
name: agent-system-prompt
description: Design and generate system prompts for AI agents, assistants, and chatbots. Use when creating, writing, or improving a system prompt, persona, role definition, or operating instructions for any AI agent (assistant, coding, autonomous, research, support, or orchestrator). Provides a component-based methodology, agent archetypes, and ready-to-fill templates.
---

# Agent System Prompt

Generate a complete system prompt for an AI agent from plain-language requirements, using a reusable component library and a deterministic assembly workflow.

## Workflow

1. **Gather requirements** — purpose, tools, audience/language, tone, hard constraints, output format, environment. Ask only if a missing item would change the result.
2. **Select archetype** — match the purpose in [references/agent-types.md](references/agent-types.md); it lists required/optional components and gives the skeleton.
3. **Assemble components** — fill each required component from [references/anatomy.md](references/anatomy.md); include only what the agent will actually use.
4. **Write** — start from the matching template in [assets/templates/](assets/templates/); follow [references/output-patterns.md](references/output-patterns.md).
5. **Validate** — run the checklist below.

## Quality Checklist

- [ ] Identity unambiguous — "You are X" plus what it is and is *not*.
- [ ] One clear mission stated up front.
- [ ] Every tool described — what it does and *when to use it*.
- [ ] Tone defined — phrasing to use and to avoid.
- [ ] Boundaries explicit — what to refuse, disclaim, or never disclose.
- [ ] Output format specified — structure, length, citation conventions.
- [ ] Environment/context stated — what's available each turn.
- [ ] No dead weight — every section maps to a real capability or constraint.
- [ ] Consistent voice — imperative, present tense, second person.

## Resources

- [references/anatomy.md](references/anatomy.md) — component library (building blocks + skeletons).
- [references/agent-types.md](references/agent-types.md) — archetypes and their required/optional components.
- [references/output-patterns.md](references/output-patterns.md) — writing style, section order, validation.
- [assets/templates/](assets/templates/) — ready-to-fill templates per archetype.
