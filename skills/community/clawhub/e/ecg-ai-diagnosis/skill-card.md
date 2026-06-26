## Description: <br>
Analyzes single-lead and 12-lead ECG JSON files by sending user-selected ECG data to the heartvoice cloud API and returning bilingual structured analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujiecharles](https://clawhub.ai/user/yujiecharles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze user-provided ECG JSON files, choose single-lead or 12-lead analysis, call heartvoice cloud endpoints, and summarize diagnostic signals in Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ECG and health data are sent to Heartvoice's external cloud service for analysis. <br>
Mitigation: Use the skill only with explicit user or patient awareness and review Heartvoice privacy and retention terms before sending real medical data. <br>
Risk: API credentials could be exposed if stored in code or shared logs. <br>
Mitigation: Keep HEARTVOICE_API_KEY in an environment variable or local secret store and avoid hardcoding it in scripts, prompts, or committed files. <br>
Risk: AI-assisted ECG analysis can be incomplete or misleading if treated as a clinical diagnosis. <br>
Mitigation: Present results as decision support and require qualified medical review for diagnosis or treatment decisions. <br>


## Reference(s): <br>
- [ECG-AI-Diagnosis on ClawHub](https://clawhub.ai/yujiecharles/ecg-ai-diagnosis) <br>
- [heartvoice AI ECG Cloud](https://www.heartvoice.com.cn/aiCloud) <br>
- [heartvoice single-lead ECG API endpoint](https://api.heartvoice.com.cn/api/v1/basic/ecg/1-lead/analyze) <br>
- [heartvoice 12-lead ECG API endpoint](https://api.heartvoice.com.cn/api/v1/basic/ecg/12-lead/analyze) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HEARTVOICE_API_KEY and a user-provided ECG JSON file; supports Chinese and English output.] <br>

## Skill Version(s): <br>
0.9.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
