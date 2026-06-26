## Description: <br>
OpenClaw skill for source-backed web search, page reading, and evidence-aware claim checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, read source pages, verify concrete factual claims, and produce citation-ready evidence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised external Python package source may be unavailable or may not match the intended release. <br>
Mitigation: Confirm the package source before installing, and prefer a reviewed, pinned repository or release. <br>
Risk: Search queries can disclose secrets, confidential business claims, or private personal data to a search provider. <br>
Mitigation: Do not send sensitive content through third-party search providers; use a trusted self-hosted SearXNG instance when privacy is required. <br>
Risk: Claim verification is heuristic and may surface conflicting evidence without resolving it. <br>
Mitigation: Review cited URLs and conflict signals before relying on the verdict in user-facing or high-impact answers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wd041216-bit/cross-validated-search) <br>
- [Project homepage](https://github.com/wd041216-bit/cross-validated-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-capable command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source URLs, explicit verdicts, support and conflict scores, page-aware verification status, and next steps.] <br>

## Skill Version(s): <br>
16.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
