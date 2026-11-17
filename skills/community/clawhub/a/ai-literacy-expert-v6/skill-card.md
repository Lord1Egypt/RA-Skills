## Description:

玩转AI校园(BNBU) is an AI literacy teaching workflow skill that helps agents generate interactive courseware, games, lesson packs, adaptive assessments, recommendations, collaboration spaces, and WorkBuddy-oriented delivery plans for students, teachers, enterprises, and BNBU/SAI users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linix-2026](https://clawhub.ai/user/linix-2026)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, students, training teams, and BNBU/SAI users use this skill to plan and generate AI literacy learning materials, including p5.js courseware, learning games, lesson documents, assessments, study plans, and collaboration workflows. Agents can use it to orchestrate an end-to-end teaching workflow from intent classification through verification, packaging, delivery, reporting, and follow-up learning recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose broad automatic cloud, sharing, device, and recurring workflow actions through WorkBuddy-centered teaching flows.

Mitigation: Require explicit user review before writing content, sharing materials, creating reminders or calendar items, enabling recurring actions, or retaining workflow state.

Risk: Generated or shared teaching materials may include student, teacher, class, or institution information.

Mitigation: Minimize sensitive data, confirm authorized destinations before saving to IMA or Tencent Docs, and restrict sharing to the intended class or teaching group.

Risk: The security evidence warns against unpinned global npm or npx setup guidance.

Mitigation: Use pinned local dependencies in a trusted environment before running automation or Playwright-based verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linix-2026/skills/ai-literacy-expert-v6)
- [Workflow orchestrator](artifact/references/workflow-orchestrator.md)
- [Automation operations](artifact/references/automation-ops.md)
- [WorkBuddy adaptation](artifact/references/workbuddy-adaptation.md)
- [BNBU/SAI module](artifact/references/module-e-bnbu-sai.md)
- [Assessment guide](artifact/references/assessment-guide.md)
- [Recommendation engine](artifact/references/recommendation-engine.md)
- [Collaboration guide](artifact/references/collaboration-guide.md)
- [Courseware guide](artifact/references/p5js-courseware-guide.md)
- [Game design guide](artifact/references/p5js-game-design-guide.md)
- [IMA AI literacy course knowledge base](https://ima.qq.com/wiki/?shareId=8beb984ebb359e372653e0c32376ee62aa2320088c3571954e2c3c844c41d552)
- [TRAE IDE reference knowledge base](https://lcnziv86vkx6.feishu.cn/wiki/GEEnwlfTQi8qZrkFsPycfkUKnul)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated HTML/code blocks, lesson assets, assessment reports, study plans, workflow status summaries, and packaging or delivery instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include p5.js single-file HTML, document package plans, adaptive quiz content, WorkBuddy delivery steps, and verification summaries.]

## Skill Version(s):

6.0.0 (source: server release metadata and artifact/meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
