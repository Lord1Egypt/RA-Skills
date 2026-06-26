## Description: <br>
CJL Skills Collection is a personal Claude Code plugin with 17 production skills for reading papers, creating content cards, designing presentations, analyzing relationships, improving writing, researching travel, learning vocabulary, investment analysis, and related workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this plugin to invoke specialized personal workflow skills for research, writing, visual content generation, presentations, travel planning, investment analysis, relationship analysis, and media download tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Several workflows automatically save generated notes, visuals, presentations, or media into fixed local folders, which can persist sensitive content. <br>
Mitigation: Review or override save paths before execution and ask the agent not to save sensitive outputs unless the destination is explicitly approved. <br>
Risk: Relationship and investment analysis workflows may process and save sensitive personal, business, or financial material. <br>
Mitigation: Avoid providing confidential inputs unless local file creation is acceptable, and require explicit approval before writing analysis files. <br>
Risk: The X/Twitter download workflow can use Chrome browser cookies for authenticated downloads, exposing local browser-session access to the agent workflow. <br>
Mitigation: Do not allow Chrome cookie access unless authenticated media download is required and the user understands the browser-session exposure. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/0xcjl/cjl-plugin) <br>
- [Publisher profile](https://clawhub.ai/user/0xcjl) <br>
- [CJL Plugin GitHub repository](https://github.com/0xcjl/cjl-plugin) <br>
- [Adapted source skills](https://github.com/lijigang/ljg-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and org-mode reports, generated HTML or presentation assets, PNG/media files, shell commands, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Several skills write generated notes, visuals, presentations, or downloaded media to local folders such as ~/Documents/notes/ or ~/Downloads/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
