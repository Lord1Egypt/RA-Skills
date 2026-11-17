## Description:

Express Tracker helps agents identify common Chinese courier companies from tracking numbers and generate Kuaidi100 lookup links for single or batch shipments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create courier tracking lookup links without a Kuaidi100 API key. It supports single-package and batch workflows with text, JSON, or Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can import executable code from an unreviewed developer-specific path before using the bundled files.

Mitigation: Review or remove the hardcoded external Python import path before running the scripts.

Risk: Opening generated Kuaidi100 links shares tracking numbers with Kuaidi100.

Mitigation: Open generated links only when sharing the tracking number with that site is acceptable.

Risk: Batch input and output paths could expose or overwrite files the user did not intend to use.

Mitigation: Keep input and output paths limited to files explicitly chosen for the tracking workflow.

## Reference(s):

- [Express Tracker ClawHub page](https://clawhub.ai/wang-junjian/skills/express-tracker)
- [Kuaidi100 query page](https://www.kuaidi100.com/chaxun?nu=YT2538259220416)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text, JSON, or Markdown containing courier names and Kuaidi100 lookup links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write results to a user-selected output file and can open generated links in a browser when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
