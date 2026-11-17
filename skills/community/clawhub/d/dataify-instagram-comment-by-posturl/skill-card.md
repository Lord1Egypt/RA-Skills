## Description:

Collects comments from a known Instagram post URL and returns the collected results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify collection jobs for comments on specific Instagram post URLs, monitor the asynchronous task, and receive the final collected result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Dataify API TOKEN and can submit paid Dataify collection jobs.

Mitigation: Install and run it only if you are comfortable granting that token access and paying for Dataify collection tasks.

Risk: Post-submission monitoring depends on an external Dataify task runtime that is not included in the package.

Mitigation: Review or provide the missing dataify-task-operations dependency from a trusted source before relying on final-result monitoring.

Risk: Implicit invocation can be risky for ambiguous Instagram requests.

Mitigation: Confirm the target post URL and any cost-affecting scope before execution when the user's request is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-instagram-comment-by-posturl)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task or result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit paid Dataify collection jobs; waits up to 600 seconds for ordinary collections unless no-wait behavior is requested.]

## Skill Version(s):

1.3.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
