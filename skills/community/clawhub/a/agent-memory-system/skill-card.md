## Description: <br>
Provides an OpenClaw long-term memory workflow with hot/warm/cold organization, scheduled archiving, nightly reflection, and lesson-to-skill extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccyaolei](https://clawhub.ai/user/ccyaolei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give an OpenClaw agent a persistent local memory structure, maintain daily logs and lessons, archive older memory files, and extract reusable skills from lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can add recurring scheduled jobs that run local maintenance scripts. <br>
Mitigation: Review the install script before execution and check crontab after installation to confirm only intended jobs were added. <br>
Risk: The skill persists local memory files that may contain sensitive information if the user records it. <br>
Mitigation: Do not store secrets or sensitive personal details in memory files; periodically review and prune local memory content. <br>
Risk: Skill extraction accepts lesson and skill names that affect local paths. <br>
Mitigation: Use trusted simple names only, and do not run extract-skill.sh with path-like or untrusted lesson or skill names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccyaolei/agent-memory-system) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples, local file templates, and generated memory or skill files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files, archive files, cron entries, and generated skill scaffolds in the configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
