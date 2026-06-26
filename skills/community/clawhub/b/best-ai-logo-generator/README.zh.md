# AI Logo Generator — Claude Code Skill

直接在终端里用 AI 生成专业 Logo，由 [ailogogenerator.online](https://ailogogenerator.online) 提供支持。描述你的品牌，选择风格，几秒钟即可得到可用于生产的 Logo 文件——无需任何设计技能。

---

## 安装

```bash
npx skills add qq919006380/ai-logo-generator
```

完成。Claude Code 会自动加载 `~/.claude/skills/` 目录下的 skill。

---

## 使用方法

打开 Claude Code，描述你的需求：

```
> /ai-logo-generator

你: 帮我给初创公司 "Luminary" 做一个 Logo，简洁现代风，浅紫色和白色

Claude: 正在为 Luminary 生成 Logo...
        生成中... (已用时 3s)
        生成中... (已用时 6s)
        完成！已保存到 ./logo-luminary.png
```

也可以不用斜杠命令，直接对话触发：

```
你: 帮我给命令行工具 "Stackr" 做一个深色科技风 Logo，只要图标不要文字

Claude: [自动加载 ai-logo-generator skill 并生成]
```

---

## 账号认证

首次使用时，skill 会打开浏览器，引导你在 ailogogenerator.online 登录或注册。认证成功后，token 会保存在：

```
~/.config/ailogogenerator.online/auth.json
```

后续使用直接读取缓存 token，无需再次打开浏览器。如需退出登录或切换账号，删除该文件后重新运行 skill 即可。

---

## 工作原理

```
你描述想要的 Logo
        |
        v
Claude 读取 ~/.config/ailogogenerator.online/auth.json
        |
   有 token？
   /         \
  有           没有
  |              |
  |         login.mjs 打开浏览器
  |         捕获回调中的 ?token=
  |         保存到 auth.json
  |              |
  +------+-------+
         |
         v
  POST /api/ai/logo/generate
  (主题、风格、颜色、文字、形状...)
         |
         v
  每 3 秒轮询 /api/ai/logo/query
         |
    状态：completed
         |
         v
  下载 imageUrl -> ./logo-*.png
         |
         v
  告知用户保存路径
```

---

## 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `subject` | string | Logo 代表什么（必填） |
| `vibe` | string | 风格 — modern（现代）、minimalist（极简）、bold（粗犷）、playful（活泼）、elegant（优雅）、vintage（复古）、techy（科技） |
| `colors` | string[] | 十六进制颜色，如 `["#1a1a2e","#e94560"]`。空数组 = AI 自动选色 |
| `text` | string 或 null | Logo 中显示的文字。`null` = 纯图标（不含文字） |
| `withBackground` | boolean | 是否包含背景（默认 false = 透明背景） |
| `shape` | string | 形状 — square（方形）、circle（圆形）、hexagon（六边形）、free（自由） |
| `detail` | string | 附加描述 — "用咖啡杯剪影"、"加一道闪电" |

---

## 积分说明

每次生成消耗 4 积分。新账号注册即赠送积分。如需充值请访问 [ailogogenerator.online](https://ailogogenerator.online)。

---

## 环境要求

- [Claude Code CLI](https://claude.ai/code)
- Node.js >= 18
- 网络连接

---

## 开源协议

[MIT-0（MIT No Attribution）](./LICENSE)
