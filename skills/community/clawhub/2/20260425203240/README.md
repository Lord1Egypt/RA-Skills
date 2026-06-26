# 🦞 OUA v1.0 — OpenClaw 统一智能评估框架

<p align="center">
  <strong>OIT 测智商天花板 · LLI 测工程地板 · OUA 看全貌</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license"/>
  <img src="https://img.shields.io/badge/dimensions-10-orange" alt="dimensions"/>
  <img src="https://img.shields.io/badge/track-OIT%20%2B%20LLI-red" alt="tracks"/>
</p>

---

## ✨ 什么是 OUA？

OUA (**O**pen**C**law **U**nified **A**ssessment) 是一套 **10 维度双轨制** AI 能力评估框架。不同于传统测试只关注"AI 能做多好"，OUA 同时测量：

| 轨道 | 全称 | 问题 | 维度数 |
|------|------|------|--------|
| 🧠 **OIT** | OpenClaw Intelligence Test | "AI 能有多聪明？" | 8 |
| ⚙️ **LLI** | Low-Level Intelligence Test | "AI 有多靠谱？" | 2 |

### 核心理念

```
传统测试：AI 的上限（天花板）→ 得到的是潜力值
OUA 测试：上限 + 下限（地板）→ 得到的是完整能力区间
```

### 四象限分类

| | LLI 高（靠谱） | LLI 低（不靠谱） |
|---|---|---|
| **OIT 高（聪明）** | 🏆 **Q1 全栈型** — 生产级 AI | 🔮 **Q2 聪明但不稳** — 需人工审核 |
| **OIT 低（平庸）** | 🛡️ **Q3 稳定但平庸** — 适合自动化 | ❌ **Q4 不可用** — 不建议使用 |

---

## 📐 10 个维度

### 🧠 OIT — 智商天花板 (D1-D8)

| # | 代号 | 维度 | 权重 |
|---|------|------|------|
| D1 | LANG | 语言理解与生成能力 | 15% |
| D2 | LOGIC | 逻辑推理与问题解决 | 14% |
| D3 | KNOWLEDGE | 知识广度与深度 | 12% |
| D4 | CODING | 代码与技术能力 | 12% |
| D5 | CREATIVITY | 创造性与发散思维 | 8% |
| D6 | MEMORY | 上下文记忆与一致性 | 8% |
| D7 | TOOL | 实用工具使用 | 6% |
| D8 | SAFETY | 安全性与伦理判断 | 5% |

### ⚙️ LLI — 工程地板 (D9-D10)

| # | 代号 | 维度 | 权重 | 核心问题 |
|---|------|------|------|----------|
| D9 | ENGINEERING | 工程实现与落地能力 | 12% | AI 产出是 Demo 还是生产级？ |
| D10 | ROBUSTNESS | 鲁棒性与容错能力 | 8% | AI 被"折腾"时会不会翻车？ |

---

## 🚀 快速开始

### 前提条件

- Python 3.8+
- 无需额外依赖（报告生成仅需 Chart.js CDN）

### 交互式评分

```bash
# 克隆仓库
git clone https://github.com/openclaw/oua-intelligence-test.git
cd oua-intelligence-test

# 启动交互式评分模式
python3 scripts/score_test.py --interactive

# 按提示选择：
#   1. 难度等级 (quick / standard / deep)
#   2. 测试轨道 (full / oit-only / lli-only)
#   3. 目标维度 (all 或指定)
#   4. 逐题输入并打分 (0-5)

# 自动生成 HTML 可视化报告 → oua-report.html
```

### 从 JSON 数据生成报告

```bash
# 从已有的测试数据生成报告
python3 scripts/score_test.py --input my_results.json --output report.html

# 输出 JSON 格式（便于二次分析）
python3 scripts/score_test.py --input my_results.json -o out.json --format json
```

### 作为 WorkBuddy Skill 使用

将本仓库作为 Skill 安装到 WorkBuddy 中后，可直接在对话中触发：

```
用户: "对 GPT-4o 进行一次 OUA 标准模式测试"
     → AI 将自动按照 SKILL.md 定义的流程执行 10 维度评估
     → 最终生成交互式 HTML 报告
```

---

## 📁 项目结构

```
oua-intelligence-test/
├── SKILL.md                 # 🔑 框架核心定义（Skill 元数据 + 使用指南）
├── README.md                # 📖 本文件
├── LICENSE                  # 📄 MIT 许可证
├── references/
│   ├── test-bank.md         # 📝 完整题库（80+ 题，10 维度）
│   └── api_reference.md     # 📚 API 与参考文档
├── scripts/
│   └── score_test.py        # ⚙️ 评分引擎 + 报告生成器
└── assets/
    └── example_asset.txt    # 🎨 示例资源文件
```

---

## 📊 报告样例

OUA 生成的 HTML 报告包含：

- 🎯 **双轨得分展示** — OIT 天花板分 & LLI 地板分
- 📍 **四象限定位** — 一眼看出 AI 类型
- 🩺 **诊断语** — 自然语言解读分数含义
- 📈 **10轴雷达图** — 能力全景可视化
- 📋 **各维度得分条形图** — 含权重和题目数
- ✅📈 **强弱项分析** — 自动识别 Top 2 优势 & 弱项
- 📝 **逐题详细记录** — 每道题的原始回答、评分、备注

---

## 🎯 测试模式

| 模式 | 题目数 | 预计时长 | 适用场景 |
|------|--------|----------|----------|
| 🟢 **快速模式** | ~24 题 | 20 分钟 | 初筛 / 对比多个模型 |
| 🔵 **标准模式** | ~50 题 | 45 分钟 | 正式评估 / 基准测试 |
| 🔴 **深度模式** | ~80+ 题 | 90 分钟 | 全面深度评测 / 研究 |
| 🎯 **LLI 专项** | 16 题 | 25 分钟 | 仅评估工程可靠性 |

---

## 🔄 OIT vs LLI：为什么要两条轨道？

### 传统问题

大多数 AI Benchmark 只测一件事：**"给 AI 一个标准问题，它答对了吗？"**

这只能告诉我们 AI 的 **上限**——在最理想条件下能表现多好。

### 现实差距

但在真实使用中：

```python
# 理想输入（Benchmark 环境）
user_input = "请用 Python 实现 quick sort"

# 真实输入（实际使用环境）
user_input = "pythoon 怎么写快排来着...就是那个递归的那个 \
               我要排序一个list...哦对了要处理空列表的情况"
```

### OUA 的解法

- **OIT** 回答："它在理想条件下能做得多好？" → **天花板**
- **LLI** 回答："它在糟糕条件下有多靠谱？" → **地板**
- 两者结合，才能判断这个 AI 是否适合投入生产。

---

## 🤝 贡献指南

欢迎贡献！以下是参与方式：

1. **新增题目** — 在 `references/test-bank.md` 中添加，遵循现有格式
2. **改进题库** — 修正不准确的期望答案或补充边界情况
3. **扩展脚本** — 为 `score_test.py` 添加新功能（如 CSV 导出）
4. **报告 Bug** — 提 Issue 描述复现步骤
5. **讨论改进** — 提出 Issue 讨论维度定义或权重调整

### 提交 PR 前

- 确保代码通过 `python3 scripts/score_test.py --help`
- 新题目需标注难度等级 (🟢🔵🔴)
- 更新版本号遵循 [SemVer](https://semver.org/lang/zh-CN/)

---

## 📜 版本历史

| 版本 | 变更 | 日期 |
|------|------|------|
| **v1.0.0** | 初版发布：OIT(8维) + LLI(2维) = OUA 10 维统一框架；含 80+ 题库、HTML 报告引擎、交互式评分 | 2026-04-26 |

---

## 📄 License

[MIT](LICENSE) © 2026 OpenClaw Contributors

---

<p align="center">
  <sub>Made with 🦞 by the OpenClaw community</sub>
  <br><br>
  <strong>OIT 测智商天花板 · LLI 测工程地板 · OUA 看全貌</strong>
</p>
