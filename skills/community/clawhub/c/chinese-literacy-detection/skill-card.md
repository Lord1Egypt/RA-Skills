## Description: <br>
Provides a Chinese-language conversational assessment for estimating Chinese character recognition in children ages 3-12 using stratified sampling, early stopping, and positive follow-up guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwang4git](https://clawhub.ai/user/wangwang4git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, including parents, caregivers, and education assistants, use this skill to run an in-chat Chinese character recognition assessment, review missed characters, and understand age-based literacy references. The skill is intended for guidance and learning support, not clinical or formal educational placement decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill displays a QR code for an optional external WeChat mini-program. <br>
Mitigation: Continue in chat unless the QR-code destination and publisher are trusted. <br>
Risk: The assessment asks for a child's age and recognition responses. <br>
Mitigation: Avoid entering sensitive child, account, or identifying information into the chat or any external mini-program. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangwang4git/chinese-literacy-detection) <br>
- [Usage guide](artifact/USAGE.md) <br>
- [Algorithm specification](artifact/references/algorithm-spec.md) <br>
- [Data schema](artifact/references/data-schema.md) <br>
- [Chatbot workflow](artifact/references/chatbot-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown conversation with tables, status summaries, assessment reports, and review prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language interaction; may ask for a child's age and test responses; includes an optional QR-code prompt for a WeChat mini-program.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
