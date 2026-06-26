## Description: <br>
EasyEDA API Skill helps AI agents work with EasyEDA Pro projects by providing API references, extension-development guidance, document format documentation, and a local bridge for executing code in a connected EasyEDA client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanranxiaoxi](https://clawhub.ai/user/yanranxiaoxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and electronics engineers use this skill to inspect EasyEDA APIs, write or debug EasyEDA extensions, and automate PCB, schematic, library, and project workflows through an EasyEDA Pro client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a local bridge that runs arbitrary code inside the user's active EasyEDA session. <br>
Mitigation: Install only when intentional, keep projects backed up, stop the bridge when finished, and require review and approval before executing code that modifies designs or files. <br>
Risk: Automation may target the wrong connected EasyEDA window. <br>
Mitigation: Verify the selected EasyEDA window before running code and explicitly select the intended window when multiple clients are connected. <br>


## Reference(s): <br>
- [ClawHub EasyEDA API Skill](https://clawhub.ai/yanranxiaoxi/easyeda-api) <br>
- [EasyEDA Run API Gateway Extension](https://ext.lceda.cn/item/oshwhub/run-api-gateway) <br>
- [API Reference Index](references/_index.md) <br>
- [API Quick Reference](references/_quick-reference.md) <br>
- [Document Source Format Reference](format/index.md) <br>
- [Extension Development Guide](guide/how-to-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include code intended for execution through a local EasyEDA bridge after user review and approval.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata, skill metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
