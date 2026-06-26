## Description: <br>
Mobile browser and native app automation via ATL (iOS Simulator). Navigate, click, screenshot, and automate web and native app tasks on iPhone/iPad simulators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JordanCoin](https://clawhub.ai/user/JordanCoin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate mobile Safari and native iOS Simulator workflows, including navigation, element discovery, taps, screenshots, and app control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots, PDFs, DOM output, and cookie values from simulator sessions can expose private data. <br>
Mitigation: Use a dedicated simulator, avoid sensitive logged-in accounts unless necessary, and do not share captured outputs from private sessions. <br>
Risk: The install flow clones and builds an unpinned external ATL GitHub project. <br>
Mitigation: Review the referenced project before installation and pin a vetted revision for controlled or repeated deployments. <br>
Risk: Local ATL automation servers can continue accepting commands while running. <br>
Mitigation: Keep the servers local to the development machine and stop them when automation work is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JordanCoin/atl-mobile) <br>
- [Referenced ATL repository for installation](https://github.com/JordanCoin/Atl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with Xcode simulator tooling and local ATL servers on ports 9222 and 9223.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
