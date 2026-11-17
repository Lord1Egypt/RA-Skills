## Description:

Helps agents perform lightweight defensive red-team reviews of AI automation workflows, focusing on misuse paths, boundary failures, and data leakage risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, workflow owners, and security reviewers use this skill to turn AI workflow descriptions, inputs and outputs, and permission boundaries into a structured defensive red-team brief before deployment or operational changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Python helper reads user-provided paths and may access sensitive workspace or home-directory files if invoked broadly.

Mitigation: Run it only on intended review inputs or in a restricted workspace, and avoid granting access to sensitive directories.

Risk: The helper can write report files and may overwrite writable local files when given an unsafe output path.

Mitigation: Use stdout, dry-run mode, or a dedicated output directory, and review output paths before execution.

Risk: User-controlled filenames may be unsafe if copied into shell commands without quoting.

Mitigation: Pass paths as arguments without shell interpolation and avoid untrusted filenames in pasted command lines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/ai-workflow-red-team-lite)
- [ClawHub Publisher Profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or JSON defensive review brief; may include local Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces attack surface summaries, misuse paths, boundary failures, data risks, mitigations, checklists, confirmation items, and next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
