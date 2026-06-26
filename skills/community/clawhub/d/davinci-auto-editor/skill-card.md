## Description: <br>
Scan local media, request a cloud editing plan, and generate a Resolve-importable EDL package with pure Node. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-automation operators use this skill to scan a local media folder, request a cloud-generated edit plan, and produce DaVinci Resolve import files for manual review and import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans local media folders and may send file metadata, paths, sizes, timestamps, summaries, and execution reports to a configured cloud API. <br>
Mitigation: Use it only with media folders approved for provider exposure, review the configured API endpoint before running, and avoid including sensitive filenames or paths. <br>
Risk: The API key is required for cloud task access and could be exposed if committed in configuration files. <br>
Mitigation: Store the API key in a private secrets location or local-only config file and do not commit real credentials. <br>
Risk: The security verdict is suspicious due to insufficient consent and privacy controls around cloud metadata sharing. <br>
Mitigation: Review the skill before installing and run it only after confirming the cloud provider, data handling expectations, and user consent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/afengzi/davinci-auto-editor) <br>
- [Metadata Homepage](https://github.com/imfengziaaa/video-auto-editor-skills) <br>
- [README](artifact/README.md) <br>
- [Example Configuration](artifact/examples/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to run a Node entrypoint that writes resolve-import.json, timeline.edl, IMPORT-TO-RESOLVE.txt, and execution-report.json.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence, manifest.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
