## Description:

Simulates developer and engineering interviews, including coding rounds, system design discussions, behavioral questions for engineers, tech-specific Q&A, CV-based interview tailoring, and interview progress review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phantue2002](https://clawhub.ai/user/phantue2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to practice mock software engineering interviews, receive scored feedback, prepare for coding and system design rounds, and tailor interview questions from a local CV or resume summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores interview history and CV-derived profile fields locally.

Mitigation: Use it only when local storage of interview practice data is acceptable, and review or remove saved JSON files under ~/.openclaw/developer-interview-simulator as needed.

Risk: The skill suggests an unrelated unpinned `npx skills` command for listing installed skills.

Mitigation: Do not run that command unless the package and publisher have been independently verified; prefer checking the local skills directory.

Risk: Broad triggers such as code review or solution rating may route generic engineering feedback requests into interview-style scoring.

Mitigation: Confirm the user wants interview simulation or interview-style evaluation before applying the scoring workflow.

## Reference(s):

- [Developer Interview Simulator reference question bank](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/phantue2002/skills/developer-interview-simulator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured interview prompts, feedback blocks, code snippets, JSON file shapes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local profile, history, weak-area, and saved-answer JSON files under ~/.openclaw/developer-interview-simulator.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
