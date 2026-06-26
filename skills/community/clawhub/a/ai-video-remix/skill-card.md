## Description: <br>
Ai Video Remix helps agents plan and render styled video remixes from a user's ShotAI-indexed local video library using semantic search, optional LLM planning, ffmpeg clip extraction, and Remotion rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abu-shotai](https://clawhub.ai/user/abu-shotai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and external users use this skill to have an agent create styled highlight reels, travel vlogs, sports clips, nature montages, or other video remixes from a local ShotAI-indexed footage library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to clone and run a separate runtime that can execute npm install and npx commands. <br>
Mitigation: Review the separately cloned runtime before execution and install only when the user intends to use ShotAI for local video remixing. <br>
Risk: Local footage, SHOTAI_TOKEN, and optional LLM API keys may be sensitive. <br>
Mitigation: Keep tokens and keys out of logs and repositories, and use AGENT_PROVIDER=none or a local provider for sensitive footage. <br>
Risk: Optional YouTube music downloads may introduce network access, availability issues, or licensing concerns. <br>
Mitigation: Use --bgm with a licensed local music file when network access or music licensing is a concern. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abu-shotai/ai-video-remix) <br>
- [ShotAI](https://www.shotai.io) <br>
- [Setup Guide](references/setup.md) <br>
- [Configuration Reference](references/config.md) <br>
- [Video Quality Tuning Guide](references/tuning.md) <br>
- [Composition Guide](references/composition-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; runtime code is cloned separately before rendering video output.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
