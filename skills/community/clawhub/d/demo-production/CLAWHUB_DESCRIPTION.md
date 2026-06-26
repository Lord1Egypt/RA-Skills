# Clawhub Description

## Short Description

Turn rough product ideas into interactive demos with a structured prototype-review-production pipeline.

## Full Description

Demo Production helps a coding agent transform vague or incomplete project ideas into usable, interactive demos. It is built for users who know what they want in broad terms but have not fully specified the workflow, data model, UI structure, or technical plan.

The skill guides the coding agent through a 4-stage pipeline:

1. Intent intake and reconstruction
2. Planning and project structure design
3. Interactive demo production with a mandatory review gate
4. Production-style demo completion and edge case validation after approval

Its default behavior is to autonomously build until the interactive prototype is ready, then stop and ask the user to review the workflow, visual direction, missing screens, and whether to continue. This makes it especially useful for fuzzy ideas where building too far in the wrong direction would waste time.

It can also perform focused reference research when an idea resembles known products, open-source projects, or mature software categories. References are used to improve workflows, information architecture, interaction patterns, terminology, and expected UI states without cloning branding or proprietary design.

Best for:

- Vague product ideas
- MVP-style demos
- Clickable prototypes
- AI tool demos
- Dashboard demos
- Internal workflow demos
- Product concepts inspired by known tools

Key behaviors:

- Reduces user prompting
- Makes assumptions explicit
- Separates mocked, simulated, and real behavior
- Builds interactive prototypes before finalizing
- Stops at the review gate by default
- Continues to production demo only after approval, unless the user asks for autonomous completion
- Includes edge case validation for demo reliability

Example prompt:

```text
Use $demo-production to turn this rough idea into an interactive demo with a review gate:

Build something like Notion mixed with Trello, but for indie game makers managing tasks, assets, and versions.
```

## Tags

demo, prototype, product-design, mvp, ai-demo, web-demo, planning, workflow, coding-agent-skill
