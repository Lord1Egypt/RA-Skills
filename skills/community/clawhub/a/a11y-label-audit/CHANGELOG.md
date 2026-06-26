# Changelog

## [1.0.0] - 2026-04-10

### 新增
- 6 条核心无障碍检测规则：
  - icon-button-a11y：纯图标按钮缺少 aria-label
  - div-button-a11y：div/span 模拟按钮缺少 role 和键盘交互
  - img-alt-a11y：图片缺少有意义的 alt 文本
  - form-label-a11y：表单元素缺少 label 关联
  - dialog-a11y：弹窗缺少 aria-modal 和焦点管理
  - live-region-a11y：动态内容缺少 aria-live
- 第 7 条跨平台兼容性规则（compat-a11y），包含 7 个子规则：
  - compat-inert：inert 属性回退
  - compat-dialog：原生 dialog 兼容
  - compat-focus-visible：focus-visible 伪类回退
  - compat-live-region：aria-live 多通道反馈
  - compat-focus-trap：小程序焦点管理限制
  - compat-role：X5 内核 role 支持
  - compat-hydration：suppressHydrationWarning 交叉检查
- 完整的 5 步扫描工作流
- reference.md 详细参考文档
- examples.md 修复前后代码示例
- 支持 React / TSX / HTML 文件扫描
- 支持 i18n 函数自动包裹
- 修复优先级排序
