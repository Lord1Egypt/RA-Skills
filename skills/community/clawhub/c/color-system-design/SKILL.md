---
name: color-system-design
description: 给 1 个主视觉 Hex 色号，生成明暗双模式 UI 颜色矩阵、HTML 预览报告与 CSS/Tailwind 颜色变量的 Skill + CLI。当用户说"生成配色方案/定一套主视觉色/暗黑模式配色/Vibe Coding 配色不乱/Tailwind 颜色变量/检查对比度或硬编码 Hex"时使用；融合 Primer、Leonardo、OKLCH、DTCG 与 APCA/WCAG 双校验，纯脚本计算无大模型幻觉。不用于品牌 Logo 艺术创作或印刷 CMYK 配色。
metadata:
  version: "2.0.0"
---

# Color System Design Skill

用来解决做网站、App 或 Vibe Coding 时颜色越改越乱的问题。  
融合了 **GitHub Primer**（颜色角色分工）、**Adobe Leonardo**（对比度计算）、**W3C DTCG**（标准格式）和 **APCA**（感知对比度校验）。生成的配色**不会太惊艳，但绝对不会出错**。

---

## 怎么用（核心流程）

### 1. 先向用户要 1 个主视觉色号
不要凭空乱猜。先让用户给出一个主视觉 Hex 色号（比如 `#007275`）；如果用户还没想好，可以先问他想要什么风格，给他 2-3 个 Hex 候选让他挑一个。

### 2. 跑脚本生成颜色矩阵
拿到色号后，直接运行：

```bash
pnpm generate -- --seed "<HEX>"
```

如果需要调整背景灰的倾向，可以加 `--tint subtle|pure|warm|cool`（默认 `subtle`）。

### 3. 交付两样东西
运行完后，把 `dist/` 里的产物交给用户和后续代码：
1. **给人看的 HTML**：让用户打开 `dist/color-report.html`，里面有网站和 App 的实际预览、亮暗切换、每个颜色怎么安排，以及对比度实测。
2. **给 AI / 代码用的约束工具**：
   - 写界面时只使用 `dist/tokens.css` 里的语义变量（或 `dist/tailwind.theme.css` / `dist/tailwind.preset.cjs`），**不要自己在代码里硬编码新的 Hex 色号**。
   - 需要检查有没有写乱时，运行 `pnpm tokens:check`（存量项目可加 `--scan ./src`）。

---

## 必须守住的 3 条底线

写界面用色时，不管什么场景都要遵守：
1. **一屏只用一个主强调色**：`accent` 只用来表示“可以点 / 当前选中”，别拿来当普通装饰。
2. **字和底成对用**：实底按钮或深图版上的字，必须用配对的 `fgColor.onEmphasis` / `fgColor.onDeep`，别自己瞎改透明度。
3. **别只靠颜色表达状态**：报错、成功、警告、禁用，必须同时配上文字或图标。

---

## 为什么这套方案不会出错（避坑经验）

- **背景灰不靠猜**：纸面和中性灰在 OKLCH 下固定极低彩度反解，不会出现“页面灰蒙蒙或偏色”的问题。
- **暗色模式单独算**：不直接把亮色反色过来，而是单独给暗底算一套高对比度的亮色调，避免暗色下发灰看不清。
- **暗底卡片分不开时**：不硬压黑，直接用 `borderColor.muted` 加 1px 边框兜边。
- **同时算 WCAG 和 APCA**：传统 WCAG 在暗色模式下经常算不准，脚本会同时输出 `apca-w3` 的 `Lc` 值作为参考。
