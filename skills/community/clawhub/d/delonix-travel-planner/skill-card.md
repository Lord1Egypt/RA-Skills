## Description:

This skill helps business travelers plan trips by comparing transport and hotel options, estimating budgets, gathering destination context, and generating HTML travel reports with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Business travelers and assistants use this skill to gather trip requirements, compare trains, flights, routes, hotels, budgets, weather, and destination details, then produce a practical itinerary and HTML travel report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive itinerary, location, identity, budget, and booking preferences may be shared with travel, map, hotel, search, and optional MCP services.

Mitigation: Share only the minimum necessary trip details, disclose external services to users, and restrict environment variables to the AMap keys needed for the selected workflow.

Risk: The skill describes unpinned npx execution for MCP packages.

Mitigation: Pin and review MCP package versions before use, avoid latest-style npx execution in privileged environments, and run the skill in a restricted sandbox.

Risk: Travel prices, availability, routing, weather, and booking links may become stale or inaccurate.

Mitigation: Treat generated options as planning guidance and require users to verify final availability, price, and terms on the relevant official booking or service page before purchase.

Risk: Generated HTML reports can contain private trip details and external links.

Mitigation: Review report content and links before sharing, and avoid publishing previews or filenames that expose private travel information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/skills/delonix-travel-planner)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and generated HTML report content with tables, timelines, budgets, maps, and booking links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external travel-service links, MCP configuration snippets, itinerary attachments, and preview metadata.]

## Skill Version(s):

9.9.9 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
