## Description: <br>
Alibaba Cloud WAF 3.0 read-only diagnostic assistant for interception diagnosis, rule queries, and text-only configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud security operators use this skill to query Alibaba Cloud WAF and SLS data, diagnose blocked requests or rules that are not taking effect, and receive console-only remediation steps for manual WAF configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud credentials to query WAF and SLS data. <br>
Mitigation: Use a constrained RAM user, review commands before execution, and avoid exposing credentials or credential files. <br>
Risk: The security evidence notes local CLI configuration changes and plugin update or install commands despite the read-only diagnostic positioning. <br>
Mitigation: Run in a controlled environment and explicitly review any Alibaba Cloud CLI AI-mode or plugin commands before allowing them. <br>
Risk: Rule and log JSON may contain sensitive WAF or traffic details. <br>
Mitigation: Avoid storing sensitive rule or log JSON in shared temporary paths and remove local diagnostic files when finished. <br>
Risk: The package includes an unrelated translation script that can rewrite a skill file. <br>
Mitigation: Remove the translation script from runtime packages when possible and restrict execution to the diagnostic script required for rule matching. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-rule-management) <br>
- [CLI guide](references/cli_guide.md) <br>
- [CLI commands](references/cli_commands.md) <br>
- [CLI traps](references/cli_traps.md) <br>
- [WAF API reference](references/api_reference.md) <br>
- [Security rules](references/security_rules.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Configuration guide](references/configuration_guide.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-language console steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic flow; commands use Alibaba Cloud CLI and SLS with user-controlled credentials, and configuration changes are described for manual console completion.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
