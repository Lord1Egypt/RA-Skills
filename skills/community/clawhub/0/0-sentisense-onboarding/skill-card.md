## Description:

Read first when using any SentiSense stock market skill: API key setup and which skill owns each task. Patterns to adapt, not scripts. The user's task always wins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and people using SentiSense stock market skills can use this onboarding guide to choose the skill for a task, configure the shared API key, and follow the documented read-only data access patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a purpose mismatch and is partial; its guidance recommends checking whether the AAPL quote retrieval example fits this onboarding skill.

Mitigation: Review the sample AAPL quote request and the unresolved local path reference before use; the scan reports a benign verdict with medium confidence.

## Reference(s):

- [SentiSense API reference](https://sentisense.ai/skill.md)
- [SentiSense API documentation](https://sentisense.ai/docs/api)
- [Get a SentiSense API key](https://app.sentisense.ai/get-api-key)
- [ClawHub release](https://clawhub.ai/thesentitrader/skills/0-sentisense-onboarding)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with tables and inline curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
