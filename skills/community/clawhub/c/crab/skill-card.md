## Description: <br>
Crab Catch is a Web3 research skill that automatically collects and organizes project data and potential risks from social media, websites, code, and on-chain data, and produces a complete and objective research report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NotevenDe](https://clawhub.ai/user/NotevenDe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and Web3 analysts use this skill to investigate projects by collecting website, social, GitHub, and on-chain evidence, then producing a concise risk-focused research report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses a global browser automation tool. <br>
Mitigation: Review the install step before use and run the skill in an isolated environment when possible. <br>
Risk: The skill stores reusable Crab credentials under ~/.config/crab and report artifacts under ~/.crab-catch/reports. <br>
Mitigation: Protect or periodically remove local credential and report files, especially on shared machines. <br>
Risk: Research targets and investigation details may be sent to Crab, Grok, GitHub, and on-chain services. <br>
Mitigation: Avoid confidential, authenticated wallet, exchange, account, or private investigation targets unless explicitly authorized. <br>


## Reference(s): <br>
- [Crab ClawHub listing](https://clawhub.ai/NotevenDe/crab) <br>
- [API Explorer documentation](API_EXPLORER.md) <br>
- [Architecture documentation](ARCHITECTURE.md) <br>
- [Report template](REPORT_TEMPLATE.md) <br>
- [Crab API base URL](https://crab-skill.opsat.io) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research report with cited findings and optional saved PDF report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output language follows the user's input language, with Chinese as the documented default.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact metadata says 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
