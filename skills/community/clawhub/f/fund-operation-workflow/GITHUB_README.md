# 基金运营工作流 Skill

**基于《公募基金互金电商业务搭建工作流》+ MBTI 特质匹配 + STAR+ 合规前置框架**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-available-blue)](https://clawhub.com)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/lj22503/fund-operation-workflow)

---

## 🎯 一句话介绍

帮助基金运营人构建**可落地的 AI 工作流**，将 6 大运营节点 × MBTI 特质匹配 × STAR+ 合规前置框架，让 AI 输出**可用、合规、可执行**的运营方案。

---

## 📐 为什么需要这个 Skill？

### 基金运营人的 AI 困境

**❌ 你是不是也遇到过：**

1. **AI 输出不能用**
   - 让 AI 做竞品分析，输出悬浮的报告，无法用在业务中
   - 让 AI 写文案，生成违规内容（承诺收益/保本）
   - 让 AI 设计策略，泛泛而谈，无法落地执行

2. **合规风险高**
   - AI 不懂基金行业合规红线
   - 生成"保本""稳赚""预期收益"等违规表述
   - 事后修改成本高，不如自己写

3. **工作流缺失**
   - 知道 AI 强大，但不知道如何嵌入日常工作
   - 单点使用 AI，没有系统性工作流
   - 依赖个人经验，无法沉淀和复用

**✅ 这个 Skill 能帮你：**

- ✅ **STAR+ 合规前置框架**：让 AI 在轨道上发挥，输出直接可用
- ✅ **6 节点×MBTI 匹配**：每个节点调用最适合的 AI 角色
- ✅ **子节点细化**：实施层差异化管理，针对性解决具体问题
- ✅ **合规检查清单**：每个节点嵌入合规检查，避免违规风险

---

## 🚀 快速开始

### 方式 1：OpenClaw + ClawHub（推荐）

```bash
# 1. 安装 OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. 安装技能
clawhub install fund-operation-workflow

# 3. 使用技能
@ant 使用 fund-operation-workflow skill，制定年度运营规划
```

### 方式 2：直接使用提示词模板

1. 克隆本仓库
2. 打开 `prompts/` 目录，选择对应节点的提示词模板
3. 复制提示词，填入你的具体信息
4. 发送给 AI（Claude/ChatGPT/其他）

---

## 📁 目录结构

```
fund-operation-workflow/
├── SKILL.md                          # 技能主文档
├── README.md                         # 本文件
├── QUICKSTART.md                     # 快速启动指南
├── LICENSE                           # MIT 许可证
│
├── references/                       # 参考文档
│   ├── mbti-mapping.md              # MBTI 特质匹配详解
│   ├── compliance-checklist.md      # 合规检查清单
│   └── star-framework.md            # STAR+ 合规前置框架
│
├── prompts/                          # 提示词模板
│   ├── 01-collect-enfp.md           # 收集节点（ENFP）
│   ├── 02-archive-istj.md           # 归档节点（ISTJ）
│   ├── 03-strategy-intp.md          # 策略节点（INTP）
│   ├── 04-implement-entj.md         # 实施节点（ENTJ）
│   ├── 05-test-isfj.md              # 测试节点（ISFJ）
│   └── 06-monitor-infj.md           # 监控节点（INFJ）
│
└── examples/                         # 实战案例
    └── case-study.md                # 完整实战案例
```

---

## 🎯 适用场景

### ✅ 推荐使用

- 基金公司互金电商业务从 0 到 1 搭建
- 年度/季度运营规划制定
- 运营团队分工与角色分配
- 工作流 SOP 标准化
- AI 提示词优化（STAR 框架）
- 合规审查嵌入日常工作流

### ❌ 不推荐使用

- 非金融行业的运营工作（需调整合规部分）
- 个人投资者（本技能面向机构）
- 替代专业合规审查（需配合持牌合规人员）

---

## 📊 核心架构

### 6 大节点 × MBTI 匹配

```
1️⃣ 收集（ENFP）→ 思维跳跃，发现新想法
   ├─ 广告投放数据
   ├─ KOL 种草数据
   ├─ 主站货架数据
   └─ ...

2️⃣ 归档（ISTJ）→ 执行规划，遵守规则
   ├─ 数据归档
   ├─ 文件归档
   ├─ 文档模板
   └─ ...

3️⃣ 策略（INTP）→ 逻辑思维，系统分析
   ├─ 用户获取策略
   ├─ 激活&体验策略
   ├─ 转化&活跃策略
   └─ ...

4️⃣ 实施（ENTJ）→ 执行力，高效领导
   ├─ 路径设计
   ├─ 文案创作
   ├─ 设计管理
   └─ ...

5️⃣ 测试（ISFJ）→ 责任感，可靠完成任务
   ├─ 功能自检
   ├─ 评审
   ├─ 模块测试
   └─ ...

6️⃣ 监控（INFJ）→ 洞察力，理解复杂模型
   ├─ 数据监控
   ├─ 用户反馈
   └─ 用户调研
```

---

## 📐 STAR+ 合规前置框架

**所有提示词统一采用此结构：**

```markdown
【角色定义】→ 激活专家模式
【STAR 背景】
  - 情境 (Situation)
  - 任务 (Task)
  - 行动 (Action)
  - 结果 (Result)
【合规约束】→ 前置红线
【输入】→ 具体信息
【输出要求】→ 格式标准
```

**驾驭 AI 四原则：**
1. 给角色 → 激活专家模式
2. 给框架 → 强制结构化思考
3. 给约束 → 合规红线前置
4. 给痛点 → 针对具体问题

---

## 🧪 使用示例

### 示例 1：竞品分析

```
你是一位资深的金融产品运营专家。

【STAR 背景】
- 情境：我正在负责 XX 短债基金在蚂蚁渠道的上新运营
- 任务：深度拆解竞品详情页，找到可复用的转化设计逻辑
- 目标：输出 3 个可立即执行的优化建议

【合规约束】
- 不得评价或排名比较竞品业绩
- 不得暗示"保本"或"稳赚"

【分析框架】
1. 页面战略定位
2. 用户旅程还原
3. 功能拆解
4. 心理学机制
5. SWOT 洞察

【输入】
竞品页面链接：xxx
当前痛点：页面跳出率 65%，用户集中在第 2 屏流失

【输出要求】
- 每个结论标注"推测"或"可验证"
- 给出可本周执行的 3 个动作，按"影响力/成本"排序
```

---

### 示例 2：年度运营规划

```
你是一位资深的公募基金投顾业务运营专家。

【STAR 背景】
- 情境：某中型公募基金公司，蚂蚁财富投顾业务优化期
- 任务：设计 2026 年度运营规划，实现投顾业务规模化增长
- 目标：12 个月内 MAU 从 5 万提升至 15 万

【合规约束】
- 不得出现"保本""稳赚""预期收益"
- 风险提示必须完整

【年度规划 7 步法】
1. 市场分析与竞品对标
2. 用户分层与需求洞察
3. 年度目标拆解
4. 核心策略设计
5. 资源投入与预算分配
6. 风险识别与应对
7. 里程碑规划

【输出要求】
- 年度运营规划文档（可直接用于汇报）
- 目标拆解表（年度→季度→月度）
- 每个策略标注"优先级"和"执行难度"
```

---

## 📚 学习路径

### 入门（1 天）
- [ ] 阅读 `SKILL.md`
- [ ] 阅读 `QUICKSTART.md`
- [ ] 了解 MBTI 基础概念

### 进阶（1 周）
- [ ] 精读 `references/star-framework.md`
- [ ] 精读 `references/compliance-checklist.md`
- [ ] 阅读 `examples/case-study.md`

### 实战（1 月）
- [ ] 选择具体业务场景
- [ ] 完整跑通 6 个节点
- [ ] 产出实际成果

---

## 🔗 相关资源

- [OpenClaw 官网](https://openclaw.ai)
- [ClawHub 技能市场](https://clawhub.com)
- [STAR 框架原文](https://my.feishu.cn/docx/TIDPdX3egoxShnxsXE0cuHSJnig)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 支持与反馈

- **问题反馈**：GitHub Issues
- **作者**：燃冰 + ant
- **版本**：v2.0.0（2026-03-26）

---

*如果这个 Skill 对你有帮助，欢迎 ⭐Star 支持！*
