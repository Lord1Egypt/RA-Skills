# Figma 转移动端（figma-mobile）

用 AI 将 Figma 设计稿转为可落地的移动端 UI 代码。

支持：**Jetpack Compose** · **Android XML** · **SwiftUI** · **UIKit**

脚本为 **JavaScript（ESM）**，需 **Node.js 18+**（内置 `fetch`）。**无需 `npm install`**，不依赖任何 npm 包；`scripts/package.json` 仅用于声明 `"type": "module"` 与 `npm run` 快捷命令。

## 演示

与 Figma 社区 [Material Design 3 Messaging App](https://www.figma.com/community/file/1169726503071187057/) 的对比示例：

![Figma 与 Compose 对比](assets/demo-comparison.png)

**左：** Figma 设计稿 · **右：** 生成的 Jetpack Compose 在 Android Studio 中运行

工具读取 Figma 节点树（自动布局、样式引用、变体等），生成符合平台习惯的代码，而不是纯绝对坐标堆砌。

## 工作原理

1. **拉取**：`scripts/src/*.js` 调用 Figma REST API，导出节点树 JSON
2. **解读**：模型理解布局语义（如「6 个相似行 → LazyColumn」）
3. **生成**：输出带主题与组件惯例的代码（Material 3、SF Symbols 等）
4. **迭代**：用自然语言持续修改（如「标题栏吸顶」「换深色主题」）

## 安装

### OpenClaw

```bash
clawhub install figma-mobile
```

### Claude Code / 其它 Agent

将本技能文件夹复制到项目约定目录，例如：

```
your-project/.claude/skills/figma-mobile/
```

或：

```
your-project/.agents/skills/figma-mobile/
```

### 脚本依赖

**无需安装。** 确保本机有 Node.js 18+ 即可。若希望使用 `npm run figma-fetch` 等别名，可在 `scripts/` 目录执行 `npm install`（无依赖包，仅解析 package.json）。

## 配置

1. 获取 Figma Personal Access Token：  
   Figma → 头像 → Settings → Security → Personal Access Tokens，新建 token（一般以 `figd_` 开头）。

2. 设置环境变量，或把下面一行写入项目根目录 `.env`（脚本会自动读取）：

   ```bash
   # macOS / Linux
   export FIGMA_TOKEN="figd_your_token_here"

   # Windows PowerShell
   $env:FIGMA_TOKEN = "figd_your_token_here"
   ```

## 使用

在对话中粘贴 Figma 设计链接，例如：

> 把这个转成 Jetpack Compose：https://www.figma.com/design/xxx/Project?node-id=100-200

Agent 会：

1. 在 `scripts/` 下调用 `figma-fetch` 拉取设计数据  
2. 必要时追问平台、列表动静态等  
3. 生成工程化代码文件  
4. 根据你的反馈迭代  

常用命令（均在 `scripts/` 目录执行，`node` 与 `npm run` 二选一）：

```bash
node src/figma-fetch.js "https://www.figma.com/design/..."
npm run figma-fetch -- "https://www.figma.com/design/..."

node src/figma-fetch.js --compare "<url1>" "<url2>"

node src/project-scan.js /path/to/android/project --json -o scan-report.json
npm run project-scan -- /path/to/android/project --json -o scan-report.json

node src/feedback-analyze.js ../feedback-log.md
npm run feedback-analyze -- ../feedback-log.md
```

若省略路径，反馈分析默认读取当前工作目录下的 `feedback-log.md`。

## 与「截图转代码」类工具对比

| 能力 | 基于截图的工具 | figma-mobile |
|------|------------------|--------------|
| 输入 | 截图/图片 | Figma API（设计树） |
| 布局理解 | 像素坐标 | 自动布局语义 |
| 输出 | 绝对定位为主 | LazyColumn、VStack 等惯用写法 |
| 迭代 | 重新截图 | 自然语言修改 |
| 成本 | 多为订阅 | 开源，仅需 Figma token |

## 目录与命名

技能根目录约定：

| 类型 | 约定 | 示例 |
|------|------|------|
| Agent 入口 | 固定大写 | `SKILL.md`、`README.md` |
| 设计说明 | 小写 kebab-case | `design.md` |
| 反馈记录 | 小写 kebab-case | `feedback-log.md` |
| 参考文档 | 小写 kebab-case，带语义前缀 | `figma-interpretation.md`、`figma-scan-usage.md`、`code-generation.md`、`platform-compose.md` … |
| 脚本源码 | `scripts/src/` 下 kebab-case `.js` | `figma-fetch.js`、`project-scan.js`、`feedback-analyze.js`、`load-env.js` |

`references/` 中：**`figma-*`** 表示 Figma 节点语义与扫描用法；**`platform-*`** 表示 Android/iOS 各平台映射；**`code-generation.md`** 为代码生成总则。

## 目录结构

```
figma-mobile/
├── SKILL.md                      # Agent 主说明（中文）
├── README.md
├── design.md                     # 设计目标与演进
├── feedback-log.md               # 用户反馈记录模板
├── scripts/
│   ├── package.json              # type: "module" + npm scripts（无依赖）
│   └── src/
│       ├── figma-fetch.js        # Figma API：拉取 / 对比 / SVG
│       ├── project-scan.js       # 工程资源轻量扫描
│       ├── feedback-analyze.js   # 反馈日志分析
│       └── load-env.js           # .env 加载
├── references/
│   ├── figma-interpretation.md
│   ├── figma-scan-usage.md
│   ├── code-generation.md
│   ├── platform-compose.md
│   ├── platform-xml.md
│   ├── platform-swiftui.md
│   └── platform-uikit.md
└── assets/
    └── demo-comparison.png
```

## 环境要求

- Node.js 18+
- Figma Personal Access Token（免费申请）

## 许可证

MIT
