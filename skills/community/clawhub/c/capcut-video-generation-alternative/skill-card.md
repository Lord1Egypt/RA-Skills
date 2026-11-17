## Description:

Generates timeline-ready AI video clips with AI Hive Seedance 2.5 for CapCut, Jianying, and short-video editing workflows, including B-roll, opener, match-cut, clean-plate, and tail-extension tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, video editors, and developers use this skill to plan and generate insertable media for specific gaps in a CapCut or Jianying-style editing timeline. It is suited for short-video B-roll, opener generation, shot matching, clean background plates, and ending extensions, while final editing remains in a separate NLE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media and prompts are sent to AI Hive, and an API key may be stored locally.

Mitigation: Use non-sensitive test media first, keep API keys scoped and protected, and install only if AI Hive processing is acceptable for the intended content.

Risk: Remote service responses can influence media upload hosts and local output paths.

Mitigation: Prefer --no-download or a dedicated output directory for untrusted tasks, and review or patch host allowlisting and task ID filename validation before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/capcut-video-generation-alternative)
- [AI Hive API base endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive OpenAPI endpoint used by the artifact](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell command examples, local configuration, and generated video-file handoff details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or download generated video assets through the bundled CLI when the user runs those commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
