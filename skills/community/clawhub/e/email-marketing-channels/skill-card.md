## Description: <br>
Helps agents plan email marketing, EDM, newsletter strategy, deliverability, content cadence, and measurement for AI/SaaS products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostja94](https://clawhub.ai/user/kostja94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, founders, and developers working on AI/SaaS products use this skill to plan email campaigns, newsletters, onboarding sequences, deliverability setup, article distribution, cadence, and KPIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local project context files to tailor advice, which could expose sensitive audience, campaign, or strategy details in generated recommendations. <br>
Mitigation: Review `.claude/project-context.md` and `.cursor/project-context.md` before use and remove secrets or sensitive material that should not inform marketing output. <br>
Risk: Email deliverability and bulk-sender requirements can change, and incorrect campaign guidance can affect sender reputation or compliance. <br>
Mitigation: Verify current provider rules, unsubscribe handling, complaint thresholds, and applicable email laws before sending production campaigns. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with tables and bullet lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local project context files when present to tailor advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
