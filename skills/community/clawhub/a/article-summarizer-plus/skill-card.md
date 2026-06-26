## Description: <br>
Summarize articles and social posts from URLs using full-content retrieval first, with browser fallback when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KhalilHsu](https://clawhub.ai/user/KhalilHsu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize articles, social posts, and visible comment threads from URLs. It helps agents choose a retrieval path, keep summaries concise, and clearly label partial or inaccessible source content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summaries may be incomplete when source pages are paywalled, login-gated, dynamically rendered, or only partially visible. <br>
Mitigation: Use the documented retrieval fallback order and explicitly label inaccessible or partial content instead of guessing. <br>
Risk: Comment or reply summaries can overrepresent the small set of comments visible to the agent. <br>
Mitigation: Summarize only visible themes and state when the available comments are limited. <br>


## Reference(s): <br>
- [Retrieval Playbook](references/retrieval-playbook.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Source Notes](references/source-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with concise sections and optional comment themes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to concise summaries and reports retrieval limits when content is incomplete or inaccessible.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
