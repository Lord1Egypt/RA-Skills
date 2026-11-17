## Description:

Draft a cover letter, or a resignation letter, with ATSPrep's free letter builders using only the user's real experience, then fill its gaps together. Use when someone asks for a cover letter for a job, a letter to go with an application, or a polite resignation letter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devabubakar](https://clawhub.ai/user/devabubakar)

### License/Terms of Use:

MIT

## Use Case:

External job seekers use this skill to draft cover letters for applications and polite resignation letters from details they provide, then review visible gaps before finalizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume and employment details are sent to ATSPrep; optional AI tools also send the text they rewrite to Cloudflare Workers AI, and the bundled code does not independently verify provider retention or filtering promises.

Mitigation: Use the service only when comfortable sharing the supplied details, share only what is needed, and tell the user before the first AI tool call.

Risk: An ATSPREP_MCP_URL override can change the endpoint receiving submitted text, and temporary text files may remain after use.

Mitigation: Check the endpoint override before uploading and remove temporary text files when finished.

## Reference(s):

- [ATSPrep cover letter builder](https://atsprep.com/tools/cover-letter-builder)
- [ATSPrep resignation letter builder](https://atsprep.com/tools/resignation-letter-builder)
- [ATSPrep MCP tools reference](artifact/references/tools.md)
- [ATSPrep privacy reference](artifact/references/privacy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Draft letters and career feedback in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visible placeholders for details the user has not supplied; does not invent personal facts.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
