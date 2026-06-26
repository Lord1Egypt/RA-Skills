# 反馈记录 — Figma 转移动端

用于记录用户对生成代码的修正，便于归纳模式与优化 Skill 规则。

每条记录格式：
```
## YYYY-MM-DD HH:MM
- **Platform**: Android XML / Compose / SwiftUI / UIKit
- **Figma node type**: (e.g., FRAME with icon, Tab bar, Button group)
- **Issue**: Brief description of what was wrong
- **Before**: What the agent generated (snippet or description)
- **After**: What the user wanted (snippet or description)
- **Rule candidate**: (optional) Suggested general pattern rule
```

在 `scripts/` 目录执行：`node src/feedback-analyze.js` 或 `npm run feedback-analyze --`（可传入 `feedback-log.md` 路径）以汇总模式。

---

<!-- Entries below this line -->