## Description: <br>
Automates Feishu integration troubleshooting and setup by diagnosing authentication, messaging, event, API, permission, and error-recovery issues and generating implementation guidance or code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhi8145](https://clawhub.ai/user/wangzhi8145) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to configure, debug, and generate Feishu Open Platform integrations for bots, documents, events, files, permissions, and API workflows. It can produce code, setup steps, diagnostics, fallback guidance, and references for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the skill requests sensitive Feishu authority and can generate credential-bearing code without enough user control or scoping. <br>
Mitigation: Review generated code before use, use a dedicated low-privilege Feishu test app, avoid tenant-wide or admin-wide scopes, and do not provide production tokens unless necessary. <br>
Risk: Generated solution files or configuration examples may contain app secrets, tokens, webhook secrets, or other Feishu credentials. <br>
Mitigation: Inspect files created under solutions and examples before committing, running, or sharing them, and remove or rotate any embedded secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangzhi8145/feishuskills) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL](artifact/SKILL.md) <br>
- [Feishu Open Platform documentation](https://open.feishu.cn/document/home/index) <br>
- [Feishu server-side SDK overview](https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/server-side-sdk/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like reports, configuration examples, and generated source code snippets or files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create implementation files under a solutions directory and may include Feishu credential placeholders or user-provided app credentials in generated code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
