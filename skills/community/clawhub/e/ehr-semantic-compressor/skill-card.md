## Description:

Generates structured EHR summaries and extracts clinical sections such as allergies, medications, diagnoses, family history, procedures, and vitals from medical-record text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical operations teams can use this skill to summarize long EHR text into reviewable bullet summaries and structured clinical sections. Outputs should be manually reviewed and should not be treated as clinical decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive medical-record text and writes summaries or extracted sections that may contain protected health information.

Mitigation: Run in an isolated, access-controlled environment, keep inputs and outputs within approved storage, and treat all generated artifacts as sensitive medical data.

Risk: Security evidence says the release overstates its clinical AI capability.

Mitigation: Require clinician or qualified reviewer validation of summaries and do not use the output as clinical decision support unless claims are corrected or independently validated.

Risk: Security evidence identifies an unrelated unpinned root dependency and mismatched requirements files.

Mitigation: Remove the root main dependency, reconcile dependency files, pin expected packages, and install only in an isolated environment before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/ehr-semantic-compressor)
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai)
- [Clinical Summarization Guidelines](references/guidelines.md)
- [Python Dependencies](references/requirements.txt)
- [Sample Input](references/sample_input.json)
- [Sample Output](references/sample_output.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON by default, with documented Markdown and text output options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces EHR summaries, extracted clinical sections, status/error objects, and processing metadata.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
