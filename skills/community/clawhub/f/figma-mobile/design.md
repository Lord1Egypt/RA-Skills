# figma-mobile（Figma 转移动端）设计方案

## 核心目标

让智能体能看懂 Figma 设计稿，直接写出可用的移动端 UI 代码。
解析精度服务于代码质量——最终衡量标准是输出的代码好不好用。

## 设计原则

1. **输出即可用** — 颜色写死 hex，文本写死字符串，不引用资源 ID。复制到项目里直接能看效果
2. **提示词驱动** — 用户可以在发链接时附带平台、布局偏好、组件约定等提示，减少交互轮次
3. **交互式确认** — 只问不确定的，有优先级（输出格式必须先问），每个问题留开放入口
4. **持续迭代** — 生成后用户可以反馈修改，逐步优化，不是一次性交付
5. **不猜业务逻辑** — 列表/Adapter/自定义组件等，问用户而不是假设
6. **先 Skill 后 MCP** — 在 Skill 里验证流程，跑通后再适配 MCP Server

## 数据提取能力

`scripts/src/figma-fetch.js` 提取以下信息：
- 结构层级、节点类型（含 INSTANCE 组件实例识别）
- 颜色（hex）、渐变（类型+色标）、图片标记
- 文本属性（内容、字号、字重、字体、行高、字间距、对齐、颜色）
- 布局属性（Auto-layout 方向、间距、内边距、对齐、尺寸模式）
- 视觉效果（阴影：颜色/偏移/半径/扩展，模糊）
- 边框（颜色、宽度）、圆角（统一或四角独立）、透明度
- 自适应深度：默认 depth=5，检测到子节点截断时自动加深到 15

## 交互设计

### 问题优先级（严格顺序）
1. 输出格式（必须先问，决定后续所有措辞）
2. 结构歧义（动态列表 vs 固定项等）
3. 组件选择（自定义组件 vs 系统默认）

### 信心度标准
- ≥3 个结构相似的同级节点 → 可能是列表 → 必须问
- 共享 componentId 的 INSTANCE → 复用组件 → 提示但可默认
- 单一明确层级 → 直接生成，不问

### 每个问题的要求
- 给具体选项 + 一句话优劣
- 保留开放入口："或者聊聊这个问题"
- 问题之间有依赖关系时，先问前置问题

## references 定位

文件命名：`figma-*`（节点语义、扫描用法）、`platform-*`（各平台映射）、`code-generation.md`（生成总则）。详见仓库根目录 `README.md`「目录与命名」。

references 文件是 **Figma 属性→代码属性的映射表**：
- Auto-layout → 各平台对应写法
- 阴影/渐变/圆角 → 各平台 API
- 布局选择指南

不是教智能体写代码的教程（智能体本身就有这些知识），
而是确保 Figma 特有属性能正确映射到目标平台。

## 演进路线

| Phase | 内容 | 状态 |
|-------|------|------|
| 1 | Skill 交互式确认流程 | ✅ v0.3 |
| 1.5 | 资源生成（shape drawable + SVG 导出 + Vector Drawable） | ✅ |
| 2 | `project-scan`（`src/project-scan.js`，扫描工程资源/组件） | 部分完成（Android 资源扫描；iOS 轻量） |
| 3 | MCP Server（给 VS Code 用） | 待做 |
| 4 | Adapter 生成（可选） | 待做 |

### Phase 2 设计笔记：project-scan

**使用场景**：Phase 3 MCP Server 阶段，Agent（Claude Code / Copilot 等）在 VS Code 中工作，需要引用项目已有资源而非写死值。

**扫描范围（3 层）**：
1. **目标 module**：用户指定的、或 Agent 根据上下文推断的当前 module。Agent 通常知道自己在哪个 module——当前编辑的文件、上下文引用的文件都能提供线索。
2. **依赖的内部 module**：解析目标 module 的 `build.gradle`，找 `implementation project(':xxx')` 引用的同项目 module，扫描它们的 `res/`。
3. **不扫描外部依赖**：三方库的资源不可控，不纳入匹配范围。

**扫描内容**：
- `res/values/colors.xml` → 颜色名+值，按 hex 值匹配
- `res/values/strings.xml` → 字符串名+值（用于判断是否有现成文案）
- `res/values/dimens.xml` → 尺寸名+值
- `res/values/styles.xml` / `themes.xml` → 已有样式
- `res/drawable/` → 已有 shape/vector drawable，按视觉特征匹配（颜色+形状+圆角）
- 自定义 View 类 → 按类名识别（如 `CompactSwitchCompat`、`RoundImageView`）

**输出模式切换**：
- Phase 1（当前）：所有值写死，即复即用
- Phase 2+：匹配到已有资源 → 引用（`@color/primary`），未匹配 → 创建到目标 module 的 `res/` 对应文件中

**关键设计决策（待定）**：
- 颜色匹配：完全相同的 hex 才算匹配？还是近似色也算？（建议：严格匹配 hex，近似提示但不自动引用）
- 新建资源的命名规范：跟随项目已有命名风格？还是用固定前缀？
- 多 flavor / buildType 的资源覆盖如何处理？
