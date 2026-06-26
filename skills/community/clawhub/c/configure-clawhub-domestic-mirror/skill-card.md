## Description: <br>
Configures ClawHub CLI to use the cn.clawhub-mirror.com domestic mirror for faster skill search, download, and install operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roger0808](https://clawhub.ai/user/roger0808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when ClawHub installs, searches, or updates are slow or timing out and they want persistent shell configuration for a domestic mirror plus verification commands. <br>

### Deployment Geography for Use: <br>
Global, with practical applicability for environments that intentionally route ClawHub CLI traffic through cn.clawhub-mirror.com. <br>

## Known Risks and Mitigations: <br>
Risk: The skill and bundled script can permanently change shell startup configuration so ClawHub CLI traffic uses cn.clawhub-mirror.com. <br>
Mitigation: Install only when that routing is intentional; review the script first, back up the shell profile, and remove the CLAWHUB_REGISTRY and CLAWHUB_SITE lines to revert. <br>
Risk: The security summary notes unrelated cron, repository, learning-archive, and workspace-sync content in the artifact. <br>
Mitigation: Treat the release as scoped to mirror configuration and ignore unrelated operational notes unless those separate actions were explicitly requested. <br>


## Reference(s): <br>
- [ClawHub mirror verification record](references/clawhub-mirror-verification.md) <br>
- [ClawHub skill listing](https://clawhub.ai/roger0808/configure-clawhub-domestic-mirror) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest persistent edits to shell startup files such as ~/.bashrc or ~/.zshrc and optional one-shot registry flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
