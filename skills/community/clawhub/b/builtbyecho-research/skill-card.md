## Description: <br>
Use when a user asks an agent to do web research, source discovery, citation-backed reporting, page extraction, crawling, or browser-rendered research using the BuiltByEcho Research npm package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to run web research workflows, discover and inspect sources, crawl or render pages, extract structured fields, and produce citation-backed reports. It can also guide installation and use of the @builtbyecho/research npm package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Networked research may collect or summarize sensitive source material. <br>
Mitigation: Use clear target limits, review gathered material before sharing it, and avoid entering secrets or private content into research prompts. <br>
Risk: Optional upload of reports or traces to Vaultline can expose research artifacts to a third-party service. <br>
Mitigation: Upload only after explicit approval and after reviewing the report or trace bundle for sensitive information. <br>
Risk: Browser rendering and crawling can interact with site controls or terms of service. <br>
Mitigation: Do not bypass CAPTCHA, login walls, paywalls, robots or ToS restrictions, or other access controls. <br>
Risk: Citation-backed generated prose can still contain incorrect or misleading conclusions. <br>
Mitigation: Verify citations and source claims before using results for high-stakes or public decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/builtbyecho/builtbyecho-research) <br>
- [BuiltByEcho Research homepage](https://github.com/BuiltByEcho/research) <br>
- [BuiltByEcho publisher profile](https://clawhub.ai/user/builtbyecho) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include citation-backed reports, research traces, extracted structured fields, crawl outputs, and installation or configuration steps.] <br>

## Skill Version(s): <br>
0.5.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
