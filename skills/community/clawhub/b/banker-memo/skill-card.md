## Description:

Generates investment-banker-grade research memos, slide outlines, and data-provenance files from China-focused raw-data snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run a China-focused banker-memo workflow against validated raw-data snapshots for A-share, H-share, or non-listed Chinese companies. It produces a research memo, slide blueprint, and source-provenance record for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted filenames, paths, parameters, or JSON snapshots can be embedded into the generated prompt and processed by an agent with file-write access.

Mitigation: Use trusted raw-data only, avoid attacker-supplied filenames or snapshots, and restrict the agent to read only the validated raw-data directory and write only the chosen output directory.

Risk: The security verdict requires review before use because the workflow can generate investment and credit analysis from supplied data.

Mitigation: Review outputs before relying on them, run the strict provenance and authenticity checks described by the artifact, and use a fresh output directory for each run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackdark425/skills/banker-memo)
- [Banker Prompt Template](artifact/references/banker_prompt_template.md)
- [Build Banker Prompt Helper](artifact/scripts/build_banker_prompt.py)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with prompt guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analysis.md, slides-outline.md, and data-provenance.md in the chosen output directory; expects validated raw-data snapshots as input.]

## Skill Version(s):

0.9.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
