## Description: <br>
Post and schedule content across multiple social platforms via the Blotato API with platform-specific formatting and media upload support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to prepare, publish, or schedule one piece of content across connected Twitter, LinkedIn, Facebook, Instagram, TikTok, Threads, Bluesky, Pinterest, and YouTube accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Blotato API key can allow the agent to publish or schedule real posts through connected social accounts. <br>
Mitigation: Provide the key only at runtime or through a proper secret store, and do not store it in plaintext workspace files. <br>
Risk: Content, media, target platforms, accounts, or scheduled times may be wrong before posts are submitted. <br>
Mitigation: Manually verify the final text, media files, selected accounts or platforms, and posting time before each run. <br>


## Reference(s): <br>
- [Blotato API Reference](references/api.md) <br>
- [Blotato API Base URL](https://backend.blotato.com/v2) <br>
- [Blotato Account Settings](https://my.blotato.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and JSON API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Blotato API key at runtime and can publish or schedule posts through connected social accounts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
