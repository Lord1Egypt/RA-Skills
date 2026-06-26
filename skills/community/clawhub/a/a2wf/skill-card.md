## Description: <br>
Validate, generate, and audit A2WF siteai.json files for website AI agent governance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wolfuser45](https://clawhub.ai/user/Wolfuser45) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate local siteai.json files, generate siteai.json policies, and review A2WF compliance posture for websites. It helps agents reason about website permission, identification, scraping, and legal policy signals before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live website checks require fetching public siteai.json files and may create temporary local files. <br>
Mitigation: Use web_fetch only for the requested siteai.json URL, save results to a temporary file, and remove temporary files after local validation. <br>
Risk: The advertised live-audit command should be treated as limited local analysis unless the publisher clarifies or fixes the live-audit documentation. <br>
Mitigation: Use the local validator for saved siteai.json files and avoid relying on the audit command as proof of network discovery behavior. <br>


## Reference(s): <br>
- [A2WF homepage](https://a2wf.org) <br>
- [A2WF specification](https://a2wf.org/specification/) <br>
- [A2WF core schema v1.0](https://a2wf.org/schema/core-v1.0.json) <br>
- [A2WF Agent Implementer's Guide](references/implementer-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce validator reports and complete siteai.json policy documents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
