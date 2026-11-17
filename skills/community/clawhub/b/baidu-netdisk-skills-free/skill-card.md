## Description: <br>
Baidu Netdisk Skills Free helps agents use the bdpan CLI for basic Baidu Netdisk status checks, directory listing, uploads, and small-file downloads within /apps/bdpan/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to perform constrained Baidu Netdisk file-management tasks from an agent, including checking login status, listing files, uploading files, and downloading files up to 50 MB under /apps/bdpan/. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan found broad, unrelated triggers and capabilities that could cause unsafe use outside the Baidu Netdisk purpose. <br>
Mitigation: Use the skill only for explicit Baidu Netdisk tasks under /apps/bdpan/ and do not allow generic file-processing, Security-task, API-key, search, delete, rename, or backup behavior unless the publisher provides a corrected artifact. <br>
Risk: The skill can lead an agent to run shell commands and perform write operations through bdpan. <br>
Mitigation: Require explicit user confirmation for uploads, downloads that overwrite local files, and any ambiguous path; validate paths stay within /apps/bdpan/ before execution. <br>
Risk: The artifact references install and login scripts without providing auditable script names in the release artifact. <br>
Mitigation: Do not run placeholder install or login commands; require clear supported commands and auditable install/login scripts from the publisher before enabling those flows. <br>
Risk: Credential exposure is possible if an agent reads or prints local bdpan configuration. <br>
Mitigation: Do not read or output ~/.config/bdpan/config.json or other token-bearing files, and avoid direct bdpan login commands outside the documented safe flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/baidu-netdisk-skills-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON-style result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operations are scoped to /apps/bdpan/; direct downloads are limited to files up to 50 MB.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
