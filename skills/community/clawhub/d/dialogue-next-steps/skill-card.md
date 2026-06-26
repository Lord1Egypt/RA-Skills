## Description: <br>
Guides assistants to answer first and, when useful, add concise numbered next-step options that help users continue a conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqfcyily](https://clawhub.ai/user/sqfcyily) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to make conversational answers easier to continue, especially for beginner, conceptual, emotional, or underspecified requests. It helps an assistant provide a direct answer, then offer a small set of distinct follow-up actions or questions when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Follow-up suggestions can add unwanted verbosity for users who prefer terse answers. <br>
Mitigation: Suppress next steps when the user asks for just the answer, no suggestions, or no follow-up questions. <br>
Risk: Next-step guidance can be less useful when the request is high-stakes, ambiguous, or missing key context. <br>
Mitigation: Answer the core question first, state assumptions, ask only the most important missing detail when needed, and include critical or risk-oriented options for high-stakes topics. <br>
Risk: Lightweight personalization could over-emphasize a preferred style of follow-up. <br>
Mitigation: Keep personalization within the current session and ask a single preference question when the user's preferred direction is unclear. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with optional numbered next-step lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should come first; next-step lists are gated, localized to the user's language, capped at five items, and suppressed when the user asks for no suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
