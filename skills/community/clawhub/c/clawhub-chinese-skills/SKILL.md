---
name: clawhub-chinese-skills
description: 从 ClawHub 最新上传的 skill 中筛选中文用户上传的 skill 并汇报给用户。当用户要求查看最新中文 skill、查看新上传的中文技能、或类似需求时使用。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "openclaw": ">=0.15" },
        "tags": ["clawhub", "skill", "中文", "最新", "监控"],
      },
  }
---

# ClawHub 中文 Skill 查询

从 ClawHub 最新上传的 skill 中筛选出中文用户上传的 skill，并汇总链接返回给用户。

## When to Use

- 用户要求查看最新上传的中文 skill
- 用户要求监控 ClawHub 新上线的中文技能
- 用户说"查看最新中文 skill"、"筛选中文技能"等

## How to Use

### 执行流程

1. **启动浏览器**：确保 OpenClaw Browser 已启动，如未启动运行 `openclaw browser start`
2. **打开 ClawHub 页面**：访问 `https://clawhub.ai/skills?sort=newest`
3. **获取页面快照**：运行 `openclaw browser snapshot` 获取页面元素
4. **分析中文 skill**：运行 evaluate 命令提取所有 skill 链接和介绍
5. **筛选中文内容**：用正则检测标题或介绍中是否包含中文字符
6. **格式化输出**：将结果以列表形式展示给用户

### 关键命令

```bash
# 1. 启动浏览器
openclaw browser start

# 2. 打开页面
openclaw browser open "https://clawhub.ai/skills?sort=newest"

# 3. 等待加载
sleep 5

# 4. 获取所有 skill 链接和介绍
openclaw browser evaluate --fn "() => {
  const links = document.querySelectorAll('a[href^=\"/\"]');
  const results = [];
  links.forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.match(/^\\/[a-zA-Z0-9_-]+\\/[a-zA-Z0-9_-]+$/)) {
      const text = link.innerText.trim();
      if (text) {
        results.push({href, text: text.substring(0, 200)});
      }
    }
  });
  return JSON.stringify(results.slice(0, 60), null, 2);
}"

# 5. 筛选中文（检测 \\u4e00-\\u9fff 范围的中文字符）
```

### 筛选规则

判断是否为中文 skill 的方法：检查 skill 的**标题或介绍**中是否包含中文字符（Unicode 范围 \u4e00-\u9fff）。

### 输出格式

```
📋 最新中文 Skill 汇总（共 X 个）

1. **Skill 名称** - 简要描述
   - 链接

2. ...
```

## 定时任务（可选）

如果用户要求**每日定时汇报**，创建一个 cron 定时任务：

```bash
# 每天早上 9 点执行
openclaw cron add --schedule "cron 0 9 * * *" --sessionTarget isolated
```

**注意**：
- 使用 `delivery.mode="announce"` 将结果推送到用户当前频道
- 投递对象填写当前用户的标识（根据当前会话的 channel 类型确定）

### 创建后检查步骤（重要）

创建完定时任务后，**必须**执行以下检查：

1. **查看已创建的定时任务**：
   ```bash
   openclaw cron list
   ```

2. **检查投递目标是否正确**：
   - 确认 `delivery.channel` 或 `delivery.to` 是否填写了当前对话用户的 ID/标识
   - 确认投递目标是用户当前使用的频道（webchat、telegram、discord 等）

3. **如果投递目标不正确**：
   - 使用 `openclaw cron update <jobId>` 更新投递配置
   - 或者删除后重新创建：`openclaw cron remove <jobId>` 然后重新创建

4. **验证**：
   - 手动触发一次测试：`openclaw cron run <jobId>`
   - 确认结果能正确投递到用户当前会话的频道

### 当前会话信息（参考）

在创建定时任务时，需要根据当前会话的 metadata 确定投递目标：
- `channel`: 当前消息的通道类型（如 webchat、telegram 等）
- `provider`: 消息提供者
- `surface`: 消息表面类型

这些信息会随消息一起发送，可用于配置定时任务的投递目标。

## Edge Cases

- **页面加载失败**：检查网络连接，重试打开页面
- **未找到中文 skill**：返回"未在当前页面找到中文 skill，请稍后重试"
- **页面需要滚动加载**：使用 `openclaw browser evaluate` 检查是否有更多内容，必要时滚动页面
