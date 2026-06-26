# 🎬 douyindownload - 视频解析 MCP/CLI 工具

去水印解析抖音视频，支持 MCP 协议和 CLI 两种调用方式。

---

## 安装

```bash
cd douyindownloadmcp
npm install
npm run build
```

---

## CLI 模式

```bash
# 解析视频
node dist/cli.js parse "https://v.douyin.com/xxx"

# 激活授权码
node dist/cli.js activate YOUR-KEY

# 查看状态
node dist/cli.js status

# 全局命令（需 npm link）
douyin-mcp parse "https://v.douyin.com/xxx"
```

---

## MCP 模式

### 1. 在 OpenClaw 中配置

在 `~/.openclaw/config.json` 的 `mcp` 段落添加：

```json
{
  "servers": {
    "douyindownload": {
      "command": "node",
      "args": ["/Users/steven/Desktop/douyindownloadmcp/dist/index.js"]
    }
  }
}
```

重启 OpenClaw 后生效。

### 2. 可用的 Tool

| Tool | 说明 |
|------|------|
| `parse_video` | 解析视频链接，返回无水印地址 |
| `activate_subscription` | 激活授权码 |
| `check_quota` | 查看当前额度 |

---

## 定价

| 套餐 | 价格 | 次数 | 适用 |
|------|------|------|------|
| 免费版 | 0 | 10次/月 | 试用 |
| 基础版 | 9.9元/月 | 500次/月 | 个人用户 |
| Pro版 | 29.9元/月 | 无限次 | 重度用户/商用 |

---

## 额度用尽时的展示

当 `parse_video` 返回 `QUOTA_EXCEEDED` 时，AI 智能体会自动向用户展示：

```
⚠️ 免费次数已用完

需要更多调用次数？
💎 基础版：9.9元/月 = 500次
🚀 Pro版：29.9元/月 = 无限次

请联系管理员获取授权码激活。
```

---

## 文件结构

```
douyindownloadmcp/
├── src/
│   ├── config.ts    # 配置（定价、文案）
│   ├── parser.ts    # 视频解析核心
│   ├── license.ts   # 授权与用量管理
│   ├── index.ts     # MCP Server（stdio 协议）
│   └── cli.ts       # CLI 入口
├── dist/            # 编译输出
├── SKILL.md         # OpenClaw Skill 说明
├── package.json
└── tsconfig.json
```

---

## 扩展方向

- [ ] 接 GitHub OAuth 做线上激活码系统
- [ ] 支持 TikTok / Instagram / YouTube
- [ ] 打包成 Homebrew / npm 全局包
- [ ] 做独立支付页面（微信/支付宝当面付）
- [ ] 接入 Stripe 出海收款

---

*联系 Steven 获取授权码或定制开发*