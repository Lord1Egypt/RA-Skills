## Description:

Case Extraction helps an agent review chat transcripts or oral experience descriptions and turn them into structured case-study documentation using the SPAS method.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and knowledge-management teams use this skill to turn interviews, chat records, or narrated best-practice experiences into structured SPAS case documentation. The skill can first assess whether source material contains enough interview coverage, then guide follow-up questions or draft the case structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional parser can leave cleaned chat contents in a predictable local file named _cleaned_temp.txt.

Mitigation: Run the parser only on non-confidential material in trusted folders, and delete _cleaned_temp.txt after use unless retaining it is intentional.

Risk: The skill may process sensitive chat or business materials supplied by the user.

Mitigation: Review input sensitivity before use and avoid placing confidential transcripts in shared or untrusted workspaces.

## Reference(s):

- [SPAS model reference](references/spas-model.md)
- [Case template reference](references/case-template.md)
- [ClawHub skill page](https://clawhub.ai/pengpengliu1212-art/skills/case-extraction)
- [ClawHub publisher profile](https://clawhub.ai/user/pengpengliu1212-art)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance and structured case-document content; optional parser output is plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce supplemental interview-question lists when source coverage is incomplete.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
