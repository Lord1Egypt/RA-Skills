## Description:

Uses the chill.institute web UI to search for content and send selected results to put.io, best paired with the putio skill for transfer verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baanish](https://clawhub.ai/user/baanish)

### License/Terms of Use:


## Use Case:

External users use this skill to guide an agent through a browser-based chill.institute workflow, select appropriate results, send them to put.io, and verify transfers when the putio skill is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses browser login and account access for chill.institute and put.io.

Mitigation: Keep authentication in the browser, do not share passwords in chat, and do not scrape or store cookies or session tokens.

Risk: The agent may send a selected result to the user's put.io account.

Mitigation: Review the selected content and confirm the user has rights or permission before sending it to put.io.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baanish/skills/chill-institute)
- [chill.institute sign-in](https://chill.institute/sign-in)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with browser workflow steps and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the user to remain logged in through the browser and to review selected content before sending it to put.io.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
