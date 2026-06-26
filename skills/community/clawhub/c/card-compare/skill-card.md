## Description: <br>
Side-by-side comparison of two major-US credit cards across fees, earning rates, credits, transfer partners, and key benefits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahongc](https://clawhub.ai/user/jiahongc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to compare two exact credit card variants side by side using issuer-first web research and approved secondary sources. It is intended for compact factual comparisons, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credit-card names and comparison queries may be sent to web search and fetch services. <br>
Mitigation: Use the skill only when those queries are acceptable to share with the selected search and fetch providers. <br>
Risk: Optional Brave API use may consume API quota and requires a sensitive credential. <br>
Mitigation: Provide BRAVE_API_KEY only when the Brave search path is desired, and manage the key as a normal secret. <br>
Risk: Credit-card offers, fees, credits, and benefits can change. <br>
Mitigation: Verify important terms against issuer pages before acting on a comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiahongc/card-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown comparison report with two-column tables, confidence notes, and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask a clarification question when a card name is ambiguous; may use optional Brave Search API credentials when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
