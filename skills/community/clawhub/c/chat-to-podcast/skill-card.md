## Description: <br>
Transforms selected AI chat history into a podcast-style article draft, asks the user to confirm it, and publishes it to a Halo blog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-shen1121](https://clawhub.ai/user/alex-shen1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and blog maintainers use this skill to turn selected OpenClaw conversations into human-reviewed podcast-style Markdown articles and publish them through a configured Halo account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search selected or historical OpenClaw chat sessions, which may expose private or sensitive conversation content. <br>
Mitigation: Require the agent to show the exact sessions or files it plans to read, limit extraction to specific messages, and review the full draft for private information before publication. <br>
Risk: The skill can publish content publicly through a configured Halo account. <br>
Mitigation: Verify the Halo profile, URL, slug, visibility, and overwrite behavior before approving any publish step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alex-shen1121/chat-to-podcast) <br>
- [Publisher profile](https://clawhub.ai/user/alex-shen1121) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown draft with confirmation prompts and Halo publishing commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate article imagery and update a local episode counter after successful publication.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
