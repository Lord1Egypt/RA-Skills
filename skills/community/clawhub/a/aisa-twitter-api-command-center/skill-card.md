## Description: <br>
Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa for trend tracking, competitor monitoring, and publish-ready workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to research Twitter/X accounts and narratives, monitor watchlists or launch reactions, and prepare or publish posts after OAuth approval through AIsa. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AIsa API key can appear in normal command output, which may leak a sensitive credential into logs or agent transcripts. <br>
Mitigation: Avoid running authorize or post commands where terminal output is logged, shared, or captured; rotate the key if exposure is suspected. <br>
Risk: The skill can publish externally to Twitter/X and upload selected local media files through AIsa. <br>
Mitigation: Confirm the exact post text, target tweet or account context, and media file paths before publishing. <br>
Risk: AIsa receives Twitter/X data, post content, selected media files, and the configured AISA_API_KEY. <br>
Mitigation: Use this skill only when the user trusts AIsa for that data and provide only the intended API key and user-attached files. <br>


## Reference(s): <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa Twitter/X API endpoint](https://api.aisa.one/apis/v1/twitter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON client output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; may send approved text and selected media files to AIsa's Twitter/X API endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
