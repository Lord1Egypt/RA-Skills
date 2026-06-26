## Description: <br>
Amazon Rufus Optimizer helps sellers evaluate product listing readiness for Rufus-style shopping conversations by simulating buyer prompts, diagnosing intent tag coverage, and proposing listing copy improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon marketplace sellers and listing optimization teams use this skill to check whether a product's title, bullet points, and positioning cover the buyer intents Rufus-style shopping assistants may use. It produces scenario simulations, missing intent tags, conversational copy rewrites, cross-category suggestions, and a visibility score for review before applying listing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Listing suggestions may be inaccurate, overstate Rufus behavior, or conflict with Amazon policy if applied without review. <br>
Mitigation: Review every recommendation against Amazon policy, product facts, and current marketplace performance before changing a live listing. <br>
Risk: Users may provide sensitive product or listing details while requesting optimization advice. <br>
Mitigation: Only provide product or listing information that is appropriate to share with the agent and avoid unnecessary confidential data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangm-a3/amazon-rufus-optimizer) <br>
- [Rufus intent taxonomy](artifact/references/intent-taxonomy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown-style diagnostic report with scores, simulated prompts, intent tag gaps, listing copy suggestions, and optional JSON from the bundled analyzer script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and should be reviewed against Amazon policy, product facts, and actual marketplace performance before implementation.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
