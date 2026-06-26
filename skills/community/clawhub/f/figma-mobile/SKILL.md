---
name: figma-mobile
description: >
  将 Figma 设计稿转为移动端 UI 代码（Android Jetpack Compose / XML，iOS SwiftUI / UIKit）。
  在用户粘贴 Figma 链接并希望生成布局代码时使用。
  通过 Figma REST API 提取设计树与 token，必要时追问澄清，再输出可落地的工程代码。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"], "env": ["FIGMA_TOKEN"] },
        "primaryEnv": "FIGMA_TOKEN",
        "install": [],
      },
  }
---

# Figma 转移动端

用交互式澄清流程，把 Figma 设计转为移动端 UI 代码。

支持：Android Compose、Android XML、iOS SwiftUI、iOS UIKit。

## 环境要求

- 环境变量 `FIGMA_TOKEN`（Figma → 头像 → Settings → Security → Personal Access Tokens）
- **Node.js 18+**（内置 `fetch`；脚本为纯 JavaScript，**无需** `npm install`）
- 脚本入口：在 `scripts/` 下执行 `node src/figma-fetch.js`，或 `npm run figma-fetch --`（`package.json` 仅用于声明 `type: module` 与 npm 脚本快捷方式，无第三方依赖）

## 触发与输入

用户粘贴 **Figma 设计链接** 时启用本技能。

用户也可能在链接旁给出 **内联提示**，例如：

- 目标平台：「Android XML」「Compose」「SwiftUI」「UIKit」
- 布局偏好：「用 ConstraintLayout」「优先 StackView」
- 组件说明：「开关用我们的 CompactSwitch」「这块是动态列表」

**若用户已通过内联说明回答某类问题，则不要再问同类问题。**
例如用户已写「Android XML，三张卡是 RecyclerView 列表」，则不要再问输出格式或列表动静态。

## 工作流

### 步骤 1：拉取与分析

用户提供 Figma 链接后：

1. 在技能根目录进入 `scripts/`，运行：
   `node src/figma-fetch.js "<url>" [--json] [--depth N]`
   若用户提供 **多个链接**（同一页不同状态），使用 `--compare` 拉取并对比差异，便于多状态代码（selector、条件样式等）：
   `node src/figma-fetch.js --compare "<url1>" "<url2>" [--json]`
2. 分析结构：区块、重复模式、组件类型
3. 关注 **INSTANCE** 节点（组件实例），结合 `variantProperties` 理解状态（如 State=Default）
4. 复杂渐变/阴影在总结中向用户点明
5. 生成代码前遵守 `references/figma-interpretation.md` 中的节点语义规则

**详细解读规则**：阅读 `references/figma-interpretation.md`

### 步骤 1.5：结构摘要

在提问之前，先用 **2～3 行** 向用户确认你理解的结构，例如：

> 我看到：顶部导航（返回 + 标题）→ 两大块内容（用户资料卡、设置列表约 8 项）→ 底部主按钮。约 25 个节点。

需覆盖：主要区域、重复模式（如「8 个相似列表项」）、显眼元素（渐变、插画、叠卡）。

若用户纠正结构，先修正理解再进入步骤 2。

结构非常简单时（如单卡片 + 少量输入框）可跳过本步。

### 步骤 2：确认与追问

**问题顺序（严格先问靠前的）：**

1. **输出形态**（除非用户已说明，否则必须先问）
   → Android XML / Compose / SwiftUI / UIKit  
   决定后续分析与代码风格。

2. **结构歧义**（只问真正不确定的）
   → 「这几项看起来相似——动态列表还是写死布局？」
   → 「这块是整图资源还是图标+背景组合？」

3. **组件选型**（仅在与平台相关时）
   → 「是否有指定自定义组件？没有则使用系统默认。」

**追问规则：**

- 用户已在提示里回答的项一律跳过
- 总共 **最多 3～5 个问题**，越少越好
- 每个问题给具体选项 + 一句利弊，并保留「或详细说说你的需求」
- 自然语言表述，不要甩原始 JSON
- 若上下文已足够且结构简单，**可跳过步骤 2** 直接进入步骤 3

**何时追问 vs 直接生成：**

- 同级下 **≥3 个**结构相似子节点 → 可能是列表 → **应追问**动静态
- 共享 `componentId` 的 INSTANCE → 复用组件 → **可说明**并给默认实现
- 层次单一、无歧义 → 高置信度 → **可不问**直接生成
- 设计中有渐变/重阴影 → 在摘要中说明处理方式

### 步骤 2.5：工程扫描（可选，建议）

若本地能访问目标工程，可运行扫描以复用颜色、字符串等资源：

```bash
cd scripts
node src/project-scan.js /path/to/project --json --output scan-report.json
```

**如何在生成代码时使用扫描结果**：阅读 `references/figma-scan-usage.md`

### 步骤 3：生成代码

用户确认后（或无需追问时）生成代码文件。

**详细生成规则**：阅读 `references/code-generation.md`

多文件时每个文件用清晰标题标出，例如：

```
📄 activity_notification_settings.xml
[代码]

📄 item_expert_notification.xml
[代码]
```

### 步骤 4：迭代与反馈记录

展示代码后简短询问：

> 是否贴合设计？需要调整的地方？

用户可能继续迭代：间距、替换组件、删区块、换平台、改色值等。

**除非用户要求整页重写，否则每轮只改变化部分。**

**反馈记录（建议自动执行）：**  
每当用户纠正生成结果，在项目根目录维护 `feedback-log.md`（不存在则创建）。每条格式：

```
## YYYY-MM-DD HH:MM
- **Platform**: Android XML / Compose / SwiftUI / UIKit
- **Figma node type**: （如：带图标的 FRAME、Tab 栏、按钮组）
- **Issue**: 问题简述
- **Before**: 原先生成内容（片段或说明）
- **After**: 用户期望（片段或说明）
- **Rule candidate**: （可选）可沉淀为通用规则的说明
```

记录应 **简洁、可分类、偏映射错误**；不要记录纯个人偏好或一次性命名。

可在适当时机或应用户要求运行：

```bash
cd scripts
node src/feedback-analyze.js [path/to/feedback-log.md]
```

用于汇总模式与规则候选（默认读取当前目录下的 `feedback-log.md`）。

## 矢量与 SVG

需从 Figma 导出 SVG 时（见 `references/code-generation.md`）：

```bash
cd scripts
node src/figma-fetch.js "<url>" --export-svg [--nodes "节点id1,节点id2"]
```

简化后的 JSON 中每个节点含 `id` 字段，可用于 `--nodes` 附加导出。

## 异常处理

- **`FIGMA_TOKEN` 未设置**（脚本打印 `FIGMA_TOKEN_NOT_SET`）→ **不要**让用户自行敲复杂命令。应：
  1. 说明需要 Figma Personal Access Token
  2. 指引：Figma → 头像 → Settings → Security → Personal Access Tokens
  3. 请用户在对话中粘贴 token（通常以 `figd_` 开头）
  4. 将 token 写入项目根目录 `.env`：`FIGMA_TOKEN=figd_xxx`（脚本会自动读取 `.env`）
  5. 再次执行 `node src/figma-fetch.js` 或 `npm run figma-fetch --`

- **Token 无效**（401/403）→ 可能过期或撤销，请用户重新生成并更新 `.env`

- **链接无效** → 给出正确示例：`https://www.figma.com/design/<fileKey>/<name>?node-id=<id>`

- **API 其它错误** → 展示错误信息，提示检查网络/代理

- **子节点过多（>200）** → 脚本会在 JSON 中标注 `_largeChildList`，建议缩小选区 Frame

- **深度截断** → 脚本会将 `_truncated` 标在节点上，必要时提高 `--depth`（最高可自动提升到 15 层对比模式）

## 参考文档说明

`references/` 下文档按 **命名约定** 区分用途（见 `README.md`「目录与命名」）：`figma-*` 为 Figma 语义与扫描用法，`platform-*` 为各平台映射表，`code-generation.md` 为生成总则。正文为 **中文**，代码与 API 标识保留英文原名；工作流以本 **SKILL.md** 为准。
