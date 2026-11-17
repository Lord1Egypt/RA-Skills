## Description:

AI Code Review helps agents review pull request diffs, optionally transcribe voice notes, and send Discord review notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to automate preliminary pull request review workflows, capture optional voice-note context, and route review status to Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan verdict is suspicious and reports under-disclosed high-impact behavior plus file and network handling weaknesses.

Mitigation: Review carefully before installing or running, use a controlled environment, and restrict allowed diff sources.

Risk: Diff fetching can reach external URLs and may be unsafe if internal-network overrides are enabled.

Mitigation: Keep internal diff URLs blocked unless explicitly required and limit accepted diff hosts to trusted sources.

Risk: Voice note handling and webhook use can expose local files or secrets if configured too broadly.

Mitigation: Restrict voice-note directories, protect API and webhook secrets, and avoid broad filesystem access.

Risk: The healthcheck script can restart system services when run with sufficient privileges.

Mitigation: Run health checks with narrowly scoped privileges and only on hosts where restarting those services is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/ai-code-review-service)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)
- [code_review_service.py](references/code_review_service.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and JSON review results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch pull request diffs, call the OpenAI transcription API, and send Discord notifications when configured.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
