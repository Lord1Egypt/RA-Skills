## Description: <br>
Operate and improve the Delx Wellness Next.js site, including SEO, GEO, analytics, and agent-readiness discovery files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to maintain the Delx Wellness site, improve SEO and agent discovery, check analytics or Search Console wiring, and troubleshoot setup and safety boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may involve OAuth tokens, service-account JSON, analytics credentials, or Search Console credentials. <br>
Mitigation: Use least-privilege credentials, keep public analytics IDs separate from private keys, and do not print tokens, API keys, service-account JSON, local token files, or private user data. <br>
Risk: Live provider calls, API proxying, or writes can consume quotas or affect production services. <br>
Mitigation: Prefer connection status, manifest, doctor, privacy audit, or dry-run surfaces first, and require explicit approval before live writes or quota-consuming calls. <br>
Risk: Wellness site operations output could be mistaken for regulated medical, legal, financial, or platform-policy advice. <br>
Mitigation: Treat outputs as site operations guidance, keep user consent explicit, and route regulated advice questions to qualified review. <br>


## Reference(s): <br>
- [Delx Wellness Site Repository](https://github.com/davidmosiah/delx-wellness-site) <br>
- [Delx Wellness Site](https://wellness.delx.ai) <br>
- [ClawHub Skill Release](https://clawhub.ai/davidmosiah/delx-wellness-site) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run recommendations, privacy checks, and explicit approval prompts before live writes or quota-consuming provider calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
