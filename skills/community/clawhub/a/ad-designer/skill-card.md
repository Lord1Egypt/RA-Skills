## Description: <br>
Generates marketing ad images with Nano Banana Pro from campaign briefs and brand visual guidance, using platform aspect ratios, draft-first review, and final image output paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baitoxkevin](https://clawhub.ai/user/baitoxkevin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing teams and agents use this skill to turn campaign-planner creative briefs and brand visual guidance into platform-ready ad image drafts and approved final images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign and brand details are sent through the Gemini/Nano Banana Pro image workflow. <br>
Mitigation: Install and use the skill only when that exposure is acceptable for the campaign data being processed. <br>
Risk: The prerequisite guidance includes a curl-to-shell uv installer command. <br>
Mitigation: Prefer an operating-system package manager or verify Astral's installer before allowing an agent to run it. <br>
Risk: Generated images may contain hallucinated logos, brand names, or incorrect text. <br>
Mitigation: Use the skill's draft-first self-review loop and require user approval before producing final 4K outputs. <br>


## Reference(s): <br>
- [Ad Designer Prompt Templates and Reference](references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with file paths and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates draft and final image files under /tmp/marketing/assets/images/ through the nano-banana-pro dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
