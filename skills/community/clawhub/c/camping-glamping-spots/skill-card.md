## Description: <br>
Find camping grounds and glamping sites, from wild tent pitches to luxury safari tents with beds, electricity, and mountain views, using FlyAI/Fliggy travel data and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for camping and glamping options by city, compare real-time FlyAI/Fliggy results, and present booking links in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install an unpinned global FlyAI CLI package. <br>
Mitigation: Install and verify the FlyAI CLI from a trusted source yourself before using the skill, and avoid allowing unattended global package installation. <br>
Risk: The artifact behavior may persist raw travel searches in a local .flyai-execution-log.json file. <br>
Mitigation: Check for that file after use and remove or disable local query logging when travel searches should not be retained. <br>
Risk: The security review verdict is suspicious for this release. <br>
Mitigation: Review the skill instructions and security guidance before installation, especially its CLI installation and local logging behavior. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/camping-glamping-spots) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel results with comparison tables, booking links, and occasional shell commands for FlyAI CLI setup or checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a working FlyAI CLI for real-time results; every listed result should include a booking link from the CLI output.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
