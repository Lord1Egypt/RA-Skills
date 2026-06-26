## Description: <br>
Generate dark-themed animated trend charts and static overview images from time-series JSON data with customizable titles and frame rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ravenquasar](https://clawhub.ai/user/ravenquasar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and presentation authors use this skill to turn time-series JSON data into animated trend charts, optional MP4 video, and a static overview image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The chart generator creates or overwrites files in the selected output directory. <br>
Mitigation: Review the input JSON and choose an output directory that does not contain files you need to preserve. <br>
Risk: Installing or running the tool depends on local Python packages and optional ffmpeg support. <br>
Mitigation: Install dependencies only from trusted package sources and treat MP4 output as optional when ffmpeg is unavailable. <br>


## Reference(s): <br>
- [Chart Animation Skill Page](https://clawhub.ai/ravenquasar/chart-animation) <br>
- [Publisher Profile](https://clawhub.ai/user/ravenquasar) <br>
- [Usage and Data Format](artifact/SKILL.md) <br>
- [Examples](artifact/examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance plus generated GIF, PNG, and optional MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-provided JSON file and writes chart outputs to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
