## Description:

Checks current electricity availability for Odesa, vul. Chikalenka Yevhena, 43 through DTEK Odesa Electric Grids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kapishdima](https://clawhub.ai/user/kapishdima)

### License/Terms of Use:


## Use Case:

Residents or agents assisting this Odesa address use the skill to check whether electricity is currently available and to summarize outage or restoration information.

### Deployment Geography for Use:

Ukraine

## Known Risks and Mitigations:

Risk: The skill runs local JavaScript and launches a browser to query DTEK for the disclosed address.

Mitigation: Review the script before installation and run it only in an environment where this address lookup is acceptable.

Risk: The documented invocation locates executable code by searching the agent's skills directory.

Mitigation: Prefer invoking the bundled script through a fixed relative path.

Risk: The Playwright dependency is mutable and no lockfile is present.

Mitigation: Pin Playwright with a lockfile before operational use.

Risk: Broad trigger phrases may run the check when the user did not intend to query the address.

Mitigation: Use an explicit command or narrowly scoped prompt before running the check.

## Reference(s):

- [DTEK Odesa Electric Grids Shutdowns](https://www.dtek-oem.com.ua/ua/shutdowns)
- [ClawHub Skill Page](https://clawhub.ai/kapishdima/skills/dtek-light)
- [Publisher Profile](https://clawhub.ai/user/kapishdima)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with a local shell command and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Playwright with Chromium and queries a fixed disclosed address.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
