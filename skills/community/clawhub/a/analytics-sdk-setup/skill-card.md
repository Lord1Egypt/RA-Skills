## Description: <br>
Guides repo-aware coding agents through auditing, installing, reconciling, aligning, or fixing TikTok Pixel and Meta Pixel integrations, with attention to duplicate initialization, event drift, consent, CSP, LDU, privacy gating, and analytics ownership. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peter-wf](https://clawhub.ai/user/peter-wf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when they want an agent to inspect a real repository, choose the right execution mode, and produce questions, plans, shell commands, configuration guidance, or code changes for TikTok and Meta Pixel tracking work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated changes may add or alter third-party tracking behavior, including Pixel identifiers, consent handling, CSP allowlists, or Advanced Matching. <br>
Mitigation: Review proposed changes before deployment and require privacy or legal approval before enabling identifiers, Advanced Matching, or new tracking behavior. <br>
Risk: Incorrect event mapping or duplicate initialization can create misleading analytics or duplicate conversion reporting. <br>
Mitigation: Verify per-platform initialization, event timing, deduplication, and cross-platform consistency in the target repository before relying on analytics results. <br>


## Reference(s): <br>
- [Analytics SDK Setup README](README.md) <br>
- [Install and event details](references/install-and-events.md) <br>
- [Privacy, CSP, and data handling](references/privacy-and-csp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mode selection, questions, implementation plans, repository findings, patches, event mappings, and verification notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
