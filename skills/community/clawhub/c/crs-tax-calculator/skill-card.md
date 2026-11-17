## Description:

CRS Tax Calculator helps an agent submit brokerage statements to a remote tax-calculation service, calculate capital gains with FIFO or ACB methods, and generate Excel tax audit workbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halleymagic](https://clawhub.ai/user/halleymagic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process annual brokerage statement files for China CRS supplementary tax calculations or Canada CRA tax reporting. The skill uploads PDF, Excel, CSV, or image statements to the provider service and returns concise audit results plus generated Excel workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote API can control generated output filenames, which may overwrite user-owned files outside the intended output folder.

Mitigation: Run the skill as a least-privileged user in an empty dedicated output directory until output filename handling is fixed.

Risk: The skill uploads brokerage statements and uses CRS_API_KEY with the wealthlplantation.com service.

Mitigation: Install and run it only if the user trusts wealthlplantation.com with full brokerage statements and the API key.

## Reference(s):

- [CRS Tax Calculator ClawHub listing](https://clawhub.ai/halleymagic/skills/crs-tax-calculator)
- [WealthLPlantation API homepage](https://wealthlplantation.com/api)
- [WealthLPlantation pricing](https://wealthlplantation.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and CRS_API_KEY; generated Excel filenames are returned by the remote service.]

## Skill Version(s):

3.4.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
