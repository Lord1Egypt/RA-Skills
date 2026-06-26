## Description: <br>
Guides frontend interaction motion strategy, tool selection, performance budgets, and accessible reduced-motion behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend designers use this skill to plan, implement, or review UI motion for page transitions, scroll animation, microinteractions, animation performance, and reduced-motion fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner guidance notes that repo-maintenance helpers can perform high-impact actions when explicitly invoked. <br>
Mitigation: Review the skill and any generated recommendations before deployment or execution. <br>
Risk: Motion guidance that is applied without accessibility review can produce excessive or inaccessible animation. <br>
Mitigation: Check reduced-motion behavior, avoid rapid flashing, preserve focus and reading order, and verify the interface remains usable without animation. <br>
Risk: Heavy animation libraries or continuous animations can degrade loading and interaction performance. <br>
Mitigation: Lazy-load heavy motion components, animate transform and opacity where possible, pause continuous animation when hidden, and test on target viewport sizes and devices. <br>


## Reference(s): <br>
- [Motion Interaction on ClawHub](https://clawhub.ai/bovinphang/fec-motion-interaction) <br>
- [Bovinphang publisher profile](https://clawhub.ai/user/bovinphang) <br>
- [Motion patterns reference](references/motion-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers motion purpose, technical approach, intensity level, reduced-motion fallback, performance boundaries, and validation checks.] <br>

## Skill Version(s): <br>
2.5.0 (source: evidence.release.version, package.json, metadata.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
