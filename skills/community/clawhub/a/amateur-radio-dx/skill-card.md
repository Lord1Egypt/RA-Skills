## Description: <br>
Monitor DX clusters for rare station spots, track active DX expeditions, and get daily band activity digests for amateur radio operators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External amateur radio operators use this skill to monitor public DX cluster spots, identify rare or workable stations, generate band activity digests, and configure local alerts for new DX activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor connects to public DX cluster servers and may use a real callsign. <br>
Mitigation: Install only if public cluster connectivity is acceptable, and choose callsign/configuration values deliberately. <br>
Risk: Station and QTH details can be stored locally when AI-enhanced setup is used. <br>
Mitigation: Review dx-ai-config.json before use and avoid storing station details that should not be kept locally. <br>
Risk: Automated monitoring examples use cron-style recurring execution. <br>
Mitigation: Review any cron job before adding it and run the monitor as a normal, non-root user. <br>
Risk: Monitor state is written to /tmp/dx-monitor-state.json. <br>
Mitigation: Treat the state file as local runtime data and clean it up when disabling monitoring. <br>


## Reference(s): <br>
- [NG3K Amateur Radio Contest/DX Page](https://www.ng3k.com/misc/adxo.html) <br>
- [DX-World](https://www.dx-world.net/) <br>
- [425 DX News](http://www.425dxn.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown digest sections, JSON when requested, and shell command/configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally produce JSON spot records from the watch command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
