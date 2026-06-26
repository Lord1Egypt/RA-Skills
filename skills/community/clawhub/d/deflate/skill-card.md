## Description: <br>
Deflate helps OpenClaw agents compress and manage conversation context using topic tracking, /new versus /compact recommendations, and Cornell-MapReduce summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thevibestack](https://clawhub.ai/user/thevibestack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Deflate to monitor context growth, decide when to start a new chat or compact, and preserve important session details in memory while reducing token spend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages storing broad conversation details in MEMORY.md, which can accidentally preserve secrets or personal data. <br>
Mitigation: Do not write passwords, API keys, tokens, cookies, private URLs, or personal data into summaries or MEMORY.md unless the user explicitly approves that specific write. <br>
Risk: Compression and topic summaries can omit or distort details that should remain exact. <br>
Mitigation: Review compressed summaries before relying on them, and preserve identifiers, dates, amounts, URLs, file paths, and configuration values exactly. <br>


## Reference(s): <br>
- [Deflate on ClawHub](https://clawhub.ai/thevibestack/deflate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured checklists, status reports, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend /new, /compact, or MEMORY.md updates based on token-zone analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
