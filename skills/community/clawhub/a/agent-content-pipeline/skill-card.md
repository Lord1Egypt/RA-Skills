## Description: <br>
Safe content workflow (drafts/reviewed/revised/approved/posted) with human-in-the-loop approval, plus CLI to list/move/review and post to LinkedIn/X. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larsderidder](https://clawhub.ai/user/larsderidder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, content operators, and agent users use this skill to set up a reviewed social-content workflow where agents draft and revise posts while humans approve and post them through the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow installs an external global npm posting tool and can involve social-media credentials. <br>
Mitigation: Install only if the publisher and npm package are trusted; prefer dry runs, secure mode, and a dedicated browser profile or test account. <br>
Risk: Manual X cookie handling can expose session tokens if pasted into the wrong place. <br>
Mitigation: Paste auth_token and ct0 only into the local CLI prompt and avoid storing or sharing them elsewhere. <br>
Risk: Agent-produced content could be posted before appropriate human review. <br>
Mitigation: Keep the agent limited to drafting and revision states; require human approval through content review and manual confirmation before posting. <br>


## Reference(s): <br>
- [Agent Content Pipeline ClawHub release](https://clawhub.ai/larsderidder/agent-content-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content drafts, YAML frontmatter examples, and CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized around draft, review, revision, approval, and posting states.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
