# 高级用法

## 连接已有 Chrome 实例

不启动新浏览器，而是连接到已运行的 Chrome：

```bash
# 先启动 Chrome 并开启远程调试
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222

# 配置 MCP 连接到该端口
```

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest",
               "--browser-url=http://127.0.0.1:9222"]
    }
  }
}
```

适用场景：调试已登录状态的页面、连接特定浏览器 Profile。

---

## Slim 模式（轻量基础功能）

只需要截图、导航等基础操作时，使用 `--slim` 减少工具数量：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--slim", "--headless"]
    }
  }
}
```

Slim 模式工具集更小，适合 Token 敏感场景，完整工具列表见 [Slim 工具参考](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/slim-tool-reference.md)。

---

## 无头模式（CI 环境）

在 CI/CD 中使用，无需图形界面：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--headless"]
    }
  }
}
```

CI 环境会自动禁用使用统计（检测到 `CI` 环境变量）。

---

## 禁用自动更新检查

```bash
export CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS=1
```

---

## 工具参考速查

完整 MCP 工具列表（从对话中直接调用）：

| 工具类别 | 说明 |
|---------|------|
| `screenshot` | 截图当前页面 |
| `navigate` | 导航到 URL |
| `click` | 点击元素 |
| `type` | 输入文本 |
| `evaluate` | 执行 JavaScript |
| `network` | 检查网络请求 |
| `console` | 读取控制台消息 |
| `performance` | 录制性能 Trace |

完整工具文档：https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md

---

## 完成确认检查清单

- [ ] 成功连接到已有 Chrome 实例（如有需要）
- [ ] Slim 模式测试通过（如需精简功能）
- [ ] 无头模式在 CI 脚本中运行成功

---

## 相关链接

- [故障排查](../troubleshooting.md)
- [完整工具参考](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)
- [设计原则](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/design-principles.md)
