# FeishuMention Resolver (v2.0) - 调试指南

## 🔍 问题诊断步骤

### Step 1: 检查 OpenClaw 配置

解析器完全依赖 `~/.openclaw/openclaw.json`。

1.  打开配置文件：
    ```bash
    cat ~/.openclaw/openclaw.json
    ```
2.  检查 `channels.feishu.accounts` 部分：
    *   是否存在你使用的 `accountId` (例如 `elves`)？
    *   是否存在你要 @ 的机器人账号 (例如 `product`)？
    *   `appId` 和 `appSecret` 是否正确？

### Step 2: 开启调试日志

设置环境变量 `DEBUG=true` 运行你的脚本或 Agent，以查看详细的解析日志。

```bash
DEBUG=true node your_script.js
```

**日志示例：**
```
[FeishuMention INFO] 正在刷新机器人缓存...
[FeishuMention INFO] 成功获取机器人信息: Product (open_id: ou_xxx)
[FeishuMention INFO] 解析提及: "@product" -> "<at user_id="ou_xxx">product</at>"
```

### Step 3: 检查机器人缓存

解析器会将发现的机器人信息缓存到本地。检查缓存文件确认是否成功获取了 Bot ID。

```bash
cat ~/.openclaw/workspace/cache/feishu_mentions/bots_info.json
```

**预期内容：**
```json
{
  "updated_at": 1710000000000,
  "data": [
    {
      "name": "Product Bot",
      "open_id": "ou_c610...",
      "accountId": "product"
    }
  ]
}
```
*如果 `data` 为空，说明 API 调用失败，请检查 Step 1 中的凭证。*

---

## 🐛 常见错误及解决方案

### 错误 1: `@product` 未被解析 (原样输出)

**可能原因:**
1.  `openclaw.json` 中没有配置 `product` 账号。
2.  配置的 `appId/Secret` 错误，导致无法调用 API 获取 Bot ID。
3.  机器人在飞书后台的名称不是 "Product"，且你使用的 `@` 名称与 Account ID 也不匹配。

**解决方案:**
*   确保 `openclaw.json` 正确。
*   尝试删除缓存文件 `rm ~/.openclaw/workspace/cache/feishu_mentions/bots_info.json` 强制刷新。

### 错误 2: 群成员解析失败

**可能原因:**
1.  使用的 `accountId` (调用者) 所在的机器人未加入该群。
2.  机器人未开通「获取群组成员」权限。

**解决方案:**
*   在飞书客户端拉机器人进群。
*   在飞书开发者后台 -> 权限管理 -> 搜索 "获取群组信息" 和 "获取群组成员" 并开通。

---

## ✅ 验证脚本

使用内置的测试脚本验证环境：

```bash
# 1. 进入目录
cd ~/.openclaw/skills/feishu-mention

# 2. 运行测试 (使用你的 accountId)
# 修改 test.js 中的 accountId 和 chatId
DEBUG=true node test.js
```
