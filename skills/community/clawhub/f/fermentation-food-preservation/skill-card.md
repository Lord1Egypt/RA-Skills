## Description:

Guides agents in food preservation techniques including fermentation, pickling, canning, drying, and smoking for preserving harvests, extending shelf life, reducing waste, and building food resilience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to choose appropriate home food-preservation methods and receive step-by-step guidance for ferments, pickles, canning, dehydration, sourdough starter maintenance, and related safety checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests filesystem access that is not clearly necessary for food-preservation guidance.

Mitigation: Deny or remove filesystem access before installation when the agent platform allows it.

Risk: The installation command is unpinned, which can make the installed content change over time.

Mitigation: Use a pinned or otherwise trusted ClawHub installer and verify the release before deploying it.

Risk: Incorrect food-preservation advice can create serious safety hazards, especially for canning and botulism prevention.

Mitigation: Use tested recipes and official preservation references, and require altitude and method checks before canning guidance.

Risk: Scheduled reminders or proactive prompts may be unwanted in some agent deployments.

Mitigation: Review or disable automation triggers before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/fermentation-food-preservation)
- [USDA Complete Guide to Home Canning](https://nchfp.uga.edu/publications/publications_usda.html)
- [National Center for Home Food Preservation](https://nchfp.uga.edu)
- [Anthropic: Labor market impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with checklists, recipes, safety rules, agent state, and automation trigger configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes high-stakes food-safety guidance and optional reminder-style automation triggers.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
