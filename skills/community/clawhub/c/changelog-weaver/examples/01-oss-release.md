# Example: Open Source Library Release

## Scenario

You maintain `react-data-grid` (a React table component library) and are preparing the v4.2.0 release. The project has 47 commits since v4.1.0, following Conventional Commits. You need to produce:

1. A `CHANGELOG.md` for the project root (Keep a Changelog format)
2. A GitHub Release body
3. A 飞书 announcement for the team channel

## Step-by-Step

### 1. Collect commits

```bash
cd ~/projects/react-data-grid
python3 ~/.openclaw/skills/changelog-weaver/scripts/weaver.py collect \
  --from v4.1.0 --to v4.2.0 \
  --version 4.2.0 \
  -o v4.2.0-commits.json
```

**Output:** `[SUMMARY] 47 commits, 5 contributors, 1 breaking changes`

### 2. AI Semantic Rewrite

Load `v4.2.0-commits.json` into chat:

> **Prompt:** "Load `v4.2.0-commits.json`. Rewrite all commit descriptions to be concise, user-facing, and professional. Merge the 3 commits about 'column resize' into 1 entry. The audience is React developers reading a changelog. For the breaking change, write a migration note."

**AI Response (excerpt):**
```json
{
  "ai_rewrites": {
    "a3f2c1d8": "Added dark mode theme with system preference auto-detection",
    "b8e4f9a2": "Export dashboard as PDF with custom branding options (logo, colors, header/footer)",
    "c7d1e2f3": "Fixed date picker visual offset in Safari browsers",
    "MERGE_845_867_881": "Column resize handles — drag to resize any column, double-click for auto-fit width"
  },
  "breaking_notes": {
    "d9e8f7a6": "Removed `legacyRowRenderer` prop. Use `rowRenderer` with the new `RowConfig` interface instead. See migration guide in docs/migration-v4.2.md."
  }
}
```

Copy the `ai_rewrites` into `v4.2.0-commits.json`.

### 3. Generate CHANGELOG.md

```bash
python3 scripts/weaver.py generate \
  -i v4.2.0-commits.json \
  -f changelog \
  -o CHANGELOG.md
```

### 4. Generate GitHub Release

```bash
python3 scripts/weaver.py generate \
  -i v4.2.0-commits.json \
  -f release \
  -o RELEASE_NOTES.md
```

### 5. Generate 飞书 Announcement

```bash
python3 scripts/weaver.py generate \
  -i v4.2.0-commits.json \
  -f plain \
  -p feishu \
  -o feishu-v4.2.0.txt
```

## Final Output: CHANGELOG.md

```markdown
# Changelog

## [4.2.0] - 2026-06-15

### ⚠️ Breaking Changes
- Removed `legacyRowRenderer` prop — migrate to `rowRenderer` with the new `RowConfig` interface (#892) — @dave

### ✨ Features
- Added dark mode theme with system preference auto-detection (#856) — @bob
- Column resize handles — drag to resize any column, double-click for auto-fit width (#845, #867, #881) — @sarahchen
- Export dashboard as PDF with custom branding options (#842) — @alice
- Virtual scrolling for 100K+ row datasets with <50ms render time (#878) — @mikez
- Multi-select cells with Shift+Click and Ctrl+Click (#903) — @alexk

### 🐛 Bug Fixes
- Fixed date picker visual offset in Safari browsers (#849) — @charlie
- Fixed column reorder breaking when a column is hidden (#895) — @linday
- Fixed pagination reset on filter change with server-side data (#862) — @bob

### ⚡ Performance
- Reduced VirtualScroll re-render count by 40% with memoization (#887) — @mikez
- Optimized column width calculation with ResizeObserver batching (#872) — @sarahchen

### 🙏 Contributors
@alexk, @alice, @bob, @charlie, @dave, @linday, @mikez, @sarahchen
```

## Final Output: 飞书 Announcement

```
📦 react-data-grid v4.2.0 发布通知 (2026-06-15)

【新功能】
  • 支持暗色模式主题，自动跟随系统偏好
  • 列宽拖拽调整，双击自适应列宽
  • Dashboard 导出 PDF，支持自定义品牌（Logo、颜色、页眉页脚）
  • 虚拟滚动支持 10 万行数据，渲染 <50ms
  • 多选单元格（Shift+Click / Ctrl+Click）

【问题修复】
  • 修复 Safari 浏览器日期选择器偏移
  • 修复隐藏列时列排序异常
  • 修复服务端数据切换筛选时分页重置
  ... 及其他 13 项修复

⚠️ 破坏性变更: legacyRowRenderer 属性已移除，请迁移至 rowRenderer + RowConfig 接口

👥 贡献者: alexk, alice, bob, charlie, dave, linday, mikez, sarahchen
```
