## Description:

Solve CAPTCHAs with 2Captcha from the command line during browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adinvadim](https://clawhub.ai/user/adinvadim)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation engineers use this skill to solve CAPTCHA challenges through 2Captcha during authorized browser automation and scripting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CAPTCHA content, page URLs, sitekeys, challenge IDs, and task metadata are sent to 2Captcha and its human solvers.

Mitigation: Use the skill only for authorized automation, and avoid sensitive, regulated, internal, or third-party user data unless that workflow is approved.

Risk: Installing or running the CLI from an unreviewed source can introduce supply-chain risk.

Mitigation: Prefer the reviewed bundled script or a pinned commit or release, and avoid sudo or global installation unless it is required.

Risk: The skill requires a 2Captcha API key for paid service access.

Mitigation: Keep the API key scoped to 2Captcha, provide it through the documented credential sources, and check account balance before heavy automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adinvadim/skills/2captcha)
- [Project homepage](https://github.com/adinvadim/2captcha-cli)
- [2Captcha service](https://2captcha.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON CLI output, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a 2Captcha API key supplied by flag, environment variable, or local config file.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
