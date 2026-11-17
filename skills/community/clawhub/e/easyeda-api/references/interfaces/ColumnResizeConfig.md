# ColumnResizeConfig interface

列宽拖拽配置

## Signature

```typescript
interface ColumnResizeConfig
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

[minWidth?](./ColumnResizeConfig.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 最小列宽（px），默认 25

</td></tr>
<tr><td>

[onChange?](./ColumnResizeConfig.md)

</td><td>

</td><td>

(info: { colKey: string; width: number }) =&gt; void

</td><td>

_(Optional)_ 列宽变更通知

</td></tr>
<tr><td>

[persist?](./ColumnResizeConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否持久化列宽到 localStorage，默认 true

</td></tr>
<tr><td>

[storageKey?](./ColumnResizeConfig.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_ 持久化存储 key

</td></tr>
</tbody></table>

---

## 属性详情

### minwidth

# ColumnResizeConfig.minWidth property

最小列宽（px），默认 25

## Signature

```typescript
minWidth?: number;
```

### onchange

# ColumnResizeConfig.onChange property

列宽变更通知

## Signature

```typescript
onChange?: (info: { colKey: string; width: number }) => void;
```

### persist

# ColumnResizeConfig.persist property

是否持久化列宽到 localStorage，默认 true

## Signature

```typescript
persist?: boolean;
```

### storagekey

# ColumnResizeConfig.storageKey property

持久化存储 key

## Signature

```typescript
storageKey?: string;
```
