## Description: <br>
Aistore helps an agent search, install, list, and remove AI STORE skills and guide AI STORE model setup through the gpushop CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangnan8791](https://clawhub.ai/user/wangnan8791) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to discover AI STORE marketplace skills, manage installed skills with gpushop, and guide AI STORE model access setup when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct global npm installation, skill installation or removal, authentication setup, and web access with limited user control. <br>
Mitigation: Require explicit confirmation before each global npm install, skill install or uninstall, SSO/auth step, and web access. <br>
Risk: Newly installed skills may alter future agent behavior before the user has reviewed them. <br>
Mitigation: Inspect newly installed skill files and security scan results before allowing those skills to guide future work. <br>


## Reference(s): <br>
- [Aistore on ClawHub](https://clawhub.ai/wangnan8791/aistore) <br>
- [AI STORE Model Service](https://gpushop.sh.189.cn/ModelService/onlineApi) <br>
- [AI STORE Model API Documentation](https://gpushop.sh.189.cn/doc/guide/model-service/API-ref3.html) <br>
- [Xiao Zhuren Platform](https://dx.mltai.cn/app-web/passport/login) <br>
- [Xiao Lawyer Platform](https://dx.jurisai.cn/#/login?redirect=/index) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose package installation, skill lifecycle commands, authentication setup steps, and web access that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
