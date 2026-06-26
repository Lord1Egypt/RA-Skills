## Description: <br>
Detects Spanish and English AI-writing patterns using 49 documented detectors, statistical measures such as burstiness and type-token ratio, and vocabulary guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sitost](https://clawhub.ai/user/sitost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to analyze Spanish or English drafts, identify mechanical AI-writing patterns, and produce revision guidance or safer rewrites for content they own or are authorized to edit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill could be misused to bypass school, workplace, platform, or authorship-disclosure rules. <br>
Mitigation: Use it only for content the user owns or is authorized to edit, and disclose AI assistance when required by the relevant policy. <br>
Risk: The separate npm/GitHub CLI or MCP package is executable code outside the reviewed ClawHub artifact. <br>
Mitigation: Review and pin that package before installing it or integrating it into production environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sitost/bilingual-humanizer) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Copyleaks stylometry research](https://arxiv.org/abs/2503.01659) <br>
- [Repository referenced by artifact documentation for CLI/MCP review](https://github.com/SitoSt/bilingual-humanicer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text revision guidance, Markdown reports, JSON analysis, and CLI or MCP configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Spanish by default and English via language selection; folder scans require explicit user confirmation before broad directory analysis.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
