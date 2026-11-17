---
name: book-toolbook-html
description: |
  把一本书 / 一个主题做成「单文件 HTML 翻阅式卡片工具书」的硬编码工作流。
  当用户要"把 XX 做成精美读书笔记 / 工具书网页、单文件 HTML、可左右翻的卡片书、
  方法论口袋书、读书笔记工具书"时调用。
  硬编码资产：双模板（基础/themed 深色多主题）+ 生成脚本（JSON→HTML）+ 自检脚本。
  产出：米色纸感 + 衬线标题 + 书签色带 + 图书馆 hero 渐变蒙版 + 左右翻页（每主题一张卡）
  的响应式单文件 HTML，无外部依赖（除可选 hero 图，离线降级）、手机不裁切。
  不适用于：多页长文报告、需要后端/路由的 Web 应用、纯文字摘要。
agent_created: true
---

# 书 → 翻阅式卡片工具书（单文件 HTML）— 硬编码版

把一本书蒸馏成浏览器直接打开的「卡片书」：封面 + 使用方法 + 目录页 + N 张主题卡 + 封底，
左右翻页、点目录跳。**本版为硬编码工作流：填 JSON → 跑脚本 → 自动产出，无需手写 HTML。**

## 资产清单（直接用，不用读本文）

| 资产 | 用途 |
|---|---|
| `scripts/build_card_book.py` | **生成器**：内容 JSON → 单文件 HTML（自动同步目录/导航/卡片三处） |
| `scripts/check_card_book.py` | **自检器**：结构平衡 / 占位符 / id 对应 / safe center / 箭头分侧 |
| `assets/card-book-template.themed.html` | themed 模板（深色 ☀/🌙 + 5 色板，默认用这个） |
| `assets/card-book-template.html` | 基础模板（米色纸浅色单主题） |
| `references/prompt.md` | 严格提示词（给其它 agent / 手动生成用） |

## 使用流程（三步）

1. **填内容 JSON**（参考 `scripts/build_card_book.py` 头部的示例）：书名/书印单字/导语/关键词/公众号名/卡片数组（名/描述/命题/原文/出处/3 场景）
2. **生成**：`python3 scripts/build_card_book.py cards.json [-o out.html] [--basic]`
3. **自检**：`python3 scripts/check_card_book.py out.html` → 全 ✅ 交付

不满意就改 JSON 重跑（换书/换色/增删卡全在 JSON 层完成）。

## 页面结构（生成器已内置，勿手改）

封面 → 使用方法 → 目录页（缩略卡可跳）→ N 张主题卡（徽章/命题/原文出处/3 场景/返回目录）→ 封底（引流+免责）。
主题卡 3 色循环（c1/c2/c3），目录/导航/卡片 id 三处由脚本同步（#c01..#cN）。

## 硬编码防坑（脚本已处理，手动改模板时注意）

1. `.page` 用 `align-items: safe center`（防顶栏遮挡内容超高被裁）
2. 左右箭头分侧：`.flip.prev{left}` / `.flip.next{right}`——**基类绝不写 left/right**
3. 目录页独立保留（≠导航下拉）；下拉与目录 id 一一对应
4. 翻页**无过渡动画**（用户反感滑动特效）；移动端隐藏顶栏锚点但保留「目录 ▾」
5. hero 在线图 + 深色底色兜底（断网不破图）；中文金句注明"以权威版本为准"
6. 所有 CSS/JS 内联单文件，无外部依赖（除可选 hero 图）

## 手动生成（不跑脚本时）

用 `references/prompt.md` 的严格提示词交给任意 agent，或复制模板后替换 `{{占位符}}`（注意三处同步：目录/导航/主题卡 id 必须一致）。

## 变体说明

- **基础模板**：米色纸浅色单主题。
- **themed 模板**：表面令牌/配色令牌双层分离，顶栏 ☀/🌙 切深色 + 5 色板（classic 赭石/ink 水墨/vermilion 朱砂/jade 碧玉/amethyst 紫晶），localStorage 持久化（`tb-theme`/`tb-palette`）。封面/封底刻意保持深色（电影感）。
