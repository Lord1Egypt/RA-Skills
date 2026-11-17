## Description:

Automates filling and resuming US DS-160 visa forms using CSV data, browser scripting, LLM assistance for captchas, translations, missing data, and session persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clulessboy](https://clawhub.ai/user/clulessboy)

### License/Terms of Use:


## Use Case:

External applicants and assisting agents use this skill to automate DS-160 data entry, resume interrupted applications, translate supported Chinese inputs, and surface missing data for user completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive DS-160 personal data, application IDs, security answers, and recovery secrets.

Mitigation: Use fake data for testing, keep application IDs and security answers private, replace hardcoded answers with user-provided values, and avoid logging or persisting recovery secrets in plaintext.

Risk: LLM or image calls for captchas, translation, missing elements, or validation errors may disclose form data or conflict with site rules.

Mitigation: Require explicit confirmation before external LLM or image calls and use manual captcha entry when automation is not appropriate.

Risk: Browser automation can enter incorrect information or proceed farther than intended on a government form.

Mitigation: Review every page before continuing, save progress before pauses, and require manual confirmation before any final or irreversible submission.

## Reference(s):

- [DS-160 element mappings](references/ds160-elements.yaml)
- [DS-160 user data CSV template](references/ds160-user-info.csv)
- [CEAC DS-160 start page](https://ceac.state.gov/genniv/)
- [ClawHub skill page](https://clawhub.ai/clulessboy/skills/ds160-autofill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown/text progress reports with JavaScript browser automation calls, CSV inputs, and JSON session files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create ds160/ds160-session.json and ds160/ds160-user-info.csv; final submission should remain manual.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
