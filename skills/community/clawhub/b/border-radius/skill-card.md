## Description: <br>
Generate CSS border-radius code. Use when the user asks to generate rounded corners, create a border radius, make a blob shape, or produce border-radius CSS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to generate CSS border-radius values and matching Tailwind utility classes for uniform, per-corner, and preset rounded shapes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A future version could request unnecessary credentials, local file access, network access, or command execution. <br>
Mitigation: Re-review and rescan any version that adds those capabilities before installation or deployment. <br>
Risk: Generated CSS or Tailwind classes may not match the user's intended unit or corner order. <br>
Mitigation: Review the generated CSS value and Tailwind class before applying them to production UI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ohernandez-dev-blossom/border-radius) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown with CSS snippets and Tailwind utility classes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Caps negative border-radius values at 0, caps values above 9999, and omits Tailwind arbitrary values for non-px units.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
