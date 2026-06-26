## Description: <br>
Diagnose and mitigate exec-related tooling failures around ClawHub publishing and GitHub CLI queries, including authentication, browser login, missing dependencies, pending scan visibility, URL mismatches, and GitHub CLI JSON field errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlueBirdBack](https://clawhub.ai/user/BlueBirdBack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose failed ClawHub skill publishing workflows, prepare safer publish commands, handle headless authentication, and work around GitHub CLI repository search field mismatches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publish wrapper can publish using the currently logged-in ClawHub account. <br>
Mitigation: Confirm the ClawHub account, skill path, slug, version, and changelog before running publish commands. <br>
Risk: Diagnostic whoami output can be written to predictable temporary files. <br>
Mitigation: Avoid shared machines for publishing diagnostics or remove temporary diagnostic files after use. <br>
Risk: Installing or invoking local CLI tools from untrusted sources can affect the publishing environment. <br>
Mitigation: Install clawhub and gh only from trusted sources and verify the active binaries before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BlueBirdBack/exec-clawhub-publish-doctor) <br>
- [ClawHub Publish Error Map](references/error-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and script paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include retry-aware publishing steps, dependency checks, authentication guidance, and GitHub CLI fallback commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
