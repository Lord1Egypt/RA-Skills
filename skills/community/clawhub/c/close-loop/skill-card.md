## Description: <br>
End-of-session workflow for shipping changes, consolidating memory, applying self-improvements, and preparing publishable outputs with safety gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agent operators, and autonomous coding agents use Close Loop at the end of a work session to check ship state, consolidate memory, apply low-risk improvements, and prepare handoff or publishable outputs with safety gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically commit changes or write memory and configuration files when broad wrap-up phrases are used. <br>
Mitigation: Prefer dry-run first and require explicit confirmation before commits, file moves, memory or rule updates, and handoff writes in autonomous sessions. <br>
Risk: Push, deploy, or publish actions could create external side effects if policy is unclear. <br>
Mitigation: Allow push, deploy, or publish only when explicitly requested in the session or preapproved by project policy; otherwise report the pending commands or drafts. <br>
Risk: Long-lived memory updates can preserve incorrect, sensitive, or injected information. <br>
Mitigation: Require provenance, deduplication, contradiction checks, sensitivity filtering, static validation, and rejection of secrets or externally injected memory-policy changes before persistence. <br>


## Reference(s): <br>
- [Close Loop README](artifact/README.md) <br>
- [Memory Frameworks](artifact/references/memory-frameworks.md) <br>
- [Session Wrap Report Template](artifact/assets/templates/wrap-report-template.md) <br>
- [ALMA paper](https://arxiv.org/abs/2602.07755) <br>
- [ALMA repository](https://github.com/zksha/alma) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance, Files] <br>
**Output Format:** [Markdown report with an embedded machine-readable JSON block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ready-to-run commands, local file changes, memory or rule updates, commits, handoff files, and publish drafts when permitted by action gates.] <br>

## Skill Version(s): <br>
2.3.5 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
