## Description:

Douyin comment operations workflow for collecting, classifying, drafting, reviewing, and semi-automating replies to comments under the user's own Douyin videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to classify Douyin video comments, draft public replies and DM follow-ups, prioritize leads, define escalation rules, and run a review-first or semi-automated reply workflow for their own accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser execution workflow can post from an authenticated Douyin account.

Mitigation: Use the review-first workflow, run dry-run mode before sending, limit replies per run, sample-check sent replies, and use a separate low-privilege browser profile.

Risk: The executor uses unsafe shell-based, unpinned runtime tooling when invoking the browser command.

Mitigation: Pin or locally install the browser tool, avoid untrusted browser command values, and do not pass untrusted URLs, selectors, or draft files into the executor.

Risk: Public replies can be misleading, repetitive, or inappropriate for sensitive comments if sent without review.

Mitigation: Manually review price objections, skepticism, support issues, disputes, compliance claims, harassment, and high-value leads before publishing replies.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jinhuadeng/skills/douyin-comment-auto-reply)
- [Douyin Comment Ops Playbook](references/playbook.md)
- [Douyin Lead-Gen Template](references/douyin-lead-gen-template.md)
- [Automation Roadmap](references/automation-roadmap.md)
- [Reply Execution Plan](scripts/reply_execution_plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON draft files, CSV templates, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch draft generation can emit JSON items with intent, priority, suggested action, public reply, optional DM follow-up, and notes; browser execution can write a sent log.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
