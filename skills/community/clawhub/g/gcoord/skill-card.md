## Description: <br>
Use when converting coordinates between WGS84, GCJ02, BD09, BD09MC, or WebMercator coordinate systems for Chinese map services such as Baidu, Amap, Google China, and Tencent Maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhyt1985](https://clawhub.ai/user/zhyt1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and mapping workflows use this skill to convert individual coordinates, coordinate arrays, GeoJSON, or batch coordinate text among Chinese map coordinate systems. It helps normalize coordinates when moving data between GPS, Baidu, Amap, Tencent, and Web Mercator map contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private location coordinates entered for conversion may be visible to the local agent session processing them. <br>
Mitigation: Avoid submitting sensitive locations unless the local workspace, logs, and agent session are appropriate for that data. <br>
Risk: The skill relies on an external Node dependency for coordinate conversion. <br>
Mitigation: Install dependencies from a trusted registry or the provided lockfile, and review dependency integrity before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhyt1985/gcoord) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhyt1985) <br>
- [README.md](README.md) <br>
- [gcoord 1.0.7 package tarball](https://registry.npmmirror.com/gcoord/-/gcoord-1.0.7.tgz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and coordinate conversion text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates are returned in the same general shape as the input when using the bundled conversion script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
