## Description:

Followers is a third-party command-line skill advertised for follower analytics, but the inspected release behaves primarily as a local free-form logging utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users or developers may use this skill to record and review local entries related to follower workflows. They should not rely on it for actual follower growth, unfollow, engagement, or demographic analytics unless the implementation is corrected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the release claims follower analytics but mostly implements local free-form logging.

Mitigation: Validate functionality against analytics requirements before use and prefer a corrected release with explicit documentation, commands, storage, export, and deletion behavior.

Risk: Commands can retain user-entered text locally under ~/.local/share/followers.

Mitigation: Avoid entering credentials, private account details, or sensitive audience data, and review or remove local logs when they are no longer needed.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review the artifacts carefully before installing or executing the skill.

## Reference(s):

- [ClawHub Followers skill page](https://clawhub.ai/bytesagain1/skills/followers)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text CLI output and local log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes command entries and history under ~/.local/share/followers; advertised export behavior is not reliable in the inspected script.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
