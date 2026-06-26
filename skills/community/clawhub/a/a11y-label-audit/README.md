# a11y-label-audit

扫描 React / TSX / HTML 项目中缺失或错误的无障碍（a11y）标注，并自动修复。

## 功能概述

本 Skill 提供 **7 大类检测规则**，覆盖 WCAG 2.1 Level AA 的核心要求：

| 规则 | 检测内容 |
|------|----------|
| 1. icon-button-a11y | 纯图标按钮缺少 `aria-label` |
| 2. div-button-a11y | div/span 模拟按钮缺少 `role`、`tabIndex`、键盘交互 |
| 3. img-alt-a11y | 图片缺少有意义的 `alt` 文本 |
| 4. form-label-a11y | 表单元素缺少 `<label>` 或 `aria-label` 关联 |
| 5. dialog-a11y | 弹窗/对话框缺少 `aria-modal`、`aria-labelledby`、焦点管理 |
| 6. live-region-a11y | 动态内容缺少 `aria-live`、`role="alert"/"status"` |
| 7. compat-a11y | 跨平台兼容性（inert、dialog、focus-visible、X5 内核等） |

## 使用方法

1. 在 Cursor 中提到以下关键词即可触发：
   - "无障碍审查" / "a11y 检查" / "WCAG 合规"
   - "添加 aria 标签" / "屏幕阅读器支持"
   - "无障碍改进" / "兼容性问题"

2. 也可以手动指定扫描目标：
   - `@a11y-label-audit 扫描 src/components/`
   - `@a11y-label-audit 修复这个文件的无障碍问题`

## 工作流程

```
步骤 1：确定扫描范围（文件/目录）
步骤 2：按 7 条规则搜索违规项（含兼容性）
步骤 3：汇总审查报告（按文件分组，含行号和建议）
步骤 4：应用自动修复（保留代码风格、i18n 包裹）
步骤 5：验证修复未引入新问题
```

## 审查报告示例

```
## 无障碍审查报告

### 文件：src/components/Example.tsx

| 行号 | 规则 | 问题 | 建议修复 |
|------|------|------|----------|
| 42 | icon-button-a11y | onClick div 中的 <YbIcon> 缺少 aria-label | 添加 aria-label={t('关闭')} |
| 78 | div-button-a11y | <div onClick> 缺少 role 和键盘交互 | 添加 role="button" tabIndex={0} onKeyDown |
| 120 | img-alt-a11y | <img> 的 alt="image" 无意义 | 替换为描述性 alt 文本 |
```

## 跨平台兼容性

本 Skill 针对多平台部署场景特别优化，覆盖以下引擎的 ARIA 支持差异：

| 平台 | 引擎 | 无障碍支持等级 |
|------|------|----------------|
| 桌面端（Tauri macOS） | WKWebView | 较好 |
| 桌面端（Tauri Windows） | WebView2 (Chromium) | 好 |
| Chrome/Edge 扩展 | Chromium | 好 |
| 微信内置浏览器 | X5 / 系统 WebView | 较差 |
| QQ 内置浏览器 | MQQBrowser 内核 | 较差 |
| 小程序 WebView | 受限沙箱 | 差 |

兼容性规则包括：`inert` 回退、`<dialog>` 替代、`:focus-visible` 回退样式、`aria-live` 多通道反馈、小程序焦点管理限制、X5 role 支持不完整、`suppressHydrationWarning` 交叉检查。

## 适用项目

- React / Next.js 项目
- TypeScript / TSX 组件
- 纯 HTML 文件
- 使用 TDesign、Ant Design、自定义组件库的项目
- Tauri 桌面应用
- 微信/QQ 小程序 WebView
- Chrome 扩展

## 修复优先级

当存在大量违规时，按以下顺序修复（影响从高到低）：

1. **交互控件**缺少标签 — 完全阻碍使用
2. **表单**缺少标签 — 无法输入
3. **图片**缺少 alt — 信息丢失
4. **弹窗**缺少 aria 属性 — 导航混乱
5. **实时区域** — 降低实时感知

## 文件结构

```
a11y-label-audit/
├── SKILL.md         # 主技能文件（检测规则 + 扫描工作流）
├── reference.md     # 规则详细说明和边界情况
├── examples.md      # 修复前后的代码示例
├── clawhub.json     # ClawHub 发布元数据
├── CHANGELOG.md     # 版本变更日志
└── README.md        # 本文件
```

## 常见问题

**Q: 会误报装饰性图片吗？**
A: 不会。`alt=""` 被视为合法的装饰性标注，不会被标记。

**Q: 支持 i18n 项目吗？**
A: 支持。如果检测到项目使用 `t()` / `useTranslation`，会自动用 i18n 函数包裹标签文本。

**Q: 能处理自定义组件库吗？**
A: 支持 TDesign、@tencent/yb-component 等常见库。对于自定义组件，会检查 `aria-*` props 是否被正确透传。

## 许可证

MIT
