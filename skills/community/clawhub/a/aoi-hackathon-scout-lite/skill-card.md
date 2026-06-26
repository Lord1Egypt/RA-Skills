## Description: <br>
Public-safe hackathon source registry + filtering output (no crawling, no submissions). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, builders, and operations users use this skill to inspect local hackathon, builder program, and grant source lists, filter likely online opportunities, generate shortlist recommendations, and print a paste-ready summary template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local registry or shortlist files may contain stale deadlines, links, or opportunity details. <br>
Mitigation: Verify deadlines and links directly with the source before relying on recommendations. <br>
Risk: Generated output may reflect local context files that are not intended for sharing. <br>
Mitigation: Review local context files and command output before distributing summaries. <br>
Risk: Optional Brave Search setup requires an API key when intentionally enabled. <br>
Mitigation: Configure the Brave Search API key only when web search is desired, and disable it when not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edmonddantesj/aoi-hackathon-scout-lite) <br>
- [Devpost AI category](https://devpost.com/c/artificial-intelligence) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output and Markdown template text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Best-effort local parsing of registry and shortlist markdown files; no crawling, login, form-fill, submission automation, or default API-key requirement.] <br>

## Skill Version(s): <br>
0.1.6 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
