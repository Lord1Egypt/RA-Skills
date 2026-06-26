## Description: <br>
Generate AI images from text prompts. Pay per request with USDC on Solana via x402. No API keys, no accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geometrydotsh](https://clawhub.ai/user/geometrydotsh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate AI images from text prompts through Geometry's x402-enabled API, checking quotes and submitting paid generation requests when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid generation requests spend USDC from a Solana wallet. <br>
Mitigation: Check the free quote endpoint first, use a dedicated low-balance wallet, and require explicit confirmation before each paid generation request. <br>
Risk: Prompts are sent to Geometry's image-generation API. <br>
Mitigation: Avoid sending sensitive or confidential prompt content unless the user has approved that use. <br>


## Reference(s): <br>
- [Geometry skill page](https://clawhub.ai/geometrydotsh/geometry) <br>
- [Geometry homepage](https://geometry.sh) <br>
- [Geometry developer docs](https://app.geometry.sh/developers) <br>
- [Geometry agent card](https://api.geometry.sh/.well-known/agent.json) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents through free quote checks and paid image-generation API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
