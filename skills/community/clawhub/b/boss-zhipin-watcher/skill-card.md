## Description: <br>
BOSS Zhipin desktop automation skill that detects BOSS windows, captures screenshots, reads page content with OCR or vision workflows, and can run broader recruiting actions such as greeting candidates, processing chats, and collecting resumes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxj20060702-del](https://clawhub.ai/user/lxj20060702-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters or operators use this skill to inspect BOSS Zhipin desktop windows, capture chat and candidate information, and coordinate repetitive recruiting workflows. It is also able to execute active desktop actions, so use should be supervised in environments where candidate messaging or resume handling is sensitive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill goes beyond screenshot watching and can actively click, message candidates, collect resumes, run workflow commands, and store recruiting data. <br>
Mitigation: Install only when active BOSS desktop automation is intended, keep a human supervisor in the loop, and remove or disable bulk greeting, messaging, resume, offer, shell workflow, and persistent storage steps that are not needed. <br>
Risk: Recruiting workflows may expose candidate chats, resumes, personal information, and workplace communication details through screenshots or saved metadata. <br>
Mitigation: Limit output directories and retained captures to approved locations, review generated files before sharing, and follow the organization's candidate-data handling rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxj20060702-del/boss-zhipin-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/lxj20060702-del) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with executable command examples and generated screenshot or metadata files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots, JSON metadata, workflow state, and recruitment records to local files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
