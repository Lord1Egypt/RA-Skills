# CustomHeaderConfig interface

自定义表头配置（列可见性管理）

## Signature

```typescript
interface CustomHeaderConfig
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

[availableColumns](./CustomHeaderConfig.md)

</td><td>

</td><td>

[ColumnDef](./ColumnDef.md)<!-- -->\[\]

</td><td>

全部可选列（含隐藏列）

</td></tr>
<tr><td>

[onChange](./CustomHeaderConfig.md)

</td><td>

</td><td>

(visibleKeys: string\[\]) =&gt; void

</td><td>

可见列变更通知

</td></tr>
<tr><td>

[persist?](./CustomHeaderConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否持久化，默认 true

</td></tr>
<tr><td>

[storageKey?](./CustomHeaderConfig.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_ 持久化存储 key

</td></tr>
<tr><td>

[visibleKeys](./CustomHeaderConfig.md)

</td><td>

</td><td>

string\[\]

</td><td>

当前可见列 key 列表

</td></tr>
</tbody></table>

---

## 属性详情

### availablecolumns

# CustomHeaderConfig.availableColumns property

全部可选列（含隐藏列）

## Signature

```typescript
availableColumns: ColumnDef[];
```

### onchange

# CustomHeaderConfig.onChange property

可见列变更通知

## Signature

```typescript
onChange: (visibleKeys: string[]) => void;
```

### persist

# CustomHeaderConfig.persist property

是否持久化，默认 true

## Signature

```typescript
persist?: boolean;
```

### storagekey

# CustomHeaderConfig.storageKey property

持久化存储 key

## Signature

```typescript
storageKey?: string;
```

### visiblekeys

# CustomHeaderConfig.visibleKeys property

当前可见列 key 列表

## Signature

```typescript
visibleKeys: string[];
```
