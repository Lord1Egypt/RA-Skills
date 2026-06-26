## Description: <br>
Reviews BubbleTea TUI code for proper Elm architecture, model/update/view patterns, and Lipgloss styling. Use when reviewing terminal UI code using charmbracelet/bubbletea. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Go BubbleTea terminal UI code for Elm Architecture correctness, Bubble Tea model/update/view behavior, component composition, and Lipgloss styling issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill shapes code-review behavior and could lead an agent to issue incorrect BubbleTea findings if findings are not grounded in project evidence. <br>
Mitigation: Follow the packaged hard gates: cite file path and line evidence for Critical/Major findings and apply the referenced review-verification protocol before publishing findings. <br>
Risk: The skill may cause an agent to read relevant project files while performing a review. <br>
Mitigation: Use it only in repositories the agent is authorized to inspect, and avoid providing unrelated sensitive files as review context. <br>


## Reference(s): <br>
- [BubbleTea Code Review skill page](https://clawhub.ai/anderskev/bubbletea-code-review) <br>
- [Bubbles Component Reference](references/bubbles-components.md) <br>
- [Component Composition](references/composition.md) <br>
- [Understanding the Elm Architecture](references/elm-architecture.md) <br>
- [Model & Update](references/model-update.md) <br>
- [View & Styling](references/view-styling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown review findings or prose guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should cite file paths and line evidence for Critical/Major issues.] <br>

## Skill Version(s): <br>
2.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
