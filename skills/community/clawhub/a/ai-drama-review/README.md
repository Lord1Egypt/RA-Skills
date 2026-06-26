# ai-drama-review

> AI 短剧合规审查技能包 — OpenClaw / ClawHub Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-ai--drama--review-blue)](https://clawhub.com/skills/ai-drama-review)
[![Stage](https://img.shields.io/badge/stage-beta-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

AI 短剧内容合规审查技能包，提供**版权侵权检测**、**年龄分级扫描**、**小说魔改评估**三大能力，采用本地关键词快速扫描 + AI 深度语义分析的两层架构。

---

## 核心能力

### 1. 版权侵权检测

三重相似度算法交叉验证：

| 算法 | 检测能力 | 权重 |
|------|---------|------|
| n-gram Jaccard 系数 | 局部词汇重复 | 0.3 |
| 归一化编辑距离 | 整体文本差异 | 0.3 |
| TF-IDF 余弦相似度 | 语义主题相似 | 0.4 |

综合得分 > 0.7 的段落标记为疑似侵权，再由 AI 进行语义级确认排除误报。

### 2. 年龄分级合规检测

两层扫描架构：

- **Layer 1 — 本地快速扫描**：分类关键词库（暴力 / 色情 / 恐怖 / 脏话 / 烟酒毒品）逐段扫描
- **Layer 2 — AI 上下文分析**：排除否定语境、文学修辞、历史引用等误报

输出分级：`全年龄` / `12+` / `18+` / `不合规`

### 3. 小说魔改检测

- 动态规划算法（Needleman-Wunsch 变体）对齐原著与改编版结构
- 角色偏离检测（性格 / 关系 / 命运改动）
- 偏离度评分：`0-30 忠实改编` / `30-60 合理改编` / `60-100 严重魔改`

### 4. 结构化合规报告

汇总所有检测结果，输出：

- 总体风险等级（低 / 中 / 高 / 严重）
- 违规位置精确标注
- 针对性整改建议清单

---

## 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install ai-drama-review

# 或 clone 本仓库
git clone https://github.com/AAAlenwow/ai-drama-review.git
```

### 环境配置

```bash
# AI 深度分析（可选，启用混合模式以提高精度）
export OPENAI_API_KEY="your-key"
# 或
export ANTHROPIC_API_KEY="your-key"
```

无 API 密钥时自动降级为**纯本地模式**（仅关键词匹配 + 文本算法），仍可使用。

### 一键完整审查

```bash
python3 scripts/review_orchestrator.py \
  --input script.txt \
  --reference-dir ./references/ \
  --original original_novel.txt \
  --target-rating 12+ \
  --checks copyright rating adaptation
```

### 单项检测

```bash
# 版权检测
python3 scripts/text_similarity.py --input script.txt --reference-dir refs/

# 年龄分级
python3 scripts/age_rating_scanner.py --input script.txt --target-rating 12+

# 魔改检测
python3 scripts/adaptation_detector.py --original novel.txt --adapted script.txt

# 生成报告
python3 scripts/report_generator.py --results results.json --format markdown
```

---

## 项目结构

```
ai-drama-review/
├── SKILL.md                          # 技能定义（ClawHub 入口）
├── scripts/
│   ├── review_orchestrator.py        # 完整审查编排
│   ├── text_similarity.py            # 版权侵权检测
│   ├── age_rating_scanner.py         # 年龄分级扫描
│   ├── adaptation_detector.py        # 小说魔改检测
│   ├── content_analyzer.py           # 内容分析
│   ├── report_generator.py           # 报告生成
│   ├── credential_manager.py         # 凭证管理
│   └── env_detect.py                 # 环境检测
├── assets/
│   ├── keyword_databases/            # 分类关键词库
│   ├── rating_rules/                 # 分级规则
│   └── report_templates/             # 报告模板
├── references/                       # 参考文档
└── tests/                           # 测试
```

---

## 依赖

- Python 3.8+
- jieba（可选，提升中文分词精度）
- AI API 密钥（可选，启用混合模式）

---

## 免责声明

本技能包提供的合规检测结果**仅供参考，不构成法律意见**。使用者应结合专业法律顾问的意见做出最终判断。检测结果可能存在误报或漏报，建议对高风险内容进行人工复核。
