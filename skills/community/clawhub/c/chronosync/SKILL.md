---
name: session-sync
version: 1.0.1
description: >
  跨会话聊天记录同步工具。自动备份 OpenClaw 各会话的聊天记录，
  实现会话间记忆共享，避免切换会话后丢失上下文。
author: SmallC
license: MIT
tags: [session, sync, memory, chat-history, backup]
compatibility:
  requires:
    - Python 3.8+
    - OpenClaw 2026.3.0+
---

# Session Sync - 跨会话记忆同步

**一句话：让 OpenClaw 各会话共享聊天记录，换会话不丢上下文。**

---

## 解决什么问题？

OpenClaw 的每个会话是独立的，切换会话后无法访问其他会话的历史记录。

**这个技能帮你：**
- ✅ 自动同步各会话聊天记录到共享文件
- ✅ 跨会话访问历史消息
- ✅ 增量同步，避免重复存储
- ✅ 支持 JSON + Markdown 双格式输出

---

## 怎么用？

### 1. 安装前检查

```bash
# 下载后先检查环境
python check_install.py
```

如果显示 "检查完成，可以正常使用！" 就可以继续。如果报错，按提示修复。

### 2. 安装

```bash
# 方式1：通过 OpenClaw 安装
openclaw skills install session-sync

# 方式2：手动复制到技能目录
cp -r session-sync ~/.openclaw/skills/
```

### 3. 配置自动备份（每30分钟）

```bash
openclaw cron add session-sync \
  --interval "30m" \
  --command "python -m session_sync"
```

### 3. 手动备份（现在立刻执行）

```bash
python -m session_sync
```

---

## 会产生什么文件？

同步完成后，聊天记录会保存到：

```
~/.openclaw/workspace/memory/sync/
├── shared_chat.md      ← Markdown 格式，方便人工阅读
├── shared_chat.json    ← JSON 格式，方便程序处理
└── .last_hash          ← 变化检测缓存文件
```

**shared_chat.md** 格式示例：

```markdown
# 共享聊天记录

> 最后同步：2026-03-14T12:21:28

---

## 会话：abc123...

- 消息数：200
- 最后更新：2026-03-14T04:11:29

### 消息 1
**role:** user  
**content:** [内容已脱敏]  
**timestamp:** 2026-03-14T04:11:29.776Z

### 消息 2
...
```

---

## 实际场景

### 场景1：跨会话查看历史

在 Telegram 会话中聊完后，切换到 Control UI 会话：

```
用户：查看 Telegram 会话的最后一条消息
AI：[读取 shared_chat.json 中的 Telegram 会话记录]
```

### 场景2：会话间数据共享

在 Webhook 会话中接收外部数据，在 Telegram 会话中查看：

```
Webhook 接收数据 → 同步到 shared_chat.json → Telegram 会话可访问
```

### 场景3：历史记录备份

定期同步所有会话记录，防止数据丢失：

```bash
# 手动备份
python -m session_sync

# 或配置定时任务自动备份
openclaw cron add session-sync --interval "30m" --command "python -m session_sync"
```

---

## 和其他方案的区别

| | Session Sync | OpenClaw 内置 compaction |
|---|---|---|
| **触发时机** | 定时任务（可配置） | 系统自动触发 |
| **数据位置** | workspace/memory/sync/ | 各会话独立存储 |
| **访问方式** | 跨会话共享 | 会话隔离 |
| **文件格式** | Markdown + JSON | 内部格式 |
| **脱敏处理** | ✅ 自动脱敏 | ❌ 无 |

---

## 隐私与安全

### 数据安全
- ✅ **纯本地运行**：所有数据保存在 `~/.openclaw/workspace/memory/sync/`
- ✅ **无网络连接**：仅读取本地会话文件，不访问任何外部服务
- ✅ **自动脱敏**：邮箱、手机号、API Key 会被替换为 `[EMAIL]`、`[PHONE]` 等

### 生成文件
```
~/.openclaw/workspace/memory/sync/
├── shared_chat.json    # 聊天记录（JSON格式）
├── shared_chat.md      # 聊天记录（Markdown格式）
├── decisions/          # 提取的决策和知识点
├── todos/              # 提取的待办事项
└── .last_hash          # 变化检测缓存
```

### 安全验证
已通过以下测试：
1. ✅ **插件系统测试**：`knowledge` 和 `todo` 插件正常加载运行
2. ✅ **网络监控**：运行期间无外部网络连接
3. ✅ **文件访问**：仅访问 `~/.openclaw/agents/main/sessions/` 目录
4. ✅ **代码审查**：`import os` 已正确包含，无语法错误

---

## 配置（可选）

```bash
# 改备份目录
export SESSION_SYNC_OUTPUT=/你的/自定义/路径

# 改 OpenClaw 目录
export OPENCLAW_STATE_DIR=/你的/openclaw/路径
```

---

## 插件系统

Session Sync 支持插件扩展，内置以下插件：

| 插件 | 功能 | 状态 |
|------|------|------|
| knowledge | 自动提取关键决策和知识点 | ✅ 已启用 |
| todo | 追踪待办事项 | ✅ 已启用 |

### 开发自定义插件

1. 创建 `plugins/my_plugin.py`
2. 继承 `Plugin` 基类
3. 实现 `on_sync` 方法
4. 创建插件实例 `plugin = MyPlugin()`

## 后续计划

| 功能 | 状态 | 说明 |
|------|------|------|
| 自动提取知识点 | ✅ 已实现 | knowledge 插件基础功能 |
| 自动追踪待办 | ✅ 已实现 | todo 插件基础功能 |
| 智能知识提取 | 🔄 待优化 | 使用更好的 NLP 模型 |
| 网页版查看器 | ❌ 未实现 | 计划开发 Web UI |
| 数据可视化 | ❌ 未实现 | 聊天记录统计图表 |

## 版本历史

### v1.0.1 (2026-03-14)
- ✅ 修复 Windows UTF-8 编码问题
- ✅ 修复 OpenClaw 2026.3.x 路径兼容（`agents/main/sessions`）
- ✅ 修复插件系统导入问题

### v1.0.0 (2026-03-10)
- ✅ 基础同步功能
- ✅ JSON + Markdown 双格式输出
- ✅ 增量同步，智能去重
- ✅ 敏感信息自动脱敏

---

## License

MIT - 免费使用，自由修改
