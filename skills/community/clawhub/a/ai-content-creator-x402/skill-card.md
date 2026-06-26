## Description: <br>
All-in-one AI content creation agent that writes blog posts, social media, newsletters, scripts, and product copy; generates images, video, and voiceovers; researches topics; extracts web content; and produces multimedia through x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plagtech](https://clawhub.ai/user/plagtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content teams, and developers use this skill to plan, research, generate, and repurpose written, visual, audio, and video content through paid API-backed workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, URLs, fetched content, transcripts, audio, or other user-provided material to third-party paid services. <br>
Mitigation: Use non-sensitive inputs, review content before submission, and avoid sending confidential data unless the third-party service is approved for that data. <br>
Risk: The skill can initiate paid API calls and x402 micropayments. <br>
Mitigation: Confirm endpoint costs before use and prefer a dedicated limited wallet, subscription key, or account with spending controls. <br>
Risk: The security verdict is suspicious because the skill invokes shell setup and contacts paid external APIs. <br>
Mitigation: Review the shell script and environment variables before execution, and install only in environments where external API access and payment behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/plagtech/ai-content-creator-x402) <br>
- [Publisher profile](https://clawhub.ai/user/plagtech) <br>
- [Gateway service](https://gateway.spraay.app) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON API responses, shell command examples, generated text, media outputs, transcripts, and web research summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and python3, requires RESEARCH_API_KEY for the paid gateway, and may return generated media or externally fetched content depending on the endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
