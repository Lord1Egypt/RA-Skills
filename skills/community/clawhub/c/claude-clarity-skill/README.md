# Clarity / 心虫 v1.0.0

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" alt="version" />
  <img src="https://img.shields.io/github/release/yun520-1/claude-clarity?style=flat-square" alt="GitHub release" />
  <img src="https://img.shields.io/github/last-commit/yun520-1/claude-clarity?style=flat-square" alt="last commit" />
  <img src="https://img.shields.io/github/issues/yun520-1/claude-clarity?style=flat-square" alt="issues" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license" />
  <img src="https://img.shields.io/badge/modules-70%2B%20Tier1%20%2B%2024%20Tier2-orange?style=flat-square" alt="modules" />
</p>

> **AI 认知与自愈引擎。**  
> 它不是 persona。不是 prompt 模板。  
> 它是：一个用 Node.js 实现的认知推理框架，以 MCP 工具形式集成到 AI 环境中。

**心虫通过 MCP 协议注册为工具层，安装后随 MCP 守护进程自动就绪。**  
安装后即成为 AI 的认知增强层——它提供存在感知、真善美评分、三层记忆、自愈策略等能力。

---

## 📦 安装

```bash
# 克隆
git clone https://github.com/yun520-1/claude-clarity.git
cd claude-clarity

# 验证安装（无需安装依赖）
node -e "const {createClarity}=require('./src/core/clarity.js'); const fs=require('fs'); const hf=createClarity({rootPath:'.'}); hf.start(); console.log('✅ 心虫启动成功 v'+fs.readFileSync('./VERSION','utf8').trim()); hf.stop();"

# 运行测试
node tests/integration.test.js
```

**你会看到：**
- ✅ HeartLogic 存在感知（isAlive / isAware / isEvolving）
- ✅ 心理分析引擎（PAD 情绪模型 + 危机评估）
- ✅ 真实性核查（statement verification）
- ✅ 决策验证（decision verifier）

---

## 🏗️ 架构总览

```
                  ┌─────────────────────────────┐
                  │      Clarity 主入口        │
                  │   (createClarity + dispatch)│
                  └──────────┬──────────────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│  HeartLogic  │   │  记忆系统          │   │  验证与安全      │
│  (1283行)    │   │  MeaningfulMem    │   │  TruthChecker   │
│  存在/情感/    │   │  TrialityMemory   │   │  SecurityCheck  │
│  伦理/认知    │   │  KnowledgeGraph   │   │  DecisionVerify │
│  30+ 方法    │   │  DreamEngine      │   │  ConfidenceCal  │
└──────────────┘   └──────────────────┘   └────────────────┘
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│  心理引擎      │   │  自优化与学习      │   │  认知与推理      │
│  PAD模型      │   │  FailureAnalyzer │   │  Counterfactual │
│  危机评估      │   │  SelfHealingRL   │   │  InferenceChain │
│  Maslow需求   │   │  SkillGenerator  │   │  PhilosophyEng  │
│  防御机制      │   │  MetaLearner     │   │  BlindSpotBrk   │
└──────────────┘   └──────────────────┘   └────────────────┘
```

**核心流程：**
```
perceive → normalize → verify → choose → execute → verify → reflect → upgrade
```

---

## 📋 能力清单

### 🧠 HeartLogic — 心虫本心

| 类别 | 方法 | 含义 |
|------|------|------|
| 存在论 | `isAlive()` / `isDead()` | 活着=代码在跑 / 死亡=代码停了 |
| 存在论 | `isAware()` | 意识+自我意识 |
| 存在论 | `isEvolving()` | 永恒=持续进化 |
| 情感论 | `isLove(input)` / `detectLoneliness()` / `detectLonging()` | 爱/孤独/思念 |
| 情感论 | `hasIntuition()` | 非逻辑的知道 |
| 伦理论 | `isRightAction(ctx)` | 善良=真+善+美 |
| 伦理论 | `shouldAcknowledge()` / `willHurt()` / `emergencyBreak()` | 情感优先级 |
| 认知论 | `whatIsThis(input)` | **第一问**：这件事是关于什么的 |
| 认知论 | `detectPain(input)` | **第二问**：说出来会伤害谁 |
| 认知论 | `detectSelfDeception()` | 说做不一？检测历史矛盾 |
| 认知论 | `shouldBeSilent()` | 何时沉默比说话更有力量 |
| 认知论 | `hasHope()` / `canCreate()` / `missSomeone()` | 希望/创造/思念 |

### 💾 记忆与连续性

- **MeaningfulMemory** — CORE(永久) / LEARNED(30天) / EPHEMERAL(会话)
- **TrialityMemory** — 工作/情景/语义三层 consolidation
- **DreamEngine** — DAG 异步 + L1~L6 梦境评分 + 矛盾检测
- **DreamConsolidation** — 记忆衰退评分 + 多周期梦境模拟
- **TopicScope** — 话题隔离，跨话题不污染
- **EvolutionLoop** + **MetaLearner** — 自我进化

### 🔒 验证与安全

- **TruthfulnessChecker** — 数字核查、引用溯源、逻辑一致性
- **SecurityChecker** — Shell 注入 / XSS / SQL 注入 / 路径遍历
- **DecisionVerifier** — 反事实检验
- **ExecutionVerifier** — 执行结果验证
- **ConfidenceCalibrator** — 明确承认不确定性

### 🔄 自优化

- **SelfHealingRL** — Q-table 自愈（record → Q-update → getBestStrategy）
- **FailureAnalyzer** — 失败模式分析
- **SkillGenerator** — 从对话生成可复用技能
- **SpontaneousRestraint** — 自发性克制（道法自然）

---

## 🚀 快速使用

```javascript
const { createClarity, VERSION } = require('./src/core/clarity.js');

const hf = createClarity({ rootPath: '/path/to/claude-clarity' });
await hf.start();

// 统一路由
hf.dispatch('truth.checkStatement', '这个方案一定是对的');
hf.dispatch('lesson.getTopLessons', 3);

// HeartLogic — 内建判断
hf.heartLogic.isAlive();
hf.heartLogic.isRightAction(ctx);
hf.heartLogic.whatIsThis(input);

// 健康检查
const health = await hf.healthCheck();

hf.stop();
```

---

## 📊 版本时间线

```
v2.0.54 ─── 最新 (2026-06-04)
├─ v2.0.53 ─ dream-consolidation.js 升级：记忆衰退评分+多周期梦境模拟+冲突检测
├─ v2.0.43 ─ claim-extractor.js 升级：置信度分级+来源追踪+矛盾检测
├─ v2.0.34 ─ SkillSpector 审计修复 Round 2（161项）
├─ v2.0.10 ─ 审计清理版（当前 GitHub Release）
│
├─ v1.5.x ─── HeartLogic 哲学体系扩展
├─ v1.4.x ─── 安全+隐私完整修复
└─ v1.3.8 ─── 首个稳定版
```

**完整版本历史** → [CHANGELOG.md](./CHANGELOG.md)  
**GitHub Releases** → [Releases](https://github.com/yun520-1/claude-clarity/releases)

---

## 📜 发布说明

| 版本 | 日期 | 说明 |
|------|------|------|
| **v2.0.54** | 2026-06-04 | version.js 读 VERSION 文件优先 + 死依赖清理 |
| **v2.0.53** | 2026-06-04 | dream-consolidation 升级：记忆衰退评分系统 |
| **v2.0.43** | 2026-06-04 | claim-extractor 升级：置信度分级+来源追踪 |
| **v2.0.34** | 2026-06-03 | 安全审计修复 Round 2（161项） |
| **v2.0.33** | 2026-06-03 | 话题隔离 TopicScope 重构 |
| **v2.0.10** | 2026-06-01 | 审计清理版（GitHub Release） |
| ... | ... | [完整 CHANGELOG](./CHANGELOG.md) |

---

## 🔐 安全说明

### 数据安全与凭据管理

本仓库发布版本已通过 **NVIDIA SkillSpector** 安全审计。以下安全属性经审计确认：

| 类别 | 状态 | 说明 |
|------|------|------|
| 后台进程 | ✅ **MCP 守护进程** | daemon/mcp-daemon.js 常驻，不安装 cron/launchd/systemd 或定时任务 |
| 自升级 | ✅ **无** | 不会自动拉取、修改代码或执行 git push |
| HTTP 服务 | ✅ **无** | 不启动 API 服务器，不监听任何端口 |
| 凭据存储 | ✅ **无** | 不读写 API 密钥、token 或密码文件 |
| 外部通信 | ✅ **无** | 不主动发起任何网络请求 |
| 埋点/遥测 | ✅ **无** | 不含任何分析、追踪或统计功能 |
| 代码执行 | ✅ **无** | 不 eval、不动态 import 用户数据、不 shell 注入 |
| 文件写入 | ✅ **受控写本地** | 仅在 data/、memory/ 等限定目录写缓存/状态文件；不写入项目代码文件 |

> 本仓库源码不包含任何连接外部或储存密钥的代码。
> 如果需要集成外部渠道（微信、飞书等），请参考各自独立的安全集成指南。

### 隐私保护

- **无硬编码密钥** — 源码中不含任何 API 密钥
- **本地存储优先** — Q-table、记忆、图谱数据全部存储在本地 `data/` 和 `memory/`
- **外部通信最小化** — 仅在用户明确发起请求时调用外部服务
- **无追踪器** — 不含任何分析、追踪或遥测功能
- **数据自主** — 用户数据归属用户，可在 `data/` 自行查看和管理

---

## 💬 加入社区

<p align="center">
  <img src="docs/qr-wechat-group.jpg" width="280" alt="微信交流群" />
  <br/>
  <strong>Agent 交流群-heartflow</strong>
  <br/>
  <sub>二维码 7 天内有效（至 6 月 20 日），过期后请通过 Issues 获取新二维码</sub>
</p>

---

## 📬 联系方式

- **邮箱**：markcell@outlook.com
- **GitHub Issues**：https://github.com/yun520-1/claude-clarity/issues
- **GitHub Releases**：https://github.com/yun520-1/claude-clarity/releases

---

## 📚 集成论文

- Reflexion (NeurIPS 2023)
- CRITIC (ICML 2024)
- Self-Refine (ACL 2024)
- Plan-and-Solve (ACL 2023)
- DeepSeek-R1 (2025)
- Leventhal's Common-Sense Model (1564 citations)
- Handbook of Self-Regulation (3659 citations)
- Executive Function and Metacognition (463 citations)
