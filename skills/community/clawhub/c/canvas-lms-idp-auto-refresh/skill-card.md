## Description: <br>
Automatically refreshes Canvas LMS API tokens by replaying institutional CAS/IDP login with RSA-encrypted credentials, SSO ticket exchange, token creation, and optional old-token cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[summers-tars](https://clawhub.ai/user/summers-tars) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to restore Canvas API access when tokens expire behind an institutional SSO layer. It is intended for agent workflows that need to create, store, validate, and rotate Canvas API tokens with user-provided institutional credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles institutional SSO passwords and Canvas API tokens. <br>
Mitigation: Install and run it only when token creation through institutional credentials is intended, keep .env and token files outside repositories, and restrict local file permissions. <br>
Risk: Debug output may include sensitive token or session artifacts. <br>
Mitigation: Delete or protect debug_output after each run and sanitize artifacts before sharing troubleshooting data. <br>
Risk: Token cleanup can delete existing Canvas tokens that match the configured purpose. <br>
Mitigation: Use cleanup-dry-run before deleting old tokens and set a distinct token purpose for agent-created tokens. <br>
Risk: Institutional SSO automation may conflict with local policy or be less appropriate than official authorization flows. <br>
Mitigation: Prefer institution-approved OAuth or scoped service-account flows when available. <br>


## Reference(s): <br>
- [IDP Adaptation Guide](references/idp-adaptation.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/summers-tars/canvas-lms-idp-auto-refresh) <br>
- [Publisher Profile](https://clawhub.ai/user/summers-tars) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, configuration variables, and token output as NEW_TOKEN=<token_value>] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local .env, token, cookie, cleanup summary, and debug_output artifacts depending on user configuration and CLI flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
