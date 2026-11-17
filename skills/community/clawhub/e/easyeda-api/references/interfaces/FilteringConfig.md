# FilteringConfig interface

筛选配置

## Signature

```typescript
interface FilteringConfig
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[caseSensitive?](./FilteringConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否区分大小写，默认 false

</td></tr>
<tr><td>

[debounce?](./FilteringConfig.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 输入防抖毫秒数，默认 300

</td></tr>
<tr><td>

[defaultFilters?](./FilteringConfig.md)

</td><td>

</td><td>

Record&lt;string, string&gt;

</td><td>

_(Optional)_ 非受控：初始筛选值

</td></tr>
<tr><td>

[filters?](./FilteringConfig.md)

</td><td>

</td><td>

Record&lt;string, string&gt;

</td><td>

_(Optional)_ 受控：外部维护的筛选值（key 为 colKey）

</td></tr>
<tr><td>

[onChange?](./FilteringConfig.md)

</td><td>

</td><td>

(filters: Record&lt;string, string&gt;) =&gt; void

</td><td>

_(Optional)_ 筛选变更通知

</td></tr>
<tr><td>

[onFilterCancel?](./FilteringConfig.md)

</td><td>

</td><td>

() =&gt; void

</td><td>

_(Optional)_ 筛选取消通知

</td></tr>
<tr><td>

[placeholder?](./FilteringConfig.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_ 筛选输入框占位符，默认 '筛选...'

</td></tr>
<tr><td>

[position?](./FilteringConfig.md)

</td><td>

</td><td>

'inline' \| 'popover'

</td><td>

_(Optional)_ 筛选位置：popover 弹窗 / inline 表头内联行，默认 'popover'

</td></tr>
</tbody></table>

---

## 属性详情

### casesensitive

# FilteringConfig.caseSensitive property

是否区分大小写，默认 false

## Signature

```typescript
caseSensitive?: boolean;
```

### debounce

# FilteringConfig.debounce property

输入防抖毫秒数，默认 300

## Signature

```typescript
debounce?: number;
```

### defaultfilters

# FilteringConfig.defaultFilters property

非受控：初始筛选值

## Signature

```typescript
defaultFilters?: Record<string, string>;
```

### filters

# FilteringConfig.filters property

受控：外部维护的筛选值（key 为 colKey）

## Signature

```typescript
filters?: Record<string, string>;
```

### onchange

# FilteringConfig.onChange property

筛选变更通知

## Signature

```typescript
onChange?: (filters: Record<string, string>) => void;
```

### onfiltercancel

# FilteringConfig.onFilterCancel property

筛选取消通知

## Signature

```typescript
onFilterCancel?: () => void;
```

### placeholder

# FilteringConfig.placeholder property

筛选输入框占位符，默认 '筛选...'

## Signature

```typescript
placeholder?: string;
```

### position

# FilteringConfig.position property

筛选位置：popover 弹窗 / inline 表头内联行，默认 'popover'

## Signature

```typescript
position?: 'inline' | 'popover';
```
