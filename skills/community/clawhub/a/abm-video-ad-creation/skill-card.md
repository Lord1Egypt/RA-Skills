## Description: <br>
Helps users create Remotion video advertisements in standard 15s, 30s, and 60s formats with scene-based storytelling for hook, value proposition, and call-to-action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and creative teams use this skill to plan and implement React and Remotion video ad compositions for digital advertising. It guides duration selection, scene structure, composition registration, component creation, preview, and render commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local product-marketing context may be incomplete, outdated, or not approved for the current campaign. <br>
Mitigation: Review any `.agents/product-marketing-context.md` or `.claude/product-marketing-context.md` file before relying on it for ad copy, claims, or brand direction. <br>
Risk: Suggested `npx remotion` commands execute inside the user's project and can use project dependencies and assets. <br>
Mitigation: Run preview and render commands only in a trusted Remotion project, then review the browser preview before producing final ad video files. <br>


## Reference(s): <br>
- [Ad Format Specifications](references/formats.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mariokarras/abm-video-ad-creation) <br>
- [Publisher Profile](https://clawhub.ai/user/mariokarras) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline TSX and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Remotion composition guidance, scene component code, preview commands, and render commands for the selected ad duration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
