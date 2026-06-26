## Description: <br>
Use when implementing UI from Figma, Sketch, MasterGo, Pixso, Modao, MockingBot, screenshots, design selections, design tokens, or design-to-code tasks for production frontend components/pages; Chinese triggers include 设计稿, 按设计实现. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to turn design artifacts or design-tool context into production frontend components and pages. It emphasizes reusing existing components, mapping visual decisions to design tokens, preserving accessibility, and validating the result after implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide code edits from incomplete or sensitive design context. <br>
Mitigation: Review the implementation plan before file changes and provide only the design screenshots, selections, or metadata needed for the task. <br>
Risk: Generated frontend changes may diverge from the existing design system or accessibility requirements. <br>
Mitigation: Check component reuse, token mapping, keyboard support, visible focus states, and available lint or test results before relying on the implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-implement-from-design) <br>
- [Design plan template](references/design-plan-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown implementation plan, code changes, and validation command summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a timestamped design implementation plan report before code changes when enough design context is available.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence, package.json, metadata.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
