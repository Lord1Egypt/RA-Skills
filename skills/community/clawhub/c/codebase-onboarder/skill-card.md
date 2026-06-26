## Description: <br>
AI-powered codebase analysis for generating architecture docs, onboarding guides, and key-flow walkthroughs for any project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect an unfamiliar repository and produce onboarding documentation, architecture summaries, key-flow walkthroughs, setup steps, and gotchas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated onboarding guides can expose secrets, internal hostnames, service names, or other sensitive configuration details found in a repository. <br>
Mitigation: Review the generated guide before sharing it and redact real secrets, tokens, internal hostnames, and sensitive service details. <br>
Risk: The skill asks an agent to inspect repository contents for documentation. <br>
Mitigation: Use it only on repositories you are comfortable having an agent analyze. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/codebase-onboarder) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown onboarding guide with tables and optional command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes repository structure, entry points, dependencies, data layer, API surface, configuration, tests, CI/CD, key flows, and gotchas.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
