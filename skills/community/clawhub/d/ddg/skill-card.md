## Description: <br>
Use ddgr, DuckDuckGo from the terminal, to perform privacy-focused web searches from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[instant-picture](https://clawhub.ai/user/instant-picture) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other command-line users use this skill to search DuckDuckGo from a terminal, retrieve text or JSON results, use DuckDuckGo bangs, and open results when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing ddgr from an untrusted source could introduce unwanted or unsafe software. <br>
Mitigation: Install ddgr from trusted package-manager sources when possible and review source installations before use. <br>
Risk: Search queries can reveal secrets, credentials, or sensitive personal information to external search services. <br>
Mitigation: Do not include secrets or sensitive personal data in search queries. <br>
Risk: Opening search results or disabling Safe Search can expose users to unsafe or unwanted content. <br>
Mitigation: Review result URLs before opening them and use --unsafe only when Safe Search is intentionally disabled. <br>


## Reference(s): <br>
- [ddgr GitHub repository](https://github.com/jarun/ddgr) <br>
- [DuckDuckGo](https://duckduckgo.com) <br>
- [DuckDuckGo Bangs](https://duckduckgo.com/bang) <br>
- [usage-patterns.md](references/usage-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON search output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search behavior depends on ddgr installation, network access, DuckDuckGo availability, and selected options such as region, time filter, Safe Search, proxy, and JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
