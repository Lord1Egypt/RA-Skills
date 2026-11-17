## Description:

Read cookies from mainstream browsers and convert them to a specified format.

This skill is for research and development only.

## Publisher:

[dkgee](https://clawhub.ai/user/dkgee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically capable users can use this skill to export their own browser cookies for a named domain into JSON, HTTP Cookie header, or cURL command formats for learning and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and exports browser cookies, which can include sensitive session credentials.

Mitigation: Run it only for cookies you own, protect terminal logs and output files like passwords, and avoid sharing generated cookie headers or cURL commands.

Risk: cURL output can make sensitive cookies easy to paste into another context.

Mitigation: Inspect generated commands before use, keep them out of shared shells or logs, and prefer JSON output when review or storage is needed.

Risk: The skill depends on local browser storage access and the rookiepy package.

Mitigation: Run it in a controlled environment with a pinned dependency version and only grant the local permissions required to read your own browser data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands]

**Output Format:** [JSON, HTTP Cookie header text, or cURL command text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print cookie values to stdout or write them to a user-specified file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
