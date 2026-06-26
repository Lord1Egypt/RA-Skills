## Description: <br>
Vibe-Learning creates context-aware micro-learning cards for developers waiting on AI coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skJack](https://clawhub.ai/user/skJack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill during idle moments in agent workflows to receive a short, context-aware feed of adjacent learning cards, source links, and a browser-readable HTML page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use current conversation context to form web searches, which may expose sensitive project details if invoked during confidential work. <br>
Mitigation: Ask the agent to keep search queries generic, avoid confidential identifiers, or invoke the skill only when the surrounding context is safe to use. <br>
Risk: The skill writes to a fixed standalone HTML output path and may overwrite a previous learning feed. <br>
Mitigation: Review or move any existing /mnt/user-data/outputs/vibe-learn-feed.html file before running the skill when preserving prior output matters. <br>
Risk: Broad waiting-related phrases can trigger the skill proactively when the user may not intend to generate a learning feed. <br>
Mitigation: Use an explicit trigger such as "vibe learn" for predictable activation, especially in workflows where idle-time comments should not start web search or file output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skJack/checkai) <br>
- [Publisher profile](https://clawhub.ai/user/skJack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [React JSX artifact plus a self-contained HTML page and concise chat note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or overwrites /mnt/user-data/outputs/vibe-learn-feed.html and uses web search to populate source-backed cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
