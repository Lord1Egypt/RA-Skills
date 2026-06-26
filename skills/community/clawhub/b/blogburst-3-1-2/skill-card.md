## Description: <br>
BlogBurst is an AI marketing agent for generating and repurposing content, managing multi-platform posting, checking analytics, and running SEO/GEO and competitor workflows through the BlogBurst API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xspeter](https://clawhub.ai/user/0xspeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and business operators use this skill to ask an agent for blog drafts, social posts, repurposed content, trend discovery, analytics checks, and marketing automation across connected platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish and engage from connected social or messaging accounts. <br>
Mitigation: Confirm connected platforms, posting frequency, review process, pause controls, and revocation steps before enabling auto-pilot or auto-engagement. <br>
Risk: The skill requires a BlogBurst API key and the artifact suggests shell-based setup that may persist credentials. <br>
Mitigation: Use a safer secret store or session-scoped environment variable, avoid printing the key, and rotate or revoke the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/0xspeter/blogburst-3-1-2) <br>
- [BlogBurst website](https://blogburst.ai) <br>
- [BlogBurst API docs](https://api.blogburst.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API request examples, and API-returned text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BLOGBURST_API_KEY; actions may publish or engage through connected social and messaging accounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json lists 3.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
