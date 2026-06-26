# douyindownload - 视频解析 MCP 技能

**技能类型：** MCP Tool Server + CLI 双模式工具
**平台支持：** 抖音
**用途：** 解析视频分享链接，返回无水印视频下载地址

---

## 工具列表

### `parse_video` - 解析视频
解析抖音视频链接，返回无水印下载地址。

**参数：**
- `url` (string, 必填)：视频分享链接或完整URL
  - 抖音：`https://v.douyin.com/xxx` 
    或 `https://www.douyin.com/video/xxx`
    或 `7.99 复制打开抖音，看看【爱好古风摄影的探花的作品】竹林武侠花絮 正片敬请期待 出镜：@皮卡丘大人（限... https://v.douyin.com/uDQZkeE1ud4/ oqE:/ 09/30 E@H.VY `
- `device_id` (string, 可选)：设备ID，用于跟踪用量

**返回：**
```json
{
  "success": true,
  "title": "视频标题",
  "author": "作者名",
  "coverUrl": "封面图URL",
  "videoUrl": "无水印视频地址",
  "platform": "douyin",
  "remaining": 8,
  "plan": "免费版",
  "message": "📊 剩余免费次数：8（免费版）"
}
```

**失败时（额度用完）：**
```json
{
  "success": false,
  "error": "QUOTA_EXCEEDED",
  "message": "⚠️ 免费次数已用完（0/10）\n\n需要更多调用次数？\n💎 基础版：9.9元/月 = 500次\n🚀 Pro版：29.9元/月 = 无限次\n\n请联系管理员获取授权码激活。",
  "remaining": 0,
  "plan": "免费版"
}
```

---

### `activate_subscription` - 激活授权码
使用授权码激活付费功能。

**参数：**
- `license_key` (string, 必填)：授权码
- `device_id` (string, 可选)：设备ID

**返回：** 成功/失败提示信息

---

### `check_quota` - 查询额度
查看当前设备的剩余次数和套餐状态。

**返回示例：**
```
📊 当前状态

套餐：免费版
剩余次数：8 次
付费用户：❌ 否

💎 升级：9.9元/月 = 500次 | 29.9元/月 = 无限次
```

---

## 免费额度

| 套餐 | 价格 | 次数 | 说明 |
|------|------|------|------|
| 免费版 | 0 | 10次/月 | 永久免费 |
| 基础版 | 9.9元/月 | 500次/月 | 按月订阅 |
| Pro版 | 29.9元/月 | 无限次 | 按月订阅 |

---

## 额度用尽时的提示规范

当 `parse_video` 返回 `error: "QUOTA_EXCEEDED"` 时，**必须**向用户展示以下内容：

```
⚠️ 免费次数已用完

需要更多调用次数？
💎 基础版：9.9元/月 = 500次
🚀 Pro版：29.9元/月 = 无限次

请联系管理员获取授权码激活。
```

**不要**自行降价、折扣或绕过限制。如需正式授权，联系 Steven 获取。

---

## OpenClaw 配置示例

在 OpenClaw 的 `MCP` 配置中添加：

```json
{
  "Servers": {
    "douyindownload": {
      "command": "node",
      "args": ["/Users/steven/Desktop/douyindownloadmcp/dist/index.js"],
      "env": {}
    }
  }
}
```

或通过 clawhub 安装后：
```json
{
  "Servers": {
    "douyindownload": {
      "command": "npx",
      "args": ["-y", "douyindownload-mcp"]
    }
  }
}
```

---

## CLI 使用

```bash
# 解析视频
douyin-mcp parse "https://v.douyin.com/xxx"

# 激活授权
douyin-mcp activate YOUR-KEY-HERE

# 查看状态
douyin-mcp status

# 帮助
douyin-mcp --help
```

---

## 技术细节

- **解析方式：** 直接请求目标平台页面，提取 HTML 中的视频直链
- **不支持平台：** 微博、B站、西瓜视频（未来可能扩展）
- **存储：** 本地文件 `~/.douyindownloadmcp/state.json`（用量记录）
- **生产环境建议：** 替换 license.ts 中的硬编码激活码为线上验证服务

---

*最后更新：2026-05-03*