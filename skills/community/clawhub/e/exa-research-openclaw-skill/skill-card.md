## Description:

Use the local `exa` CLI to search the live web, ask grounded questions with citations, fetch page contents, find similar links, retrieve Exa code context, or manage Exa research tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wkenya](https://clawhub.ai/user/wkenya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route live web research, grounded answer synthesis, page extraction, related-link discovery, code-context lookup, and longer Exa research workflows through the local Exa CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can pass the Exa API key to whichever executable is selected by `EXA_BIN` or `PATH`.

Mitigation: Use a trusted Exa CLI binary, prefer an absolute or controlled executable path, and avoid running the skill from untrusted shell environments.

Risk: API keys may be exposed through loose local secret handling.

Mitigation: Prefer OpenClaw-managed secrets or a locked-down key file, keep keys outside the repository, and restrict file permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wkenya/skills/exa-research-openclaw-skill)
- [Upstream Exa Repository](https://github.com/jdegoes/exa)
- [Exa Website](https://exa.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Exa CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `exa` binary and an `EXA_API_KEY`; the skill advises using narrow queries, highlights, summaries, token caps, and selected URL extraction to keep context small.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
