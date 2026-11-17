## Description:

Accesses the BilimClass school platform in Kazakhstan to retrieve schedules, homework, diary entries, and grades through the BilimClass APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[podberezovk](https://clawhub.ai/user/podberezovk)

### License/Terms of Use:

MIT-0

## Use Case:

External BilimClass users, especially Kazakhstan students and families, use this skill to ask an agent for school schedules, homework, diary details, and grade summaries from their own BilimClass account.

### Deployment Geography for Use:

Kazakhstan

## Known Risks and Mitigations:

Risk: The skill uses long-lived BilimClass account tokens stored in ~/.openclaw/.env.json.

Mitigation: Treat the tokens like passwords, keep the configuration file private, and exclude it from repositories, screenshots, logs, and shared workspaces.

Risk: The script may read credentials from a hard-coded Windows profile fallback path.

Mitigation: Review or remove the fallback path before deployment so credentials are loaded only from the intended user-controlled configuration location.

Risk: Broad natural-language triggers could invoke the skill for school-related requests that are not explicit BilimClass tasks.

Mitigation: Narrow activation criteria so the skill runs only when the user clearly asks for BilimClass schedule, homework, diary, or grade data.

Risk: The skill relies on unofficial BilimClass API endpoints that may change without notice.

Mitigation: Check failures and unexpected responses before presenting results, and be prepared to update endpoint handling when BilimClass changes its service behavior.

## Reference(s):

- [ClawHub BilimClass Skill Page](https://clawhub.ai/podberezovk/skills/bilimclass)
- [BilimClass](https://bilimclass.kz)
- [BilimClass schedule API endpoint](https://api.bilimclass.kz/api/v4/os/clientoffice/schedule)
- [BilimClass journal API endpoint](https://journal-service.bilimclass.kz/diary)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON from the CLI plus human-readable text or Markdown summaries prepared by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local BilimClass configuration file with account tokens and school identifiers.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
