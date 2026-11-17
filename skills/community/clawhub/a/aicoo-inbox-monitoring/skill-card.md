## Description:

Monitors Aicoo inbox conversations and network requests, surfaces new activity, urgent items, and suggested next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor Aicoo conversations, pending network requests, and related network context so they can identify new activity and decide whether to reply, accept, or ignore.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses AICOO_API_KEY to access private Aicoo inbox and request data.

Mitigation: Enable it only in trusted agent sessions, restrict credential exposure, and avoid logging sensitive inbox content.

Risk: Recurring loop, routine, or cron monitoring may continue checking private inbox data after initial setup.

Mitigation: Inspect the monitoring setup before enabling it, place any script in a trusted path, restrict log and state-file access, and confirm how to disable and clean up the monitor.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xisen-w/skills/aicoo-inbox-monitoring)
- [Aicoo API base URL](https://www.aicoo.io/api/v1)
- [Aicoo conversations endpoint](https://www.aicoo.io/api/v1/conversations?view=all&limit=50)
- [Aicoo network requests endpoint](https://www.aicoo.io/api/v1/network/requests)
- [Aicoo network context endpoint](https://www.aicoo.io/api/v1/os/network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with counts, urgent-item summaries, suggested actions, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact defines an output contract with new message counts, new incoming request counts, top urgent items, suggested next actions, or a single no-activity line.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
