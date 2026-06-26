## Description: <br>
Douyin comment operations workflow for your own account videos. Use when the user wants to collect, classify, draft, review, or semi-automate replies to comments under their own Douyin videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to classify Douyin comments, draft public replies and DM follow-ups, design review-first reply SOPs, and optionally execute approved replies through a controlled browser workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live browser automation can publish replies from the user's Douyin account without a strong confirmation gate. <br>
Mitigation: Use draft and dry-run modes first, review generated JSON before sending, keep --max-replies low, and avoid --force-review unless every reply has been inspected. <br>
Risk: Untrusted browser command, URL, or selector values could cause unintended browser automation behavior. <br>
Mitigation: Use a vetted local browser automation command and do not pass untrusted values into --browser-cmd, URL, or selector arguments. <br>
Risk: Automated public replies may mishandle sensitive disputes, support issues, or price objections. <br>
Mitigation: Route refund, dispute, policy-sensitive, support, skepticism, and pricing-conflict comments through manual review before execution. <br>


## Reference(s): <br>
- [Douyin Comment Ops Playbook](references/playbook.md) <br>
- [Douyin Lead-Gen Template](references/douyin-lead-gen-template.md) <br>
- [Automation Roadmap](references/automation-roadmap.md) <br>
- [Douyin Creator Comment Management](https://creator.douyin.com/creator-micro/content/manage) <br>
- [ClawHub skill page](https://clawhub.ai/jinhuadeng/douyin-comment-auto-reply) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON reply drafts, CSV templates, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate review-first reply drafts and sent-reply logs for approved browser execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
