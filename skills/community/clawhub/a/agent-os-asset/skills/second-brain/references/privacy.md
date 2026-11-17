# Privacy Rules / 隐私规则

English is normative; ZH-CN is paired. / 英文为规范文本；简体中文为配对译文。

- Exclude any Markdown file tagged `PII` in frontmatter.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 排除 frontmatter 中带有 `PII` 标签的任何 Markdown 文件。
- Exclude files listed in root `tag_report*.json` under `pii_files`.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 排除根目录 `tag_report*.json` 的 `pii_files` 中列出的文件。
- Default `agent-readable` mode indexes `.agent.md` only.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 默认 `agent-readable` 模式仅索引 `.agent.md`。
- `asset-manifest` mode indexes only final retained rows and skips `privacy=pii`, embedded attachments, generated reports, temporary files, and non-final candidates.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: `asset-manifest` 模式只索引最终保留行，并跳过 `privacy=pii`、嵌入附件、生成报告、临时文件和非最终候选项。
- Federated retrieval accepts only registry entries whose current manifest and index hashes match a final, non-PII-ready workspace.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 联邦检索只接受当前 manifest 与 index 哈希匹配、且 workspace 已达到最终非 PII 就绪状态的注册条目。
- Do not index archived/extracted content, templates, operational root documents, profile notes, hidden/plugin/cache/trash/attachment directories, or files tagged `archived`.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 不索引 archived/extracted 内容、模板、根目录操作文档、profile 笔记、hidden/plugin/cache/trash/attachment 目录，或带 `archived` 标签的文件。
- Do not reuse unrelated embedding stores because they may contain stale or sensitive chunks.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 不要复用无关 embedding store，因为其中可能包含过期或敏感 chunk。
- Keep snippets short and source-linked; do not copy whole notes into Skill references.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: snippet 应简短并链接来源；不要把整篇笔记复制进 Skill reference。
- Local indexing and lexical retrieval are the default and require no network access.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 默认使用本地索引和 lexical retrieval，不需要网络访问。
- Remote summary and embedding features require explicit opt-in, dedicated credentials, and HTTPS endpoints.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 远程摘要和 embedding 功能需要显式 opt-in、专用凭据与 HTTPS endpoint。
- Semantic rerank may receive only the user query and bounded indexed candidate `search_text`; never send raw source files, PII rows, or credentials.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: Semantic rerank 只能接收用户查询与有界索引候选的 `search_text`；绝不发送原始源文件、PII 行或凭据。

Run after index changes:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 索引变更后运行：

```bash
SKILL_DIR="/path/to/second-brain"
python3 "$SKILL_DIR/scripts/validate_privacy.py"
```
