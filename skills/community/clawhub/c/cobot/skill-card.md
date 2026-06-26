## Description: <br>
Collaborative robot task planner. Use when json cobot tasks, csv cobot tasks, checking cobot status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Cobot to keep a local command-line log of cobot-related task notes, status checks, searches, statistics, and JSON or CSV exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local entries may contain sensitive operational data and are persisted on disk. <br>
Mitigation: Avoid storing secrets or sensitive operational details unless local persistence in COBOT_DIR or ~/.cobot is acceptable. <br>
Risk: The remove command deletes entries immediately. <br>
Mitigation: Export or back up important entries before using remove, and confirm the entry number before deletion. <br>
Risk: Exports copy saved entries into the current working directory. <br>
Mitigation: Run exports only from an intended directory and review generated JSON or CSV files before sharing. <br>


## Reference(s): <br>
- [Cobot on ClawHub](https://clawhub.ai/ckchzh/cobot) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Bash command examples; the skill script produces terminal text and JSONL, JSON, or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local persistence under COBOT_DIR or ~/.cobot; export writes cobot-export.json or cobot-export.csv in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
