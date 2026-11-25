# 设计一致性

检查改动后的 UI 在视觉上是否与应用其余部分保持一致。这能抓住"能用但看起来不对"的问题——间距不匹配、颜色、圆角、组件样式不一致。

### 如果存在 `references/design-system.md`

用户已经记录了他们的设计令牌（design tokens）和约定。把它当作基准事实来用。（预期格式见 `references/design-system.example.md`。）

```bash
# Read the design system
cat references/design-system.md
# or: cat .claude/skills/chrome-qa-agent/references/design-system.md

# Then screenshot the changed page and check against documented patterns
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/changed-page.png" }
# Compare: does spacing match the grid? Are colors from the palette? Correct font weights?
```

把任何偏离已记录系统之处标记为 `STEP_FAIL`：
```
STEP_FAIL|design-spacing|design system specifies 8px grid → new modal uses 6px gap
STEP_FAIL|design-button|design system: destructive buttons use outline style → new delete button uses filled red
```

### 如果不存在设计系统——从应用中学习

在测试改动后的页面之前，先对 2-3 个**未改动**的页面截图，以建立一条基线：

```
# Step 1: Capture baseline from existing pages
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/" }
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/baseline-home.png" }
# Note: spacing rhythm, border radii, font sizes, button styles, color palette

mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/settings" }  # or any other established page
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/baseline-settings.png" }
# Note: same patterns — confirm consistency

# Step 2: Now visit the changed page
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/changed-page" }
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/changed-page.png" }
# Compare against baseline: does it match the established patterns?
```

关注以下方面：
- **间距节奏** — 新 UI 是否使用与既有页面相同的间隙/内边距？
- **圆角** — rounded-sm 与 rounded-md 与 rounded-lg 的一致性
- **按钮样式** — 主要/次要/危险按钮是否沿用相同的模式？
- **排版** — 标题字号、字重、正文字号是否一致？
- **颜色用法** — 调色板是否一致？语义色是否一致（红=错误，绿=成功）？
- **组件模式** — 如果其他页面用内联确认，新页面是否反而用了模态框？

以结构化发现的形式报告：
```
STEP_PASS|design-consistency|new sidebar uses same border-l, bg-white, and shadow pattern as existing sidebar on /sessions
STEP_FAIL|design-inconsistency|existing pages use rounded-lg on cards → new component uses rounded-sm
```

设计一致性是一种**视觉判断**——是最弱的断言类型。务必明确说明你在对比什么（哪个页面、哪个元素、哪个属性）。
