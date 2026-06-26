## Description: <br>
CellCog is an any-to-any AI sub-agent for research, multimodal generation, documents, dashboards, 3D models, diagrams, and code through the CellCog cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to offload complex multimodal tasks to CellCog, including analysis, research, file-based workflows, and generation of documents, media, dashboards, or code. It is suited for workflows where the user intentionally shares tagged local files and wants CellCog to return text or downloaded artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses CellCog's cloud service and requires a CellCog API key. <br>
Mitigation: Install only when the user accepts CellCog service use, credential setup, and possible service credit consumption. <br>
Risk: Files wrapped in SHOW_FILE tags are uploaded to CellCog. <br>
Mitigation: Tag only files intended for upload and avoid secrets, private keys, .env files, SSH keys, confidential documents, or other sensitive material. <br>
Risk: Generated files may be downloaded to requested paths or default CellCog locations. <br>
Mitigation: Review requested output paths before use and inspect downloaded artifacts before relying on them. <br>


## Reference(s): <br>
- [CellCog skill page](https://clawhub.ai/nitishgargiitd/cellcog) <br>
- [CellCog homepage](https://cellcog.ai) <br>
- [CellCog Python SDK source](https://github.com/CellCog/cellcog_python) <br>
- [CellCog Python SDK package](https://pypi.org/project/cellcog/) <br>
- [DeepResearch Bench leaderboard](https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead the agent to call CellCog, upload files explicitly wrapped in SHOW_FILE tags, and download generated files to requested or default paths.] <br>

## Skill Version(s): <br>
2.0.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
