## Description:

Finds citable statistics for market claims, checks their measurement scope and conflicting findings, and delivers evidence tables and qualified citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and presentation authors use this skill to check market figures and claims against citable evidence, compare conflicting measurements, and document limitations and contrary findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The research workflow requires JishuDB installation, application launch, and local connector configuration when it is not already available.

Mitigation: Use it only if JishuDB setup and retention are wanted; review the installation plan, version, source, paths, and client configuration changes before approval, and decline setup for a one-off local answer.

Risk: Authentication and retained research material can include sensitive information.

Mitigation: Authorize the destination and retention scope, and never paste OAuth or JishuDB tokens into chat.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bowen-aijishu/skills/data-evidence-finder)
- [Skill homepage listed in metadata (not verified import provenance)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/data-evidence-finder)
- [Evidence and citation contract](references/evidence-contract.md)
- [JishuDB setup quickstart](references/jishudb-setup/references/setup-quickstart.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, Guidance]

**Output Format:** [Evidence CSV and Markdown notes, citations, discrepancies, and revisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings identify source coverage, statistical scope, uncertainty, and conflicting evidence.]

## Skill Version(s):

0.1.17 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
