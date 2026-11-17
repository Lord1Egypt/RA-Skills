## Description:

Automate web tasks like form filling, data scraping, testing, monitoring, and scheduled jobs using Selenium or Puppeteer with retry and proxy support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kesepain](https://clawhub.ai/user/kesepain)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to automate authorized web scraping, form interactions, scheduled checks, testing, and monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unrestricted network requests and advertises scheduled, proxy, and automated submission behavior without enough user controls.

Mitigation: Use it only for authorized targets and add URL allowlists plus internal-address blocking before deployment, especially in environments with access to private networks or cloud metadata endpoints.

Risk: Automated submissions or scheduled jobs can affect destinations if pointed at services the operator does not control.

Mitigation: Avoid automated submissions or scheduled runs unless the operator controls the destination and has reviewed the target, schedule, and submitted data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kesepain/skills/ai-web-automation-1-0-0)
- [Publisher profile](https://clawhub.ai/user/kesepain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write timestamped scraping reports to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact package.json, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
