## Description: <br>
ccdb helps agents query Carbonstop CCDB carbon emission factor data through the pinned carbonstop-ccdb CLI for keyword search, structured JSON retrieval, and multi-keyword comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijihua2017](https://clawhub.ai/user/lijihua2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and sustainability analysts use this skill to find carbon emission factors by keyword, region, or year, then compare factors or use structured results in carbon calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a pinned npm CLI and queries an external CCDB API. <br>
Mitigation: Run the CLI in a sandbox where possible and verify the npm package version or registry hash before use. <br>
Risk: Emission factors can be incorrect for a calculation if the wrong region, year, unit, or source is selected. <br>
Mitigation: Confirm the intended region, year, unit, and source before using any returned factor in carbon accounting or compliance workflows. <br>
Risk: Formatted CLI output may be less reliable for arithmetic than structured records. <br>
Mitigation: Use JSON output for calculations and inspect units before multiplying by activity data. <br>


## Reference(s): <br>
- [ClawHub ccdb skill page](https://clawhub.ai/lijihua2017/ccdb) <br>
- [carbonstop-ccdb npm package](https://www.npmjs.com/package/carbonstop-ccdb) <br>
- [Carbonstop CCDB CLI source](https://github.com/carbonstop/skills/tree/main/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs pinned npx carbonstop-ccdb@1.0.1; requires Node.js 18 or newer and external CCDB API access.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
