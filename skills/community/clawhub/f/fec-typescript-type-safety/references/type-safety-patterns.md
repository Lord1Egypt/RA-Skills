# Type safety mode

## Type Boundary Review Checklist

- DTOs should correspond to external loads and be converted at API boundaries.
- Domain model or view model uses front-end naming and stable union types.
- Component props need to be named clearly and exported only when reused outside this file.
- Public functions must have explicit parameter and return value types.
- External input must start from `unknown` and be gradually narrowed through schema verification or type guarding.
- Configure mapping tables using `as const` and `satisfies` first to avoid broad assertions.

## Use the configuration mapping table of `satisfies`

```ts
type Tone = "neutral" | "success" | "warning" | "danger";

const STATUS_TONE = {
  draft: "neutral",
  paid: "success",
  overdue: "danger",
} as const satisfies Record<string, Tone>;

type InvoiceStatus = keyof typeof STATUS_TONE;
```

This not only preserves the literal value, but also verifies that the mapping table conforms to the expected value range.

## Mapping type used for form errors

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

## Template literal type is used for event naming

```ts
interface AnalyticsPayloads {
  checkoutStarted: { cartId: string };
  checkoutCompleted: { orderId: string };
}

type AnalyticsEventName = keyof AnalyticsPayloads;
type AnalyticsHandlerName = `on${Capitalize<string & AnalyticsEventName>}`;
```

Use this pattern when there is already an event naming convention in the project. Don't introduce it for one-time strings.

## Safer generic component pattern

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

## Type Review Feedback

When reporting a type safety issue, include:

- Type boundaries that are too broad, too narrow, or unreasonable.
- Behavior that may fail at runtime despite passing TypeScript.
- Minimal replacement type or guard scheme.
- Whether the change requires testing or type testing.
