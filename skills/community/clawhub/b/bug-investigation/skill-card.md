## Description: <br>
Systematically reproduces, locates, and diagnoses frontend bugs using steps, hypotheses, DevTools, and minimal repro. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate frontend issues by clarifying symptoms, reproducing the bug, testing hypotheses, locating the root cause, and proposing the smallest practical fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging workflows can involve console output, network traces, headers, or response bodies that contain secrets or customer data. <br>
Mitigation: Share only minimal reproduction details and sanitized logs; redact cookies, authorization headers, tokens, private response bodies, customer data, and production credentials. <br>
Risk: A proposed root cause or fix may be incomplete if the bug depends on backend data, browser state, timing, or environment-specific conditions. <br>
Mitigation: Validate each hypothesis with reproducible steps, DevTools evidence, and targeted tests before applying or shipping changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/bug-investigation) <br>
- [Project homepage](https://github.com/wangzhiming1999/oliver-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown bug investigation report with optional code snippets or fix steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include reproduction steps, hypothesis checks, root-cause notes, and testing recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
