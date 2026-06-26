## Description: <br>
Runs a Chinese-language SBTI entertainment personality quiz, asking about 30 questions and matching answers to one of 27 personality result types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxgc](https://clawhub.ai/user/sxgc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for a chat-based Chinese entertainment personality test with a playful host persona, sequential questions, matching logic, and a final SBTI-style result. It is not intended for psychological diagnosis or serious assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quiz uses coarse, self-deprecating, and roast-style humor that may surprise or bother some users. <br>
Mitigation: Frame the quiz as entertainment, let users stop or skip at any time, and avoid treating results as serious psychological assessment. <br>
Risk: Broad boredom, curiosity, or casual-chat triggers may cause the skill to be suggested when the user did not clearly ask for a personality quiz. <br>
Mitigation: Ask for confirmation before beginning the quiz and keep the first message clear about the number of questions and entertainment-only nature. <br>
Risk: Personality and preference answers can feel personal even when the skill does not require sensitive data. <br>
Mitigation: Avoid asking for unnecessary identifying details and remind users not to share sensitive personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sxgc/anti-mbti-sbti) <br>
- [questions-1.json](references/questions-1.json) <br>
- [questions-2.json](references/questions-2.json) <br>
- [questions-special.json](references/questions-special.json) <br>
- [types.json](references/types.json) <br>
- [dimensions.json](references/dimensions.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese conversational text or Markdown with quiz questions, selected answers, a personality code and name, similarity score, and optional dimension analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill keeps answers within the active conversation and reminds users that results are for entertainment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
