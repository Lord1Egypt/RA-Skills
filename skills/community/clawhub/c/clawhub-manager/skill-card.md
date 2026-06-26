## Description: <br>
Clawhub Manager helps agents manage ClawHub skills by publishing, deleting, inspecting, searching, and listing skills through the ClawHub CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to manage ClawHub releases, inspect skill statistics, search the ClawHub catalog, and list locally installed skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish and delete ClawHub skills using the active CLI login. <br>
Mitigation: Verify the logged-in ClawHub account, target skill directory, slug, and version before running publish or delete commands. <br>
Risk: The publish workflow includes a --skip-security option that bypasses the built-in scan. <br>
Mitigation: Do not use --skip-security for real releases; run the included security check before publishing. <br>
Risk: test-security-scan.sh can unexpectedly reach the real publish flow. <br>
Mitigation: Avoid running the test script unless live publish side effects are acceptable or the CLI is isolated to a test account. <br>


## Reference(s): <br>
- [Clawhub Manager on ClawHub](https://clawhub.ai/franklu0819-lang/clawhub-manager) <br>
- [README.md](artifact/README.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>
- [SECURITY.md](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawhub CLI; jq is used for JSON-formatted inspection output.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
