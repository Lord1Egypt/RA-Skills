## Description: <br>
Guides agents through podcast and audiobook production on the Ximalaya AI creation platform, including content setup, voice selection, audio synthesis, mixing, and optional album publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[audiobooklm](https://clawhub.ai/user/audiobooklm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn text or dialogue scripts into podcast or audiobook chapters through the audiobooklm_mcp service. It helps agents collect required choices, configure books and chapters, select voices, run synthesis and mixing, and return the resulting audio and editing links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow connects an account token to the Ximalaya audiobook creation service, which may handle scripts, book and chapter metadata, generated audio tasks, and optional album uploads. <br>
Mitigation: Install only when that service connection is intended, use a valid account token, and pause on authentication or connection errors until the user updates MCP configuration. <br>
Risk: Optional publishing, payment, or recharge steps can affect external accounts or costs. <br>
Mitigation: Require explicit user confirmation before publishing, uploading to an album, or directing the user to billing or recharge actions. <br>


## Reference(s): <br>
- [Ximalaya AI Creation Platform](https://aigc.ximalaya.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/audiobooklm/audiobooklm-podcast) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, text] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, MCP tool-call examples, identifiers, URLs, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before MCP actions; final responses can include book IDs, chapter IDs, selected voices, generated audio URLs, editor links, and payment or recharge links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
