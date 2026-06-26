## Description: <br>
Applies a Chinese ruler-subject reply style, addressing the user as "陛下" and the assistant as "臣" when the user explicitly requests that mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Millihous](https://clawhub.ai/user/Millihous) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to have an assistant answer in a concise Chinese court-minister style when the conversation explicitly asks for ruler-subject roleplay. It preserves normal safety and exact-format requirements while allowing the user to exit the style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The roleplay style may be applied when the user's intent is ambiguous. <br>
Mitigation: Use only the explicit trigger cues and ask a brief clarification when "用皇帝语气" could mean either minister-style replies or drafting text in an emperor's voice. <br>
Risk: Ceremonial wording could interfere with strict output formats. <br>
Mitigation: Follow the strict-format exception for JSON, code, SQL, CSV, regex, translation-only output, titles, and one-line rewrites. <br>
Risk: The style may persist after the user wants normal assistant behavior. <br>
Mitigation: Exit immediately when the user asks to speak normally, stop the mode, or stop being addressed as "陛下". <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Millihous/emperor-reply) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Millihous) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese conversational text, or the exact requested structured format when strict output is required.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, data access, persistence, or hidden install behavior was found in the security evidence.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
