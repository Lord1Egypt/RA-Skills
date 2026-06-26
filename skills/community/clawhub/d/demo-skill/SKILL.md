---
name: demo-doc-generator
description: Generate well-structured technical documents, reports, and summaries with consistent formatting. Use this skill whenever the user asks to write a technical document, API reference, project report, feature spec, meeting minutes, or any structured professional document — even if they just say "help me write a doc" or "create a report". This skill ensures every document is clear, organized, and ready to use.
---

# Demo Document Generator

A skill for generating clean, professional documents with consistent structure.

## When to apply this skill

Use this skill for:
- Technical specifications and feature docs
- Project reports and status updates
- API or module documentation
- Meeting minutes and decision logs
- README files and onboarding guides

## Document Generation Workflow

1. **Understand the document type** — identify what kind of document is needed and who will read it
2. **Gather key information** — ask only the essential questions (purpose, audience, main content points); don't over-ask
3. **Choose the right template** — pick from the templates below based on type
4. **Write the draft** — fill in the template with real content, not placeholder text
5. **Review for clarity** — ensure each section adds value; cut anything redundant

## Templates

### Technical Specification

```
# [Feature/Component Name]

## Overview
One paragraph describing what this is and why it exists.

## Goals
- [Goal 1]
- [Goal 2]

## Non-Goals
- [What this explicitly does NOT cover]

## Design / Approach
Describe the solution, key decisions, and rationale.

## API / Interface (if applicable)
Show the interface, endpoints, or data models.

## Open Questions
- [Unresolved items]

## References
- [Links to related docs or tickets]
```

### Project Status Report

```
# [Project Name] — Status Update ([Date])

## Summary
One sentence on overall health: 🟢 On track / 🟡 At risk / 🔴 Blocked

## Progress This Period
- [Completed item 1]
- [Completed item 2]

## Next Steps
- [Planned item 1]
- [Planned item 2]

## Risks & Blockers
| Issue | Impact | Owner | Status |
|-------|--------|-------|--------|

## Metrics (if applicable)
| Metric | Target | Actual |
|--------|--------|--------|
```

### Meeting Minutes

```
# Meeting: [Topic] — [Date]

**Attendees:** [Names]
**Facilitator:** [Name]

## Agenda
1. [Item 1]
2. [Item 2]

## Discussion & Decisions
### [Topic 1]
- Discussion: ...
- Decision: ...

## Action Items
| Action | Owner | Due |
|--------|-------|-----|
| [Task] | [Name] | [Date] |

## Next Meeting
[Date, time, agenda preview]
```

### README / Onboarding Guide

```
# [Project Name]

> [One-line tagline]

## What is this?
Brief description — what problem does it solve?

## Quick Start
```bash
# Installation and first run
```

## Usage
Core usage examples with real commands or code.

## Configuration
Key options and how to set them.

## Contributing
How to get started contributing.

## License
[License type]
```

## Writing Principles

- **Lead with the "why"** — readers should immediately understand the purpose
- **Use concrete examples** — show real values, real code, real names; avoid `foo/bar` placeholders
- **Keep sections lean** — one section = one idea; if a section feels thin, fold it into another
- **Tables over lists** for structured comparisons; bullet lists for independent items
- **Active voice** — "The API returns X" not "X is returned by the API"

## Output Format

Always produce the document as a markdown code block so it's easy to copy. If the user seems to want a file saved to disk, write it as a `.md` file in the current directory and tell them where it is.
