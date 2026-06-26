## Description: <br>
Analyzes your conversation transcripts daily to find patterns, suggest SOUL.md improvements, and recommend skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dainash](https://clawhub.ai/user/dainash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review OpenClaw conversation transcripts, identify repeated patterns, analyze failures, tool usage, and costs, and produce concise optimization recommendations for SOUL.md and skill adoption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The transcript extraction can read more private conversation history than the daily or recent framing suggests. <br>
Mitigation: Run it manually on a limited transcript folder first, and use it only after reviewing the privacy implications. <br>
Risk: Generated SOUL.md and workflow recommendations may be incorrect or overfit to recent behavior. <br>
Mitigation: Review each recommendation before applying it; the skill is designed to provide suggestions only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dainash/clawforage-prompt-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/dainash) <br>
- [InspireHub Labs](https://inspireehub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown optimization reports with inline shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only and suggestion-based; reports are capped at 500 words and require bash and jq.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
