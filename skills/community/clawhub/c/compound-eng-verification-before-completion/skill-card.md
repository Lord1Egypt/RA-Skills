## Description: <br>
Enforces fresh verification evidence before any completion claim, including tests passing, bugs fixed, work done, merge readiness, or handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to avoid unverified completion claims and to report work status only after fresh build, lint, test, scan, diff, or manual verification evidence is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification may involve shell commands such as tests, builds, lint, scans, git status, or similar checks. <br>
Mitigation: Review commands before execution and keep state-changing actions such as commits, stashes, and --no-verify use explicitly user-directed. <br>
Risk: The skill can make agents more conservative about claiming completion when verification is missing or failing. <br>
Mitigation: Report the exact verification result and limit completion claims to evidence that was freshly observed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iliaal/compound-eng-verification-before-completion) <br>
- [System-Wide Test Check](references/system-wide-test-check.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and completion report structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts agents to run fresh verification checks and report actual evidence before claiming completion.] <br>

## Skill Version(s): <br>
4.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
