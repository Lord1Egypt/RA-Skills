---
name: simple-review-analyzer
description: |
  AI驱动的电商评论深度分析工具，支持22维度智能标签、用户画像识别、VOC洞察和可视化看板生成。

  当用户需要以下功能时触发：
  - 分析电商产品评论（Amazon/eBay/AliExpress等平台）
  - 从评论中提取用户画像、痛点和VOC（客户之声）
  - 生成产品洞察报告和机会点分析
  - 创建专业的可视化分析看板
  - 进行竞品分析和市场定位研究

  触发关键词：电商评论分析、评论分析、竞品分析、用户洞察、VOC分析、产品优化、市场调研、评论数据挖掘

  AI Agent 约束：必须通过 AskUserQuestion 收集分析数量后再执行分析
license: MIT
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Write
  - Edit
---

# Simple Review Analyzer

AI驱动的电商评论深度分析工具，提供22维度智能标签、用户画像识别和专业的可视化看板。

## 核心特性

### 22维度智能标签系统
全面覆盖评论信息的8大维度：
- **人群维度 (4)**: 性别、年龄段、职业、购买角色
- **场景维度 (1)**: 使用场景
- **功能维度 (2)**: 满意度、具体功能
- **质量维度 (3)**: 材质、做工、耐用性
- **服务维度 (5)**: 发货速度、包装质量、客服响应、退换货、保修
- **体验维度 (4)**: 舒适度、易用性、外观设计、价格感知
- **市场维度 (2)**: 竞品对比、复购意愿
- **情感维度 (1)**: 总体评价

### 三位一体输出
1. **CSV标签数据**: 原始评论 + 22维度 AI 标签
2. **Markdown洞察报告**: 战略机会点、痛点、优化建议
3. **HTML可视化看板**: 6个交互式图表、黑金设计

### 四位一体VOC系统
- 用户画像识别（3-4类典型用户）
- 黄金样本（每类6条精选评论）
- 3D头像系统（6种风格）
- 情感分析（分布与关键词）

## 快速开始

### 首次使用

1. 准备 CSV 文件（支持自动模糊匹配列名）
2. 在 Claude Code 中调用：
   ```
   请分析这个产品的评论：reviews.csv
   ```

### CSV 文件格式要求

**必需列**（自动模糊匹配）：
- 评论内容：内容/评价/body/review/text/comment
- 评分：打分/rating/score/star

**可选列**：
- 时间：时间/date/日期/time
- 标题：标题/title/summary
- 用户名：用户/user/username

## 核心工作流程

### 第一步：收集参数
使用 AskUserQuestion 收集：
- 分析数量（100条/300条/全部）

### 第二步：执行分析
1. 读取并解析 CSV 文件
2. 批量标签提取（每批最多30条）
3. 统计分析与用户画像识别
4. 生成洞察报告
5. 生成 HTML 可视化看板

### 第三步：展示结果
在 `output/` 目录下按**产品名_日期**创建文件夹，生成三种报告：

```
output/
├── 产品A_20260320/
│   ├── reviews_labeled.csv
│   ├── 分析洞察报告.md
│   └── 可视化洞察报告.html
├── 产品B_20260321/
│   ├── reviews_labeled.csv
│   ├── 分析洞察报告.md
│   └── 可视化洞察报告.html
└── ...
```

**命名规则**：
- 文件夹：`{产品名}_{日期YYYYMMDD}`
- CSV：`reviews_labeled.csv`
- Markdown：`分析洞察报告.md`
- HTML：`可视化洞察报告.html`

## 技术架构

### 文件结构
```
simple-review-analyzer/
├── skill.md              # Skill 定义文件
├── prompts/              # 提示词模板
│   ├── tagging.txt      # 单条评论打标
│   ├── tagging_batch.txt # 批量打标
│   └── insights.txt     # 洞察报告生成
├── templates/            # 输出模板
│   └── report.html      # HTML 可视化模板
└── utils/               # 工具脚本
    ├── transform_logic.py  # JSON↔CSV双向转换工具
    └── csv_reader.sh    # CSV 读取辅助

输出文件：生成到 output/{产品名}_{日期}/ 目录
```

### 提示词模板
- **单条打标**: 基于 prompts/tagging.txt，分析单条评论返回22维度标签
- **批量打标**: 基于 prompts/tagging_batch.txt，一次处理最多30条评论
- **洞察报告**: 基于 prompts/insights.txt，生成深度分析报告

## 使用场景

### 场景1：产品优化
分析自己产品的评论，发现用户痛点，优化产品功能和设计。

### 场景2：竞品分析
分析竞品评论，了解竞争对手的优势和劣势，寻找差异化机会。

### 场景3：市场调研
批量分析多个产品的评论，了解市场需求、用户偏好和行业趋势。

### 场景4：用户洞察
深度了解目标用户群体，构建精准用户画像，优化营销策略。

## 输出文件说明

### CSV 标签数据
- 原始评论数据（保留所有原始列）
- 22维度 AI 标签列（新增）
- 用途：数据分析、导入 BI 工具、筛选过滤

### Markdown 洞察报告
- 执行摘要：分析概述、关键发现
- 战略机会点：市场机会、产品差异化
- 用户痛点：问题分类、改进建议
- 用户画像：典型用户类型、需求特点
- VOC 分析：黄金样本、情感分布

### HTML 可视化看板
- 黑金奢华设计风格
- 6个交互式 Chart.js 图表
- 响应式设计，支持移动端
- 纯 HTML 文件，可直接浏览器打开

## 工具使用

### transform_logic.py - 数据格式转换工具

位置：`utils/transform_logic.py`

**功能**：JSON（嵌套结构）与 CSV（扁平格式）之间的双向转换

**使用方法**：

```bash
# JSON → CSV（扁平化输出，22维度标签展开为独立列）
python3 .claude/skills/simple-review-analyzer/utils/transform_logic.py json \
    tagged_reviews.json \
    reviews_labeled.csv

# CSV → JSON（恢复嵌套结构，22维度标签聚合为tags对象）
python3 .claude/skills/simple-review-analyzer/utils/transform_logic.py csv \
    reviews_labeled.csv \
    tagged_reviews.json
```

**数据结构对比**：

| JSON (嵌套) | CSV (扁平) |
|-------------|------------|
| `tags.人群_性别` | `人群_性别` |
| `tags.场景_使用场景` | `场景_使用场景` |
| `tags.功能_满意度` | `功能_满意度` |
| ... | ... |

**应用场景**：
- 将AI分析结果导出为Excel/BI工具兼容格式
- 从已有标签数据恢复嵌套JSON结构
- 数据格式验证和转换

## 注意事项

1. **分析数量**: 推荐选择 100 条评论以平衡速度与质量
2. **并发限制**: 每批最多处理 30 条评论
3. **输出目录**: `output/{产品名}_{日期}/` （自动创建）
4. **文件命名**: 固定文件名，便于对比同一产品的多次分析
5. **编码支持**: UTF-8/GBK/GB2312 自动检测
6. **工具使用**: 可单独使用 `transform_logic.py` 进行数据格式转换

