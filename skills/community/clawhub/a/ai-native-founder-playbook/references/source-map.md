# Source Map And Caveats

This skill is an independent, source-attributed synthesis for agent use. The repository includes source PDFs under `docs/` for convenient reading and attribution, while the skill instructions avoid long verbatim excerpts and use original operational synthesis.

## Primary Startup Source

- Anthropic / Claude blog: "The founder's playbook: Building an AI-native startup", published May 14, 2026.
- Public PDF: "The Founder's Playbook: Building an AI-Native Startup", 36 pages.
- Included English PDF: `docs/The-Founders-Playbook-05062026_v3.pdf`
- Included Chinese PDF: `docs/创业者手册-构建AI原生创业公司-中文.pdf`

Source-derived ideas used here:

- The startup lifecycle is reframed as Idea, MVP, Launch, and Scale.
- The founder role shifts from individual contributor toward orchestrator of agents and systems.
- AI is most useful when it compresses research, coding, and operational workflow loops without bypassing evidence.
- Each stage needs exit criteria, common failure modes, and AI-assisted exercises.
- The largest AI-native risks are building before validating, agentic technical debt, false product-market fit, founder bottlenecks, deferred security/compliance, and scaling without operational maturity.
- Defensibility at scale comes from domain depth, user data loops, integrations, workflow lock-in, and auditable operating systems.

## Agent Skills Sources

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills overview: https://agentskills.io/home
- Agent Skills creator best practices: https://agentskills.io/skill-creation/best-practices
- Anthropic Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Bilingual README structure reference: https://github.com/marswaveai/skills/tree/main

Skill design choices used here:

- Keep `SKILL.md` concise and under the progressive disclosure budget.
- Put only `name` and `description` in frontmatter for broad compatibility.
- Put "when to use" trigger language in the description.
- Move detailed frameworks into `references/`.
- Add paired `.zh.md` reference files for Chinese users.
- Use scripts only for deterministic, repeatable helper output.

## Caveats

- Verify current availability and behavior of specific products, beta features, APIs, security tools, and compliance requirements before relying on them.
- Do not treat AI-generated security, legal, compliance, fundraising, or financial recommendations as professional advice.
- Do not copy long passages from the source documents into downstream generated artifacts unless the user has rights to do so.
- Attribute the public source when publishing outputs substantially based on this framework.
