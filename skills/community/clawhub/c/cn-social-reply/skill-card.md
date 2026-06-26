## Description: <br>
A Chinese social media reply assistant that helps content creators generate single or batch comment replies with platform-specific tones and reusable style templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and brand teams use this skill to draft replies for comments across Chinese social platforms while matching a selected platform tone, reply strategy, and saved personal style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved reply-style templates may retain personal, brand, or account details on local disk. <br>
Mitigation: Avoid saving sensitive details in templates and review ~/.qclaw/workspace/cn-social-reply/styles.json before sharing or removing the skill. <br>
Risk: Generated replies may not match the creator's intended public voice or may mishandle hostile comments. <br>
Mitigation: Review generated replies before posting, especially for sensitive, critical, or brand-impacting interactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-social-reply) <br>
- [AISoBrand](https://aisobrand.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional shell commands for managing local style templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local reply-style templates at ~/.qclaw/workspace/cn-social-reply/styles.json when the bundled style manager is used.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
