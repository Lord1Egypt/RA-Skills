## Description: <br>
Captures learnings, errors, and corrections so agents can log, review, and promote reusable knowledge across future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture command failures, user corrections, missing capabilities, and recurring best practices in structured learning files for later review and promotion into agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning files and promoted memory may retain secrets, personal data, proprietary content, raw transcripts, or raw command output. <br>
Mitigation: Require review and redaction before writing or promoting entries, and avoid storing sensitive raw outputs. <br>
Risk: Broad hooks or cross-session sharing can spread low-quality or sensitive context beyond the intended workspace. <br>
Mitigation: Keep hooks project-local, avoid global empty matchers, and use cross-session transcript or messaging features only with explicit approval. <br>
Risk: Incorrect or misleading lessons can be promoted into persistent agent context and affect future behavior. <br>
Mitigation: Review learning entries before promotion and resolve or remove entries that are stale, inaccurate, or too project-specific. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entries intended for human review before promotion into persistent agent context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
