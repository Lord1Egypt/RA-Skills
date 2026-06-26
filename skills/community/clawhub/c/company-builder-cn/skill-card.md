## Description: <br>
帮助中文用户通过对话规划并创建 OpenClaw 智能体虚拟公司，包括公司目标、组织架构、岗位、员工和相关工作区文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hkagi](https://clawhub.ai/user/hkagi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking OpenClaw users use this skill to design a multi-agent company and generate the files and configuration needed for departments, roles, employees, and ongoing team administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad OpenClaw administration behavior may change workspace files, assistant behavior, skill assignments, and local configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json and the workspace before use, then review generated AGENTS.md, TOOLS.md, HEARTBEAT.md, and configuration changes before restarting OpenClaw. <br>
Risk: Optional account, communication, git, or skill-management actions could exceed a simple company setup workflow. <br>
Mitigation: Enable email, calendar, social, git push, Telegram account changes, or skill distribution and deletion only when explicitly needed and after reviewing each requested change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hkagi/company-builder-cn) <br>
- [Publisher profile](https://clawhub.ai/user/hkagi) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown files with OpenClaw configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update OpenClaw workspace files, agent files, skill assignments, and local configuration after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
