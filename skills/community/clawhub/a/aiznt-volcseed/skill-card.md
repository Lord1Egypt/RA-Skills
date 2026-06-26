## Description: <br>
Volcseed submits prompt-based image-editing jobs with reference image URLs to configured Tianshu/Volcseed proxy endpoints and fetches task results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image workflow users use this skill to submit prompt-based image edits with reference image URLs and poll Volcseed task results through configured Tianshu credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured proxy endpoints receive prompts and referenced image URLs. <br>
Mitigation: Use only trusted Tianshu/Volcseed proxy endpoints and submit private image URLs or sensitive prompts only when that transfer is intended. <br>
Risk: Credentials in TS_TOKEN and AIZNT_PROXY_URLS can authorize user-run submit and fetch commands. <br>
Mitigation: Treat both values as secrets and avoid sharing logs, examples, or shell history that expose them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangshengli0421/aiznt-volcseed) <br>
- [Publisher Profile](https://clawhub.ai/user/wangshengli0421) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Text guidance and shell commands that return JSON task data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TS_TOKEN and AIZNT_PROXY_URLS environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
