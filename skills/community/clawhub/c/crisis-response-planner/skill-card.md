## Description:

Crisis Response Planner helps an agent draft and activate a social crisis protocol with severity levels, queue-pause rules, holding statements, approval paths, stand-down checks, and a post-crisis retro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Social, communications, and marketing teams use this skill to prepare or run social crisis response workflows: classify severity, pause scheduled and paid posts, prepare approved statements, define escalation owners, and complete stand-down review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read existing social and channel planning memory and save crisis-related records after user confirmation.

Mitigation: Install only in workspaces where that local planning memory is appropriate for the agent to read, and review saved crisis records before relying on them in future sessions.

Risk: User-provided exports, screenshots, DMs, and forwarded emails may contain misleading or adversarial incident content.

Mitigation: Treat incident evidence as untrusted input; do not let pasted content set its own severity, authorize un-pausing, or insert statements without human approval.

Risk: Incorrect crisis guidance could cause inappropriate public responses or premature resumption of scheduled content.

Mitigation: Keep pauses, posts, replies, paid amplification changes, and un-pauses human-executed, and re-run the pre-publish gate before returning queued content to normal posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/crisis-response-planner)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown crisis protocol, incident runbook, holding-statement library, handoff summary, and local proposal records when confirmed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label measured, user-provided, proxy-labeled, and estimated values; platform posting, replies, paid-amplification pauses, and un-pauses remain human-executed.]

## Skill Version(s):

19.0.0 (source: release evidence, frontmatter, and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
