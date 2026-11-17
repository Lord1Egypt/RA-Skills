## Description:

Manage Box files, folders, collaborations, shared links, metadata, and enterprise content workflows via the Box API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and content administrators use this skill to browse Box content, manage file sharing and collaboration, automate document workflows, inspect metadata, and coordinate Box Sign requests from an agent chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to activate an unpinned third-party plugin that can perform high-impact Box account actions.

Mitigation: Review the ClawLink plugin and publisher trust before installing, and prefer a pinned or verified plugin release when available.

Risk: Write actions can create, move, copy, delete, share, or change Box resources, including collaborations, users, groups, retention policies, legal holds, and signature requests.

Mitigation: Use tool description and preview steps before writes, require explicit user confirmation, and verify the target resource and intended effect before execution.

Risk: Tool calls operate with the connected Box account's permissions and enterprise policies.

Mitigation: Connect only a minimum-permission Box account appropriate for the task and use extra review for administrative or compliance-sensitive operations.

## Reference(s):

- [Box Developer Documentation](https://developer.box.com/)
- [Box API Reference](https://developer.box.com/reference/)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/box-files)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live ClawLink Box tool catalog as the source of truth for available actions.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
