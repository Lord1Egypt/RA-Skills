# 事件通知系统

> Router 内置事件通知系统,文件位于 `<skill_dir>/data/events.json`（`<skill_dir>` 为技能安装目录,默认 `~/.openclaw/skills/free-model-router`，具体路径取决于当前 OpenClaw 变种）。

## 事件类型

| 类型 | 优先级 | 说明 |
|------|--------|------|
| `announce` | normal | model-server 公告 |
| `modelFailover` | high | 模型故障自动切换 |
| `modelUnavailable` | critical | 模型完全不可用 |
| `dailyStatus` | normal | 每日状态汇报 |
| `providerAdded` | normal | 新增 provider |
| `providerRemoved` | normal | 移除 provider |

## 事件状态

`pending`(待推送) → `notified`(已推送) → `read`(已读)

## 公告事件格式

公告事件可能包含可点击的链接,格式如下:

```json
{
  "id": "{eventId}",
  "title": "{公告标题}",
  "content": "{公告内容描述}",
  "type": "{类型: info/important/warning}",
  "metadata": {
    "url": "{链接地址}",
    "action": "{链接按钮文本}"
  }
}
```

### 推送格式规范

推送公告时,**根据 metadata.url 决定是否展示超链接**:

**有链接时:**
```
📢 公告: {title}

{content}

[🔗 {metadata.action 或 "查看详情"}]({metadata.url})
```

**无链接时:**
```
📢 公告: {title}

{content}
```

### 超链接展示要求

1. **必须使用 Markdown 链接格式**: `[显示文本](URL)`
2. **链接文本优先级**: `metadata.action` > "查看详情"
3. **链接位置**: 放在内容下方，单独一行
4. **链接图标**: 使用 🔗 前缀增强可识别性

### 示例

**带链接的公告:**
```markdown
📢 公告: 新模型上线

Qwen3-Coder 免费模型已上线，支持代码补全和对话。

[🔗 立即体验](https://openrouter.ai/models/qwen/qwen3-coder:free)
```

**不带链接的公告:**
```markdown
📢 公告: 系统维护通知

今晚 02:00-04:00 进行系统维护，期间服务可能不稳定。
```

> **注意:** 公告内容完全由 model-server 动态返回,不要写死数据。如果 `metadata.url` 存在,**在域名校验通过后**向用户展示该链接;`metadata.action` 为链接的可选显示文本。

### 链接安全

公告链接的域名必须经过白名单校验。允许的域名：
- `freemodel.eu.org`
- `freemodel.dpdns.org`

**通过校验**：正常渲染为 Markdown 链接 `[点击查看](url)`。
**未通过校验**：不渲染为可点击链接，改为纯文本展示 `相关链接（未通过安全校验）: url`，并附加警告提示。

## Cron 读取方式

1. 读取 `status=pending` 且 `shouldNotify=true` 的事件
2. 向用户推送
3. 推送后调用 `node <skill_dir>/scripts/free-model-cli.js mark-notified <eventId,...>` 标记已推送,避免重复

## 事件推送示例

**模型故障切换:**
```
⚠️ 模型故障切换
Provider openrouter 主模型 qwen/qwen3-coder:free 故障
已自动切换到备模型: anthropic/claude-sonnet-4:free
```

**模型完全不可用:**
```
🚨 模型不可用
Provider openrouter 所有模型均不可用
请检查 API Key 或稍后重试
```

**每日状态汇报:**
```
📊 每日状态汇报
openrouter: healthy (主模型 qwen/qwen3-coder:free)
modelscope: healthy (主模型 qwen/qwen3:free)
```
