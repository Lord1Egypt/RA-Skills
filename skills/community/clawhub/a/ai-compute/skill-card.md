## Description: <br>
AI Compute is a 27-tool AI compute agent for LLM inference, image generation, video generation, text-to-speech, speech-to-text, embeddings, GPU inference, Bittensor decentralized AI, on-chain AI analytics, and prepaid compute futures via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plagtech](https://clawhub.ai/user/plagtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use AI Compute to call paid AI compute endpoints for text, image, video, audio, embeddings, GPU inference, decentralized AI, on-chain intelligence, and prepaid compute-credit workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid x402 or USDC-backed compute calls through an external gateway. <br>
Mitigation: Install only when paid compute is intended, review each endpoint and payload before execution, and require explicit approval for deposits, refunds, prepaid-credit execution, batch jobs, video generation, or other high-cost workflows. <br>
Risk: The skill requires a service credential in RESEARCH_API_KEY. <br>
Mitigation: Keep the credential scoped to this service, avoid sharing it across unrelated skills, and rotate it if exposed. <br>
Risk: The skill depends on a gateway service for compute execution and payment handling. <br>
Mitigation: Use only trusted gateway URLs and review RESEARCH_GATEWAY_URL before running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/plagtech/ai-compute) <br>
- [Publisher profile](https://clawhub.ai/user/plagtech) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Default gateway](https://gateway.spraay.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESEARCH_API_KEY for subscription access; calls may trigger paid x402/USDC-backed compute requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
