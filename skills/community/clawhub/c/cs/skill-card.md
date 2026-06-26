## Description: <br>
Automatically extracts key points from long Chinese or English text using summarize-related keyword triggers or a length trigger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1466561686](https://clawhub.ai/user/1466561686) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub users and agents use this skill to produce concise summaries of long messages, emails, meeting notes, articles, and chat discussions. It supports Chinese and English inputs and can trigger from summarize-related keywords or plain text over 100 characters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages over 100 characters can trigger summarization without an explicit summarize request, sending message content to the configured LLM provider. <br>
Mitigation: Install only when automatic summarization is desired, avoid sending sensitive long messages through the skill, or adjust the length trigger before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1466561686/cs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Concise bullet-point summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mirrors the input language when possible; artifact requests stable, concise output with a 1000-token response cap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
