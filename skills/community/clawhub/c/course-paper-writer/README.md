# Course Paper Writer · 课程论文写作

把一份"作业要求文件"变成一份"可以交的 Word 论文"。

不是帮你写一段文字，而是把整条流水线跑完：**读约束 → 找文献 → 取证 → 搭结构 → 成文 → 清文风 → 排版 → 自查 → 交付**。

---

## 它解决什么问题

课程论文的失分，很少是因为"写得不够好"，多半是因为**要求没对齐**：

- 字数写了 5200，要求 3500–5000
- 摘要 343 字，要求 250–300
- 参考文献 20 条，其中 18 条是网页和公告，真正发表的论文只有 2 篇
- 近 5 年文献占比算成 68%，其实只有 52%（把网址里的访问日期当成了出版年）
- 字体设了"宋体"，但只设了西文，Word 用别的字体渲染汉字
- 引用序号 1–20 连续，但正文的 [1] 指向了文献表里的另一篇
- 时间线写"两个月后"，实际只有一个月
- 通篇"随着科技的发展""具有重要意义"

这个 Skill 把这些全部变成**可执行的检查**。

---

## 什么时候会触发

- "写一篇《工程伦理》结课论文，正文 3500–5000 字，参考文献不少于 10 篇"
- "根据这个 PDF 里的要求写课程论文，交 Word"
- "期末论文，要有 2 个真实案例，用功利主义和义务论分析"
- "帮我把这篇的参考文献改成 GB/T 7714 格式"
- "这几段读起来太像 AI 了，改一下"
- "把这篇草稿按学校格式排一下，宋体小四 1.5 倍行距"

不适用：投稿论文、需要实验数据的科研论文、纯文学创作。

---

## 工作流程

```
① 读要求文件          extract_doc.py / extract_pdf.py
     ↓                填满硬约束表（字数/字体/文献/案例/评分权重）
② 题目 → 问题链        拆成能回答的问题；先判"困境 vs 失范"
     ↓
③ 找文献              literature-search.md
     ↓                检索式、追引用链、三分钟筛一篇
④ 联网取证            evidence-protocol.md
     ↓                三档源 + 记录表 + 查不到标"待定"
⑤ 结构                paper-structures.md
     ↓                六种文体骨架，反模板三条
⑥ 写并清文风          ai-voice.md
     ↓                12 类病灶 + 保留清单
⑦ 引文                citation-formats.md
     ↓                GB/T 7714 为主，附 APA/IEEE/MLA
⑧ 生成 DOCX           docx_helpers.py，⟦n⟧ 占位符 + 自动重排
     ↓
⑨ 自查交付            check_paper.py + citation_formatter.py + 五视角通读
```

---

## 三个它特别擅长的点

### 一、去 AI 味（12 类病灶）

| 病灶 | 例子 |
|---|---|
| 意义通胀 | "标志着重要转折""具有里程碑意义" |
| 引言三连问 | "本文要回答的是：A 是什么，B 为什么……" |
| 摘要表态 | "据此，本文主张……" |
| 动词强过证据 | 两个案例就"证明"了普遍规律 |
| 创新性注水 | "首次提出""填补空白"（无检索证据） |
| 公式化开头 | "随着科技的飞速发展……" |
| 连接词堆砌 | 连续三句"此外""同时""另外" |
| 超长从句 | 一句话三个分句两个"而" |
| 破折号滥用 | 一页两个"——" |
| 引用堆砌 | "已有大量研究[3][7][9][12]" |

关键一条：**改文风不改数字、不改结论、不改引用**。还要分清哪些不能删——有证据支撑的限定语（"提示""可能"）是严谨，不是含糊。

### 二、出处可核验

每个论断都要求"答得出凭什么"。查不到就标"待定"，交付时列成待核对清单——**不编造引用**是这个 Skill 的硬约束。

### 三、字数报三档

含小标题 / 不含小标题 / 不含标点。因为**只报一个数一定误导**——上标算不算、小标题算不算，差两百字很常见。摘要单独报含标点和不含标点两档。

---

## 安装

```bash
# 从 ClawHub 安装
clawhub install course-paper-writer
```

或手动放进 skills 目录：

```
~/.dsh/skills/course-paper-writer/
```

依赖：

- Python 3.9+
- `python-docx`（只在生成/检查 .docx 时需要）
- 提取器 `extract_doc.py` / `extract_pdf.py` 是**纯标准库**，不需要 LibreOffice

---

## 目录

```
course-paper-writer/
├── SKILL.md                        主流程（四层加载）
├── clawhub.json                    上架元数据
├── README.md                       本文件
├── scripts/
│   ├── doctor.py                   发布前体检（零依赖）
│   ├── check_paper.py              论文自检（字数/引用/页数）
│   ├── citation_formatter.py       文献表体检（年份/类型/标点）
│   ├── docx_helpers.py             排版函数
│   ├── extract_doc.py              .doc 提取（标准库）
│   └── extract_pdf.py              .pdf 提取（标准库）
└── references/
    ├── literature-search.md        文献检索与筛选
    ├── paper-structures.md         六种文体结构模板
    ├── frameworks.md               学科分析框架
    ├── evidence-protocol.md        取证规范
    ├── ai-voice.md                 AI 文风清理（12 类病灶）
    ├── citation-formats.md         引用格式速查
    ├── docx-formatting.md          排版与字数统计
    ├── self-review.md              五视角交稿自查
    └── pitfalls.md                 14 条实战踩坑
```

---

## 快速试用

```bash
# 1. 检查一篇写好的论文
python scripts/check_paper.py 论文.docx --min 3500 --max 5000 --min-refs 10

# 2. 检查参考文献表
python scripts/citation_formatter.py refs.txt --recent-years 5 --check-punct

# 3. 发布前体检（仅维护者需要）
python scripts/doctor.py .
```

---

## 已知边界

- **不做学术不端**：不伪造数据、不生成虚假引用、不代投期刊。
- **不替你判断学科事实**：涉及标准适用性、材料性能等问题，以你提供的教材与标准原文为准。
- **扫描版 PDF 读不出文字**，会请你手动贴文本，而不是硬猜。
- 页数是**估算**（A4 + 常规页边距 + 小四 1.5 倍行距），精确页数请用 Word 或 LibreOffice 确认。
- 不替代查重，也不帮助规避 AI 使用声明。

---

## 致谢与参考

流程设计参考了公开的学术写作类 Agent Skill 与攻略，主要有：

- [academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) — AI 文风病灶分类与"claim-evidence 配对"思路
- [awesome-paper-research-skills](https://github.com/fengmo11/awesome-paper-research-skills) — 论文全周期阶段划分
- [学术研究助手](https://docs.clawhub.ai/yezhaowang888-stack/skills/academic-research-assistant) — 文献检索/投稿/工具模块的组织方式

本 Skill 只吸收方法论，不包含上述项目的代码或文本。

---

## 版本

- `2.1.0` 扩为全流程：文献检索、结构模板库、AI 文风清理、引用速查、五视角自查、`citation_formatter.py`。
- `2.0.0` 通用化重构：学科无关的取证协议、排版规范、AI 文风清单；新增 `doctor.py`。
- `1.x` 早期版本，仅覆盖工科/思政两类。

## 许可

MIT-0
