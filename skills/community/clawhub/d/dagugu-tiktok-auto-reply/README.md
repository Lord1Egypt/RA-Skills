# TikTok 自动回复技能

⚠️ **重要提醒**：使用自动化回复可能违反 TikTok 服务条款，请谨慎使用！

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/tiktok-auto-reply
npm install
```

### 2. 配置账号

```bash
cp config.example.json config.json
```

编辑 `config.json`，填入你的 TikTok API 凭证：

```json
{
  "tiktok": {
    "accessToken": "你的访问令牌",
    "clientKey": "你的客户端密钥",
    "clientSecret": "你的客户端密码"
  }
}
```

### 3. 获取 TikTok API 权限

1. 访问 [TikTok for Developers](https://developers.tiktok.com/)
2. 注册开发者账号
3. 创建应用
4. 申请以下权限：
   - `video.list` - 获取视频列表
   - `comment.list` - 读取评论
   - `comment.create` - 发布评论

### 4. 运行

```bash
# 测试运行（不会实际发送）
npm start

# 持续监控
npm run watch
```

## 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `keywords` | 搜索关键词列表 | `["热门", "教程"]` |
| `replyTemplates` | 回复模板池 | 见示例 |
| `checkIntervalMinutes` | 检查间隔（分钟） | `30` |
| `maxRepliesPerHour` | 每小时最大回复数 | `10` |
| `dryRun` | 演示模式（不实际发送） | `true` |

## 安全建议

1. **先开启 dryRun 模式测试**
2. **回复频率不要太高** - 建议每小时不超过 10 条
3. **多样化回复内容** - 避免被识别为机器人
4. **定期监控账号状态** - 发现异常立即停止

## 集成到 OpenClaw

将此技能目录添加到 OpenClaw 的技能路径：

```bash
# 在 OpenClaw 配置中添加
~/.openclaw/workspace/skills/tiktok-auto-reply
```

## 常见问题

**Q: 为什么获取不到视频？**
A: 需要 TikTok 企业 API 权限，个人账号权限有限。

**Q: 回复发不出去？**
A: 检查 API 权限是否包含 `comment.create`。

**Q: 账号被限制了怎么办？**
A: 立即停止使用，等待限制解除，降低回复频率。

---

🦞 由 小龙虾 为你打造
