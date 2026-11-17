## Description:

Automates access to Financial Times articles and produces structured bilingual English-Chinese summaries with key arguments, data, and conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouziyue233](https://clawhub.ai/user/zhouziyue233)

### License/Terms of Use:


## Use Case:

External users, analysts, and professionals use this skill to have an agent retrieve selected Financial Times articles and prepare concise bilingual reports for academic or professional reading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to use stored FT credentials and a persistent browser session.

Mitigation: Use a dedicated FT-only browser profile, avoid placing real passwords in skill text, and require explicit user approval before each authenticated run.

## Reference(s):

- [Financial Times](https://www.ft.com)
- [ClawHub skill page](https://clawhub.ai/zhouziyue233/skills/ft-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown bilingual English-Chinese article reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May split large article sets across multiple turns to avoid truncation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
