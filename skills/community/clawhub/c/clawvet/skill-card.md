## Description: <br>
Code quality and safety linter for OpenClaw skills. Runs 6 analysis passes before you install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MohibShaikh](https://clawhub.ai/user/MohibShaikh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use Clawvet to scan OpenClaw skill files for prompt injection, credential theft, remote code execution, typosquatting, and supply-chain risks before installation or CI release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads local skill files and can audit installed OpenClaw skill directories. <br>
Mitigation: Run it only on skill directories you intend to inspect, and avoid pointing it at unrelated workspaces or sensitive local files. <br>
Risk: Optional telemetry, remote fetching, and cloud semantic analysis may disclose scan context or metadata outside the local machine. <br>
Mitigation: Review configuration before use, keep cloud analysis opt-in for sensitive skills, and disclose telemetry/provider behavior to users. <br>
Risk: The bundled API/dashboard includes auth, scan history, cloud analysis, telemetry, and webhook behavior that may be unsafe for shared deployment without review. <br>
Mitigation: Do not expose the API/dashboard publicly until auth, JWT settings, scan ownership checks, webhook URL restrictions, and telemetry/provider disclosures are tightened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MohibShaikh/clawvet) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/MohibShaikh) <br>
- [npm package](https://www.npmjs.com/package/clawvet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, JSON, SARIF, Markdown snippets, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm. The CLI can audit local skill directories, fetch remote skills, and optionally use telemetry or cloud semantic analysis when configured.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
