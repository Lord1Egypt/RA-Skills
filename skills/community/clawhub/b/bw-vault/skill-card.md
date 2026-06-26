## Description: <br>
Set up and use Bitwarden CLI (bw). Use when installing the CLI, authenticating (login/unlock), or reading secrets from your vault. Supports email/password, API key, and SSO authentication methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StartupBros](https://clawhub.ai/user/StartupBros) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate the Bitwarden CLI, authenticate to Bitwarden or Vaultwarden, and retrieve vault secrets for local workflows or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vault secrets or BW_SESSION values can be exposed through logs, shared shells, broad vault listings, or leftover environment variables. <br>
Mitigation: Install only the official Bitwarden CLI, unlock the vault only for the task at hand, request specific items, keep secrets out of logs and shared shells, unset exported secrets after use, and run bw lock or bw logout when finished. <br>


## Reference(s): <br>
- [Bitwarden CLI Documentation](https://bitwarden.com/help/cli/) <br>
- [ClawHub Skill Page](https://clawhub.ai/StartupBros/bw-vault) <br>
- [Get Started Guide](references/get-started.md) <br>
- [CLI Examples](references/cli-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands for Bitwarden CLI authentication, vault access, session management, and self-hosted server configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
