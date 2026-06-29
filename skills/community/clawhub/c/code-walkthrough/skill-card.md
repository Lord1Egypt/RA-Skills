## Description: <br>
Generates a self-contained HTML code walkthrough with call-flow tracing, source annotations, and trust-boundary labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to explain a module's entry points, data flow, call stack, and trust boundaries during onboarding, code review, or security-oriented walkthroughs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated walkthroughs may expose source snippets, file paths, or security-sensitive implementation details. <br>
Mitigation: Use the skill only on repositories or modules suitable for inclusion in the generated output, and review the HTML before sharing it outside the workspace. <br>
Risk: Call-flow or trust-boundary explanations may be incomplete if the agent misses relevant code paths. <br>
Mitigation: Review the generated walkthrough against the source code before relying on it for onboarding, review, or security decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/code-walkthrough) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Self-contained HTML with embedded CSS, call-flow sections, source annotations, and trust-boundary notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include quoted code excerpts, file paths, line numbers, diagrams expressed in HTML, and reviewer-facing security boundary labels.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
