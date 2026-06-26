## Description: <br>
Search Twitter/X for tweets, discussions, and sentiment on topics, people, or brands using Exa's tweet category search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to find relevant Twitter/X conversations about a topic, person, brand, or competitor and synthesize sentiment, themes, notable voices, and actionable insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics may be sent to Exa for Twitter/X research. <br>
Mitigation: Use the skill only for topics appropriate to share with Exa, and avoid confidential or sensitive queries. <br>
Risk: The workflow depends on the local `tools/clis/exa.js` helper. <br>
Mitigation: Confirm the helper is present and trusted before running the suggested commands. <br>
Risk: Optional product marketing context files may contain sensitive launch or customer information. <br>
Mitigation: Review and redact sensitive details before allowing the skill to use those files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mariokarras/abm-exa-x-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tweet summaries, sentiment labels, synthesis sections, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include individual tweet summaries, overall sentiment, key themes, notable voices, conversation trend, and actionable insights.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
