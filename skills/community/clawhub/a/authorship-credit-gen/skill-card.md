## Description:

Generates CRediT contributor statements from supplied author, affiliation, contribution role, equal-contribution, and corresponding-author metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googolme](https://clawhub.ai/user/googolme)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and publication support teams can use this skill to generate CRediT contribution statements from structured author metadata. Authorship ordering, dispute resolution, and fairness decisions should remain human-reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill overstates its ability to make fair authorship decisions and resolve disputes.

Mitigation: Treat outputs as draft contribution statements and require human review for author order, dispute resolution, and ICMJE-compliance decisions.

Risk: Untrusted author metadata may be embedded in XML output.

Mitigation: Avoid untrusted metadata for XML generation or sanitize author names, affiliations, and role values before using XML output.

Risk: Generated files can be written to caller-provided output paths.

Mitigation: Use explicit, reviewed output paths and avoid running the skill where accidental overwrite of important files is possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googolme/skills/authorship-credit-gen)
- [ClawHub publisher profile](https://clawhub.ai/user/googolme)

## Skill Output:

**Output Type(s):** [text, JSON, XML, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; generated contribution statements can be text, JSON, XML, or bilingual text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated statements to an explicit output file when the command-line output option is used.]

## Skill Version(s):

0.1.0 (source: release evidence and tile.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
