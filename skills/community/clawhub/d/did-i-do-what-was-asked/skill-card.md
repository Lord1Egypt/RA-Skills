## Description:

Checks whether an agent's reply matches the user's request by comparing request and reply fingerprints with intervening tool actions and returning COHERENT, PARTIAL, INCOHERENT, or NO_PAIR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after an agent reply to check whether the reply covered the request and whether the actions taken between request and reply were proportionate and successful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required local plugin keeps a ledger of request, action, and reply metadata for self-checking.

Mitigation: Confirm the user is comfortable enabling clawphylax before installation and rely on the reviewed behavior that message texts are not stored and nothing leaves the machine.

Risk: The skill cannot judge tone or factual correctness.

Mitigation: Use its verdict only as a request-vs-reply coherence check and apply separate review for factual accuracy, safety, and tone.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aeneassoft/skills/did-i-do-what-was-asked)
- [Project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with verdict labels, evidence notes, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one of COHERENT, PARTIAL, INCOHERENT, or NO_PAIR with reasons; it does not assess tone or factual correctness.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
