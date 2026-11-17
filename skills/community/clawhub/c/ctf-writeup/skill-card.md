## Description:

Generates a single standardized submission-style CTF writeup for competition handoff and organizer review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

CTF players, security teams, and competition participants use this skill after solving a challenge to produce a concise, reproducible submission writeup. It organizes challenge metadata, solution steps, tools or scripts used, and flag handling into a reviewer-friendly Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads challenge-related files from the active workspace while gathering writeup evidence.

Mitigation: Run it from a dedicated CTF workspace that contains only files intended for challenge analysis.

Risk: The skill may create writeup.md in the active workspace, which can conflict with existing notes.

Mitigation: Check for an existing writeup.md before use or request a challenge-specific output filename.

Risk: CTF writeups can include flags, exploit code, command output, or other sensitive challenge details.

Mitigation: Review the Markdown report before sharing and redact sensitive material when the competition or team policy requires it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gandli/skills/ctf-writeup)
- [Publisher profile](https://clawhub.ai/user/gandli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown writeup with YAML front matter and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single CTF writeup file such as writeup.md or writeup-<challenge-name>.md in the active challenge workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
