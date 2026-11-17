## Description:

Monitor and fetch real-time Baidu hot search topics, rankings, trends, and keyword popularity without needing an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piaomiao123](https://clawhub.ai/user/piaomiao123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current Baidu hot-search rankings and topic names for monitoring public trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Baidu when invoked, which may disclose that the user or agent requested hot-search data.

Mitigation: Install and invoke it only in environments where outbound requests to top.baidu.com are acceptable.

Risk: Broad trigger terms can cause accidental activation.

Mitigation: Prefer explicit invocations such as baidu-hot or Baidu hot-search ranking.

## Reference(s):

- [Baidu Hot ClawHub skill page](https://clawhub.ai/piaomiao123/skills/baidu-hot)
- [Baidu realtime board API endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text terminal output with ranked Baidu hot-search topics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and network access to top.baidu.com; default output is the top 20 items unless a positional count is supplied.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
