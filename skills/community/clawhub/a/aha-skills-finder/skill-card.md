## Description: <br>
Aha Skills Finder helps agents surface hard-to-find skill and capability candidates across registries, packages, repositories, MCP catalogs, and provider surfaces while preserving raw signals for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[its-how](https://clawhub.ai/user/its-how) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need broad, traceable discovery of candidate skills, MCPs, CLIs, plugins, registries, extensions, SaaS/provider routes, repo tools, or native runtime capabilities before a separate adoption or safety review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad search expansion can include irrelevant source surfaces or unintended language and region assumptions. <br>
Mitigation: Set explicit runtime, platform, language, and region constraints before use, and review source gaps and false positives in the generated artifacts. <br>
Risk: Find-stage outputs are raw candidate signals and do not prove candidate safety, maintenance, source quality, or adoption fit. <br>
Mitigation: Run a separate source, security, permission, maintenance, and install-readiness review before adopting, installing, enabling, or configuring any discovered candidate. <br>


## Reference(s): <br>
- [Aha Skills Finder repository](https://github.com/its-How/aha-skills-finder) <br>
- [ClawHub skill page](https://clawhub.ai/its-how/skills/aha-skills-finder) <br>
- [Candidate Pool Contract](artifact/references/candidate-pool-contract.md) <br>
- [Research Brief Contract](artifact/references/research-brief-contract.md) <br>
- [Source-family checklist](artifact/sources.yaml) <br>
- [Curated and adjacent discovery-source registry](artifact/source-registries/curated-skill-lists.yaml) <br>
- [skills.sh API documentation](https://www.skills.sh/docs/api) <br>
- [ClawHub public search API example](https://clawhub.ai/api/v1/search?q={query}&limit=10) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown research brief and candidate pool records with structured fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Find-stage artifacts preserve raw source signals, source gaps, false positives, and deferred adoption-review boundaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
