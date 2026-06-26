# browser-mcp

> Chrome DevTools MCP Skill for OpenClaw / QClaw

通过 Chrome DevTools MCP 协议远程控制 Chrome 浏览器，执行网页自动化任务。

## 功能特性

- 🌐 **网站导航** - 打开任意网站
- 🔍 **内容搜索** - 自动搜索关键词
- 🖱️ **元素交互** - 点击、输入、表单填写
- 📄 **多页面深入** - 列表页→详情页→继续深入
- 📸 **页面截图** - 截取整个页面或局部
- 🚫 **SSRF 白名单** - 支持配置绕过域名拦截
- 🔗 **跨平台连接** - 支持 Windows/Mac/Linux

## 适用场景

- 打开被 SSRF 拦截的网站（ChatGPT、Gemini、X.com 等）
- 自动化网页操作（搜索、填表、点击）
- 远程操控老板的 Chrome 浏览器
- 多步骤复杂网页任务

## 快速开始

### 1. 安装 Skill

```bash
# 使用 clawhub 安装
clawhub install browser-mcp

# 或手动复制 SKILL.md 到 skills 目录
```

### 2. 配置 Chrome 远程调试

Chrome 地址栏输入：
```
chrome://inspect/#remote-debugging
```
勾选 "Discover network targets"

### 3. 配置 openclaw.json

```json
{
  "browser": {
    "ssrfPolicy": {
      "dangerouslyAllowPrivateNetwork": false,
      "allowedHostnames": [
        "*.chatgpt.com",
        "*.gemini.google.com",
        "*.twitter.com",
        "*.x.com",
        "*.github.com"
      ]
    },
    "profiles": {
      "user": {
        "driver": "existing-session",
        "attachOnly": true,
        "cdpPort": 9222,
        "cdpUrl": "http://127.0.0.1:9222"
      }
    }
  }
}
```

### 4. 重启 OpenClaw

## 使用示例

### 打开网站
```
"打开 ChatGPT"
"帮我打开百度"
```

### 搜索内容
```
"帮我搜索 QClaw 最新功能"
"打开 Google 搜索 xxx"
```

### 操作网页
```
"点进去看看"
"帮我填这个表单"
"翻到下一页"
```

## 支持平台

| 平台 | 状态 | 说明 |
|------|------|------|
| Windows 11 + QClaw | ✅ 当前 | Chrome DevTools MCP |
| Windows 11 + OpenClaw | ✅ 支持 | 同上配置 |
| Linux 远程连接 Windows Chrome | 🚧 待支持 | 需要配置远程 CDP |
| Mac 远程连接 Windows Chrome | 🚧 待支持 | 需要配置远程 CDP |

## 触发关键词

打开网站、搜索内容、帮我操作网页、点进去看看、查看详情、打开 ChatGPT/Gemini 等。

## 文档

详细文档请查看 [SKILL.md](./SKILL.md)

## License

MIT
