## Description:

clawCat-BRIEF generates structured industry briefing reports from multi-source retrieval and LLM-assisted analysis, with HTML, PDF, PNG, Markdown, and JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llx9826](https://clawhub.ai/user/llx9826)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create daily or weekly topic briefs, financial and news reports, technology research updates, and open-source competitive analyses from selected public data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM-controlled inputs can trigger broad network retrieval across configured news, search, finance, social, and research sources.

Mitigation: Run the skill in an isolated workspace and network, restrict or review enabled sources, and validate user-provided RSS URLs before use.

Risk: The pipeline writes generated report files and persistent item-memory data to local paths.

Mitigation: Use a dedicated output directory, validate output paths, and avoid running the skill with access to sensitive workspaces.

Risk: Configuration may rely on API keys or environment variables for LLM and optional service access.

Mitigation: Avoid exposing sensitive environment variables, keep credentials in local configuration, and use least-privilege keys.

Risk: Report rendering may include fetched or configured external content.

Mitigation: Vendor or block remote report assets and review generated reports before sharing them in sensitive contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llx9826/skills/clawcat-brief)
- [Artifact README](artifact/README.md)
- [Artifact skill overview](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, JSON]

**Output Format:** [HTML, PDF, PNG, Markdown, and structured JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated from a user topic, report cadence, selected public data sources, and configured LLM credentials.]

## Skill Version(s):

0.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
