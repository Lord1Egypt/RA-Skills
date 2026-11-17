## Description:

AI 通识课教学与备课助手，用于课程材料分析、知识点筛选、课件编排、评估生成、端云协同教学工作流和 p5.js 互动控件质量门控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linix-2026](https://clawhub.ai/user/linix-2026)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, curriculum designers, education technologists, and AI literacy course teams use this skill to prepare AI literacy lessons, analyze local course materials, select knowledge points, compose Markdown lessons, generate assessment JSON, and build HTML p5.js interactive courseware. Developers can also use its scripts and references to run edge-cloud protocol validation, privacy redaction, cost monitoring, and interaction completeness gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and bootstrap paths can download and execute external FFmpeg or model artifacts.

Mitigation: Review the setup path before installation, run as a normal user, and pin and verify FFmpeg and model artifacts before bootstrap.

Risk: Cloud exchange paths may expose student or personal data if privacy controls are misconfigured or over-trusted.

Mitigation: Use a trusted HTTPS cloud endpoint, avoid sending student or personal data through cloud exchange, and review privacy behavior before deployment.

Risk: Documented deployment defaults may include weak operational settings.

Mitigation: Replace the documented Grafana password and avoid unpinned latest image tags before any deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linix-2026/skills/ai-literacy-expert-v8-1-0-aipc)
- [README](README.md)
- [Skill Specification](SKILL.md)
- [Edge-Cloud Architecture](references/edge-cloud-architecture.md)
- [Edge-Cloud Protocol](references/edge-cloud-protocol.md)
- [Edge-Cloud Protocol Schema](references/edge-cloud-protocol-schema.json)
- [Zero-Upload Privacy](references/zero-upload-privacy.md)
- [NPU Scheduling Guide](references/npu-scheduling-guide.md)
- [Local AI Quality Gate](references/local-ai-quality-gate.md)
- [Interactive Lesson Builder Guide](references/interactive-lesson-builder-guide.md)
- [p5.js Courseware Guide](references/p5js-courseware-guide.md)
- [p5.js Game Design Guide](references/p5js-game-design-guide.md)
- [Assessment Guide](references/assessment-guide.md)
- [Recommendation Engine](references/recommendation-engine.md)
- [Cost Optimization](references/cost-optimization.md)
- [Deployment Guide](references/deployment-guide.md)
- [p5.js CDN Reference](https://cdn.jsdelivr.net/npm/p5@2.3.1/lib/p5.min.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown lessons, assessment JSON, HTML courseware, reports, inline commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local workspace files such as final_lesson.md, assessment.json, courseware.html, edge-cloud request JSON, and work summary reports.]

## Skill Version(s):

8.1.1 (source: server release evidence; artifact metadata references 8.1.0-aipc)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
