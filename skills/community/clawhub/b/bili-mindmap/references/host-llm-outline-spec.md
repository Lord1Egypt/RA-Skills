# Host LLM Outline Spec

## Goal

Generate an `outline.md` that feels like a human-organized mind map rather than a transcript or ASR chunk dump.

## Source Priority

1. Full subtitle text or ASR transcript
2. Video metadata such as title, author, link, duration, and metrics
3. Site AI summary as supplemental material
4. Hot comments as supplemental feedback and debate

If sources conflict, prefer subtitles or ASR over the AI summary and comments.

## Required Thinking Pattern

1. Infer the video's central thesis first.
2. Group the full source into 3-6 logical modules.
3. Name each module with an abstract topic label.
4. Distill cross-section conclusions into `核心内容`.
5. Preserve mechanisms, examples, evidence, data, and contrasts in `关键细节`.
6. Keep comments in `评论反馈` instead of letting them dominate the outline.

## Hard Requirements

- Use the video title as the root topic.
- Follow the template structure from `references/mindmap-outline-template.md`.
- Organize `内容脉络` by logic, not by transcript or ASR order.
- Use abstract topic labels instead of copying spoken transcript lines.
- Merge adjacent spans when they are explaining the same underlying idea.
- `核心内容` should contain synthesized conclusions, not timeline bullets.
- `关键细节` should stay concrete: mechanisms, evidence, cases, numbers, steps, or contrasts.
- Mark uncertainty explicitly instead of inventing facts.

## Failure Modes

- Bad: branch titles that still read like raw transcript sentences.
- Bad: treating each time slice or ASR segment as a sibling branch.
- Bad: repeating the same idea in both `内容脉络` and `核心内容`.
- Bad: letting comments replace the source transcript as the main structure.
- Good: short abstract titles that sound like a human summary.
- Good: a branch structure that reveals argument and causality instead of speaking order.

## Output Requirements

- Output clean Markdown only.
- Start with `# <video title>`.
- Use Markdown bullet indentation for hierarchy.
- Do not add prefaces, notes, or explanations outside the outline itself.
