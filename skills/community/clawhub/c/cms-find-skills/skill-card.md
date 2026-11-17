## Description:

Cms Find Skills helps agents browse, search, inspect, install, and update ClawHub skills through the aishuo.co marketplace using skill codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spzwin](https://clawhub.ai/user/spzwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to find available ClawHub skills, inspect skill details, and install or update selected skills in the current agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AppKey and userId values and delegates installation through a remote marketplace service.

Mitigation: Install only when aishuo.co and the surrounding platform are trusted, and require clear disclosure and consent for AppKey and userId use.

Risk: The security guidance calls for removing insecure TLS settings before use.

Mitigation: Require verified TLS connections in managed environments before querying or installing skills.

Risk: Remote installation can introduce untrusted skill code into the current agent workspace.

Mitigation: Prefer local signed-package verification and review or scan installed skills before loading them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spzwin/skills/cms-find-skills)
- [aishuo.co marketplace endpoint](https://aishuo.co)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON command output with skill lists, details, URLs, and installation status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use AppKey and userId values supplied by the surrounding platform context when querying or installing skills.]

## Skill Version(s):

1.7.1 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
