## Description:

$0 test-time scaling with online learning. Classify, generate, and verify using free model ensembles. Models self-select via ELO scoring and A/B testing from deployment data, with NVIDIA NIM models and optional Copilot integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isotrivial](https://clawhub.ai/user/isotrivial)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add ensemble-based classification, generation, verification, model health checks, and online model selection around NVIDIA NIM free-tier models. It is suited for workflows such as code review, content moderation, fact-checking, summarization, CI gates, and agent self-evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and context may be sent to NVIDIA NIM and, when optional Copilot paths are enabled, GitHub Copilot.

Mitigation: Use only data approved for those providers, and disable or avoid Copilot and audit features unless provider use and logging are acceptable.

Risk: The security evidence reports that the skill can reuse local GitHub/Copilot credentials.

Mitigation: Review the local OpenClaw credential environment before use, restrict credentials to the intended workspace, and avoid Copilot model aliases unless that credential use is expected.

Risk: Online learning and feedback features can retain prompt-derived model votes and feedback state locally.

Mitigation: Set a controlled FREE_SCALING_STATE_DIR for sensitive runs, review retained state files, and clear local cache state when retention is not appropriate.

## Reference(s):

- [Free Scaling ClawHub page](https://clawhub.ai/isotrivial/skills/free-scaling)
- [NVIDIA NIM build catalog](https://build.nvidia.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python and shell examples; runtime calls may return text labels, generated text, dataclass-style results, or JSON from CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include model votes, confidence, latency, health status, generated candidates, judge votes, and ELO or feedback state summaries.]

## Skill Version(s):

3.3.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
