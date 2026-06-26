## Description: <br>
Prevents AI from fabricating facts by forcing source-based responses and uncertainty statements when records are missing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiping3](https://clawhub.ai/user/yiping3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, teams, and developers use this skill to make AI assistants check available records before making factual claims, especially in client communication, customer support, research, investment analysis, and content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make an assistant more cautious, leading to more refusals or uncertainty statements when records are missing. <br>
Mitigation: Review strict mode, trigger phrase behavior, and expected source availability before deployment. <br>
Risk: Optional deep-check behavior may cause the assistant to search files or the web more often than intended. <br>
Mitigation: Keep check_depth set to basic unless web cross-verification is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiping3/anti-hallucination) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown or plain text responses with source references, uncertainty statements, or requests for clarification.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only behavior; no external scripts, API calls, or code execution are shipped in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
