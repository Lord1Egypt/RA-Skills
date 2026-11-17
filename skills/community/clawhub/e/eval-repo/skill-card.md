## Description:

Fetch GitHub repository metadata and project files, generate an evidence-based repository evaluation, and save the evaluation into the target knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research teams use this skill to evaluate GitHub repositories against an existing knowledge base, including relevance, dependencies, activity, license, reproducibility risk, and whether the repository is worth deeper review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags use of high-impact Gitea admin credentials.

Mitigation: Use least-privilege credentials for the configured Gitea host and review permissions before installation.

Risk: The security evidence flags under-scoped persistent write paths for knowledge-base updates.

Mitigation: Restrict save targets to approved personal or team repositories and review generated Markdown before allowing persistent writes.

Risk: The skill fetches external GitHub repository content and writes derived evaluations into a knowledge base.

Mitigation: Run in a controlled environment, validate fetched repository content, and document how fetched content and knowledge-base writes are handled.

Risk: The setup flow installs unpinned Python dependencies.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/myd2002/skills/eval-repo)
- [Publisher Profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown evaluation with shell command examples and JSON status outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes repository evaluation Markdown into a configured knowledge base and returns a saved page link when successful.]

## Skill Version(s):

3.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
