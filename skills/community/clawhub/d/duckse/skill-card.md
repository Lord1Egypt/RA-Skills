## Description: <br>
Duckse helps agents run DDGS-based web, news, image, video, and book searches through the duckse CLI with pretty text or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwirx](https://clawhub.ai/user/dwirx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and external users use Duckse to run web, news, image, video, and book searches through the duckse CLI, including current-event lookup, quick research, and fact-checking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends installing duckse through a remote GitHub script piped directly into bash. <br>
Mitigation: Review the upstream install script or use a pinned, vetted release before installation, and do not allow an agent to run the curl-to-bash installer automatically. <br>


## Reference(s): <br>
- [Duckse ClawHub page](https://clawhub.ai/dwirx/duckse) <br>
- [Duckse installer referenced by the skill](https://raw.githubusercontent.com/dwirx/duckse/main/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; duckse command output may be pretty text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports search type, result limit, time filter, region, safe search, backend selection, JSON output, URL expansion, proxy, timeout, and verification options.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
