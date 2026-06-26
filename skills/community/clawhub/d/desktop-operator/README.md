# Desktop Operator Skill

通过 **Puppeteer CDP** 连接 Electron 应用，实现自动打开应用、查找文本元素、点击、截图的 OpenClaw Skill。

## 原理

Electron 应用基于 Chromium，支持通过 `--remote-debugging-port` 开启 Chrome DevTools Protocol（CDP）。本 Skill 启动 Electron 应用时注入该参数，再用 Puppeteer 连接 CDP，像操作网页一样精确定位 DOM 元素并点击，无需 OCR，准确率 100%。

## 功能特性

- 自动找到应用可执行文件并以 CDP 模式启动
- Puppeteer 连接 CDP，枚举所有页面
- 遍历 DOM 找到包含目标文本的可见元素并点击
- 等待页面渲染稳定后截图
- 纯 Node.js 实现，无 Python 依赖

## 使用

```bash
node dist/index.js --app "应用名称" --target "目标文本"
```

**参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `--app` | 应用名称（`/Applications/` 下的 `.app` 名） | `DaveBella` |
| `--target` | 要点击的元素文本 | `订单中心` |

**示例：**

```bash
node dist/index.js --app "DaveBella" --target "订单中心"
```

## 输出

标准输出 JSON：

```json
{ "screenshot": "/tmp/desktop_operator_skill_1234567890.png" }
```

## macOS 权限

首次使用需在系统设置中授权：

**系统设置 → 隐私与安全性 → 辅助功能** — 允许 Terminal / Node

## 注意事项

- 仅适用于 Electron 应用（基于 Chromium）
- 应用必须安装在 `/Applications/` 目录下
- 如果应用已在运行，建议先退出再重新启动（避免 CDP 端口冲突）

## 技术栈

- **Node.js**: >= 18
- **TypeScript**
- **Puppeteer**: CDP 连接与 DOM 操作
