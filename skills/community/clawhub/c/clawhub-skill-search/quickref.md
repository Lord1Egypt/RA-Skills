# Clawhub 技能搜索快速参考 🚀

**一页纸掌握技能搜索核心技巧**

---

## 快速决策树

```
你的需求是什么？
│
├─ 📚 搜索文献 → citation-management
│   ├─ Google Scholar/PubMed → citation-management
│   └─ arXiv/Semantic Scholar → academic-research-hub
│
├─ ✍️ 论文写作 → academic-writing
│   ├─ 润色语言 → academic-writing --action polish
│   └─ 生成摘要 → academic-writing --type abstract
│
├─ 📄 解析论文 → paper-parse
│   ├─ PDF 文件 → paper-parse --file paper.pdf
│   └─ arXiv URL → paper-parse --url "https://arxiv.org/abs/..."
│
├─ 📊 统计分析 → statistical-analysis
│   ├─ 描述统计 → --type descriptive
│   ├─ t 检验/ANOVA → --type t_test / anova
│   └─ 回归分析 → --type regression
│
├─ 📈 数据可视化 → scientific-visualization
│   ├─ publication-ready → --style journal
│   └─ 自定义图表 → matplotlib
│
└─ 📱 内容发布 → wechat-publisher
    ├─ 发布文章 → wechat-publisher --file article.md
    └─ 渲染排版 → wenyan publish article.md
```

---

## 核心技能速查表

| 技能 | 一句话用途 | 典型命令 |
|------|-----------|---------|
| **citation-management** | 文献搜索 + 引用管理 | `--search "query" --count 10` |
| **academic-writing** | 论文润色 + 写作 | `--file draft.md --action polish` |
| **paper-parse** | PDF 论文解析 | `--file paper.pdf --mode full` |
| **statistical-analysis** | 统计分析 + APA 报告 | `--file data.csv --type t_test` |
| **scientific-visualization** | publication-ready 图表 | `--data results.csv --style journal` |
| **wechat-publisher** | 微信公众号发布 | `--file article.md` |

---

## 触发关键词速查

### 文献搜索类
- "搜索文献" → citation-management
- "找论文" → citation-management
- "Google Scholar" → citation-management
- "PubMed" → citation-management
- "arXiv" → academic-research-hub
- "BibTeX" → citation-management
- "DOI" → citation-management

### 写作类
- "润色" → academic-writing
- "改写" → academic-writing
- "摘要" → academic-writing
- "语法检查" → academic-writing
- "学术写作" → academic-writing

### 分析类
- "t 检验" → statistical-analysis
- "回归" → statistical-analysis
- "ANOVA" → statistical-analysis
- "相关分析" → statistical-analysis
- "描述统计" → data-analysis

### 可视化类
- "画图" → scientific-visualization
- "可视化" → scientific-visualization
- "publication-ready" → scientific-visualization
- "Nature 风格" → scientific-visualization

### 解析类
- "解读论文" → paper-parse
- "PDF 分析" → paper-parse
- "论文总结" → paper-parse

---

## 常用命令模板

### 文献搜索
```bash
# 基础搜索
citation-management --search "subjective wellbeing China" --count 10

# DOI 转 BibTeX
citation-management --doi "10.1038/s41597-023-01234-x" --format bibtex

# 验证引用
citation-management --validate "references.bib"
```

### 论文写作
```bash
# 润色语言
academic-writing --file draft.md --action polish --output polished.md

# 生成摘要
academic-writing --type abstract --input full_paper.md

# 语法检查
academic-writing --file manuscript.md --action grammar_check
```

### 论文解析
```bash
# 解析 PDF
paper-parse --file paper.pdf --mode full

# 解析 URL
paper-parse --url "https://arxiv.org/abs/2301.12345"

# 双模式输出
paper-parse --file paper.pdf --mode dual
```

### 统计分析
```bash
# 描述统计
statistical-analysis --file data.csv --type descriptive

# t 检验
statistical-analysis --file data.csv --type t_test --group_var gender --dv wellbeing

# 回归分析
statistical-analysis --file data.csv --type regression --dv wellbeing --iv age income
```

### 数据可视化
```bash
# publication-ready 图表
scientific-visualization --config nature_style.yaml --data results.csv

# 单图生成
scientific-visualization --type barplot --data data.csv --style journal
```

### 内容发布
```bash
# 发布到公众号
wechat-publisher --file article.md

# 创建草稿
wechat-mp-publish --action create_draft --title "标题" --content "内容"

# 渲染发布
wenyan publish article.md
```

---

## 问题排查速查

### 技能未触发
```bash
# 检查技能列表
openclaw skills list

# 启用技能
openclaw skills enable <skill-name>

# 手动调用
openclaw skill run <skill-name> --help
```

### 技能报错
```
1. 检查文件路径 → ls <filepath>
2. 验证参数名称 → <skill> --help
3. 查看技能文档 → read SKILL.md
4. 检查依赖安装 → pip list | grep <package>
```

### 输出不符合预期
```
1. 检查输入质量（数据/文本）
2. 调整参数配置
3. 提供更详细的上下文
4. 尝试迭代优化
```

---

## 最佳实践清单

### ✅ 必做
- [ ] 使用具体关键词（包含研究对象、方法、地区）
- [ ] 提供上下文（研究领域、目标期刊）
- [ ] 设置合理参数（数量限制、输出格式）
- [ ] 及时保存结果（导出文件、备份）
- [ ] 验证输出质量（检查准确性、完整性）

### ❌ 避免
- [ ] 模糊描述（"分析一下"、"帮我弄一下"）
- [ ] 缺少上下文（不提供研究领域）
- [ ] 期望过高（期望一次性完美）
- [ ] 忽视验证（不检查输出质量）
- [ ] 重复劳动（不保存之前结果）

---

## 资源链接

| 资源 | 链接 |
|------|------|
| **Clawhub 官网** | https://clawhub.ai |
| **技能市场** | https://clawhub.ai/skills |
| **OpenClaw 文档** | https://docs.openclaw.ai |
| **社区 Discord** | https://discord.com/invite/clawd |

---

**快速上手**: 保存此页为书签，需要时快速查阅！🔖

**版本**: v1.0 | **更新**: 2026-03-15 | **许可**: Apache 2.0
