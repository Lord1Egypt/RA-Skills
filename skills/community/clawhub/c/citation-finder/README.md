# Citation Finder 文献查找与引文格式化

> 输入模糊文献标题，自动搜索中英文学术数据库，返回 GB/T 7714、APA、MLA 三种标准引文格式。

---

## ✨ 功能

- 🔍 **双语搜索**：同时搜索中文（百度学术、CNKI）和英文（CrossRef、Semantic Scholar）数据库
- 🎯 **模糊匹配**：基于标题相似度算法，处理不完整或有误的标题
- 📝 **三种格式**：一键输出 GB/T 7714-2015、APA 7th、MLA 9th 引文
- 🔗 **原始链接**：提供 DOI 或数据库链接方便原文查阅
- 🤔 **歧义处理**：匹配度不足时列出候选，由用户确认

---

## 🚀 快速开始

### 安装依赖

```bash
pip install requests beautifulsoup4 rapidfuzz
```

### 命令行使用

```bash
# 英文文献
python scripts/run.py "attention is all you need"

# 中文文献
python scripts/run.py "注意力机制在自然语言处理中的应用"

# 模糊描述
python scripts/run.py "transformer architecture neural machine translation 2017"
```

### 作为 OpenClaw Skill 使用

本项目为 [OpenClaw](https://openclaw.woa.com) Agent Skill 格式，安装后可直接通过对话触发：

> "帮我找一下 Attention is All You Need 的引用格式"

---

## 📁 项目结构

```
citation-finder-skill/
├── SKILL.md              # OpenClaw skill 配置
├── README.md
├── scripts/
│   ├── run.py            # 主入口
│   ├── search_en.py      # 英文搜索（CrossRef + Semantic Scholar）
│   ├── search_cn.py      # 中文搜索（百度学术 + CNKI）
│   └── format_cite.py    # 引文格式化（GB/T 7714 / APA / MLA）
└── assets/
```

---

## 📖 引文格式示例

输入：`attention is all you need`

**GB/T 7714-2015**
```
Vaswani A., Shazeer N., Parmar N., 等. Attention Is All You Need[J]. Advances in Neural Information Processing Systems, 2017, 30: 5998-6008. DOI: 10.48550/arXiv.1706.03762.
```

**APA 7th**
```
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30, 5998-6008. https://doi.org/10.48550/arXiv.1706.03762
```

**MLA 9th**
```
Vaswani, Ashish, et al. "Attention Is All You Need." Advances in Neural Information Processing Systems, vol. 30, 2017, pp. 5998-6008. doi:10.48550/arXiv.1706.03762.
```

---

## 🗃️ 数据源

| 数据源 | 语言 | 说明 |
|--------|------|------|
| CrossRef API | 英文 | 免费，DOI 权威库，覆盖广 |
| Semantic Scholar API | 英文 | 免费，AI/CS 论文覆盖优秀 |
| 百度学术 | 中文 | 中文文献主要来源 |
| CNKI | 中文 | 兜底搜索 |

---

## ⚠️ 注意事项

- 中文数据库（百度学术/CNKI）为网页抓取，可能受反爬限制影响
- 付费墙内的全文仅提供 DOI/摘要链接，不提供全文
- 建议在引用前人工核对引文细节

---

## 📄 License

MIT License

---

*Built as an OpenClaw Agent Skill · Powered by CrossRef, Semantic Scholar, Baidu Scholar*
