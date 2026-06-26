## Description: <br>
Code Reviewer conducts adversarial code and pull request reviews focused on security issues, edge cases, maintainability, accessibility, and actionable fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corbin-breton](https://clawhub.ai/user/corbin-breton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to get structured, skeptical reviews of code snippets, diffs, and pull requests. It helps identify blocking defects, required changes, structural erosion, and concrete next steps before feedback is posted or changes are accepted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review feedback may be incorrect, too severe, or unsuitable to post directly to a pull request. <br>
Mitigation: Manually confirm findings and edit feedback before sharing it with maintainers or applying recommendations. <br>
Risk: Optional dual-review mode can send code or diffs to a configured second model. <br>
Mitigation: Use dual-review mode only when the reviewed material can be shared with that second model under the applicable project and data-handling rules. <br>
Risk: Users could treat a review-only skill as permission to make source changes without supervision. <br>
Mitigation: Keep the skill in review-only use unless the user explicitly asks the agent to make code changes, then review any edits separately. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/corbin-breton/adversarial-code-reviewer) <br>
- [Publisher Profile](https://clawhub.ai/user/corbin-breton) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Structured Markdown review with severity sections, findings, verdict, and recommended next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include short code examples or replacement patterns. Optional dual-review mode can add cost, latency, and second-model data-sharing considerations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
