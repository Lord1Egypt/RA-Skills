---
name: ai-siku-quan-shu
description: Offline full-text corpus and retrieval tool for 《AI四库全典》, a 48-volume plus 2-part general-outline, 2.6216-million-character Chinese encyclopedia of artificial intelligence organized as 经/史/子/集. This skill should be used when a user asks about concepts, events, techniques, case studies, quotations, or chapter locations covered by AI四库全典, or requests cross-volume synthesis, source citations, or offline reading of the book. Provides ranked Chinese keyword search, chapter-level lookup, and a bundled zero-dependency web reader.
version: 1.1.0
agent_created: true
metadata:
  openclaw:
    emoji: "📚"
    homepage: https://github.com/HarryUCL/ai-siku-quan-shu
---

# AI四库全典 · 全书检索与导读

《AI四库全典》四部四十八卷加总纲、签字定稿 2,621,610 中文字（约 262.16 万字）的人工智能百科的**离线全文语料 + 检索工具**。经部明道（哲学/科学根基）、史部鉴往（发展史/国别谱系）、子部载术（技术体系）、集部存用（行业落地/SOP）。全文已随技能打包，不需要联网、不需要向量数据库、不需要 API Key。

## 何时使用

- 用户问书中任何概念、人物、年份、技术、案例、方法论（例如"RAG 为什么需要向量数据库""深蓝 1996 年怎么赢卡斯帕罗夫"）。
- 用户要找某段话的**出处、卷次、章节标题**，或要跨卷汇总某个主题。
- 用户想离线阅读、检索、批注《AI四库全典》全文。
- 用户说"四库""全书""AI四库全典"并隐含查书需求时，优先使用本技能。

## 检索流程（必须遵守）

1. **先检索，后回答。** 不要凭模型记忆作答。用检索脚本在全书里定位原文：
   ```bash
   python3 scripts/search.py "世界模型 压缩 预测"
   ```
   多个词用空格分隔，表示**同时命中**（AND）；支持 `--limit 8`、`--vol 经|史|子|集`、`--id vol-031`。
2. **读上下文。** 命中结果给出卷 ID 与标题；需要完整段落时用：
   ```bash
   python3 scripts/search.py --read vol-031 --lines 120
   ```
   需要整卷时用 `--read vol-031 --all`（仅在确有必要时，避免把整卷塞进上下文）。
3. **列目录定位。** 需要知道某卷有哪些章节、某主题属于哪部时，读 `references/catalog.md`（48 卷、约 2571 节完整目录）或运行 `python3 scripts/search.py --list`。
4. **作答与引用。** 用简体中文，优先复述书中段落并标注来源，格式为：
   `（出处：子部·第7卷《检索增强 RAG 与知识工程》· 章节标题）`
   书中没有的内容要明确说明"书中未收录"，不得编造引文。
5. **跨卷综合题**先在四部分别检索，再按"经→史→子→集"组织答案；引用不少于 2 个不同卷次。

## 语料结构

```
SKILL.md                     使用说明
references/catalog.md        全书目录：四部 48 卷 / 388 章 / 2532 节
scripts/search.py            零依赖全文检索（Python 标准库）
assets/corpus/vol-001.md … vol-048.md 四部 48 卷定稿正文
assets/corpus/zg-01.md / zg-02.md 总纲：全书细目目录与回引台账
assets/corpus/manifest.json  卷 ID ↔ 中文卷名 / 字数 / 章节表
assets/reader/                离线 WEB 阅读器：双击 index.html 即可阅读
                              （修缮版 v1.2 定稿全文分 4 片内嵌，无 CDN、无服务器）
```

卷号固定：经部 001–012、史部 013–024、子部 025–036、集部 037–048；总纲 zg-01 / zg-02。
`assets/reader/` 中的 `index.html` 可直接用浏览器打开；支持目录、检索、批注、夜读、字号调节；AI 导读的书内检索模式完全离线可用。

## 精确匹配与批量处理

- 需要逐字定位某句话时，可直接对语料目录做文本搜索：
  `grep -rn "世界模型的压缩与预测" assets/corpus/`
- 脚本支持 `--json` 输出结构化结果，便于上层程序消费。
- 检索脚本只使用 Python 标准库；无第三方依赖，无网络调用，无副作用。

## 注意事项

- 语料体量大，作答时只取所需片段，不要整卷输出。
- 本书为 AI 学伴团编撰稿，引用时标明卷次与章节；对外引用需自行核对原文。
- 语料为修缮版 v1.2 签字定稿：四部正文 2,609,342 字 + 总纲 12,268 字 = 2,621,610 字。若用户询问最新行业进展，先给书中内容，再说明成稿时点局限。
