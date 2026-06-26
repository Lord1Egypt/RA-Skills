## Description: <br>
E2E automation engineer skill for route smoke checks, HTTP reachability, and lightweight UI confidence validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly verify that changed routes, pages, APIs, or UI surfaces still load, route correctly, and avoid obvious 404, 405, authentication, or rendering failures. It is intended for focused smoke validation before deeper acceptance or end-to-end testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A passing smoke check may be mistaken for full authentication, security, business-logic, or end-to-end coverage. <br>
Mitigation: Use the result only as scoped reachability and rendering confidence, then run deeper tests for auth, security, and business-critical flows when those areas are affected. <br>
Risk: Route-refresh or runtime validation commands can affect a development environment if run without confirming scope. <br>
Mitigation: Confirm the affected route or UI surface and run the narrow command in the appropriate development or test environment before reporting results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/e2e-ui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise command and validation-result details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the route path or browser path checked, the command or minimal smoke action used, and a pass, failure, or follow-up result.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
