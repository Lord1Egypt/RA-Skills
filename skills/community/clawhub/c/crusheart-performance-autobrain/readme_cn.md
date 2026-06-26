<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-2026.5.0%2B-blueviolet" alt="OpenClaw">
  <img src="https://img.shields.io/badge/version-6.3.1-green" alt="Version">
  <img src="https://img.shields.io/badge/status-stable-brightgreen" alt="Status">
</p>

<h1 align="center">🦞 灵枢AutoBrain</h1>
<p align="center">
  <em>为你的 OpenClaw Agent 装上大脑——长期记忆、防幻觉、自进化、工作流编排，开箱即用。</em>
</p>

---

## ✨ 功能概述

AutoBrain 是一个 **插件 + 技能混合包**，将 OpenClaw Agent 从无状态聊天机器人升级为持久化、自我进化的 AI 助手。它注入 Agent 生命周期，自动部署 90+ 个 Python 引擎，覆盖 8 个引擎组 + 3 个子系统。

| 能力 | 说明 |
|------------|------|
| 🧠 **长期记忆** | 五层记忆体系（会话→短期→梦境固化→归档→向量检索），跨会话记住你是谁 |
| 🛡️ **防幻觉** | 权威域名白名单、知识断言校验、多源交叉验证（16 个引擎） |
| 🔄 **自进化** | LLM-as-Judge 自评分 + Reflexion 反思（失败模式、根因、修复策略） |
| 🎯 **双模式 + R-CCAM** | 简单问答快速通道，复杂任务深度推理 |
| 🩺 **健康巡检** | 每日定时任务——引擎状态、磁盘空间、网关健康、异常检测（0-100 评分） |
| 🔌 **故障转移 + 错误隔离** | 主模型失败自动切换到备用模型。熔断器带超时保护、自动重试、断点接续 |
| 🔀 **工作流编排** | 多技能协调、冲突检测、任务路由、规则引擎 |
| 📋 **上下文胶囊 (DAG)** | 基于 DAG 的上下文管理，增量摘要，SQLite 存储 |
| 🔍 **增强检索** | 查询重写 + RRF 融合 + 检索置信度评估 |
| 🧵 **后台子代理** | 异步任务调度 + 子代理会话，心跳保活 + 超时回收 |

## 🚀 快速开始

### 前提条件

- **OpenClaw** ≥ 2026.5.0
- **Node.js** ≥ 18
- **Python** ≥ 3.10

### 安装

```bash
# ⚠️ 独占插件槽位 — 自动检测功能重叠插件，冲突则阻止安装。

openclaw plugins install --dangerously-force-unsafe-install ./crusheart-pack/

# 重启 Gateway
supervisorctl restart openclaw-gateway
```

> **为什么需要 `--dangerously-force-unsafe-install`？**
> 插件 `index.js` 在启动时通过 `child_process` 调用 Python 引擎。这是误报——代码完全是本地的，不涉及远程。

### 验证

```bash
openclaw plugins list | grep crusheart
# 启动日志应显示：
#   ✅ 引擎部署完成
#   ✅ 安装向导 8 步完成
#   ✅ 2 个定时任务已注册
```

## 🏗️ 架构总览

```
openclaw-gateway
  │
  ├── crusheart-autobrain-turbo (插件)
  │     ├── index.js                    ← Node.js 桥接（4 个生命周期钩子）
  │     ├── bundle/crusheart-core.tar.gz  ← 90+ 个 Python 引擎
  │     └── skill/                       ← OpenClaw 技能元数据
  │
  ├── core/engines/                     ← 部署到工作区（8 个引擎组）
  │     ├── init/      (12)  — 配置、会话、上下文胶囊、自动加载
  │     ├── memory/     (7)  — 五层记忆、向量索引、用户画像
  │     ├── quality/   (11)  — 防幻觉、评审引擎、异常检测
  │     ├── operations/ (7)  — 健康巡检、决策核心、自治周期
  │     ├── workflow/   (7)  — 编排器、规则引擎、串行通道、目标编译
  │     ├── tools/     (12)  — 故障转移、数据库、模板库、追踪时间线
  │     ├── hooks/      (4)  — 双模式分类器、自进化 v3/v4
  │     └── compat/     (2)  — 第三方引擎注册
  │
  ├── core/pipeline/    (10)  — 10 阶段消息流水线
  ├── core/planner/     (6)   — 目标解析与任务分解
  └── core/capability/  (1)   — 任务图模型
```

## 📦 包含内容

| 制品 | 路径 | 用途 |
|------|------|------|
| 插件入口 | `index.js` | Python 引擎与 OpenClaw 生命周期桥接 |
| 插件清单 | `openclaw.plugin.json` | OpenClaw 插件注册 |
| 引擎包 | `bundle/crusheart-core.tar.gz` | 90+ Python 引擎 + 流水线 + 规划器 |
| 技能元数据 | `skill/_meta.json` | 技能市场注册 |
| 技能文档 | `skill/SKILL.md` | 技能文档（英文） |
| 自述文件 | `README.md` | 英文自述 |
| 自述文件（中文） | `readme_cn.md` | 中文自述 |
| 技能文档（中文） | `skill_cn.md` | 中文技能文档 |
| 架构参考 | `bundle/ARCHITECTURE.md` | 完整架构与文件快速查找 |
| 系统规则 | `bundle/SOUL.md` | Agent 行为铁律（部署到工作区根目录） |
| 安装指南 | `bundle/INSTALL_GUIDE.md` | 安装向导文档 |
| 自动部署脚本 | `bundle/*.py`, `bundle/*.sh` | 8 个脚本自动部署到工作区 scripts/ |

## 🔧 配置

### 环境变量（可选）

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `EMBEDDING_API_URL` | 远程嵌入服务 URL | _(本地 TF-IDF 回退)_ |
| `EMBEDDING_API_KEY` | 嵌入 API 的 Bearer Token | _(无)_ |
| `FALLBACK_MODEL` | 备用模型（主模型失败时切换） | _(用户自行配置)_ |
| `CRUSHEART_PYTHON` | Python 解释器路径 | `python3` |

不配置以上变量时，系统使用本地 TF-IDF 向量搜索——精度略低但功能完整。

### 定时任务（自动注册）

| 时间 | 名称 | 说明 |
|------|------|------|
| `0 1 * * *` | 统一维护（含记忆维护） | 健康巡检+记忆固化+系统清理+梦境扫描+ReplayBuffer蒸馏+执行复盘+记忆扫描/归档/索引重建+技能扫描 |
| `0 5 * * *` | 引擎初始化 + 版本检查 | `init_engines.py --bootstrap` + 新版本检查 |

> 2 个定时任务：01:00 统一维护（含记忆维护），05:00 引擎初始化+版本检查。

---

**意见反馈**: HIM603070@gmail.com
