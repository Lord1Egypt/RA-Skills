## Description: <br>
Configures and diagnoses development-tool mirror settings for China's network environment across Python, Node, Docker, APT, Rust, Go, Conda, Flutter, Homebrew, and GitHub workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loredunk](https://clawhub.ai/user/loredunk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers working in China use this skill to diagnose slow package downloads and apply mirror configurations for common development tools, with dry-run, backup, and restore workflows available before persistent changes are made. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Persistent mirror and package-source changes can alter package resolution for multiple development tools. <br>
Mitigation: Run the scripts with --dry-run first, avoid --yes until reviewed, and use the bundled backup and restore scripts for affected tool configurations. <br>
Risk: Global Git URL rewrite settings can redirect future GitHub clone and fetch operations. <br>
Mitigation: Review the exact git config --global url.*.insteadOf entries before applying them and remove unwanted entries with git config --global --unset-all. <br>
Risk: The Homebrew setup path can execute the live upstream installer. <br>
Mitigation: Do not run the Homebrew setup path unless the user explicitly accepts executing the upstream installer. <br>
Risk: Diagnostic logs may expose proxy values or network configuration details. <br>
Mitigation: Redact proxy values and sensitive environment details before sharing diagnostic output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loredunk/china-mirror-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can lead to persistent local configuration changes and diagnostic logs when the bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
