## Description: <br>
Automates video uploads and optional publishing to Kuaishou, Bilibili, and Douyin through a logged-in Chrome browser using TXT-based video metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohei2022](https://clawhub.ai/user/xiaohei2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and developers use this skill to prepare, preview, and publish short-form videos across Kuaishou, Bilibili, and Douyin from a single text configuration file. It is most useful when the user already has valid platform accounts, local video assets, and an authenticated Chrome profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish real videos from logged-in accounts. <br>
Mitigation: Run with --no-publish first, verify each platform form in the browser, and avoid publish-all until every target flow has been checked. <br>
Risk: The skill controls a logged-in Chrome browser through a local debugging port. <br>
Mitigation: Use a dedicated Chrome profile, keep the debugging port bound to localhost, and close the browser session when publishing is complete. <br>
Risk: The release includes under-disclosed stealth browser automation. <br>
Mitigation: Confirm that this behavior is acceptable for the target platforms and organization before deployment. <br>
Risk: Debug HTML snapshots or browser artifacts may contain account or draft content. <br>
Mitigation: Delete debug snapshots after troubleshooting and avoid storing them in shared locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaohei2022/app-publish) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Test report](artifact/TEST_REPORT.md) <br>
- [Kuaishou flow test report](artifact/TEST_REPORT_2026-04-03.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may control a local Chrome browser over the Chrome DevTools Protocol and can publish content unless run with --no-publish.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
