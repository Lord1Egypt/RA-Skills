## Description: <br>
Dating 约会助手 helps an agent prepare a dating report from public social profiles, summarizing interests, personality cues, conversation topics, restaurant or activity ideas, and cautions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill before a date or matchmaking meeting to analyze explicitly provided public social profile links and generate practical preparation guidance. The skill is intended to support conversation planning and venue selection, not background checks or private-data discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled collectors and storage rules can gather or retain broader logged-in account data than the public dating-report workflow requires. <br>
Mitigation: Use only explicit public profile links for the person being analyzed; do not run deep collectors against logged-in accounts unless intentionally exporting your own platform data. <br>
Risk: Raw third-party profile data may be retained locally after report generation. <br>
Mitigation: Collect the minimum public data needed, avoid likes, favorites, private tabs, and full following lists, and define a deletion plan before retaining raw profile files. <br>
Risk: Personality or values analysis from social media can be incomplete or misleading. <br>
Mitigation: Label conclusions as public-data-based inferences, avoid sensitive-attribute speculation, and treat the report as conversation preparation rather than a judgment about the person. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sophie-xin9/dating-prep) <br>
- [Publisher profile](https://clawhub.ai/user/sophie-xin9) <br>
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with structured analysis, recommendations, cautions, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save raw collected profile data and generated reports locally under clawcap-data when run as written.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
