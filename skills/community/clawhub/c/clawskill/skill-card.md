## Description: <br>
ClawSkill helps an agent install, verify, run, inspect, and uninstall the RTC/RustChain token miner with wallet setup and consent prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Scottcjn](https://clawhub.ai/user/Scottcjn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agent users and developers use ClawSkill to operate an RTC miner from a CLI-oriented workflow, including installation, wallet configuration, verification, foreground mining, opt-in service mode, status checks, logs, and uninstall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill asks users to install and run token-mining software that repeatedly sends hardware fingerprint data to RustChain. <br>
Mitigation: Install only when token mining is intentional, review the exact PyPI or npm package and linked source first, and monitor CPU, power, and network usage. <br>
Risk: The miner can create background services outside the reviewed skill artifact. <br>
Mitigation: Use foreground mode until trusted, avoid service mode unless persistence is intended, and use the documented uninstall command to remove files, services, and configs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Scottcjn/clawskill) <br>
- [PyPI package](https://pypi.org/project/clawskill/) <br>
- [npm package](https://www.npmjs.com/package/clawskill) <br>
- [RustChain homepage](https://rustchain.org) <br>
- [RustChain block explorer](https://bulbous-bouffant.metalseed.net/explorer) <br>
- [Linked source from artifact](https://github.com/Scottcjn/Rustchain) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command-oriented guidance for installing, verifying, starting, stopping, checking, logging, and uninstalling the miner.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
