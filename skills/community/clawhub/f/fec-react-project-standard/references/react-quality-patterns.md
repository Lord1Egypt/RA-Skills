# React quality patterns

## 样式接入

本 skill 不强制具体样式方案，默认遵循仓库现状。

适配时注意：

- Tailwind 项目继续使用 Tailwind
- CSS Modules 项目保持命名与文件组织一致
- styled-components 项目继续沿用其模式
- 主题、颜色、字号、间距等优先复用仓库 token / CSS 变量
- 避免在组件内硬编码大量视觉常量
- 禁止内联样式（除动态值外）
- 响应式处理需与项目断点约定一致

---

## 注释规范

- **优先使用中文**：解释「为什么这样做」、业务约束、边界情况、非显而易见的权衡时，优先用中文撰写注释，便于团队与业务方阅读。
- **与代码语言一致时的例外**：对接第三方协议字段名、HTTP 头、规范中的英文术语时，注释里可保留英文专有名词，必要时中英文并列说明。
- **少而精**：能通过清晰命名与类型表达清楚的逻辑不写废话注释；复杂分支、临时兼容、性能取舍必须写清意图。
- **公开 API**：模块或 hooks 的对外契约可用 JSDoc（`@param` / `@returns` / `@example`），说明用中文即可，除非仓库统一要求英文。

---

## TypeScript 规范

通用 TypeScript 工程规则由 `fec-typescript-project-standard` 负责，包括 `tsconfig`、strictness、DTO / view model 边界、`unknown` 收窄、public API 类型、声明产物和类型测试。

React 规范只补充组件、Props、事件和 TSX 泛型写法；复杂类型建模或跨框架类型契约先分流到 `fec-typescript-project-standard`。

### React 项目补充约定

- Props interface 命名: `ComponentNameProps`
- 事件处理函数: `handle` 前缀（如 `handleClick`）
- 回调 Props: `on` 前缀（如 `onChange`、`onSubmit`）
- 组件优先写显式 props 与返回值类型（`JSX.Element` / `React.ReactElement`），避免依赖 `React.FC` 的隐式 `children` 等行为差异
- 泛型组件使用 `<T>` 约束，保持调用处类型推导；回调与事件类型优先使用 DOM / React 自带类型（如 `React.ChangeEvent<HTMLInputElement>`）

```tsx
interface TableProps<T extends Record<string, unknown>> {
  data: T[];
  columns: ColumnDef<T>[];
  onRowClick?: (row: T) => void;
}
```

---

## 测试规范

### 应优先覆盖的内容

- 核心交互行为（点击、输入、提交）
- 条件渲染（loading / error / empty / data）
- 关键 hooks 的返回值和副作用
- API 调用 mock 与模块级集成测试

### 推荐风格

- 测试用户行为，而不是实现细节
- 优先使用 `screen.getByRole`、`getByLabelText`
- 避免围绕内部 state 写脆弱测试
- 只测关键行为，不机械追求覆盖率数字

### 示例

```tsx
describe("UserForm", () => {
  it("should submit with valid data", async () => {
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText("用户名"), "test");
    await userEvent.click(screen.getByRole("button", { name: "提交" }));

    expect(onSubmit).toHaveBeenCalledWith({ username: "test" });
  });

  it("should show error on invalid input", async () => {
    render(<UserForm onSubmit={vi.fn()} />);
    await userEvent.click(screen.getByRole("button", { name: "提交" }));
    expect(screen.getByText("用户名不能为空")).toBeInTheDocument();
  });
});
```

---


## 常见反模式

避免：

- prop drilling 过深却不考虑组合或局部封装
- 对局部问题过度使用 context
- 把数据请求、视图渲染、命令式 DOM 操作全塞进一个文件
- 在 useEffect 中做可以在事件处理函数中完成的事
- 用 `useEffect + setState` 模拟本可直接计算的派生值
- 将所有状态都推进全局 store
- 在 `components/` 中放业务耦合组件
- 直接绕过模块出口，从 feature 深层路径导入
- 没有明显收益却提前做复杂优化
- **新增类组件**或手写类式 Error Boundary（应函数组件 + `react-error-boundary` 等）

---

## 输出检查清单

输出 React 代码或方案时，至少检查：

- [ ] 是否先对齐了仓库现有约定
- [ ] 页面 / feature / 通用组件边界是否清晰
- [ ] 目录结构是否与模块复杂度匹配
- [ ] Props 类型完整且明确
- [ ] 解释性注释是否优先使用中文且点到要害
- [ ] 可复用逻辑是否已提取为 hooks
- [ ] loading / error / empty / data 状态是否齐全
- [ ] API 层是否具备类型约束和统一错误处理
- [ ] 复杂 DTO、外部数据收窄、公共类型或 `tsconfig` 问题是否已分流到 `fec-typescript-project-standard`
- [ ] 状态管理是否符合就近原则
- [ ] 路由级或重型模块是否考虑懒加载
- [ ] 样式方案是否与仓库保持一致
- [ ] 关键行为是否有测试覆盖
- [ ] 关键模块已用 **`react-error-boundary`**（等）包裹，且未手写类组件式 Boundary
- [ ] 超长列表是否评估虚拟化；弹窗/复合组件是否具备键盘与焦点约定
- [ ] 是否引入了不必要的新依赖或新范式

---
