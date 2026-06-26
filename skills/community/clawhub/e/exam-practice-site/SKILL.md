---
name: exam-practice-site
description: "考试刷题网站生成器。当用户需要为特定考试（考研、考公、法考、CPA、教师资格证等）搭建一个包含每日抽题、答题判分、错题本、周报分析、题库管理等完整功能的单页刷题网站时，应使用此 skill。触发词：刷题网站、考试题库、每日练习、错题本、题库网站、刷题系统、在线做题。"
---

# 考试刷题网站生成器

## 概述

此 skill 提供一个完整的考试刷题网站框架，将数据驱动的题库系统与交互式前端解耦。
核心思路：**只需替换题库内容（JSON），即可适配任何考试**，无需改动前端代码。

## 适用场景

- 考研（管综、英语、政治、数学等）
- 公务员考试（行测、申论等）
- 司法考试 / 法考
- CPA / 会计职称
- 教师资格证
- 医学考试 / 执业医师
- 任何有题库的标准化考试

## 架构

```
project/
├── index.html              # 单页应用（从 assets/template.html 复制并定制）
├── update_daily.py         # 每日抽题脚本（从 scripts/update_daily.py 复制）
├── data/
│   └── questions/
│       ├── bank.json       # 题库（核心，需按考试定制）
│       ├── today.json      # 今日题目（由脚本自动生成）
│       └── used_ids.json   # 已出题目记录（由脚本自动维护）
```

## 工作流

### 第一步：确认考试类型和题型分类

向用户确认以下信息：

1. **考试名称**：如"公务员行测"、"CPA-会计"、"法考客观题"
2. **题型分类体系**：该考试的题目如何分类？（用于周报分析和过滤）
   - 示例：行测可分为"言语理解"、"数量关系"、"判断推理"、"资料分析"、"常识判断"
   - 示例：CPA会计可分为"存货"、"固定资产"、"金融资产"、"长期股权投资"等
3. **每日题量**：默认 4 道，可根据考试调整（如行测可设 10 道）
4. **题目格式**：单选（默认）还是包含多选/判断/填空？

### 第二步：构建题库 bank.json

题库是此系统的唯一可变数据源。构建一个 `data/questions/bank.json`，格式如下：

```json
{
  "description": "考试名称 — 题库说明",
  "lastUpdated": "YYYY-MM-DD",
  "questions": [
    {
      "id": "唯一ID（建议：来源年份+题号，如 2024-26）",
      "type": "题目类型（如 single_choice, multi_choice, true_false）",
      "category": "题型分类（用于周报统计，如 言语理解-逻辑填空）",
      "source": "题目来源（如 2024年国考行测·第26题）",
      "question": "题目正文",
      "options": ["A. 选项A", "B. 选项B", "C. 选项C", "D. 选项D"],
      "answer": "正确答案（选项字母，如 A）",
      "explanation": "解析内容"
    }
  ]
}
```

**关键设计原则**：
- `category` 字段支持二级分类（如"判断推理-图形推理"），周报系统会自动按一级分类聚合
- `id` 必须唯一，脚本用此字段去重
- 题库建议至少 40 道以上，保证每日抽题的多样性

### 第三步：定制前端页面

从 `assets/template.html` 复制模板到 `index.html`，然后进行以下定制：

1. **标题**：修改 HTML title 标签和 .site-logo 中的考试名称
2. **题型分类常量**：修改 `METHOD_RULES` 对象（约第 910-947 行），替换为当前考试的题型分类：
   ```javascript
   const METHOD_RULES = {
     '言语理解': {
       label: '言语理解',
       color: '#818CF8',
       barClass: 'bar-logic',
       badgeClass: 'badge-logic',
       icon: '🔷',
       strategies: [
         { label: '方法1', desc: '具体描述...' },
         { label: '方法2', desc: '具体描述...' },
       ]
     },
     // ... 更多分类
   };
   ```
   每个分类需定义：`label`（中文名）、`color`（图表色）、`barClass`（CSS类）、`badgeClass`（标签CSS类）、`icon`（图标）、`strategies`（周报中展示的复习策略）

3. **题库指南页**：修改 `#page-guide` 中的题库管理说明，适配当前考试

4. **配色方案**：模板使用极简纸质感设计，如需调整整体风格，修改 `:root` 中的 CSS 变量

### 第四步：配置每日更新脚本

将 `scripts/update_daily.py` 复制到项目根目录，调整以下常量（脚本顶部）：

```python
DAILY_COUNT = 4          # 每日题目数量
WARNING_THRESHOLD = 8    # 题库剩余预警阈值
```

**脚本行为**：
- 从 `data/questions/bank.json` 随机抽取 N 道未出过的题目
- 排除记录在 `data/questions/used_ids.json` 中的题目ID
- 覆盖写入 `data/questions/today.json`
- 题库耗尽时自动清空已出记录并重新抽取（输出警告）

**运行方式**：
```bash
cd /path/to/project
python3 update_daily.py
```

### 第五步：部署与自动化

网站是纯静态 HTML + JSON 数据驱动，部署方式灵活：

1. **本地使用**：直接打开 `index.html`（需本地服务器以加载 JSON，推荐 `python3 -m http.server`）
2. **自动化每日更新**：配置定时任务（cron / launchd）每日执行 `update_daily.py`
3. **在线部署**：可部署到任何静态托管服务（GitHub Pages、Vercel、Netlify 等）

**定时任务示例**（macOS launchd，配置 StartCalendarInterval，Hour=8, Minute=0，路径为 ~/Library/LaunchAgents/com.exam.update-daily.plist）

## 数据流

```
bank.json ──→ update_daily.py ──→ today.json
                  │
                  └──→ used_ids.json (去重记录)
                           │
index.html ──→ fetch today.json ──→ 渲染题目
     │
     └──→ localStorage ──→ 错题本 & 完成状态
```

## 前端功能清单

模板 `assets/template.html` 已包含以下完整功能，无需额外开发：

| 功能 | 说明 |
|------|------|
| 今日练习 | 加载 today.json，逐题作答，提交后自动判分并显示解析 |
| 错题本 | 自动收录错题（localStorage），支持按类型筛选，支持重新作答 |
| 周报 | 本周错题统计，类型分布柱状图，针对性复习建议 |
| 题库指南 | 题库格式说明，手动更新指引 |
| 进度追踪 | 答题进度条，提交按钮智能启用 |
| 响应式 | 适配手机/平板/桌面 |

## 适配新考试检查清单

- [ ] 确认考试名称、题型分类、每日题量
- [ ] 构建 `data/questions/bank.json`（至少 40 道题）
- [ ] 从 `assets/template.html` 复制模板为 `index.html`
- [ ] 修改 HTML title 标签和 .site-logo 中的考试名称
- [ ] 修改 `METHOD_RULES` 对象，替换为当前考试的分类和复习策略
- [ ] 修改 `#page-guide` 中的题库指南内容
- [ ] 将 `scripts/update_daily.py` 复制到项目根目录
- [ ] 调整 `DAILY_COUNT` 和 `WARNING_THRESHOLD`
- [ ] 运行 `python3 update_daily.py` 生成首日题目
- [ ] 启动本地服务器测试 `python3 -m http.server 8080`
- [ ] （可选）配置每日自动更新定时任务
