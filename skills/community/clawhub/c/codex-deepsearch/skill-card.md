## Description: <br>
Guides Codex through deep, source-backed research workflows with evidence separation, source and claim ledgers, review gates, privacy-safe repository handling, and readiness decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoqing404](https://clawhub.ai/user/shaoqing404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical decision makers use this skill when Codex needs to perform evidence-heavy research, architecture discovery, product or API analysis, or research that may become a plan, specification, roadmap, PRD, or engineering input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to inspect local repository files or make user-requested documentation or skill-file edits. <br>
Mitigation: Use it only with explicit workspace authority, keep edits scoped to the requested project or research directory, and review changes before relying on them. <br>
Risk: Research outputs can be misleading if claims are based on incomplete, stale, or snippet-only evidence. <br>
Mitigation: Maintain source and claim ledgers, label uncertainty, check counter-evidence, and run the review gate before treating outputs as decision-ready. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaoqing404/skills/codex-deepsearch) <br>
- [Server-resolved GitHub source](https://github.com/shaoqing404/codex-deepsearch/tree/main/plugins/codex-deepsearch/skills/codex-deepsearch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, ledgers, status labels, and optional code or configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final status is reported as DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
