# 类型安全模式

## 类型边界审查清单

- DTO 应与外部载荷对应，并在 API 边界处进行转换。
- 领域模型或视图模型使用前端命名和稳定的联合类型。
- 组件 props 需命名明确，仅在该文件外复用时才导出。
- 公开函数必须有显式的参数和返回值类型。
- 外部输入必须从 `unknown` 开始，通过 schema 校验或类型守卫逐步收窄。
- 配置映射表优先使用 `as const` 和 `satisfies`，避免宽泛断言。

## 使用 `satisfies` 的配置映射表

```ts
type Tone = "neutral" | "success" | "warning" | "danger";

const STATUS_TONE = {
  draft: "neutral",
  paid: "success",
  overdue: "danger",
} as const satisfies Record<string, Tone>;

type InvoiceStatus = keyof typeof STATUS_TONE;
```

这样既保留了字面量值，又验证了映射表符合预期的值域。

## 映射类型用于表单错误

```ts
type FieldErrors<TValues extends Record<string, unknown>> = {
  [Key in keyof TValues]?: string;
};

interface ProfileFormValues {
  email: string;
  displayName: string;
}

type ProfileFormErrors = FieldErrors<ProfileFormValues>;
```

## 模板字面量类型用于事件命名

```ts
interface AnalyticsPayloads {
  checkoutStarted: { cartId: string };
  checkoutCompleted: { orderId: string };
}

type AnalyticsEventName = keyof AnalyticsPayloads;
type AnalyticsHandlerName = `on${Capitalize<string & AnalyticsEventName>}`;
```

当项目中已有事件命名规范时使用此模式。不要为一次性字符串引入。

## 更安全的泛型组件模式

```tsx
interface Entity {
  id: string;
}

interface EntityPickerProps<TEntity extends Entity> {
  items: TEntity[];
  selectedId: string | null;
  getLabel: (item: TEntity) => string;
  onSelect: (item: TEntity) => void;
}

export function EntityPicker<TEntity extends Entity>({
  items,
  selectedId,
  getLabel,
  onSelect,
}: EntityPickerProps<TEntity>) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          <button
            aria-pressed={item.id === selectedId}
            type="button"
            onClick={() => onSelect(item)}
          >
            {getLabel(item)}
          </button>
        </li>
      ))}
    </ul>
  );
}
```

## 类型审查反馈

报告类型安全问题时，需包含：

- 过于宽泛、过于狭窄或不合理的类型边界。
- 尽管通过 TypeScript 但可能在运行时失败的行为。
- 最小替换类型或守卫方案。
- 该变更是否需要测试或类型测试。
