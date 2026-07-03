## Description: <br>
Helps agents manage Volcengine CDN domains through the Volcengine CLI, including adding domains and submitting cache refresh or preload tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare and run Volcengine CDN domain creation, cache refresh, and content preload workflows with guided parameters and recommended CDN settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Volcengine CLI credentials that are authorized to manage CDN resources. <br>
Mitigation: Use least-privilege AK/SK credentials and avoid pasting real secrets into prompts, commands, examples, or shared logs. <br>
Risk: Generated add-domain, refresh, and preload commands can affect live CDN configuration and content delivery. <br>
Mitigation: Review every domain, origin, service region, refresh URL, and preload URL before execution, and treat scripts as production-affecting operations rather than dry runs. <br>
Risk: The artifact includes CLI installation and upgrade guidance that downloads and installs the Volcengine CLI. <br>
Mitigation: Install the CLI from the official Volcengine source, verify the CLI version is at least 1.0.39, and confirm credentials are configured for the intended account and region. <br>


## Reference(s): <br>
- [Parameter Reference](references/parameters.md) <br>
- [Usage Examples](references/examples.md) <br>
- [CLI Installation Guide](references/install-guide.md) <br>
- [FAQ](references/faq.md) <br>
- [Volcengine CLI](https://github.com/volcengine/volcengine-cli) <br>
- [Volcengine CDN AddCdnDomain API](https://www.volcengine.com/docs/6454/97340) <br>
- [Volcengine CDN SubmitRefreshTask API](https://www.volcengine.com/docs/6454/97345) <br>
- [Volcengine CDN SubmitPreloadTask API](https://www.volcengine.com/docs/6454/97346) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce executable Volcengine CLI commands for live CDN resource changes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
