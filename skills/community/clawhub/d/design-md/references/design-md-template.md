# DESIGN.md 模板

> 复制此模板，根据实际项目填写每个模块。

```markdown
# [项目名称] Design Specification

> 版本：1.0.0 | 最后更新：[YYYY-MM-DD]
> 格式标准：Google Stitch DESIGN.md v1.0

---

## M1 — Visual Theme & Atmosphere

### 品牌气质
- **定位人群**：[描述目标用户]
- **情绪关键词**：[3-5个品牌调性词]
- **情绪版参考**：[1-2个参考产品/品牌]
- **设计哲学**：[一句话设计哲学]

### 明暗与密度
- **明暗倾向**：偏亮 / 偏暗 / 中性
- **内容密度**：紧凑 / 中等 / 宽松
- **主色调温度**：冷 / 暖 / 中性

---

## M2 — Color Palette & Roles

| 角色 | 名称 | 色值 | 使用场景 |
|------|------|------|---------|
| Primary | 主色 | #XXXXXX | 主按钮、导航激活态 |
| Primary Light | 主色浅 | #XXXXXX | Hover态 |
| Primary Dark | 主色深 | #XXXXXX | 按下态 |
| Accent | 强调色 | #XXXXXX | CTA、重要提示 |
| Background | 背景色 | #XXXXXX | 全局背景 |
| Surface | 表面色 | #XXXXXX | 卡片、浮层 |
| Text Primary | 正文色 | #XXXXXX | 正文 |
| Text Secondary | 辅助色 | #XXXXXX | 说明文字 |
| Border | 边框色 | #XXXXXX | 分割线 |

---

## M3 — Typography Rules

### 字体族
- 中文：
- 英文/数字：

### 字号层级
| 标签 | 字号 | 字重 | 行高 | 用途 |
|------|------|------|------|------|
| Hero | px | 700 | 1.3 | 大标题 |
| H1 | px | 700 | 1.4 | 页面标题 |
| H2 | px | 600 | 1.4 | 模块标题 |
| Body | px | 400 | 1.6 | 正文 |
| Caption | px | 400 | 1.5 | 说明 |
| XS | px | 400 | 1.4 | 标签 |

---

## M4 — Component Stylings

### 按钮
- **主按钮**：bg-[color] text-white rounded-[n] px-[n] py-[n]
- **次按钮**：border border-[color] text-[color] bg-transparent
- **Ghost按钮**：

### 卡片
- bg-[surface] rounded-[n] shadow-[level] p-[n]px

### 输入框
- bg-white rounded-[n] border border-[border-color]
- Focus：border-[primary] ring-2 ring-[primary]/20

### 列表项

### 导航

---

## M5 — Layout Principles

### 间距系统（4px基准）
| Token | 值 |
|-------|-----|
| xs | 4px |
| sm | 8px |
| md | 12px |
| lg | 16px |
| xl | 24px |
| 2xl | 32px |

### 页面布局

### 栅格

---

## M6 — Depth & Elevation

| Level | 样式 | 用途 |
|-------|------|------|
| L0 | 无阴影 | 默认 |
| L1 | shadow-sm | 卡片 |
| L2 | shadow-md | 浮层 |
| L3 | shadow-lg | Modal |

---

## M7 — Do's and Don'ts

### ✅ 正确
- 

### ❌ 错误
- 

---

## M8 — Responsive Behavior

### 移动端特殊处理

### 断点

---

## M9 — Agent Prompt Guide

### 快速颜色参考
- Primary：
- Accent：
- Background：
- Surface：

### Tailwind 速查

### AI 生成提示模板
```

## 使用说明

1. 复制此文件到新项目根目录
2. 将所有 `#XXXXXX` 替换为实际颜色值
3. 调整字体、间距、圆角为实际设计稿
4. 保存为 `DESIGN.md`
5. 告知 AI agent："生成页面时，请遵循根目录 DESIGN.md 中的规范"
