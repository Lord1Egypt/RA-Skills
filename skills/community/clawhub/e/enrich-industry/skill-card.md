## Description:

Backfill contact-level industry from associated company records using a HubSpot workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

External CRM operators and marketing operations teams use this skill to copy company industry values onto associated HubSpot contacts for segmentation, lead scoring, and campaign targeting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A HubSpot token with broad permissions could expose more CRM data than this enrichment task requires.

Mitigation: Run the skill and audit scripts with a least-privilege HubSpot token, as directed by the security guidance.

Risk: Local environment files or tokens could be accidentally committed or shared.

Mitigation: Keep .env files out of source control and avoid placing HubSpot tokens in skill text, logs, or generated artifacts.

Risk: Unpinned dependencies could change script behavior between audit runs.

Mitigation: Pin or lock the requests and python-dotenv dependencies before running the bundled Python scripts.

Risk: Bulk enrollment could copy industry values incorrectly if HubSpot contact and company properties are mismatched.

Mitigation: Verify property compatibility first and test the workflow on a small static list before enrolling existing contacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/enrich-industry)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell-executable audit scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scripts can write CSV audit files for before and after enrichment checks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
