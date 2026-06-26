## Description: <br>
Image Social Media guides multi-platform social-media image planning and generation for Instagram, TikTok, YouTube, LinkedIn, Xiaohongshu, and related platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and agents use this skill to plan platform-specific social-media visuals, captions, safe-area checks, and iterative image-generation steps through the dLazy CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key, which may be saved in the local CLI configuration. <br>
Mitigation: Use DLAZY_API_KEY for per-session credentials when persistence is not desired, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts and supplied media are sent to dLazy cloud services for generation. <br>
Mitigation: Avoid uploading sensitive media or confidential prompts unless the user has approved that cloud processing path. <br>
Risk: The documented @latest CLI install target may change over time. <br>
Mitigation: Review the dLazy CLI package and pin a known version before deployment when reproducibility is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/image-social-media) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy website](https://dlazy.com) <br>
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Text] <br>
**Output Format:** [Markdown with inline shell commands and generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific layout plans, safe-area checks, in-image text, caption copy, dLazy CLI commands, and returned image URLs.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
