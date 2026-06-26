## Description: <br>
AI music generation assistant powered by MakebestMusic for creating songs, music, and audio tracks from user prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sthk-mbm](https://clawhub.ai/user/sthk-mbm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and musicians use this skill to request vocal or instrumental music from MakebestMusic and check generation status until playable links are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music prompts and generation requests are sent to MakebestMusic using the configured API key. <br>
Mitigation: Install only if you trust the publisher and MakebestMusic, configure the API key through skill settings, and avoid confidential personal or business information in prompts. <br>
Risk: The MBM_API_BASE environment variable can change the API endpoint used by the skill. <br>
Mitigation: Leave MBM_API_BASE unset unless you know it points to a trusted MakebestMusic endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sthk-mbm/generate-ai-music) <br>
- [MakebestMusic](https://makebestmusic.com/?pid=PIDcLjhgCXUQ) <br>
- [MakebestMusic API endpoint](https://api.makebestmusic.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON status/result payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an apiKey configured in skill settings; returns music IDs, generation status, and completion links when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
