# AI Fiction: Pro Editor

Edit dialogue, pacing and prose while keeping the story and the author's voice. The final answer contains only edited fiction.

## Install and use in OpenClaw

Give your Claw this message:

> Install AI Fiction: Pro Editor from https://github.com/RedRookAI/openclaw-skills/tree/main/skills/ai-fiction into my workspace's skills/ai-fiction folder, including all bundled files. Preserve my existing instructions, author preferences and model settings.

Or copy this whole folder into your workspace as `skills/ai-fiction`. Start a new chat if the skill does not appear.

Then paste or attach your passage and say:

> Use AI Fiction: Pro Editor on this passage. Follow my existing style preferences.

Add genre, audience or scene notes when useful. No story bible is required.

For a writing pipeline, make AI Fiction: Pro Editor the editing step after drafting. Pass it the draft and relevant story/style context. It uses the task's chosen model or your agent's existing model settings.

Installation adds the skill files. It does not replace AGENTS.md, SOUL.md, memory, author preferences or model configuration. If this skill folder already exists, review the update before replacing your customized files.

Your applicable author preferences take precedence over the default house style. The current editing brief takes precedence over older preferences. With no override, the defaults remove em dashes, decorative triples and formulaic reversals. Review the edit before publication.

## Use as a prompt

Copy [AI-FICTION.md](AI-FICTION.md) into a chat. Replace `{INPUT_TEXT}` with your passage and `{STORY_CONTEXT}` with relevant notes, or leave the context blank.

Use it after drafting, before sharing a chapter, or before publication.

## See the results

[Before and after examples](EXAMPLES.md): deliberately bad input followed by actual Sol edits. **BEFORE is the input, not the skill's output.**

## References

- [CraftAlign: targeted story revision](https://arxiv.org/abs/2608.01377)
- [Loom: narrative rendering and fidelity](https://arxiv.org/abs/2607.00009)
- [Voice Under Revision: stylistic normalization](https://arxiv.org/abs/2604.22142)
- Related skills: [Story Skills](https://github.com/danjdewhurst/story-skills), [prose-edit](https://github.com/Mikefluff/skills/blob/main/skills/prose-edit/SKILL.md), [fiction-writing-prose](https://github.com/alt-code-ai/agent/blob/main/skills/fiction-writing-prose/SKILL.md).
- [OpenClaw skills](https://docs.openclaw.ai/tools/skills).

Version 0.1.0. [MIT-0 license](LICENSE).
