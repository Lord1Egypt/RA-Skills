## Description: <br>
Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NicholasSpisak](https://clawhub.ai/user/NicholasSpisak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to navigate Clawdbot documentation, locate setup and troubleshooting pages, retrieve docs, track recent documentation changes, and adapt common configuration snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate during general Clawdbot discussion rather than a documentation request. <br>
Mitigation: Redirect the agent to use the skill only for Clawdbot documentation navigation, configuration, setup, troubleshooting, and documentation-change questions. <br>
Risk: Users may include real provider tokens or secrets while asking for configuration help. <br>
Mitigation: Keep real provider tokens out of chat and use placeholder environment variables in configuration examples. <br>
Risk: Future releases could change the behavior or safety profile of the documentation helper. <br>
Mitigation: Review future updates before installation or deployment. <br>


## Reference(s): <br>
- [Clawdbot documentation](https://docs.clawd.bot/) <br>
- [ClawHub skill page](https://clawhub.ai/NicholasSpisak/clawddocs) <br>
- [Common Config Snippets](snippets/common-configs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite Clawdbot documentation URLs and use cached sitemap, search, fetch, recent-update, and change-tracking helper scripts.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
