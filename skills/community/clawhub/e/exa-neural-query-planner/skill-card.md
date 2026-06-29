## Description: <br>
Plan Exa neural web searches before calling any Exa wrapper by crafting queries, choosing categories, setting domain and date filters, defining fallbacks, and deciding when Exa is a better fit than keyword search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruti3](https://clawhub.ai/user/ruti3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to prepare executor-ready Exa search plans for documentation, papers, companies, news, GitHub repositories, and other web research tasks. It helps choose query wording, filters, fallback searches, and stop conditions before a separate tool performs the search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may mistake a planned query for verified live web results. <br>
Mitigation: Treat the output as a plan only; run the search in a separate executor and verify returned sources before relying on them. <br>
Risk: Search planning can expose secrets if API keys are copied into the conversation. <br>
Mitigation: Do not ask for or echo EXA_API_KEY or other credentials; pass credentials only through the executor environment when a separate search tool runs. <br>
Risk: Deep searches or high result counts can increase API cost and rate-limit pressure. <br>
Mitigation: Use conservative result counts by default and reserve deep or exhaustive searches for cases where the research goal requires them. <br>
Risk: Poorly scoped searches can produce irrelevant, stale, or terms-sensitive results. <br>
Mitigation: Use the planned domain, date, and category filters, avoid paywall or login bypass instructions, and apply the quality checks before stopping. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruti3/skills/exa-neural-query-planner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown search plan with a table, primary query, YAML API hints, fallback queries, quality checks, and stop or escalation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only output; the skill does not call Exa, handle API keys, execute code, or claim live search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
