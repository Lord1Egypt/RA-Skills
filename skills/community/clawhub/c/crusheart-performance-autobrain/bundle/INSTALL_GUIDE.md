# 🦞 灵枢 AutoBrain Turbo v6.3.1 — 安装指南

## 关于此插件

AutoBrain 是一个 **插件 + 技能混合包**，为 OpenClaw Agent 提供：
- **长期记忆** — 五层记忆体系，跨会话记住你是谁
- **防幻觉** — 权威白名单 + 多源交叉验证
- **自进化** — LLM-as-Judge 自评分 + Reflexion 反思
- **工作流编排** — 多技能协调、任务路由、规则引擎
- **错误隔离** — 熔断器（超时保护 + 自动重试 + 断点接续）
- **后台子代理** — 异步任务调度 + 子代理会话

> 90+ 个 Python 引擎 · 8 引擎组 · 10 阶段流水线

---

## 兼容性要求

| 项目 | 最低要求 | 建议版本 |
|------|---------|---------|
| OpenClaw | ≥ 2026.5.0 | 最新 stable |
| Node.js | ≥ 18 | ≥ 20 LTS |
| Python | ≥ 3.10 | ≥ 3.12 |
| 磁盘空间 | ≥ 50MB | ≥ 200MB |
| 工作区 | 标准 OpenClaw workspace | 正常初始化过 |

**⚠️ 独占插件槽位**：安装时会自动检测功能重叠的插件，冲突则阻止安装并通知用户。

---

## 安装方式

```bash
# 1. 解压插件包
unzip crusheart-fuse-v6.3.1-fixed.zip -d ./crusheart-pack/

# 2. 安装 (--dangerously-force-unsafe-install 是因 index.js 调用 child_process)
openclaw plugins install --dangerously-force-unsafe-install ./crusheart-pack/

# 3. 重启 Gateway
openclaw gateway restart
```

安装过程中系统会自动：
1. 检查兼容性（版本/磁盘/依赖）→ 不通过则拦截
2. 检测功能重叠的已安装插件 → 有冲突则通知用户
3. 部署 90+ 个引擎到 `core/engines/`
4. 部署辅助脚本到 `scripts/`
5. 安装技能到 `skills/Crusheart-AutoBrain-Turbo/`

---

## 首次初始化

首次重启 Gateway 后，系统将自动执行初始化流程：

```
[1/8] 🔧 注入行为规则      → SOUL.md 规则合并
[2/8] 🧠 记忆扫描归档      → 扫描 memory/ + 多层记忆整理
[3/8] 🗄️  数据库检测       → 检测本地 DB / 知识库并连接（没有则跳过）
[4/8] 📋 技能分类索引      → 扫描 skills/ + 自动分类
[5/8] 🔗 技能引擎连接      → 连接 SkillAutoInvoker + SelfEvolution + AutoTuning
[6/8] ⚡ 系统索引构建      → 全量索引重建
[7/8] 🕐 定时任务注册      → 01:00 统一维护 + 05:00 引擎初始化
[8/8] ✅ 运行状态验证      → 检查模块完整性 + 引擎状态
```

初始化完成后，Agent 即拥有全部 AutoBrain 能力。

---

## 架构速览

```
用户消息 → Pipeline (10阶段) → Agent
              │
         AutoBrain 引擎体系
              │
    ┌────┬────┬────┬────┬────┬────┬────┬────┐
   init memory quality ops workflow hooks tools compat
    (12)  (7)   (11)   (7)   (7)   (4)  (12)  (2)
```

---

## 更多文档

- `README.md` — 英文完整文档
- `readme_cn.md` — 中文完整文档
- `bundle/ARCHITECTURE.md` — 完整架构参考（引擎映射关系）
- `skill/SKILL.md` / `skill_cn.md` — 技能页文档

---

**意见反馈**: HIM603070@gmail.com
