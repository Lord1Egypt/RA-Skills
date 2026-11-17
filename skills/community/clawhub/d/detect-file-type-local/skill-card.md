## Description:

Local, offline AI-powered file type detection with no network calls or API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pgeraghty](https://clawhub.ai/user/pgeraghty)

### License/Terms of Use:

MIT

## Use Case:

Developers, security engineers, and automation agents use this skill to classify files by content, verify MIME types, and triage extension mismatches while keeping file bytes local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads files or directories that the user explicitly asks it to classify.

Mitigation: Run it only against intended paths and avoid broad recursive scans over sensitive directories unless that access is acceptable.

Risk: The default stdin mode can spool very large or endless input streams to a temporary file.

Mitigation: Use --stdin-mode head with a size cap or enforce external stream limits in automated workflows.

Risk: Content-based detection can produce low-confidence or incomplete results for very small files, empty files, or head-only stdin scans.

Mitigation: Check the confidence score and use additional validation before making high-impact security or ingestion decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pgeraghty/skills/detect-file-type-local)
- [Google Magika](https://github.com/google/magika)
- [MITRE ATT&CK: Masquerading](https://attack.mitre.org/techniques/T1036/)
- [Proofpoint: Multistage Polyglot Delivery](https://www.proofpoint.com/us/blog/threat-insight/call-it-what-you-want-threat-actor-delivers-highly-targeted-multistage-polyglot)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON object or array, human-readable text, or bare MIME type text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes path, detected label, MIME type, confidence score, group, description, and text/binary indicator when using JSON output.]

## Skill Version(s):

0.2.0 (source: frontmatter, pyproject.toml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
