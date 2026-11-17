## Description:

BIC-QA answers database and operating-system questions through the BIC-QA knowledge base with stateful multi-turn context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbsyd2](https://clawhub.ai/user/bbsyd2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DBAs, and operations engineers use this skill to ask BIC-QA knowledge-base questions about database systems and operating-system troubleshooting. The skill is designed for follow-up questions where preserving the same BIC-QA conversation context improves answer continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions and API credentials are sent to the BIC-QA API when the skill is used.

Mitigation: Use the skill only for questions appropriate to share with BIC-QA, keep API key files private, and avoid exposing keys in commands, files, or responses.

Risk: Local session state may contain conversation metadata and recent question text.

Mitigation: Keep BICQA_STATE_DIR and BICQA_STATE_FILE in private, non-shared locations and do not place them under version control.

Risk: A custom API base URL can receive the API key and question content if explicitly enabled.

Mitigation: Do not enable BICQA_ALLOW_CUSTOM_BASE_URL unless the endpoint is trusted and controlled; remote custom endpoints should use HTTPS.

## Reference(s):

- [BIC-QA Open API Quick Reference](artifact/references/api.md)
- [BIC-QA Homepage](https://www.bic-qa.com)
- [ClawHub Skill Page](https://clawhub.ai/bbsyd2/skills/bic-qa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional shell command examples and BIC-QA session annotations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated filenames returned by the BIC-QA API; local session metadata is maintained between related questions.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
