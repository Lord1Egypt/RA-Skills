<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-2026.5.0%2B-blueviolet" alt="OpenClaw">
  <img src="https://img.shields.io/badge/version-6.3.1-green" alt="Version">
  <img src="https://img.shields.io/badge/status-stable-brightgreen" alt="Status">
</p>

<h1 align="center">🦞 AutoBrain（灵枢）— 技能页</h1>
<p align="center">
  <em>为 OpenClaw 提供长期记忆、防幻觉、自进化和工作流编排。90+ 个 Python 引擎，覆盖 8 个引擎组 + 3 个子系统。</em>
</p>

---

## 快速安装

```bash
openclaw plugins install --dangerously-force-unsafe-install ./crusheart-pack/
# 然后重启 Gateway
```

## 功能列表

| 功能 | 说明 |
|------|------|
| **🧠 长期记忆** | 五层记忆 + DAG 上下文管理 + 记忆固化引擎 |
| **🛡️ 防幻觉** | 权威白名单 + 多源交叉验证（16 个引擎） |
| **🔄 自进化** | LLM-as-Judge 自评分 + Reflexion 反思（模式、根因、修复） |
| **🎯 双模式 + R-CCAM** | 简单问答快速通道，复杂任务深度推理 |
| **🔍 增强检索** | 查询重写 + RRF 融合 + 检索置信度评估 |
| **🩺 每日维护** | 01:00 统一定时任务：健康巡检 + 清理 + 记忆 + 梦境 + 回放 + 记忆扫描 |
| **🔀 工作流引擎** | 多技能协调、冲突检测、任务路由、规则引擎 |
| **📋 上下文胶囊** | 基于 DAG 的会话交接，SQLite 上下文图 |
| **📁 自动扫描** | 首次安装：记忆扫描 + 技能分类 + 纠错初始化 |
| **🔄 版本检查** | 安装时一键检查 clawhub.ai 新版本，每日 05:00 复查 |

## 架构概览

```
plugin (index.js) ──► 90+ 个 Python 引擎 ──► 10 阶段消息流水线
  8 个引擎组：init/memory/quality/operations/workflow/hooks/tools/compat
  + 3 个子系统：pipeline/planner/capability
  + 8 个自动部署脚本

插件槽位：独占 — 自动检测功能重叠插件并阻止安装
定时任务：统一维护(01:00)、引擎初始化+版本检查(05:00)
```

## 相关文档

- **架构参考**: `bundle/ARCHITECTURE.md` — 完整文件查找指南
- **自述文件（英文）**: `README.md`
- **自述文件（中文）**: `readme_cn.md`
- **技能页（英文）**: `SKILL.md`
- **安装指南**: `bundle/INSTALL_GUIDE.md`

---

**意见反馈**: HIM603070@gmail.com
