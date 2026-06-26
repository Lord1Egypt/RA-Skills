## Description: <br>
Coordinates multiple agents to independently argue competing approaches, then synthesizes their positions to identify the best solution for complex decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xrichyrich](https://clawhub.ai/user/0xrichyrich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run structured debates among multiple sub-agents for architecture decisions, debugging, strategy analysis, security review, and other non-obvious choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports a suspicious maintainer workflow because a bundled review helper can run nested Codex review with full sandbox bypass and can send diffs to fallback external reviewers. <br>
Mitigation: Install only if the publisher is trusted; before using review helpers, prefer --no-yolo or AUTOREVIEW_YOLO=0 and verify whether fallback external reviewers are acceptable for private diffs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xrichyrich/agent-debate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with file paths and prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses debate files under plans/debate-{topic}/ to coordinate positions, rebuttals, synthesis, and final decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
