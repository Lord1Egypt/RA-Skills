# Tailwind CSS + shadcn/ui 规范（前端工程师实现必读）

适用：Tailwind CSS 3.4+ / shadcn/ui（Radix 基座）。定位：现代 C 端、高定制设计、
设计系统自持的 React 组合；管理后台默认走 frontend-antd.md，本项目内两者不混用。

## 1. Tailwind 纪律

- **设计令牌先行**：颜色/间距/圆角/字号只从 `tailwind.config` 令牌取
  （`bg-primary`、`text-muted-foreground`），禁止散落硬编码色值（`#3b82f6`、`text-[#333]`）。
- 任意值（`w-[347px]`）仅限设计稿精确还原且无对应令牌时使用，并注释来源。
- 响应式前缀 mobile-first：`sm:` `md:` `lg:`，断点与 ui-spec 断点一致。
- `@apply` 只允许出现在全局基础样式（如 `.btn-base`），组件内类名直接写工具类。
- 暗色模式：`dark:` 变体 + 令牌切换（`darkMode: 'class'`），语义令牌覆盖而非逐元素写两套色。
- 类名顺序可读：布局 → 盒模型 → 排版 → 视觉 → 状态； prettier-plugin-tailwindcss 自动排序。

## 2. shadcn/ui 纪律

- shadcn 组件是**拷贝进仓库的源码**（非 npm 依赖）：所有权在项目，可改；
  修改限于：主题令牌、variants、尺寸——不改组件 API 形状（保持与上游可对照）。
- `cn()`（clsx + tailwind-merge）统一类名合并出口；所有动态类名拼接必经 `cn()`，
  避免冲突类残留。
- variants 用 `cva` 定义在组件文件内；变体命名与令牌对齐（`size: sm|md|lg`）。
- 组件登记制：`components/ui/` 目录即组件清单；页面不直接改 ui 组件内部，
  需差异化时包一层 business 组件（components/business/）。
- 新增 shadcn 组件经 CLI 添加（`npx shadcn@<x.y.z> add <name>`，版本号形如
  `@2.4.0`——经 registry 查询后锁定进锁文件/ADR 再执行），不手抄上游源码防漂移；
  禁止 `@latest` 与无版本后缀执行（供应链红线，见 stack-routing.md 第 5 节：
  只从官方源安装、锁文件提交、不运行未锁定版本）。

## 3. 可达性

- Radix 基座自带键盘/焦点语义：**不覆盖**其 focus 管理（禁 `focus:outline-none` 裸用，
  需自定义时提供等效 focus-visible 样式）。
- Dialog/Popover 必须有语义触发关联；图标按钮必填 `aria-label`。
- 表单：Label 关联 + 错误信息 `aria-describedby` 关联。

## 4. 性能

- 组件级懒加载重组件（cmdk、charts 类）；图表类默认动态导入。
- Tailwind 构建期树摇安全：动态类名必须来自完整类名字符串数组/记录，
  禁止字符串拼接类名（`bg-${color}-500` 摇不掉且易失效）——动态样式用 variants 映射。

## 5. 质量命令

```bash
npm run lint && npm run build
```

React 共性纪律（组件/状态/类型/测试）见 `standards/frontend-react.md`。
