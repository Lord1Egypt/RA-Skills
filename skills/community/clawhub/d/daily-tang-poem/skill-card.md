## Description:

每日唐诗 provides a daily Tang poem line with explanation, evening recitation verification, Ebbinghaus-style review questions, and poet-affinity summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romanluoman00007](https://clawhub.ai/user/romanluoman00007)

### License/Terms of Use:


## Use Case:

Chinese-language learners and poetry enthusiasts use this skill to receive a daily Tang poem line with a short explanation, verify recitation, review previously passed lines, and explore recurring poets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Poem requests, recitation attempts, review answers, activity dates, and a stable user identifier are sent to the configured external backend.

Mitigation: Install only when this data sharing is acceptable, and use a random UUID for DAILY_TANG_POEM_USER_ID instead of a chat ID, phone-related value, username, or reused identifier.

Risk: The skill documents optional API keys being appended to URLs, which can expose keys in request logs or browser and proxy history.

Mitigation: Avoid configuring DAILY_TANG_POEM_API_KEY unless the service changes to header-based authentication or URL-based exposure is acceptable for the deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/romanluoman00007/skills/daily-tang-poem)
- [Default Daily Tang Poem API](https://daily-tang-poem-nqbl.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Chinese Markdown responses with short prose, poem text, recitation feedback, review questions, and configuration guidance when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured backend API for poem selection, recitation validation, review questions, progress recording, and poet-affinity summaries.]

## Skill Version(s):

1.1.1 (source: manifest.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
