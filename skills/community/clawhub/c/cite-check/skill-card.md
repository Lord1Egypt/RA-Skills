## Description:

Confirm citations in a draft by extracting URLs and arXiv IDs, checking that they resolve, and optionally checking whether fetched sources support nearby claims with a local model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workloftai](https://clawhub.ai/user/workloftai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and publishing agents use cite-check as a blocking pre-publication gate for drafts that contain citations. It helps catch dead links, fabricated arXiv IDs, and optionally sources that do not support the cited claim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts every URL and arXiv reference found in a draft, which can expose citation targets and trigger outbound network requests from the execution environment.

Mitigation: Run it with sandboxed or allowlisted network egress, especially for untrusted drafts or environments that can reach internal services.

Risk: Phase 2 may send draft excerpts and claims to the configured Ollama endpoint.

Mitigation: Use a trusted local Ollama server for confidential material and avoid pointing the configuration at a shared or remote endpoint unless that data flow is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workloftai/skills/cite-check)
- [Workloft Labs](https://workloft.ai/labs)
- [Workloft support](https://workloft.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands; scripts can emit human-readable text or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit status is intended for CI or publishing gates: 0 when checks pass and non-zero when citations fail or require review.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter and clawhub.json state 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
