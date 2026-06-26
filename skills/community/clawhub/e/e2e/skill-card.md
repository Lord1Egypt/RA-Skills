## Description: <br>
E2E automation engineer skill for Playwright-driven flow validation, browser interaction coverage, and end-to-end regression checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate real browser user journeys, multi-step UI paths, and cross-service behavior that unit tests alone cannot prove. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-level E2E checks can change application state or exercise sensitive flows. <br>
Mitigation: Run in non-production environments with least-privilege test accounts or seed data, and keep the requested test scope narrow. <br>
Risk: Unsupported Playwright invocation patterns can produce misleading or non-representative results. <br>
Mitigation: Use the repository-supported E2E command path, such as `php bin/w e2e:run`, for the smallest scope that proves the behavior. <br>
Risk: Dedicated runtime instances can conflict with shared ports or remain running after validation. <br>
Mitigation: Avoid default WLS port `9501` when a dedicated instance is required, and stop dedicated instances after runtime-sensitive validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/e2e) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown execution summaries with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports executed scenarios, pass or failure evidence, prerequisite setup, and residual risk notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
