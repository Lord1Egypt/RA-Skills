## Description: <br>
Tiktok Auto Reply helps an agent configure and run a Node.js workflow that monitors TikTok videos by keyword, reads comments, and sends templated automated replies. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[kamiguyi](https://clawhub.ai/user/kamiguyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operators use this skill to set up TikTok keyword monitoring, comment retrieval, and controlled template-based replies with configured API credentials and rate limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended with TikTok credentials and publish public comment replies. <br>
Mitigation: Use a test or least-privilege TikTok app, avoid broad comment.create access unless needed, keep watch mode visible and stoppable, and monitor account status. <br>
Risk: The dry-run safety claim is not enforced by the code according to the server security summary. <br>
Mitigation: Do not rely on dryRun as a safety control until the code is reviewed and fixed to skip reply calls when dryRun is true. <br>
Risk: Automated replies may create platform-policy or account-restriction risk. <br>
Mitigation: Keep reply rates low, use varied templates, review platform terms and API permissions, and stop immediately if account restrictions appear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kamiguyi/dagugu-tiktok-auto-reply) <br>
- [TikTok for Developers](https://developers.tiktok.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TikTok API credentials and supports one-time checks or continuous watch mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
