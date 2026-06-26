---
name: academic-ppt-generator
description: |
  从学术文献PDF自动生成学术汇报PPT的完整工具链。
  
  **使用场景**:
  (1) 需要根据文献快速生成学术汇报PPT
  (2) 文献阅读后的内容整理与可视化呈现
  (3) 组会汇报、文献分享、学术报告准备
  (4) 需要结构化展示研究问题、方法、结论、局限
  
  **触发关键词**: "文献PPT", "汇报PPT", "学术汇报", "文献整理", "自动生成PPT",
  "presentation", "组会汇报", "文献分享"
  
  **工作流程**: 分析PDF → 提取关键信息 → 生成PPT结构 → 导出PowerPoint文件
---

# 学术汇报PPT生成器

从学术文献PDF自动生成结构化的学术汇报PPT，遵循学术汇报的标准框架。

## 功能特点

- **结构化输出**: 按照学术汇报的标准四部分组织内容
- **智能分析**: 自动提取文献的关键信息
- **专业排版**: 学术风格的配色和版式设计
- **演讲者备注**: 每页附带演讲提示

## 标准PPT结构

### Part 1: 科学问题与背景 (1-2页)
- 核心研究问题
- 研究背景
- 前人工作
- 研究空白
- 理论假设

### Part 2: 研究方法 (2-3页)
- 实验设计概述
- 被试/样本信息
- 实验流程
- 控制变量
- 方法-理论对应

### Part 3: 结论与验证 (多页)
- 主要发现（每页一个）
- 支持证据
- 假设验证结果
- 结论逻辑链

### Part 4: 研究局限 (1页)
- 方法局限
- 结果局限
- 未来研究方向

### 总结页
- 核心贡献

## 使用方法

### 完整工作流程

```
文献PDF → 分析提取 → JSON结构 → PPT文件
```

#### 步骤1: 分析文献PDF

阅读文献，提取关键信息，整理为JSON格式。参考 `references/analysis_guide.md` 了解提取要点。

#### 步骤2: 生成PPT结构

```bash
python scripts/generate_ppt_structure.py analysis.json > structure.json
```

#### 步骤3: 导出PowerPoint

```bash
python scripts/export_ppt.py structure.json output.pptx
```

### 依赖安装

```bash
pip install python-pptx
```

## 输入格式

分析结果应为JSON格式，包含以下字段：

```json
{
  "title": "论文标题",
  "authors": "作者",
  "venue": "期刊/会议",
  "year": "2024",
  "research_question": "核心问题",
  "background": ["背景要点1", "背景要点2"],
  "previous_work": ["前人工作1", "前人工作2"],
  "research_gap": ["研究空白1", "研究空白2"],
  "hypothesis": ["假设1", "假设2"],
  "experimental_design": ["设计要点"],
  "participants": "被试信息",
  "independent_variables": "自变量",
  "dependent_variables": "因变量",
  "procedure": ["步骤1", "步骤2"],
  "control_variables": ["控制变量1"],
  "method_theory_mapping": ["方法-理论对应"],
  "main_findings": ["发现1", "发现2"],
  "hypothesis_validation": ["验证结果"],
  "conclusion_logic": ["逻辑链"],
  "limitations": ["局限1", "局限2"],
  "contributions": ["贡献1", "贡献2"]
}
```

完整示例见 `references/example_analysis.json`。

## 注意事项

1. **内容简洁**: 每页PPT控制在6个要点以内
2. **逻辑清晰**: 按"问题-方法-结论-局限"的顺序组织
3. **重点突出**: 强调核心发现和理论贡献
4. **建议配图**: 导出后可手动添加关键图表

## 自定义选项

如需调整PPT样式，可修改 `scripts/export_ppt.py`:

- `COLORS` 字典: 修改配色方案
- 字体大小参数: 调整文字尺寸
- 布局常量: 修改页面元素位置
