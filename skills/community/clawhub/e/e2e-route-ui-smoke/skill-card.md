## Description: <br>
E2E automation engineer skill for route smoke checks, HTTP reachability, and lightweight UI confidence validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly check whether changed routes, pages, or API surfaces still load, route correctly, and avoid obvious 404, 405, authentication, or render failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route refresh commands and HTTP or browser probes can affect inappropriate environments if run without scope. <br>
Mitigation: Use the skill in development or test environments and provide a specific route, page, or API target before invoking checks. <br>
Risk: A reachable page or route smoke pass can be mistaken for full business-logic coverage. <br>
Mitigation: Treat smoke validation as lightweight confidence only and follow up with deeper acceptance or end-to-end testing when behavior needs proof. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/e2e-route-ui-smoke) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise validation results and inline commands or browser paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the target route or UI surface, command or smoke path used, observed pass or failure result, and any follow-up required.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
