## Description:

Guides an agent through AI video generation and post-production using Vidu model selection, prompt optimization, FFmpeg stitching, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junhongzhang77-ui](https://clawhub.ai/user/junhongzhang77-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to turn storyboard prompts into platform-adapted video generation plans, preserving prompt detail, adding negative prompts, selecting Vidu models, stitching outputs, and routing results through quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses the VIDU_TOKEN environment variable and sends prompts or reference materials to Vidu.

Mitigation: Confirm the deployment is allowed to use Vidu and that submitted prompts or reference materials do not contain sensitive content.

Risk: Prompt optimization and video stitching guidance can produce low-quality or mismatched generated clips if prompts are incomplete or quality checks are skipped.

Mitigation: Keep the source prompt intact, add negative prompts, test one or two scenes before batch generation, and run the referenced quality-check workflow before final stitching.

## Reference(s):

- [Vidu service endpoint](https://service.vidu.cn)
- [ClawHub skill page](https://clawhub.ai/junhongzhang77-ui/skills/ai-viral-team-video-generation)
- [Publisher profile](https://clawhub.ai/user/junhongzhang77-ui)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompt templates, checklists, API configuration notes, and FFmpeg-oriented workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference VIDU_TOKEN configuration and Vidu prompt or reference-material submission.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
