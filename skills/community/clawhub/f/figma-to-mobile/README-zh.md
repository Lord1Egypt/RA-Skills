# figma-to-mobile 中文说明

> 将 Figma 设计稿转换为可直接使用的移动端 UI 代码，并**自动感知现有项目资源**。

支持：**Jetpack Compose** · **Android XML** · **SwiftUI** · **UIKit**

---

## 这个工具解决什么问题

设计师交付 Figma 稿后，开发需要手动量尺寸、对色值、写布局代码，重复劳动多，还容易出现还原偏差。

市面上的 Figma 插件有两个核心问题：
- **不感知项目已有资源**：生成的颜色是 hex 硬编码，不会用你的 `colors.xml` / `Color.kt`
- **不感知项目技术栈**：不知道你用的是 XML 还是 Compose、用了哪些自定义组件

本工具在生成代码前，先扫描你的项目，构建资源索引，生成时优先复用已有资源。

---

## 工作流程

```
1. Fetch（拉取）
   调用 Figma REST API 获取完整节点树
   支持：单节点 / 多节点对比（多状态组件）/ SVG 导出

2. Scan（扫描项目）
   扫描本地项目，构建资源索引：
   - Android：colors.xml / strings.xml / dimens.xml / drawable / 自定义 View / 依赖图
   - iOS：colorset / .strings / xcassets / UIView / SwiftUI View

3. Interpret（理解设计）
   AI 分析布局语义：
   "6个相似行 → LazyColumn"
   "横向排列带间距 → Row"

4. Generate（生成代码）
   输出平台惯用代码，并优先复用已有资源：
   - Figma 色值 → 查项目颜色表（容差±5）→ 命中则用 R.color.xxx
   - Figma 图片 → 按名称/尺寸匹配 drawable → 命中则直接引用
   - Figma 组件 → 匹配项目已有自定义 View / Composable

5. Iterate（迭代）
   自然语言指令继续调整：
   "把头部改成吸顶的"
   "切换到深色主题"

6. Learn（反馈沉淀）
   错误和调整记录在 feedback-log.md
   feedback_analyze.py 分析日志 → 生成规则改进建议 → 更新 references/
   → 下次生成质量提升
```

---

## 与其他方案的对比

| | 截图类工具 | 其他 Figma 插件 | figma-to-mobile |
|---|---|---|---|
| **输入** | 截图/图片 | Figma 节点树 | Figma 节点树 |
| **布局方式** | 绝对定位 | 自动布局语义 | 自动布局语义 |
| **感知项目资源** | ❌ | ❌ | ✅ 扫描已有资源 |
| **颜色处理** | hex 硬编码 | hex 硬编码 | 匹配 colors.xml |
| **组件复用** | ❌ | ❌ | ✅ 识别自定义组件 |
| **反馈闭环** | ❌ | ❌ | ✅ 错误→规则改进 |
| **多状态支持** | ❌ | 有限 | ✅ 多节点同时对比 |
| **费用** | 付费订阅 | 不定 | 免费开源 |

---

## 快速开始

### 第一步：安装

```bash
# OpenClaw 一键安装
clawhub install figma-to-mobile

# Claude Code — 复制到项目
cp -r figma-to-mobile/ your-project/.claude/skills/

# GitHub Copilot — 复制到项目
cp -r figma-to-mobile/ your-project/.agents/skills/
```

### 第二步：使用

在 AI 助手中输入：
```
把这个转成 Jetpack Compose：
https://www.figma.com/design/xxx/Project?node-id=100-200
```

AI Agent 会依次：拉取设计树 → 扫描项目资源 → 必要时提问 → 生成引用已有资源的完整代码文件。

> ⚠️ **Figma Token** — 需要设置环境变量 `FIGMA_TOKEN`。请在 Figma → 设置 → 安全 → 个人访问令牌 生成 Token，然后在系统环境变量中配置。
>
> **不要在聊天中粘贴 Token** — 聊天记录可能会被记录。请通过环境变量设置：
>
> ```bash
> # macOS/Linux
> export FIGMA_TOKEN="figd_your_token_here"
>
> # Windows PowerShell
> $env:FIGMA_TOKEN = "figd_your_token_here"
> ```
>
> ⚠️ 请确保 `.env` 文件和 Token 不会误提交到版本控制。已配置 `.gitignore` 包含 `.env` 的仓库可以放心使用。

---

## 支持平台

| 平台 | 框架 | 主要特性 |
|------|------|---------|
| **Android** | Jetpack Compose | Material3、LazyColumn/Row、Navigation、ViewModel 友好 |
| **Android** | XML | ConstraintLayout、RecyclerView、DataBinding 友好 |
| **iOS** | SwiftUI | SF Symbols、NavigationStack、@Observable |
| **iOS** | UIKit | Auto Layout、UICollectionView、纯代码 UI |

---

## 项目结构

```
figma-to-mobile/
├── SKILL.md                      # AI Agent 指令文件
├── scripts/
│   ├── figma_fetch.py            # Figma API 数据获取（单节点/多节点对比/SVG导出）
│   ├── project_scan.py           # 多平台项目扫描入口，自动识别 Android/iOS
│   ├── feedback_analyze.py       # 分析 feedback-log.md，生成规则改进建议
│   └── scanners/
│       ├── android_scanner.py    # Android 平台检测器 + 扫描器主类
│       ├── android_resources.py  # colors/strings/dimens/styles.xml 解析
│       ├── android_drawables.py  # shape drawable 属性提取
│       ├── android_layouts.py    # 布局 XML 分析，View 使用统计
│       ├── android_views.py      # 自定义 View 子类扫描（Kotlin/Java）
│       ├── android_deps.py       # Gradle 依赖图构建
│       ├── ios_scanner.py        # iOS 平台扫描器主类
│       ├── ios_resources.py      # colorset / .strings / NSLocalizedString
│       ├── ios_assets.py         # xcassets / imageset 扫描
│       └── ios_views.py          # UIKit / SwiftUI View 定义扫描
├── references/
│   ├── figma-interpretation.md   # 哪些节点跳过、Container+Icon 合并、多状态识别规则
│   ├── generation-rules.md       # 资源匹配优先级、drawable 生成条件、命名规范
│   ├── scan-usage.md             # 如何使用扫描结果（颜色/字符串/图片匹配策略）
│   ├── compose-patterns.md       # Figma 节点 → Jetpack Compose 映射规则
│   ├── xml-patterns.md           # Figma 节点 → Android XML 映射规则
│   ├── swiftui-patterns.md       # Figma 节点 → SwiftUI 映射规则
│   └── uikit-patterns.md         # Figma 节点 → UIKit 映射规则
└── tests/
    └── test_project_scan.py      # 扫描器集成测试
```

---

## 环境要求

- Python 3.8+（依赖 `requests` 库）
- Figma 个人访问令牌（免费申请）
- 一个支持 Agent Skill 的 AI 编程助手（OpenClaw、Claude Code、GitHub Copilot 等）

---

## 设计思路

**为什么规则写在 Markdown 文件而不是代码里？**

`references/` 目录的规则文件是设计意图的载体，而不是代码逻辑。这样做有两个好处：
1. 团队成员不需要懂代码就能修改规则（比如调整哪些 Figma 节点需要跳过）
2. 规则随项目迭代积累，每次更新 `references/` 就等于让 AI "学到了新东西"

**为什么要有反馈机制？**

单次 AI 生成的质量有上限。`feedback_analyze.py` 把每次生成后的手动调整记录下来，分析出规律，提炼为新规则。质量随使用积累持续提升。

---

## 许可证

MIT © Lin Li 2026
