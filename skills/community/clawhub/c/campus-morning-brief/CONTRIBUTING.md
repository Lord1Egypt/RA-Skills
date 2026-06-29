# Contributing / 参与贡献

Thank you for improving Campus Morning Brief. This project is a reusable AI-agent skill, so contributions should keep the workflow portable, source-backed, and safe for students.

感谢你改进校园晨报。本项目是一个可复用的 AI Agent Skill，因此贡献应保持流程通用、来源可追溯，并适合学生使用。

## Good contribution areas / 推荐贡献方向

- Improve the bilingual workflow in `SKILL.md`. / 改进 `SKILL.md` 中的双语工作流。
- Strengthen content-safety rules in `references/content-guidelines.md`. / 强化 `references/content-guidelines.md` 中的内容安全规则。
- Extend or clarify the JSON payload schema in `references/brief.schema.json`. / 扩展或澄清 `references/brief.schema.json` 数据结构。
- Improve the renderer in `scripts/render_brief.py` without adding unnecessary runtime dependencies. / 改进 `scripts/render_brief.py` 渲染器，但避免增加不必要的运行时依赖。
- Add tests for validation, rendering, or edge cases. / 为校验、渲染或边界情况补充测试。

## Local checks / 本地检查

Run these before opening a pull request:

提交 Pull Request 前请执行：

```bash
python3 -S -B -m unittest discover -s tests -v
python3 scripts/render_brief.py tests/fixtures/valid.json --output-dir output
python3 /Users/wxh/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

If your environment cannot access the local `quick_validate.py` script, at minimum verify that `SKILL.md` has valid YAML frontmatter with only `name` and `description`.

如果你的环境无法访问本地 `quick_validate.py`，至少应确认 `SKILL.md` 的 YAML frontmatter 有效，且只包含 `name` 和 `description`。

## Content rules / 内容规则

- Fetch current weather and news instead of relying on model memory. / 实时获取天气和新闻，不依赖模型记忆。
- Keep news summaries original and cite publisher, publication date, and direct URL. / 新闻摘要使用原创表述，并保留发布机构、发布日期和直达链接。
- Avoid graphic violence, sexual content, gambling, self-harm details, rumors, disguised advertising, and age-inappropriate material. / 避免血腥暴力、色情、赌博、自伤细节、谣言、软性广告和不适龄内容。
- Do not commit private student data, credentials, delivery identifiers, or generated personal briefs. / 不要提交学生隐私、凭据、投递标识或已生成的个人晨报。

## Pull request expectations / PR 要求

- Keep changes focused and explain the user-facing impact. / 保持改动聚焦，并说明对用户的影响。
- Include tests or explain why tests are not applicable. / 包含测试，或说明为什么不适用测试。
- Update README or references when behavior changes. / 行为变化时同步更新 README 或参考文档。
- Preserve bilingual documentation for reader-facing docs. / 面向读者的文档保持中英文双语。
