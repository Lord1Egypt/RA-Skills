## Description: <br>
Analyzes local or remote images with ByteDance Doubao vision models and writes results to an output file for agent consumption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maoyutofu](https://clawhub.ai/user/maoyutofu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to run Doubao vision analysis on local or remote images. Agents should write the result to a unique temporary output file and read that file after the command completes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls an external Doubao API and requires an API key. <br>
Mitigation: Use a dedicated API key and avoid sensitive or regulated images unless the provider handling is acceptable. <br>
Risk: Installation relies on a third-party GitHub Release binary. <br>
Mitigation: Install only if the publisher and release artifact are trusted, and verify release checksums or signatures when available. <br>
Risk: Inference results are written to temporary files that may be overwritten or left behind. <br>
Mitigation: Use unique private output paths per run and delete result files after the agent reads them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/maoyutofu/doubao-seed-skill) <br>
- [Doubao Seed Skill GitHub releases](https://github.com/maoyutofu/doubao-seed-skill/releases/latest) <br>
- [Doubao Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Text written to a file, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ARK_API_KEY value and strongly recommends a unique temporary output file for each run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
