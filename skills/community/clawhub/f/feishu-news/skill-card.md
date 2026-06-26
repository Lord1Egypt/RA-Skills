## Description: <br>
A skill to fetch and reference news information from Feishu when interacting with users. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[yeat](https://clawhub.ai/user/yeat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users can ask an agent to retrieve, format, and cite Feishu-style news updates in conversation. The current release should be treated as a demo/mock because the included implementation returns sample articles rather than live Feishu API results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be mistaken for a live Feishu news connector even though the included code returns hardcoded sample articles. <br>
Mitigation: Treat outputs as demonstration data unless the publisher updates the implementation and documentation to use real Feishu API results. <br>
Risk: Broad dependency ranges can change behavior or increase installation risk over time. <br>
Mitigation: Review and pin dependencies before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown-formatted news summaries with source attribution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns sample article metadata including title, summary, source, URL, and date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
