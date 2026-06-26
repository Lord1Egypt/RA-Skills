## Description: <br>
Correction Memory installs a local correction tracker that logs per-agent corrections and replays recent corrections into future agent prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to persist corrections when agents repeat the same mistakes across sessions. It is intended for local correction logging and prompt preamble generation by agent type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Correction text is saved on disk and can be reused in later agent prompts, which may preserve stale, unwanted, sensitive, or proprietary instructions. <br>
Mitigation: Keep saved corrections short and specific, avoid secrets or proprietary raw prompts, and periodically review or delete files under $OPENCLAW_WORKSPACE/memory/corrections. <br>


## Reference(s): <br>
- [Correction tracker implementation](references/correction-tracker-template.js) <br>
- [ClawHub skill page](https://clawhub.ai/donovanpankratz-del/correction-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JavaScript code blocks; installed JavaScript writes JSONL correction records and markdown prompt preambles.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local correction notes under the workspace and replays corrections from the last 30 days.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
