## Description: <br>
JMCAI Comfypet lets an agent query and run configured ComfyUI image, video, audio, and file workflows through the JMCAI Comfypet desktop application. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allen-jmc](https://clawhub.ai/user/allen-jmc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to select an exposed JMCAI Comfypet workflow, provide only its published alias parameters, submit generation jobs, and retrieve local output paths for generated media or files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote bridge mode can copy local workflow input assets to another machine. <br>
Mitigation: Keep bridge_url on localhost for sensitive work, use only trusted remote bridge endpoints, and avoid passing confidential media or documents. <br>
Risk: Downloaded workflow outputs may come from remote bridge URLs and should not be assumed trustworthy. <br>
Mitigation: Treat downloaded outputs as untrusted files and inspect them before opening or sharing. <br>
Risk: File inputs can include media, subtitles, text, CSV, TSV, and PDF assets when exposed by a workflow schema. <br>
Mitigation: Use only alias parameters returned by registry --agent and pass the minimum necessary files for the selected workflow. <br>


## Reference(s): <br>
- [Workflow Bridge reference](references/bridge.md) <br>
- [Image, video, and asset workflow usage](references/usage.md) <br>
- [JMCAI Comfypet skill pack homepage](https://github.com/allen-Jmc/comfypet-jmcai-skill-pack) <br>
- [JMCAI Comfypet desktop application](https://github.com/allen-Jmc/comfypet-jmcai-Dist) <br>
- [ClawHub skill listing](https://clawhub.ai/allen-jmc/comfypet-jmcai-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns workflow status and output file paths; remote bridge outputs may be downloaded to the current machine before paths are reported.] <br>

## Skill Version(s): <br>
1.2.5 (source: release evidence and script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
