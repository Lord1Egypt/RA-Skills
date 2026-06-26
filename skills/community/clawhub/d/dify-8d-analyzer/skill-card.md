## Description: <br>
Invokes a Dify API-backed 8D report analysis workflow when an OpenClaw user message starts with the configured Chinese trigger phrase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[langwang1pm](https://clawhub.ai/user/langwang1pm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to submit 8D report analysis questions to a Dify-backed workflow and receive the workflow result as the agent reply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts, reports, and open_id values may leave the local environment through the Dify workflow. <br>
Mitigation: Use the skill only with trusted Dify endpoints and avoid confidential reports until the publisher documents the data flow. <br>
Risk: The skill hands execution to a local shell script, which makes the behavior dependent on a script outside the packaged artifact. <br>
Mitigation: Review and harden the local dify_router.sh script before deployment, and restrict execution to trusted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/langwang1pm/dify-8d-analyzer) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown response based on Dify script stdout, with shell-command guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow may take 30-120 seconds and is configured with a 180 second timeout.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
