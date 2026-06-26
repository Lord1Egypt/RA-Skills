## Description: <br>
Scans agent skills for security threats using the Cisco AI skill-scanner CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godsboy](https://clawhub.ai/user/godsboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan agent skill directories for prompt injection, data exfiltration, credential harvesting, malicious code patterns, and publish-blocking security findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional LLM-assisted scanning can send skill content to an external model provider. <br>
Mitigation: Use the default behavioral scan for private or sensitive skills and enable full LLM mode only for content approved for external processing. <br>
Risk: Installing the external skill-scanner CLI directly into a shared Python environment can affect other tooling. <br>
Mitigation: Install the CLI in an isolated Python environment or container before running scans. <br>
Risk: A clean scan means no known threat patterns were detected, not that a skill is guaranteed safe. <br>
Mitigation: Pair scanner results with human review and re-scan before deployment or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godsboy/cisco-skill-scanner) <br>
- [Cisco AI skill-scanner repository](https://github.com/cisco-ai-defense/skill-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and scanner report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default scans use behavioral analysis without an API key; full LLM-assisted scans require an approved API key and may process skill content externally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
