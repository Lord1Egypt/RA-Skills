---
name: desktop-operator
description: Operate Electron desktop applications on macOS via Puppeteer CDP. Open an app, find a UI element by text, click it, and take a screenshot.
---

# desktop-operator

通过 Puppeteer CDP 连接 Electron 桌面应用，自动完成打开应用、点击指定文本元素、截图的操作。

## 适用场景

用于自动化本地 Electron 应用（如各类管理后台、工具软件）。

示例触发语：

- 打开 DaveBella 应用，点击订单中心，然后截图
- 打开 xx 应用，点击顶部的订单中心
- 打开 xx 应用，进入数据分析页面截图

---

## Parameters

| 参数 | 说明 |
|------|------|
| `--app` | 应用名称，即 `/Applications/` 下 `.app` 文件名（不含 .app） |
| `--target` | 要点击的元素文本内容 |

---

## Execution

```
node dist/index.js --app "{appName}" --target "{targetText}"
```

示例：

```
node dist/index.js --app "DaveBella" --target "订单中心"
```

---

## Output

成功后输出 JSON：

```json
{ "screenshot": "/tmp/desktop_operator_skill_xxxxxxxxx.png" }
```

截图路径即为操作完成后的页面截图，可直接展示给用户。

---

## 注意事项

- 仅适用于 Electron 应用
- 应用需安装在 `/Applications/` 目录下
- 首次使用需在「系统设置 → 隐私与安全性 → 辅助功能」中授权 Terminal
