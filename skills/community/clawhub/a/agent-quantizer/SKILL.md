---
name: agent-quantizer
description: API 调用优化器 - 上下文压缩、缓存去重、僵尸清理、heartbeat 检查、cron 审计、模型分级、skill 管理
user-invocable: true
version: 2.0.0
---

# Agent Quantizer - 全栈优化工具包

跨实例部署的 OpenClaw 优化层。不改模型、不改代码，从调用侧省 token、省钱、省时间。

## ⚡ 自动缓存规则（强制执行）

每次调用工具（web_fetch、web_search、exec 中的网络请求等）之前，**必须先查缓存**：

```bash
# 第一步：查缓存
bash ~/.openclaw/skills/agent-quantizer/scripts/cache.sh get "查询内容" <类别>

# 如果返回 HIT → 直接使用，不要重新调用
# 如果返回 MISS → 正常调用工具，调用完后存缓存：

# 第二步：存缓存
bash ~/.openclaw/skills/agent-quantizer/scripts/cache.sh set "查询内容" "结果" <类别> <TTL秒>
```

| 类别 | TTL | 场景 |
|------|-----|------|
| `tool` | 30分钟 | 天气、汇率等半实时数据 |
| `knowledge` | 24小时 | 百科、定义等不变信息 |
| `realtime` | 5分钟 | 新闻等快速变化内容 |
| `general` | 1小时 | 其他通用查询 |

## 📊 Token 统计与扫描

用户说"查看 token 消耗"或"扫描高消耗"时：

```bash
# 查看所有 session token 排行
bash ~/.openclaw/skills/agent-quantizer/scripts/quantize.sh stats

# 扫描超阈值 session
bash ~/.openclaw/skills/agent-quantizer/scripts/quantize.sh scan
```

## 🧠 上下文压缩

对话变长、响应变慢时：

```bash
# 滑动窗口压缩（零 API 消耗）
bash ~/.openclaw/skills/agent-quantizer/scripts/quantize.sh compress <session_key> --window

# AI 摘要压缩（消耗少量 token，效果更好）
bash ~/.openclaw/skills/agent-quantizer/scripts/quantize.sh compress <session_key> --ai
```

## ✂️ Prompt 精简

精简 prompt 文件，去冗余指令和礼貌用语：

```bash
bash ~/.openclaw/skills/agent-quantizer/scripts/quantize.sh trim <文件路径>
```

## 🧟 僵尸 Session 清理

清理长期不活跃的 session，回收 token：

```bash
# 预览（不删除）
bash ~/.openclaw/skills/agent-quantizer/scripts/clean-zombies.sh 7 --dry-run

# 执行清理（7 天未活动的）
bash ~/.openclaw/skills/agent-quantizer/scripts/clean-zombies.sh 7

# 自定义天数
bash ~/.openclaw/skills/agent-quantizer/scripts/clean-zombies.sh 30
```

备份在 `.zombie-backup/` 目录，删错了可以恢复。

## 💓 Heartbeat 空转检查

检查 HEARTBEAT.md 是否在空转烧 API：

```bash
bash ~/.openclaw/skills/agent-quantizer/scripts/check-heartbeat.sh
```

标出空的或只有注释的 HEARTBEAT.md，给出修复建议。

## ⏰ Cron Job 审计

检查定时任务是否有冗余、高频、重复：

```bash
bash ~/.openclaw/skills/agent-quantizer/scripts/audit-cron.sh
```

## 🎯 模型分级配置

查看当前模型配置和推荐策略：

```bash
bash ~/.openclaw/skills/agent-quantizer/scripts/setup-models.sh
```

## 📁 Skill 分类整理

扫描所有 skill，建议哪些该放全局、哪些该放专属 workspace：

```bash
bash ~/.openclaw/skills/agent-quantizer/scripts/organize-skills.sh
```

## 快捷命令

用户可以直接说（中文即可）：
- "查看 token 消耗" / "token 统计" → 执行 quantize stats
- "扫描高消耗" → 执行 quantize scan
- "压缩上下文" → 执行 quantize compress
- "缓存统计" → 执行 quantize cache stats
- "清空缓存" → 执行 quantize cache flush
- "清理僵尸 session" → 执行 clean-zombies.sh
- "检查 heartbeat" → 执行 check-heartbeat.sh
- "检查 cron" → 执行 audit-cron.sh
- "整理 skill" → 执行 organize-skills.sh

## 文件路径

所有脚本位于：`~/.openclaw/skills/agent-quantizer/scripts/`

```
scripts/
├── quantize.sh          # 主入口（stats/scan/compress/trim/cache）
├── cache.sh             # 缓存系统
├── clean-zombies.sh     # 僵尸 session 清理
├── check-heartbeat.sh   # heartbeat 空转检查
├── audit-cron.sh        # cron job 审计
├── setup-models.sh      # 模型分级配置
└── organize-skills.sh   # skill 分类整理
```
