## Description: <br>
Operate, automate, and troubleshoot Brave Browser with profiles, Shields, extensions, and Chromium debugging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to run Brave-specific browser workflows, isolate profile and Shields issues, handle extensions, and apply Chromium-compatible automation only after the target browser surface is clear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote debugging can expose browser control or sensitive session state if left enabled. <br>
Mitigation: Enable remote debugging only for a specific approved task, prefer a disposable or automation profile, and turn it off when the task is complete. <br>
Risk: Profile cleanup, cookie clearing, Sync changes, wallet changes, or extension permission changes can affect sensitive user state. <br>
Mitigation: Confirm the target profile and get explicit approval before touching browser state, wallet-adjacent settings, Sync, or extension permissions. <br>
Risk: Global Shields relaxations can weaken privacy defaults beyond the affected site. <br>
Mitigation: Use per-site Shields changes first, verify the result in Brave, and record only durable site-specific fixes. <br>
Risk: Saving browser notes could accidentally capture secrets or detailed browsing history. <br>
Mitigation: Keep only durable operating preferences and safety boundaries under ~/brave/ after user consent, and do not store passwords, secrets, or full browsing history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/brave) <br>
- [Brave Skill Homepage](https://clawic.com/skills/brave) <br>
- [setup.md](artifact/setup.md) <br>
- [launch-and-profiles.md](artifact/launch-and-profiles.md) <br>
- [shields-and-compatibility.md](artifact/shields-and-compatibility.md) <br>
- [automation-and-debugging.md](artifact/automation-and-debugging.md) <br>
- [extensions-and-wallet.md](artifact/extensions-and-wallet.md) <br>
- [troubleshooting.md](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no undeclared remote APIs or credentials are used by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
