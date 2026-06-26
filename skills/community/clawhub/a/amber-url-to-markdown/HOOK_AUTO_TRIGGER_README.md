# Amber Url to Markdown - Hook 自动触发方案

## 问题背景

在 ClawHub 上发布的技能，用户安装后无法自动触发，需要 AI 手动调用。这是因为技能的 `SKILL.md` 中描述的"自动触发"只是文档约定，而不是真正的自动触发机制。

## 解决方案

使用 OpenClaw 的 **Hooks 系统**，创建一个监听 `message:received` 事件的 Hook，实现真正的自动触发。

## Hook 结构

```
amber-url-to-markdown/
├── hooks/
│   └── url-auto-fetch/
│       ├── HOOK.md          # Hook 元数据 + 文档
│       └── handler.ts       # Hook 实现
├── scripts/
│   └── amber_url_to_markdown.py
├── SKILL.md
└── _meta.json
```

## Hook 实现要点

### 1. HOOK.md 元数据

```yaml
---
name: url-auto-fetch
description: "自动检测用户发送的 URL 链接并调用 amber-url-to-markdown 技能抓取内容"
metadata: { "openclaw": { "emoji": "🔗", "events": ["message:received"], "requires": { "bins": ["python3"] } } }
---
```

### 2. handler.ts 实现

关键逻辑：

1. **监听 `message:received` 事件**
2. **检测 URL**：使用正则表达式匹配消息中的 URL
3. **判断触发条件**：
   - 纯 URL 消息（消息中只有 URL）
   - URL + 意图关键词（解析、转换、markdown 等）
4. **执行脚本**：异步调用 `amber_url_to_markdown.py`
5. **发送提示**：告知用户正在抓取

### 3. _meta.json 配置

```json
{
  "hooks": [
    {
      "id": "url-auto-fetch",
      "path": "hooks/url-auto-fetch",
      "description": "自动检测用户发送的 URL 链接并调用技能抓取内容",
      "events": ["message:received"],
      "auto_enable": false,
      "config": {
        "enabled": true,
        "trigger_on_pure_url": true,
        "trigger_on_intent_keywords": true
      }
    }
  ]
}
```

## 发布到 ClawHub

### 1. 更新 package.json（如果使用 npm 包）

```json
{
  "name": "amber-url-to-markdown",
  "version": "3.2.0",
  "openclaw": {
    "hooks": ["./hooks/url-auto-fetch"]
  }
}
```

### 2. 更新 SKILL.md

在文档开头添加 Hook 启用说明：

```markdown
## 🚀 自动触发（V3.2 新增）

**安装技能后，启用 Hook 即可实现真正的自动触发！**

### 启用自动触发 Hook

```bash
# 1. 查看可用 Hook
openclaw hooks list

# 2. 启用 url-auto-fetch Hook
openclaw hooks enable url-auto-fetch

# 3. 检查 Hook 状态
openclaw hooks check
```
```

### 3. 发布新版本

```bash
# 更新版本号
# _meta.json: "version": "3.2.0"

# 发布到 ClawHub
clawhub publish
```

## 用户安装流程

### 方式 1：从 ClawHub 安装

```bash
# 安装技能
clawhub install amber-url-to-markdown

# 启用 Hook
openclaw hooks enable url-auto-fetch

# 重启 Gateway
openclaw gateway restart
```

### 方式 2：手动安装

```bash
# 克隆技能
git clone https://github.com/OrangeViolin/amber-url-to-markdown.git ~/openclaw/skills/amber-url-to-markdown

# 复制 Hook 到 managed hooks 目录
cp -r ~/openclaw/skills/amber-url-to-markdown/hooks/url-auto-fetch ~/.openclaw/hooks/

# 启用 Hook
openclaw hooks enable url-auto-fetch

# 重启 Gateway
openclaw gateway restart
```

## Hook 工作原理

```
用户发送消息
    ↓
Gateway 接收消息
    ↓
触发 message:received 事件
    ↓
Hook handler 执行
    ↓
检测消息内容
    ├─ 无 URL → 跳过
    ├─ 有 URL 但无意图 → 跳过
    └─ 有 URL 且有意图 → 继续
         ↓
    执行 Python 脚本
         ↓
    异步抓取网页
         ↓
    保存 Markdown 文件
         ↓
    （可选）发送完成通知
```

## 触发条件详解

### 纯 URL 消息

消息中只包含 URL，没有其他文字：

```
https://mp.weixin.qq.com/s/xxx
```

判断逻辑：
```typescript
const isPureUrl = content.trim().replace(urlPattern, "").trim().length === 0;
```

### URL + 意图关键词

消息包含 URL 且有明确的意图关键词：

```
帮我把这篇文章转成 Markdown：https://mp.weixin.qq.com/s/xxx
解析这个链接：https://zhuanlan.zhihu.com/p/xxx
```

意图关键词列表：
- 解析、转换、转成、转为、生成、抓取、爬取、下载
- markdown、md、文章、内容

## 注意事项

### 1. 异步执行

Hook 使用 `child_process.exec` 异步执行脚本，不阻塞消息处理。这意味着：

- ✅ 不会延迟 AI 回复
- ⚠️ 无法立即返回抓取结果
- ✅ 适合后台处理

### 2. 错误处理

Hook 会捕获脚本执行错误，但不会主动通知用户（避免骚扰）。用户可以在以下位置查看结果：

- `/root/openclaw/urltomarkdown/` 目录

### 3. 性能考虑

- Hook 只在检测到 URL 时触发
- 使用异步执行，不影响正常消息处理
- 脚本执行超时设置为 2 分钟

### 4. 安全考虑

- 只处理用户发送的消息
- 跳过机器人自己的消息
- URL 经过转义后传递给脚本

## 测试 Hook

### 1. 检查 Hook 是否已启用

```bash
openclaw hooks list
# 应该显示：🔗 url-auto-fetch ✓
```

### 2. 发送测试消息

```
https://mp.weixin.qq.com/s/test123
```

### 3. 查看日志

```bash
# 查看 Gateway 日志
tail -f ~/.openclaw/gateway.log | grep url-auto-fetch

# 或查看脚本输出
tail -f /root/openclaw/skills/amber-url-to-markdown/scripts/output.log
```

### 4. 验证结果

```bash
ls -lt /root/openclaw/urltomarkdown/*.md | head -1
```

## 未来优化

1. **配置化**：允许用户自定义触发关键词
2. **通知优化**：抓取完成后主动发送通知
3. **并发控制**：限制同时抓取的 URL 数量
4. **白名单**：只处理特定网站的 URL
5. **缓存**：已抓取的 URL 不重复抓取

## 参考资料

- [OpenClaw Hooks 文档](https://docs.openclaw.ai/automation/hooks)
- [OpenClaw CLI 参考](https://docs.openclaw.ai/cli/hooks)
- [Bundled Hooks 示例](https://github.com/openclaw/openclaw/tree/main/src/hooks/bundled)
