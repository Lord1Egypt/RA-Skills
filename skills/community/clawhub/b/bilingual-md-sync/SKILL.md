---
name: bilingual-md-sync
description: Keeps English Markdown and Chinese Markdown pairs in structural and topical sync, with reciprocal language links at the top of each file. Use when the user edits or mentions README.md and README-zh.md/README-en.md, any *-zh.md or *-en.md with a sibling *.md, bilingual docs, 中英文同步, language switch links, or translating between zh/en markdown files.
disable-model-invocation: true
---

# 中英文 Markdown 同步（`*-zh.md` ↔ `*.md`）

## 适用场景

- 仓库里成对出现：`xx.md`（主语言）与 `xx-zh.md`（中文译文）或 `xx-en.md`（英文译文）。
- 用户改了一边、要求另一边跟上，或显式要求「中英文同步」「对齐两个文档」。

若命名不同（例如 `README.zh.md`、`README.cn.md`），以用户指明的路径为准；默认按下节约定识别。

## 文件命名约定（默认）

| 角色 | 典型文件名 |
|------|------------|
| 主文（源语言） | `README.md`、`guide.md`、`foo.md` |
| 中文译文 | `README-zh.md`、`guide-zh.md`、`foo-zh.md` |
| 英文译文 | `README-en.md`、`guide-en.md`、`foo-en.md` |

**配对规则**：
- 主文件不含语言后缀（如 `README.md`），其语言由内容判定。
- 若主文是英文 → 中文译文用 `-zh` 后缀：`README.md` ↔ `README-zh.md`。
- 若主文是中文 → 英文译文用 `-en` 后缀：`README.md` ↔ `README-en.md`。
- 去掉译文后缀（`-zh` 或 `-en`，在扩展名之前）即为主文件路径；例如 `concatagents/README-zh.md` ↔ `concatagents/README.md`，`concatagents/README-en.md` ↔ `concatagents/README.md`。

若只有一侧文件，先向用户确认另一侧路径或是否新建。

## 同步原则

1. **结构优先**：标题层级（`#`…`###`）、列表块、代码块边界、表格行列数应对齐；中文侧章节顺序与主文一致，便于对照。
2. **语义一致**：同一小节叙述同一主题；新增/删除/重命名章节时两侧同步增删改。
3. **代码与命令**：代码块、CLI 命令、路径、URL、配置键名保持与主文一致（勿翻译标识符）；仅翻译说明性文字与注释（若中文侧需要注释）。
4. **外链**：中文侧外链可与主文相同；若主文为英文文档链接，中文侧可改为官方中文版（存在且稳定时），否则保留原链接并在括号内说明。
5. **语言切换链接（双向）**：主文与 `-zh.md` 在文档顶部互相链接，便于读者切换语言（见下节）。
6. **Frontmatter**：若存在 YAML frontmatter，键保持一致；`description` 等可分别为英文/中文值。
7. **不臆造事实**：主文未出现的技术细节不要仅在中文侧编造；若一侧有「待办」或占位，两侧用等价标记标出。

## 语言切换链接（`*-zh.md` / `*-en.md` ↔ `*.md`）

同步或新建双语文档对时，**两侧都应在标题下方第一块内容**加入指向对端的相对链接；缺则补、错则改，已有且正确则保留。

### 放置位置

- 紧跟 `# 标题` 之后、正文第一段之前；若已有简介段落，链接放在简介段落**之前**。
- 两侧链接行位置应对齐（都在标题后第一行），不要一侧在页首、另一侧在页尾。

### 链接写法（默认同目录）

| 所在文件 | 链接目标 | 推荐 Markdown |
|----------|----------|---------------|
| 主文（英文）`foo.md` | 中文 `foo-zh.md` | `[中文](foo-zh.md)` 或 `[Read in Chinese](foo-zh.md)` |
| 中文 `foo-zh.md` | 主文（英文）`foo.md` | `[English](foo.md)` 或 `[阅读英文版](foo.md)` |
| 主文（中文）`foo.md` | 英文 `foo-en.md` | `[English](foo-en.md)` 或 `[Read in English](foo-en.md)` |
| 英文 `foo-en.md` | 主文（中文）`foo.md` | `[中文](foo.md)` 或 `[阅读中文版](foo.md)` |

- 使用**相对路径**（与文档同目录时只写文件名）；子目录文档按实际路径写，例如 `[中文](../README-zh.md)`。
- 链接文字：英文侧用 `中文` 或 `Read in Chinese`；中文侧用 `English` 或 `阅读英文版`。同一仓库内风格保持一致。
- 可选格式：单独一行，或 `[English](README.md) \| [中文](README-zh.md)` 放在英文侧；中文侧镜像为 `[English](README.md) \| [中文](README-zh.md)`（顺序可固定为 English 在前）。
- **Badge 按钮格式**（shields.io）：使用 `<p align="center">` 包裹的图片徽章链接，视觉效果更醒目，适合在 README 顶部展示。模板如下：

  中文主文 → 英文译文跳转：
  ```html
  <p align="center">
    <a href="./README-en.md"><img src="https://img.shields.io/badge/Read%20in-English-blue?style=for-the-badge" alt="English Version"></a>
  </p>
  ```

  英文主文 → 中文译文跳转：
  ```html
  <p align="center">
    <a href="./README-zh.md"><img src="https://img.shields.io/badge/%E9%98%85%E8%AF%BB-%E4%B8%AD%E6%96%87-red?style=for-the-badge" alt="中文版"></a>
  </p>
  ```

  可在一个 `<p>` 内并排放多个 badge（如语言切换 + Paper + Demo 等）；`href` 使用相对路径，`img.src` 中文字需 URL 编码。
- **不要**链到错误配对（如 `guide.md` 链到 `other-zh.md`）；重命名文件后同步更新两侧链接。
- 语言切换链接**仅指向配对文档**，与正文外链、锚点链接分开；勿把 GitHub raw URL 或绝对仓库 URL 写进同仓相对文档（除非用户明确要求）。

### 示例

**场景 A：主文为英文，译文为中文**

**`README.md`（英文）**

```markdown
# My Project

[中文](README-zh.md)

Local HTTP shim for ...
```

**`README-zh.md`（中文）**

```markdown
# My Project

[English](README.md)

面向 Claude Code 的本地 HTTP 代理 ...
```

**场景 B：主文为中文，译文为英文**

**`README.md`（中文）**

```markdown
# 我的项目

[English](README-en.md)

面向 Claude Code 的本地 HTTP 代理 ...
```

**`README-en.md`（英文）**

```markdown
# My Project

[中文](README.md)

Local HTTP shim for ...
```

**Badge 按钮示例（场景 A：主文英文 → 中文译文）**

**`README.md`（英文）**

```markdown
<p align="center">
  <a href="./README-zh.md"><img src="https://img.shields.io/badge/%E9%98%85%E8%AF%BB-%E4%B8%AD%E6%96%87-red?style=for-the-badge" alt="中文版"></a>
</p>

# My Project

Local HTTP shim for ...
```

**Badge 按钮示例（场景 B：主文中文 → 英文译文）**

**`README.md`（中文）**

```markdown
<p align="center">
  <a href="./README-en.md"><img src="https://img.shields.io/badge/Read%20in-English-blue?style=for-the-badge" alt="English Version"></a>
</p>

# 我的项目

面向 Claude Code 的本地 HTTP 代理 ...
```

## 推荐工作流（Agent）

1. **定位配对**：根据用户给出的文件或 glob，解析出 `xx.md` 与 `xx-zh.md` 或 `xx-en.md`。
2. **做结构 diff**：比对标题大纲与主要块（段落 / 列表 / 代码 / 表格）；列出「仅一侧存在」的块。
3. **定主从**：用户指定以哪边为准；未指定时以**本次编辑所改文件**为准，另一份跟进；若两边都大改，先合并主文再翻译/改写译文。
4. **改稿**：先更新主文（若需要），再按结构逐节更新译文（`-zh.md` 或 `-en.md`，或反向），避免遗漏孤立段落。
5. **补语言链接**：确认两侧标题下均有指向对端的相对链接；新建译文或重命名后必须同步更新。
6. **自检**：再次比对标题列表长度与顺序；检查代码块语言标签与内容是否一致；内部链接锚点（若有）是否仍有效；语言切换链接是否双向可达。

## 验收清单（完成前勾选）

- [ ] 两侧一级标题数量与顺序一致（或刻意差异已用注释说明）。
- [ ] 无「主文已删、中文仍保留」的过期整节（除非用户要求保留历史说明）。
- [ ] 代码块、命令、JSON/YAML 片段与主文一致。
- [ ] 英文文档顶部有指向 `-zh.md` 或主文的链接；中文文档顶部有指向 `-en.md` 或主文的链接；路径与配对文件名正确。
- [ ] 未在答复中泄露密钥或隐私；文档内敏感示例已脱敏。

## 与 verbatim 用户文案的关系

若用户在任务里粘贴了**必须逐字使用**的段落（中英任一），将该段**原样**写入目标文件，不转述、不润色、不调换语序；其余部分仍按上表原则同步。

## 可选延伸阅读

若单文件过长，可将完整术语表或长附录拆到同目录 `reference.md`，两语言各一份或共享一份，并在两份主文档中链接；本 skill 不强制拆分。
