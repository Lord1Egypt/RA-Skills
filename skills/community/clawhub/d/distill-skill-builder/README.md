# distill-skill-builder

> 将官方文档蒸馏为结构化知识技能的流水线方法论

## 什么是 distill-skill-builder

`distill-skill-builder` 是一套将官方文档、技术手册、API 文档蒸馏为高质量知识技能（Knowledge Skill）的系统性方法论。它不依赖任何特定网站或平台——任何可访问的文档源都可以通过这套流水线转化为可被 AI 助手直接使用的技能。

一个 A 级 skill 能让 AI 在对应领域达到专家级别的输出质量，而不是泛泛而谈。

## 核心能力

- **通用爬取策略**：静态 HTML → `requests + BeautifulSoup`；动态渲染 → `playwright` 无头浏览器
- **知识蒸馏法**：无法爬取的 SPA 站点，基于领域知识结构编写结构化参考文档
- **8 维质量评估**：触发词、元数据、核心内容、快速参考、避坑指南、来源标注、参考文档、输出格式
- **A 级标准**：综合得分 ≥90 为 A 级，≥95 为 A+ 级
## 流水线概览

```
Phase 1: 源分析
  └── 确定文档源 → 判断类型（静态/动态）→ 选择爬取方案

Phase 2: 内容采集
  └── 爬取或蒸馏内容 → 直接保存到 references/

Phase 3: 内容组织
  └── 创建 SKILL.md（主技能文件）
  └── 创建 references/*.md（深度参考文档）

Phase 4: 评估打分
  └── 运行 skill_evaluator_v2.py
  └── 识别短板（触发词/来源/H1 结构/快速参考/避坑指南）

Phase 5: 迭代修复
  └── 按 ROI 排序修复（3 分钟 +12 分 / 5 分钟 +6 分）
  └── 循环 Phase 4 直到达到 A 级

Phase 6: 同步部署
  └── 同步到 <hermes_dir>/<name>/
  └── 提交到 GitHub 分发
```

## 快速开始

### 目录结构

```
distill-skill-builder/
├── SKILL.md                      # 流水线主技能文件
├── README.md                     # 本文件
├── scripts/
│   └── skill_evaluator_v2.py    # 评估脚本（用于评估其他 skill）
└── references/                   # 参考文档（9 个）
    ├── distillation-workflow.md   # 完整蒸馏流程
    ├── evaluator-guide.md        # 评估器使用详解
    ├── metadata-spec.md          # frontmatter 字段规范
    ├── skillmd-structure.md       # SKILL.md 内部结构
    ├── iteration-guide.md        # 迭代提分实战手册
    ├── crawling-guide.md          # 通用爬取方法论
    ├── naming-conventions.md      # 命名与分类规范
    ├── quality-standards.md       # 评分等级标准
    └── self-checklist.md          # 质量自检清单
```

### 评估一个 Skill

评估脚本位于 `scripts/skill_evaluator_v2.py`（集中管理，不在各 skill 目录下复制）。

```bash
python scripts/skill_evaluator_v2.py <skill_dir>/<your-skill>
```

### 创建新 Skill（使用流水线）

1. **分析源**：确定目标文档 URL，判断静态还是动态
2. **采集内容**：爬取或蒸馏内容，直接保存到 `references/`
3. **组织结构**：创建 SKILL.md 和 `references/` 参考文档
4. **评估打分**：运行评估脚本，识别短板
5. **迭代修复**：按 ROI 优先级修复每个短板
6. **同步部署**：同步到 `<hermes_dir>/<name>/`，提交到 GitHub

详细流程见 [references/distillation-workflow.md](references/distillation-workflow.md)。

## 质量评级

| 等级 | 综合得分 | 说明 |
|------|----------|------|
| A+ | 95-100 | 接近完美，有少量优化空间 |
| A | 90-94 | 达到专业标准，可分发 |
| B | 70-89 | 可用，但有明显改进空间 |
| C | 50-69 | 基础框架，需要大量改进 |
| D | 30-49 | 非常基础 |
| F | 0-29 | 几乎无内容 |

## 评估维度详解

| 维度 | 满分 | 达标线 | 检查项 |
|------|------|--------|--------|
| 触发词覆盖 | 15 | 15/15 | 单行格式，30+ 个触发词 |
| 元数据完整性 | 10 | 10/10 | name/description/trigger/tags 齐全 |
| 核心内容深度 | 20 | 20/20 | H1≥5 + H2≥10 + 代码块≥10 |
| 快速参考 | 15 | 15/15 | 表格≥5 + 代码块≥10 + 关键数值≥10 |
| 避坑指南 | 15 | 15/15 | 对比表格≥3 |
| 来源标注 | 10 | 9-10/10 | 官方 URL≥3 + 日期 + 来源标记 |
| 参考文档覆盖 | 10 | 9-10/10 | 文件≥6 + 平均行数≥300 |
| 输出格式规范 | 5 | 5/5 | 回复结构 + 示例 + 禁用格式 |

## 成功案例

| Skill | 平台 | 评分 | 说明 |
|-------|------|------|------|
| [Apple Design](https://github.com/yhongm/apple-higDesign-skill) | Apple HIG | 99.0 A+ | Apple 官方人机交互指南 |
| [iOS Dev](https://github.com/yhongm/ios-dev-skill) | iOS/SwiftUI | 96.5 A | SwiftUI / UIKit / Xcode |
| [Material Design](https://github.com/yhongm/material-design-skill) | Google M3 | 96.0 A | Material Design 3 跨平台设计系统 |
| [HarmonyOS Dev](https://github.com/yhongm/harmonyos-dev-skill) | HarmonyOS | 92.5 A | ArkTS / Stage 模型 |
| [Flutter Dev](https://github.com/yhongm/flutter-dev-skill) | Flutter | 91.0 A | Widget 体系 / Riverpod / M3 迁移 |

## 贡献

这套方法论基于多个 A 级 skill 的蒸馏经验总结而成。如有改进建议，欢迎提交 Issue 或 PR。

## 许可

MIT
