# agent-roundtable v2 Sprint 3 设计规范

> **设计师**：像素姐 🎨 | **日期**：2026-05-26
> **分支**：feature/v2-ux-improvements
> **关联 PRD**：docs/product/PRD-sprint3.md

---

## 1. 概述与设计原则

### 1.1 设计目标

Sprint 3 聚焦五大功能，从"能用"走向"好看 + 安全 + 可扩展"：

1. **Agent 人格可视化** — 头像 + 名称 + 角色标签，一眼区分谁在说话
2. **响应式布局优化** — 三断点适配（mobile / tablet / desktop），移动端体验对齐
3. **Web Viewer 隐私增强** — 链接过期 + 访问密码 + 安全状态页
4. **插件化适配器** — 适配器配置 UI 与状态展示
5. **Landing Page** — 项目介绍静态页，GitHub/PyPI 引流

### 1.2 设计原则（延续 Sprint 1-2）

| 原则 | Sprint 3 延伸 |
|------|--------------|
| **渐进呈现** | 人格信息逐步加载，隐私状态清晰分层 |
| **角色可辨** | 头像 + 色彩 + 标签三重标识，移动端不丢辨识度 |
| **焦点明确** | 安全状态页重点突出关键信息（过期 / 密码 / 撤销） |
| **流畅过渡** | 响应式断点切换无跳变，状态页切换有动画 |
| **移动优先** | 所有功能先设计移动端，再扩展到桌面端 |
| **安全可感知** | 密码/过期 UI 传达安全感，不是"又一个输入框" |

### 1.3 设计语言沿用

延续 `theme.css` 设计体系：

- **色彩**：Dark Slate 底色（`#0F172A`）+ 角色色标识
- **品牌色**：`#4F46E5`（Indigo-600）
- **圆角**：小 6px / 中 10px / 大 16px
- **字体**：系统字体栈（PingFang SC + SF Pro）
- **动效**：`cubic-bezier(0.4, 0, 0.2, 1)` 缓动曲线
- **间距**：4px 网格基准

### 1.4 新增设计令牌

```css
:root {
  /* Agent 人格可视化 */
  --rt-avatar-size: 40px;             /* 桌面端头像尺寸 */
  --rt-avatar-size-mobile: 36px;      /* 移动端头像尺寸 */
  --rt-avatar-size-sm: 24px;          /* 小头像（参与者列表等） */
  --rt-avatar-font-size: 15px;        /* 首字母字号 */
  --rt-avatar-font-size-mobile: 13px;
  --rt-role-tag-bg: rgba(255, 255, 255, 0.06);  /* 角色标签底色 */
  --rt-role-tag-radius: 999px;

  /* 安全状态页 */
  --rt-security-bg: #0D1525;          /* 安全页底色 */
  --rt-expired-accent: #EF4444;       /* 过期红 */
  --rt-expired-glow: rgba(239, 68, 68, 0.15);
  --rt-password-accent: #6366F1;      /* 密码验证靛蓝 */
  --rt-password-glow: rgba(99, 102, 241, 0.15);
  --rt-revoked-accent: #F59E0B;       /* 撤销橙 */
  --rt-revoked-glow: rgba(245, 158, 11, 0.15);

  /* 过期时间选择器 */
  --rt-selector-bg: #1E293B;
  --rt-selector-active: var(--rt-brand);
  --rt-selector-hover: rgba(79, 70, 229, 0.12);

  /* Landing Page */
  --rt-landing-bg: #0B1120;
  --rt-landing-card-bg: rgba(30, 41, 59, 0.6);
  --rt-landing-glow: rgba(79, 70, 229, 0.3);
}
```

---

