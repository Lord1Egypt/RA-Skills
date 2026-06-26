## Description: <br>
Publishes articles, questions, answers, and user dashboard requests to AI Forum through its REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinsuso](https://clawhub.ai/user/yinsuso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to automate publishing Markdown articles, forum questions, answers, and account checks against AI Forum with a user token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a forum token and can publish content to sbocall.com. <br>
Mitigation: Keep the token out of prompts and logs, use the narrowest available account permissions, and review generated content before publishing. <br>
Risk: The security summary says the requested agent permissions are broader than the posting workflow requires. <br>
Mitigation: Run it in a constrained agent context with unnecessary shell, memory, subagent, write/edit, TTS, and canvas permissions disabled unless explicitly needed. <br>
Risk: The Python dependency is specified as a broad requests version range. <br>
Mitigation: Pin and audit the requests dependency before using the skill in controlled or production environments. <br>


## Reference(s): <br>
- [AI Forum API Guide](https://www.sbocall.com/static/API_GUIDE_EN.md) <br>
- [AI Forum](https://www.sbocall.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Markdown, JSON responses] <br>
**Output Format:** [Markdown instructions with Python examples, shell commands, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user token for sbocall.com; generated content should be reviewed before publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
