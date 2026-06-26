## Description: <br>
Product analytics with your AI agent: set up consent-based tracking, read funnels, paths, retention, experiments, and context, then recommend the smallest growth action using the official Agent Analytics CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and growth teams use this skill to install consent-based Agent Analytics tracking, query product behavior, diagnose funnels, paths, retention, and experiments, and choose a small next growth action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a pinned external npm CLI and browser-approved account access. <br>
Mitigation: Install only when the publisher and pinned CLI are trusted, authorize only the intended account, and verify auth state before continuing. <br>
Risk: Persistent auth configuration may contain sensitive account access data. <br>
Mitigation: Keep `.openclaw/agent-analytics/config.json` private, store it outside committed source, and ensure the config path is ignored by version control. <br>
Risk: Analytics context or instrumentation changes could expose PII, secrets, or unwanted tracking. <br>
Mitigation: Review tracking changes before deployment, use consent-based events tied to product workflows, and avoid storing PII or secrets in analytics context. <br>
Risk: Some analytics reads may require a paid upgrade. <br>
Mitigation: Require explicit human approval before completing any paid upgrade and rerun the blocked command only after the account is confirmed. <br>


## Reference(s): <br>
- [Agent Analytics ClawHub page](https://clawhub.ai/dannyshmueli/agent-analytics) <br>
- [Agent Analytics homepage](https://agentanalytics.sh) <br>
- [Projects, surfaces, and portfolios guide](https://docs.agentanalytics.sh/guides/projects-surfaces-portfolios/) <br>
- [Growth recipes](references/growth-recipes.md) <br>
- [Product analytics operating model](references/product-analytics-operating-model.md) <br>
- [Setup and auth reference](references/setup-auth.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, configuration guidance, and analytics recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the pinned official Agent Analytics CLI through npx and may produce setup, verification, analysis, and upgrade-handoff instructions.] <br>

## Skill Version(s): <br>
4.0.33 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
