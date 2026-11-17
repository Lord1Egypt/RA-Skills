## Description:

Check if your email, phone or password has been in data breaches. Full security response workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and security-conscious developers use this skill to check whether emails, phone numbers, or passwords appear in breach data and to produce prioritized response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive identifiers may be transmitted to external breach-check services if lookup endpoints are not reviewed.

Mitigation: Use only explicitly approved HTTPS endpoints, require consent before sending plaintext identifiers or hashes, and avoid periodic monitoring unless data destinations and disablement are clear.

Risk: Password checking can expose credential material if raw passwords or full hashes are sent.

Mitigation: Use the Pwned Passwords range API pattern and send only the first five SHA-1 hexadecimal characters.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON-style report text with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include breach status, breach names, exposed data categories, severity, occurrence counts for password checks, timelines, and prioritized action items.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
