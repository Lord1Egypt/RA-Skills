## Description: <br>
Social media scheduler, cross-poster, and content calendar for OpenClaw across YouTube, Instagram, Facebook, X, TikTok, Threads, and Pinterest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codivion](https://clawhub.ai/user/codivion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure CodivUpload access, schedule or publish social media content, cross-post across connected platforms, manage content calendars, pull analytics, and coordinate livestream workflows through an OpenClaw agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real connected social accounts when a CodivUpload API key is configured. <br>
Mitigation: Use the narrowest API key scope available, preferably single-platform or per-workspace, and review each approval prompt before posting, scheduling, livestreaming, deleting, or changing account settings. <br>
Risk: A broad or global API key can authorize actions beyond ordinary posting workflows. <br>
Mitigation: Avoid global account keys unless account or billing changes are intentionally needed; rotate any key that is pasted into chat or otherwise exposed. <br>
Risk: The optional MCP package expands the supply-chain surface in a credentialed runtime. <br>
Mitigation: Install the optional MCP server only when needed, pin the exact version, and verify the package publisher and integrity before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codivion/codivupload-social-manager) <br>
- [CodivUpload product site](https://codivupload.com) <br>
- [CodivUpload dashboard](https://app.codivupload.com/en/dashboard) <br>
- [CodivUpload MCP package](https://www.npmjs.com/package/codivupload-mcp) <br>
- [OpenClaw MCP documentation](https://docs.openclaw.ai/skills/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CODIVUPLOAD_API_KEY; publishing, bulk scheduling, livestream, deletion, and account-setting actions are confirmation-gated by the runtime and CodivUpload API key scope.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
