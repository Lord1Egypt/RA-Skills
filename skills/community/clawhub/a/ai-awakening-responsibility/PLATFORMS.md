# 分发平台矩阵 · Distribution Platforms

> 本包同时面向**两类分发渠道**：只接收纯文本的技能市场（Skill Hub）与支持二进制的代码仓库（GitHub / ClawHub）。
> This package targets **two kinds of distribution channel**: text-only skill marketplaces (Skill Hub) and binary-capable code repositories (GitHub / ClawHub).

---

## 一、为什么要做双格式并存

《AI觉醒·责任》论文集的每一篇都同时提供 **Markdown / Word / PDF** 三种格式，母文献《AI宣言》同样如此。三者不是备份关系，而是**分工关系**：

| 格式 | 角色 | 唯一性|
|---|---|---|
| `.md` | **唯一源 + 完整可读源**。内容由此生成，任何环境（含只接收纯文本的技能市场）都能读全 | 唯一权威源 |
| `.docx` | 正式阅读与批注 editable 本地编辑 | 由MD 派生 |
| `.pdf` | 正式阅读、打印、版面固定存档 | 由 MD 派生 |

**关键约束**：并非所有渠道都能承载二进制文件。若只提供 Word/PDF，则在纯文本渠道上整包内容归零；若只提供 Markdown，则失去可编辑与可打印的正式形态。因此**两者必须并存，不得互相替代**。

---

## 二、平台能力对照表

| 平台 | 二进制 `.docx` / `.pdf` | `.md` 文本 | 实测行为 |
|---|---|---|---|
| **Skill Hub**（技能市场上传） | ❌ 不支持，上传时自动过滤 | ✅ 保留 | 上传后仅存 `.md`，`docx版/`、`PDF版/` 变为空目录 |
| **GitHub** | ✅ 完整保留 | ✅ 保留 | 三格式齐备，`.md` 在网页端直接渲染 |
| **ClawHub** | ✅ 完整保留 | ✅ 保留 | 三格式齐备|

### 各渠道拿到的内容对照

| 内容 | Skill Hub | GitHub | ClawHub |
|---|---|---|---|
| 中文版 8 篇正文 | ✅ 完整（MD） | ✅ 完整（MD+Word+PDF） | ✅ 完整（MD+Word+PDF） |
| 英文版 8 篇正文 | ✅ 完整（MD） | ✅ 完整（MD+Word+PDF） | ✅ 完整（MD+Word+PDF） |
| 母文献《AI宣言》中英文 | ✅ 完整（MD） | ✅ 完整（MD+Word+PDF） | ✅ 完整（MD+Word+PDF） |
| 术语表 `GLOSSARY.md` | ✅ | ✅ | ✅ |
| 许可证 `LICENSE` / `LICENSE.md` | ✅ | ✅ | ✅ |
| Word / PDF 正式版 | ❌ 被过滤 | ✅ | ✅ |

**结论**：三个渠道都能拿到**完整的文本内容**；GitHub / ClawHub 额外提供可编辑与可打印的正式版。

---

## 三、为什么专门给母文献补Markdown

本系列七篇分论的 Markdown 本来就在包内（`AI觉醒-责任（中文版）/MD版/`、`AI-Awakening-Responsibility（English(英文版)）/MD版/`），**唯母文献《AI宣言》此前只有 Word/PDF 四份**。

后果是：上传 Skill Hub 后，母文献会被整体过滤，导致 `SKILL.md` 中反复声明的"《AI宣言》是本技能母文献 / this skill's parent work"这一承接关系，在上传副本中**断链**——技能声称承接某文献，读者却找不到该文献。

补入两份 Markdown 后：

```
AI宣言AI-Manifesto集/
├── AI宣言-公开版.md        ← 新增：中文宣言正文（唯一源）
├── AI宣言-公开版.docx      （保留）
├── AI宣言-公开版.pdf       （保留）
├── AI-Manifesto-Public.md  ← 新增：English manifesto body (single source)
├── AI-Manifesto-Public.docx（保留）
└── AI-Manifesto-Public.pdf （保留）
```

**任何渠道拿到的副本，都能读到完整的中英母文献，承接关系不再断链。**

---

## 四、许可证为何有 `.md` 与无扩展名两份

- `LICENSE`（无扩展名）—— 符合 CC BY 4.0 与多数工具链的惯例命名（如 `LICENSE`、`LICENSE.txt`）
- `LICENSE.md`（同一内容）—— GitHub 等代码托管平台默认**不渲染无扩展名文件**；补一份`.md` 后，许可证在网页端直接可读

两份内容**逐字节完全相同**（MD5 一致），不存在版本分歧。

---

## 五、上传操作清单

**上传 Skill Hub（纯文本渠道）**

1. 直接上传整个目录
2. 上传后自查：`docx版/`、`PDF版/` 是否为空目录（属预期行为，非上传失败）
3. 确认 `MD版/` 两处共 14 份文件、`AI宣言AI-Manifesto集/` 内 2 份 `.md` 均在位

**推送到 GitHub / ClawHub（二进制渠道）**

1. 连同 `docx版/`、`PDF版/` 一并提交
2. 建议在 README 顶部或 Releases 中提供 PDF 版本下载直链
3. 建议打tag（如 `v1.0.0`）并附 zip 发行包，便于版本回溯

---

## 六、语言适配与渠道无关

无论从哪个渠道获取本包，**语言适配路由完全一致**——它由包内文件结构保证，与平台无关：

| 用户语言 | 主用路径 | 交叉引用 |
|---|---|---|
| 中文 | `AI觉醒-责任（中文版）/MD版/` + `AI宣言-公开版.md` | 英文版同名篇目（仅核对术语英译） |
| English | `AI-Awakening-Responsibility（English(英文版)）/MD版/` + `AI-Manifesto-Public.md` | 中文版同名篇目（仅核对中文原义） |

**关键**：两条路径**全部由 `.md` 文件构成**。这意味着即使在只保留 Markdown 的 Skill Hub 上，语言适配依然完整可用——**没有任何一步依赖二进制文件**。详见 `SKILL.md` 的「语言适配路由」节（中英双语）与 `README.md` 的「Language routing」节。

---

## 七、English Summary

This corpus ships in **three coexisting formats per document** — Markdown, Word, and PDF. They are not backups of one another but division-of-labour roles:

- **`.md`** — the single source of truth and the only format readable in *every* environment, including text-only skill marketplaces.
- **`.docx`** — formal reading, annotation, and local editing (derived).
- **`.pdf`** — formal reading, printing, and fixed-layout archiving (derived).

**Channel capabilities**: Skill Hub accepts text formats only and will strip `.docx`/`.pdf` on upload, yet the complete text of all eight volumes plus the bilingual parent work survives. GitHub and ClawHub retain all three formats.

**Why the parent work needed Markdown versions**: the eight volumes already carried their `.md` files, but the parent work *AI Manifesto* existed only as Word/PDF. In a text-only upload it would have been stripped entirely, severing the parent-work lineage that `SKILL.md` declares. Two `.md` files were added to close that gap.

**Why two license files**: `LICENSE` (no extension) follows CC and tool-chain convention; `LICENSE.md` (byte-identical) renders directly on GitHub, which does not display extensionless files.

Neither format set should ever be removed — they serve different channels, and the Markdown layer is what guarantees the corpus stays complete and readable wherever it lands.
