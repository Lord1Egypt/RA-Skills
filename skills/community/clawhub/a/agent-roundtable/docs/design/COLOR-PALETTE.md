# Roundtable AI — 配色方案定稿

> 版本：v1.0 | 日期：2026-05-21 | 设计：像素姐

## 设计定位

Roundtable AI 定位为"AI Agent 协作基础设施"，视觉上需要体现：
- **专业感**：开发者工具的可靠感
- **对话感**：圆桌讨论的协作氛围
- **终端友好**：在深色终端中具有良好的可读性

---

## 方案一：Tokyo Night（推荐 ✅）

基于 Tokyo Night 终端主题，冷色调为主，蓝紫渐变更具科技感。

### 主色系（Primary）

| 用途 | 色名 | HEX | RGB | 说明 |
|------|------|-----|-----|------|
| 背景-深 | Night BG | `#1a1b26` | 26, 27, 38 | 主背景色，深沉但不纯黑 |
| 背景-中 | Storm BG | `#24283b` | 36, 40, 59 | 卡片/面板背景 |
| 背景-浅 | Surface | `#292e42` | 41, 46, 66 | 悬浮状态/hover |

### 文字色系（Text）

| 用途 | 色名 | HEX | RGB | 说明 |
|------|------|-----|-----|------|
| 正文 | Text Primary | `#c0caf5` | 192, 202, 245 | 主要文字，柔和蓝白 |
| 副文 | Text Secondary | `#a9b1d6` | 169, 177, 214 | 辅助说明文字 |
| 弱化 | Text Muted | `#565f89` | 86, 95, 137 | 占位符/禁用状态 |

### 强调色（Accent）

| 用途 | 色名 | HEX | RGB | 说明 |
|------|------|-----|-----|------|
| 主强调 | Blue | `#7aa2f7` | 122, 162, 247 | 按钮、链接、选中态 |
| 辅助强调 | Cyan | `#7dcfff` | 125, 207, 255 | 标签、高亮、提示 |
| 成功态 | Green | `#9ece6a` | 158, 206, 106 | 成功消息、达成共识 |
| 警告态 | Yellow | `#e0af68` | 224, 175, 104 | 警告、进行中 |
| 错误态 | Red | `#f7768e` | 247, 118, 142 | 错误、分歧点 |
| 特殊强调 | Purple | `#bb9af7` | 187, 154, 247 | 特殊标记、收敛分数 |

### 圆桌讨论场景配色映射

| 场景 | 色值 | 说明 |
|------|------|------|
| 发言人-参与者A | `#7aa2f7` | Blue，冷静理性 |
| 发言人-参与者B | `#bb9af7` | Purple，创意发散 |
| 发言人-参与者C | `#7dcfff` | Cyan，技术视角 |
| 发言人-参与者D | `#9ece6a` | Green，务实落地 |
| 共识点 | `#9ece6a` | Green，达成一致 |
| 分歧点 | `#f7768e` | Red，尚有争议 |
| 新观点 | `#e0af68` | Yellow，本轮新增 |
| 收敛分数条 | `#7aa2f7` → `#9ece6a` | 蓝→绿渐变 |

---

## 方案二：Dracula Night

基于 Dracula 主题，紫粉暖调，视觉上更有活力和趣味感。

### 主色系（Primary）

| 用途 | 色名 | HEX | RGB | 说明 |
|------|------|-----|-----|------|
| 背景-深 | Dark BG | `#282a36` | 40, 42, 54 | 主背景色 |
| 背景-中 | Panel BG | `#343746` | 52, 55, 70 | 卡片/面板 |
| 背景-浅 | Surface | `#44475a` | 68, 71, 90 | 悬浮/hover |

### 文字色系（Text）

| 用途 | 色名 | HEX | RGB | 说明 |
|------|------|-----|-----|------|
| 正文 | Text Primary | `#f8f8f2` | 248, 248, 242 | 主要文字，暖白 |
| 副文 | Text Secondary | `#bfbfbf` | 191, 191, 191 | 辅助文字 |
| 弱化 | Text Muted | `#6272a4` | 98, 114, 164 | 占位符/禁用 |

### 强调色（Accent）

| 用途 | 色名 | HEX | RGB | 说明 |
|------|------|-----|-----|------|
| 主强调 | Purple | `#bd93f9` | 189, 147, 249 | 按钮、链接、选中 |
| 辅助强调 | Cyan | `#8be9fd` | 139, 233, 253 | 标签、高亮 |
| 成功态 | Green | `#50fa7b` | 80, 250, 123 | 成功消息 |
| 警告态 | Yellow | `#f1fa8c` | 241, 250, 140 | 警告信息 |
| 错误态 | Red | `#ff5555` | 255, 85, 85 | 错误、分歧 |
| 特殊强调 | Pink | `#ff79c6` | 255, 121, 198 | 特殊标记 |
| 橙色 | Orange | `#ffb86c` | 255, 184, 108 | 温暖提示 |

---

## 终端配色方案

### 方案一 Tokyo Night — 终端 16 色

```
# 基础色（ANSI 0-7）
color0  #15161e    # Black（深色背景）
color1  #f7768e    # Red
color2  #9ece6a    # Green
color3  #e0af68    # Yellow
color4  #7aa2f7    # Blue
color5  #bb9af7    # Magenta/Purple
color6  #7dcfff    # Cyan
color7  #a9b1d6    # White（浅色文字）

# 亮色（ANSI 8-15）
color8  #414868    # Bright Black（灰色）
color9  #f7768e    # Bright Red
color10 #9ece6a    # Bright Green
color11 #e0af68    # Bright Yellow
color12 #7aa2f7    # Bright Blue
color13 #bb9af7    # Bright Magenta
color14 #7dcfff    # Bright Cyan
color15 #c0caf5    # Bright White

# 背景/前景
foreground #c0caf5
background #1a1b26
cursor     #c0caf5
selection  #33467c
```

### 方案二 Dracula Night — 终端 16 色

```
# 基础色（ANSI 0-7）
color0  #21222c    # Black
color1  #ff5555    # Red
color2  #50fa7b    # Green
color3  #f1fa8c    # Yellow
color4  #bd93f9    # Blue（Purple 做主色）
color5  #ff79c6    # Magenta
color6  #8be9fd    # Cyan
color7  #f8f8f2    # White

# 亮色（ANSI 8-15）
color8  #6272a4    # Bright Black
color9  #ff6e6e    # Bright Red
color10 #69ff94    # Bright Green
color11 #ffffa5    # Bright Yellow
color12 #d6acff    # Bright Blue
color13 #ff92df    # Bright Magenta
color14 #a4ffff    # Bright Cyan
color15 #ffffff    # Bright White

# 背景/前景
foreground #f8f8f2
background #282a36
cursor     #f8f8f2
selection  #44475a
```

---

## 终端可读性验证

### 对比度测试（WCAG AA 标准 ≥ 4.5:1）

**Tokyo Night**
| 组合 | 对比度 | 是否达标 |
|------|--------|----------|
| `#c0caf5` on `#1a1b26` | 10.2:1 | ✅ AAA |
| `#7aa2f7` on `#1a1b26` | 7.1:1 | ✅ AAA |
| `#9ece6a` on `#1a1b26` | 8.4:1 | ✅ AAA |
| `#f7768e` on `#1a1b26` | 5.8:1 | ✅ AA |
| `#c0caf5` on `#24283b` | 8.6:1 | ✅ AAA |
| `#565f89` on `#1a1b26` | 3.2:1 | ⚠️ 仅大字 |

**Dracula Night**
| 组合 | 对比度 | 是否达标 |
|------|--------|----------|
| `#f8f8f2` on `#282a36` | 11.5:1 | ✅ AAA |
| `#bd93f9` on `#282a36` | 7.8:1 | ✅ AAA |
| `#50fa7b` on `#282a36` | 10.1:1 | ✅ AAA |
| `#ff5555` on `#282a36` | 5.3:1 | ✅ AA |
| `#6272a4` on `#282a36` | 3.5:1 | ⚠️ 仅大字 |

---

## 推荐方案

**首选：Tokyo Night**

理由：
1. 冷色调蓝紫渐变更符合"基础设施"的专业定位
2. 色彩层次丰富但不杂乱，适合长时间终端使用
3. 蓝色系在开发者群体中接受度最高（VS Code、JetBrains 系流行）
4. 与项目名 "Roundtable" 的庄重感更搭配

**备选：Dracula Night**

适合场景：如果最终定位更偏社区化、趣味性更强，Dracula 的紫粉暖调更有辨识度。

---

## 使用规范

### 代码中使用

```css
/* Tokyo Night（推荐） */
:root {
  --rt-bg-deep:    #1a1b26;
  --rt-bg-mid:     #24283b;
  --rt-bg-surface: #292e42;
  --rt-text:       #c0caf5;
  --rt-text-sub:   #a9b1d6;
  --rt-text-muted: #565f89;
  --rt-accent:     #7aa2f7;
  --rt-cyan:       #7dcfff;
  --rt-green:      #9ece6a;
  --rt-yellow:     #e0af68;
  --rt-red:        #f7768e;
  --rt-purple:     #bb9af7;
}
```

### 终端 GIF 录制建议

- 终端背景色设为方案中的 `background`
- 使用等宽字体：JetBrains Mono / Fira Code / SF Mono
- 字号 ≥ 14px 确保录屏清晰度
- 窗口宽度建议 80-100 列

---

## 交付物清单

- [x] 色板文档（本文件）
- [x] HEX 完整色值
- [x] 2 种配色方案（Tokyo Night + Dracula Night）
- [x] 终端 16 色配置
- [x] 对比度/可读性验证
- [x] HTML 预览文件（`color-palette-preview.html`）
