## Description: <br>
Clawscan Vigil scans OpenClaw skills before installation with static and dynamic checks to identify security risks and suspicious code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjj09090](https://clawhub.ai/user/jjj09090) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan local or installed OpenClaw skills before adoption and to produce risk reports for manual review or CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dynamic scanning may execute scanned skill code inside the scanner process with weak containment. <br>
Mitigation: Prefer running scans with --no-dynamic for untrusted targets, or run the scanner in a disposable sandboxed environment. <br>
Risk: The skill may create or use local quota and license files under ~/.clawscan. <br>
Mitigation: Review local state created by the tool and avoid using sensitive profiles or shared environments for evaluation scans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jjj09090/clawscan-vigil) <br>
- [Project homepage](https://github.com/clawscan/clawscan-vigil) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [CLI text reports with optional JSON scan results and Markdown-oriented guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate low, medium, high, or scan-error outcomes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release, frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
