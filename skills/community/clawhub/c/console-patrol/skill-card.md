## Description: <br>
Console Patrol helps agents scan web applications for browser console errors and framework warnings, then report severity-ranked diagnostics and suggested fixes for React, Ant Design, and Element UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhzgao](https://clawhub.ai/user/zhzgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to scan authorized web application routes for browser console errors, runtime failures, and framework-specific warnings. The skill is useful during debugging, pre-release checks, and CI-style frontend audits where severity-ranked findings and fix suggestions are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install dependencies and run browser-based scans against web applications. <br>
Mitigation: Use it only on applications and routes you are authorized to inspect, and review dependency installation or browser-scanning steps before execution. <br>
Risk: Console findings can depend on route coverage, app load timing, and framework detection. <br>
Mitigation: Confirm the scanned routes, adjust wait time for lazy-loaded pages, and review findings before making code changes. <br>


## Reference(s): <br>
- [Console Patrol ClawHub page](https://clawhub.ai/zhzgao/console-patrol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with tables, issue lists, inline code, and optional shell or Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pages scanned, P0/P1/P2 severity counts, affected URLs, console messages, and suggested fixes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
