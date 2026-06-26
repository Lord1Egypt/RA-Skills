# Human Brainstorm Question Format

Use this format whenever Claude Code or Codex needs user input.

Rules:

- Use the user's primary language.
- Explain why the question matters.
- Provide 2 to 5 concrete options.
- Include one recommended safe default when possible.
- Include an Other/free-form option.
- Explain tradeoffs when they affect architecture, safety, product scope, data, production, or cost.
- Do not ask the user to paste secrets.

Chinese template:

```text
需要你确认一个问题，因为：<原因>

请选择：
A. <选项 A>。<后果/取舍>
B. <选项 B>。<后果/取舍>
C. <选项 C>。<后果/取舍>
D. Other：输入你的方案。

推荐：<推荐选项>，因为 <理由>。
```

English template:

```text
I need your input because: <reason>

Choose one:
A. <Option A>. <Consequence/tradeoff>
B. <Option B>. <Consequence/tradeoff>
C. <Option C>. <Consequence/tradeoff>
D. Other: describe your preferred approach.

Recommended: <option>, because <reason>.
```
