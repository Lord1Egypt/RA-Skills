## Description: <br>
AI UGC video production from the terminal using the `agent-media` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nevo-david](https://clawhub.ai/user/nevo-david) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and content teams use this skill to draft scripts and construct `agent-media` CLI commands for UGC videos, SaaS review videos, subtitles, personas, and generated media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commands may upload product screenshots, URLs, local files, face photos, voice samples, or videos to external services. <br>
Mitigation: Use only media approved for upload, review commands before execution, and verify the npm package and GitHub project before installing the CLI. <br>
Risk: Generated media jobs may use the authenticated account and consume paid credits. <br>
Mitigation: Authenticate only with the intended account and check available credits before running generation commands. <br>


## Reference(s): <br>
- [Agent Media ClawHub listing](https://clawhub.ai/nevo-david/agent-media) <br>
- [agent-media CLI GitHub project](https://github.com/gitroomhq/agent-media) <br>
- [agent-media-cli npm package](https://www.npmjs.com/package/agent-media-cli) <br>
- [Agent Media official website](https://agent-media.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, CLI flags, checklists, and short scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill itself provides guidance and command text; running those commands may produce external media URLs or downloaded media files through the agent-media CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
