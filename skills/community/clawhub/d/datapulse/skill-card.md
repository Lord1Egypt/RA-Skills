## Description:

Cross-platform content collection, web search, trending topics, confidence scoring, and watch/triage workflows for assistant and agent usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunyifei83](https://clawhub.ai/user/sunyifei83)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use DataPulse to ingest URLs, search web and trend signals, create watch missions, route alerts, triage collected items, and assemble story evidence packs for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist collected content, watch rules, alert routes, entity data, browser login state, and local operational state.

Mitigation: Review the skill before installation, keep alert tokens and Playwright session files in private directories, and run it only in working directories suitable for stored content.

Risk: Configurable alert routes and custom API endpoints can send data to user-specified services.

Mitigation: Configure only trusted endpoints, use scoped or throwaway keys for custom entity extraction endpoints, and review alert routes before enabling recurring watches.

Risk: Optional browser automation, subprocess transports, and native helper commands can expand local execution and session exposure.

Mitigation: Enable Playwright login only intentionally, invalidate session cache when no longer needed, and configure native helper commands only from trusted absolute paths.

## Reference(s):

- [DataPulse ClawHub Skill Page](https://clawhub.ai/sunyifei83/skills/datapulse)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Plain text with JSON or Markdown records depending on the entry point and requested workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist inbox, watch, triage, story, alert route, entity, and session state when users enable those workflows.]

## Skill Version(s):

0.8.1 (source: release evidence, SKILL.md heading, manifest; pyproject.toml reports 0.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
