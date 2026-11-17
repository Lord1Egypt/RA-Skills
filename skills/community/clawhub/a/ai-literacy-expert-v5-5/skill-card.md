## Description:

Generates AI-literacy teaching materials for BNBU/SAI and broader education settings, including p5.js interactive courseware, immersive learning games, lesson-prep packages, adaptive assessments, course recommendations, and collaborative teaching workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linix-2026](https://clawhub.ai/user/linix-2026)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, students, and training teams use this skill to design AI-literacy lessons, interactive p5.js courseware or games, assessment reports, learning paths, and collaborative lesson-prep assets. It is especially tailored for BNBU/SAI programs while remaining usable for general school, university, and enterprise training scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learner data caching and synchronization may be under-scoped for school, enterprise, or student-data environments.

Mitigation: Require opt-in cloud sync, clear retention and deletion controls, and a local-only assessment mode before deployment.

Risk: Cloud saving and sharing workflows may send materials or learner reports to IMA, Tencent Docs, or shared collaboration spaces.

Mitigation: Show explicit notice and require confirmation before saving, sharing, or synchronizing content outside the local session.

Risk: Runtime dependencies used by generated courseware or prep packages may not be independently verified.

Mitigation: Review local dependencies, pin trusted versions, or use subresource integrity hashes before installation or classroom use.

Risk: Broad collaboration and sharing activations could trigger external actions before the user has reviewed the output.

Mitigation: Use narrower activation rules and require confirmation for collaboration setup, cloud storage, sharing, and device-side distribution actions.

## Reference(s):

- [Skill README](README.md)
- [AI Learning Assessment Guide](references/assessment-guide.md)
- [Collaboration Lesson-Prep Guide](references/collaboration-guide.md)
- [Interactive Lesson Builder Guide](references/interactive-lesson-builder-guide.md)
- [Recommendation Engine Guide](references/recommendation-engine.md)
- [Offline Support Guide](references/offline-support-guide.md)
- [p5.js Courseware Guide](references/p5js-courseware-guide.md)
- [p5.js Game Design Guide](references/p5js-game-design-guide.md)
- [BNBU/SAI Adaptation Module](references/module-e-bnbu-sai.md)
- [AI Safety and Ethics Module](references/module-f-safety-ethics.md)
- [AI Latest Developments Module](references/module-g-latest-developments.md)
- [WorkBuddy Adaptation Guide](references/workbuddy-adaptation.md)
- [Commercial Production Standards](references/commercial-production-standards.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML/code artifacts and structured lesson, assessment, and collaboration outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include single-file p5.js HTML courseware or games, multi-format lesson-prep package instructions, assessment reports, and learning-path recommendations.]

## Skill Version(s):

5.5.0 (source: server release metadata and artifact/meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
