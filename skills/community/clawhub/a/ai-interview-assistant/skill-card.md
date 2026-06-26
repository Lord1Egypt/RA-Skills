## Description: <br>
AI 模拟面试助手通过简历画像、可选岗位匹配、五题技术面试循环、实时评分和总结报告来模拟技术面试评估。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paradise123-bot](https://clawhub.ai/user/paradise123-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, job candidates, and interview-preparation users use this skill to practice technical interviews, receive keyword-and-logic scoring, and get a structured summary report. It can optionally compare a user's technical profile against a job description before the interview loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may keep a local interview profile containing a name or anonymous label, technical tags, scores, and feedback. <br>
Mitigation: Use anonymous mode when a name is not needed, review profile-storage retention before installation, and delete stored profiles when retention is not desired. <br>
Risk: Question material may be pulled from a public GitHub repository and web-backed question sources. <br>
Mitigation: Use the skill in a sandboxed or low-sensitivity environment when external content control is required, and review fetched question material before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paradise123-bot/ai-interview-assistant) <br>
- [wdndev/llm_interview_note knowledge base](https://github.com/wdndev/llm_interview_note) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-style interview prompts, scoring feedback, and summary reports; JSON output from helper scripts when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a five-question interview flow, optional job-description matching, per-answer scoring, and local profile feedback updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
