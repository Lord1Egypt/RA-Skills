## Description: <br>
Troubleshoots CLI Proxy API configuration, authentication, model registration, request encoding, proxy connectivity, and common request failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17329971](https://clawhub.ai/user/17329971) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose CLI Proxy API issues such as missing model providers, failed auth loading, malformed request bodies, proxy timeouts, and account capability mismatches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting authentication paths can expose API keys, OAuth tokens, auth-dir contents, session files, or logs if copied into prompts or shared reports. <br>
Mitigation: Redact secrets, session material, auth directory contents, and sensitive log lines before sharing diagnostics. <br>
Risk: Sample curl or Python requests can send sensitive requests through an unintended or untrusted proxy endpoint. <br>
Mitigation: Run sample requests only against proxy endpoints the user controls or explicitly trusts. <br>


## Reference(s): <br>
- [CLI Proxy API Homepage](https://github.com/stainless-codex/cli-proxy-api) <br>
- [Source Architecture Reference](references/source-architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, YAML snippets, and source-path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only troubleshooting guidance; the skill itself does not generate files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
