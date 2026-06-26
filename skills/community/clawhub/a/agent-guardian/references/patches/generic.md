# 通用渠道适配指南

本文档说明如何将 Agent Guardian 集成到任意渠道插件中。
核心原理相同，只是 hook 点位置因渠道而异。

## 适配原理

任何渠道插件都有两个关键流程：

1. **入站（Inbound）** — 接收用户消息
2. **出站（Outbound）** — 发送AI回复

Agent Guardian 在这两个流程中插入以下逻辑：

### 入站 Hook（收到用户消息时）

```
用户消息 → 
  ① 写活跃时间 /tmp/user-last-active.txt
  ② 检测是否 /new 或 /reset → 重置工作状态
  ③ 检测"状态"关键词 → 写触发文件（绕过AI）
  ④ 检测消息语言 → 写 /tmp/user-msg-language.txt
  ⑤ 消息入队 msg-queue.py add + start
  → 正常流程继续
```

### 出站 Hook（发送AI回复时）

```
AI回复 → 
  ① 语言过滤 lang-filter.py（中文语境替换英文混用）
  ② 语言一致性检测（纯英文回复给中文用户 → 告警）
  → 发送消息
  ③ 标记消息队列完成 msg-queue.py done
  ④ 更新工作状态 update-work-state.sh done
```

## 适配步骤

### 步骤1：找到入站消息处理函数

不同渠道的入站处理位置：

| 渠道 | 文件 | 关键函数/事件 |
|------|------|--------------|
| QQ Bot | gateway.ts | C2C_MESSAGE_CREATE |
| Telegram | 通常是 webhook handler | message event |
| 微信 | 回调服务器 | text/event message |
| 飞书 | event handler | im.message.receive_v1 |
| Discord | gateway handler | MESSAGE_CREATE |

### 步骤2：找到出站消息发送函数

| 渠道 | 文件 | 关键函数 |
|------|------|---------|
| QQ Bot | outbound.ts | sendC2CMessage |
| Telegram | 通常是 sendMessage | bot.sendMessage |
| 微信 | reply handler | 被动/主动消息接口 |
| 飞书 | reply handler | im.message.create |
| Discord | outbound | channel.send |

### 步骤3：插入 Hook 代码

参考 qqbot.md 中的具体代码块，将 execSync 调用插入对应位置。

### 步骤4：测试

1. 发送普通消息 → 检查 /tmp/user-last-active.txt 是否更新
2. 发送"状态" → 检查是否秒回状态信息
3. 发送中文消息，等待包含英文混用的回复 → 检查是否被过滤
4. 发送 /new → 检查工作状态是否重置

## 不修改插件源码的降级方案

如果不想/不能修改插件源码，以下功能仍可使用（但依赖AI自觉执行）：

| 功能 | 需要插件patch | 降级方案 |
|------|:---:|---------|
| 看门狗 | ❌ | openclaw cron 直接可用 |
| 定时汇报 | ❌ | 系统 crontab 直接可用（但需AI写活跃时间） |
| 即时状态查询 | ✅ | 降级为AI处理"状态"消息 |
| 语言过滤 | ✅ | 降级为SOUL.md规则（AI自律） |
| 活跃时间记录 | ✅ | 降级为AI在SOUL.md中执行 |
| 消息队列 | ✅ | 降级为AI主动调用脚本 |

降级方案约覆盖60%功能，核心看门狗和定时汇报仍可正常工作。
