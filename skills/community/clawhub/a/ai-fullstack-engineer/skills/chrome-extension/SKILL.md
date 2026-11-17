---
name: chrome-extension
description: 浏览器扩展开发：Manifest V3 约束、权限最小化、Service Worker 陷阱与 Web Store 上架清单
source:
  type: derived
  repo: googlechrome/modern-web-guidance
  path: skills/chrome-extensions/SKILL.md
  updated: 2026-11-02
  url: https://github.com/googlechrome/modern-web-guidance/blob/main/skills/chrome-extensions/SKILL.md
  also:
    - clerk/skills@clerk-chrome-extension-patterns（14.7K 安装）
    - samber/cc-skills@chrome-extension（5.1K 安装）
metadata:
  category: 浏览器扩展
  platform: Chrome
  difficulty: 进阶
---

# Chrome 扩展（MV3 构建 → 调试 → 上架）

> 上游是 Chrome 官方团队维护的指南（2.6K stars，持续更新）。它把规则分成两类：
> **违反即构建失败/功能不可用**的强制项，和上架审查相关的建议项。下面只保留会真实咬人的部分。

## 能力

- **Manifest V3 结构**：service worker / content script / popup / side panel 的边界与消息通路
- **权限最小化**：`host_permissions` 与主动授权（activeTab）的取舍，决定过审与用户信任
- **强制规则排雷**：图标、侧栏触发器、`action.onClicked` 失效等"写完就坏"的坑
- **本地调试**：加载未打包扩展、Service Worker 日志、Content Script 注入时机
- **上架清单**：Web Store 必填项、隐私声明、审核常见驳回原因

## 硬性规则（违反 = 直接坏掉）

### 1. 图标只能引用真实存在的文件，或干脆不写

```jsonc
// ❌ 坏：三个尺寸指向同一个不存在的文件
"icons": { "16": "icon.png", "48": "icon.png", "128": "icon.png" }

// ✅ 对：每个尺寸是独立文件且像素尺寸正确
"icons": { "16": "icons/icon-16.png", "48": "icons/icon-48.png", "128": "icons/icon-128.png" }

// ✅ 也对：拿不到真 PNG 就整段删掉 icons / default_icon，Chrome 会用默认图标
```

> 写了引用却没生成文件，是新手扩展"装了没图标 / 直接加载失败"的头号原因。

### 2. 侧边栏（side panel）必须给触发入口

只声明 `"side_panel": { "default_path": "..." }` **不会让它能被打开**。要挂触发：

```js
// service-worker.js：点图标打开侧栏
// ⚠️ chrome.action.onClicked 只在【没有 default_popup】时才会触发
chrome.action.onClicked.addListener(async (tab) => {
  await chrome.sidePanel.open({ windowId: tab.windowId });
});
```

同时要从 manifest 里**移除 `default_popup`**，否则点击只会弹 popup，`onClicked` 永不触发——
这个组合坑非常隐蔽，因为两个声明看起来都"没报错"。

### 3. MV3 没有持久后台页

`background.scripts`（MV2 的页面式后台）在 MV3 不可用：

| MV2 习惯 | MV3 现实 |
|---|---|
| 后台页面常驻、全局变量存状态 | Service Worker **会被杀**，状态必须落 `chrome.storage` |
| 后台直接开 `setInterval` 做轮询 | 用 `chrome.alarms`（最小周期受限，别指望秒级） |
| 后台里任意 `fetch` 跨域 | 必须声明 `host_permissions`，否则被 CORS 拦 |

## 权限设计（影响过审与用户信任）

```
能不用 broad host_permissions 就不用；
只在当前标签页干活 → "activeTab" + 用户手势触发（点图标/快捷键）；
需要读任意网页 → <all_urls>，但商店审查会要求你在说明里写清用途；
能用 Content Script 局部注入 → 别申请整站权限。
```

- 权限声明与代码里实际调用的 API 必须**自洽**：申请了却不用，审查照样驳回
- 隐私声明里要如实说明是否外发数据、是否含分析脚本——商店会核对代码行为
- 用户数据尽量**只存本地** `chrome.storage.local`，避免"扩展偷偷同步到云端"这类驳回重灾区

## 调试要点

```bash
# 加载未打包扩展：chrome://extensions → 开发者模式 → 加载已解压
# 改完代码要点"重新加载"，Service Worker 不会自动热更
# 看后台日志：扩展卡片上的 "Inspect views: service worker" 链接
# Content Script 日志在目标页面的 DevTools Console（选对应扩展上下文）
```

| 症状 | 常见原因 |
|---|---|
| 图标点了没反应 | 配了 `sidePanel.open` 但保留了 `default_popup` |
| Content Script 没注入 | `matches` 与实际 URL 不符 / 动态渲染早于注入时机 |
| 状态一刷新就丢 | 把状态存在 SW 变量里（SW 已空闲被回收） |
| 打包后权限失效 | manifest 与代码用的 API 不一致，或漏了 `storage` 等权限 |

## 上架前清单

- [ ] 所有被引用的图标文件真实存在且尺寸正确（或已移除 icons 字段）
- [ ] `name` / `description` / `version` 语义化填写，版本随发布递增
- [ ] 权限最小化，且每条权限都能在说明里对应到功能
- [ ] 隐私声明与实际数据行为一致（含第三方脚本）
- [ ] 截图/预览图与实际功能相符（商店会核对）
- [ ] 在**干净 profile** 里跑过一遍核心链路（开发者模式装着的 profile 常已有缓存授权）
- [ ] 未打包目录体积合理，无 `.git` / `node_modules` 冗余

## 边界与协作

- 网页性能与可访问性审计 → [`web-performance`](../web-performance/SKILL.md)、`skills-repo/accessibility-engineer`
- 需要"驱动浏览器验证扩展行为" → [`browser-cli-agent`](../browser-cli-agent/SKILL.md)
- 前端组件与样式（popup/side panel 页面本体） → [`component-builder`](../component-builder/SKILL.md)、[`css-master`](../css-master/SKILL.md)
