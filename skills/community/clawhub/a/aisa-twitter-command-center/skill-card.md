## Description: <br>
Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to research and monitor X/Twitter content, then publish approved posts, replies, quotes, or media through an OAuth-based workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the AIsa relay with Twitter/X posting authority, OAuth flows, and approved media uploads. <br>
Mitigation: Install only if you trust the AIsa relay, configure the intended account, and require explicit user approval before posting or uploading media. <br>
Risk: The security scan reports that OAuth and status flows may expose AISA_API_KEY or raw relay responses in CLI output. <br>
Mitigation: Review or patch the OAuth client to redact secrets before use, avoid sharing raw logs, and rotate AISA_API_KEY if it appears in transcripts or logs. <br>
Risk: External posting can publish incorrect text, replies, quotes, or attachments to X/Twitter. <br>
Mitigation: Review post text, target tweet URLs, and local media paths before execution, and do not claim success until the publish command confirms it. <br>


## Reference(s): <br>
- [AIsa Twitter OAuth posting guide](references/post_twitter.md) <br>
- [AIsa homepage](https://aisa.one) <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/aisa-twitter-command-center) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API responses] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses from the bundled clients] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and user-approved OAuth for posting workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
