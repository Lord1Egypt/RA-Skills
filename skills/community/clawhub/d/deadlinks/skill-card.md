## Description: <br>
Check Markdown files and websites for broken links, including dead links, documentation URLs, README audits, and link health checks with zero dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and CI automation agents use this skill to audit Markdown files, documentation directories, and websites for broken local or external links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checking external links or crawling a website contacts URLs found in the target content, which can expose sensitive or internal link destinations. <br>
Mitigation: Review confidential documents before running external checks, disable external URL validation unless needed, and scope website crawling to intended targets. <br>
Risk: Recursive directory checks and website crawling can read many local files or make many outbound requests. <br>
Mitigation: Use narrow paths, conservative crawl depth, timeouts, and worker limits in automated runs. <br>


## Reference(s): <br>
- [Deadlinks README](artifact/README.md) <br>
- [Deadlinks skill definition](artifact/SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/rogue-agent1/deadlinks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and optional text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CI-friendly exit codes; optional JSON output for automation] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
