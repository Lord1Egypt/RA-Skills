## Description:

Substance use and behavioral addiction self-assessment and harm reduction guidance for people questioning their use patterns or looking for affordable support options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to guide substance use and behavioral addiction self-assessment, identify urgent medical risk, and find treatment, harm reduction, and mutual support resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access while handling sensitive health-related self-assessment information.

Mitigation: Install only in a runtime that constrains filesystem permissions, and avoid granting broad file access unless there is a clear operational need.

Risk: The skill defines substance-use state and reminder behavior that could retain or resurface sensitive personal information.

Mitigation: Keep screening data session-only unless the user explicitly opts into stored tracking or reminders with clear deletion controls.

Risk: Substance-use guidance may involve urgent medical or crisis situations.

Mitigation: Route overdose symptoms, suicidal ideation, or alcohol and benzodiazepine withdrawal risk to emergency or clinician-supervised care before continuing self-assessment.

## Reference(s):

- [WHO AUDIT Tool](https://www.who.int/publications/i/item/audit-the-alcohol-use-disorders-identification-test-guidelines-for-use-in-primary-health-care)
- [SAMHSA](https://www.samhsa.gov/)
- [National Institute on Drug Abuse](https://nida.nih.gov/)
- [SMART Recovery](https://www.smartrecovery.org/)
- [Harm Reduction International](https://www.hri.global/)
- [ClawHub Skill Page](https://clawhub.ai/howtousehumans/skills/addiction-self-assessment)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown and plain-language conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screening questions, scoring guidance, risk flags, treatment resources, and harm reduction steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
