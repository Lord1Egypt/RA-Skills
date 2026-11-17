# ColumnDef interface

列定义

## Signature

```typescript
interface ColumnDef<T = any>
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

[align?](./ColumnDef.md)

</td><td>

</td><td>

[Align](../types/Align.md)

</td><td>

_(Optional)_ 对齐方式

</td></tr>
<tr><td>

[editable?](./ColumnDef.md)

</td><td>

</td><td>

boolean \| [ColumnEditTrigger](./ColumnEditTrigger.md)

</td><td>

_(Optional)_ 是否可编辑，默认 false（不传 = 不可编辑）

</td></tr>
<tr><td>

[ellipsis?](./ColumnDef.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 单元格文本溢出省略号：true 时单行截断（…）+ hover 显示完整文本 tooltip。 默认 false —— 单元格默认换行完整显示，省略号需显式开启。

⚠️ 虚拟滚动约束：本组件虚拟滚动为「固定行高」方案（非动态测量）， 换行会撑高 `<tr>` 导致可见行定位错位。因此开启 `virtualScroll` 时， 所有可能超长换行的列必须显式 `ellipsis: true`<!-- -->（或使用 `$truncate` 插槽）保证单行。

</td></tr>
<tr><td>

[filterable?](./ColumnDef.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否可筛选

</td></tr>
<tr><td>

[filterMatchMode?](./ColumnDef.md)

</td><td>

</td><td>

[FilterMatchMode](../types/FilterMatchMode.md)

</td><td>

_(Optional)_ 筛选匹配模式，默认由 type 推断：text=contains，其余（number/select/checkbox/date/boolean）=exact

</td></tr>
<tr><td>

[fixed?](./ColumnDef.md)

</td><td>

</td><td>

'left' \| 'right'

</td><td>

_(Optional)_ 固定列位置

</td></tr>
<tr><td>

[hidden?](./ColumnDef.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否隐藏

</td></tr>
<tr><td>

[key](./ColumnDef.md)

</td><td>

</td><td>

keyof T &amp; string

</td><td>

列 key（对应数据字段名）

</td></tr>
<tr><td>

[mergeByField?](./ColumnDef.md)

</td><td>

</td><td>

keyof T &amp; string

</td><td>

_(Optional)_ 按字段分组自动合并：相同值的连续行合并为一个 cell

</td></tr>
<tr><td>

[minWidth?](./ColumnDef.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 最小列宽（px），默认 50

</td></tr>
<tr><td>

[resizable?](./ColumnDef.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否可拖拽调整列宽

</td></tr>
<tr><td>

[rules?](./ColumnDef.md)

</td><td>

</td><td>

[ValidationRule](./ValidationRule.md)<!-- -->\[\]

</td><td>

_(Optional)_ 声明式校验规则（纯数据，可序列化）

</td></tr>
<tr><td>

[selectList?](./ColumnDef.md)

</td><td>

</td><td>

[SelectOption](./SelectOption.md)<!-- -->\[\]

</td><td>

_(Optional)_ 内置下拉渲染：显示选项 text 而非原始值

</td></tr>
<tr><td>

[slot?](./ColumnDef.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_ 单元格内置插槽名（$ 前缀），从 Main 侧内置目录解析；非 $ 前缀或未命中则回退默认渲染

</td></tr>
<tr><td>

[slotProps?](./ColumnDef.md)

</td><td>

</td><td>

[Serializable](../types/Serializable.md)

</td><td>

_(Optional)_ 传给插槽组件的纯数据（Serializable，可跨广播）

</td></tr>
<tr><td>

[sortable?](./ColumnDef.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否可排序

</td></tr>
<tr><td>

[sortKey?](./ColumnDef.md)

</td><td>

</td><td>

string \| string\[\]

</td><td>

_(Optional)_ 排序字段（默认取 key，可指定字段名或字段路径数组）

</td></tr>
<tr><td>

[sortType?](./ColumnDef.md)

</td><td>

</td><td>

'string' \| 'number' \| 'date'

</td><td>

_(Optional)_ 排序类型（默认由 type 推断）

</td></tr>
<tr><td>

[title](./ColumnDef.md)

</td><td>

</td><td>

string

</td><td>

列标题

</td></tr>
<tr><td>

[type?](./ColumnDef.md)

</td><td>

</td><td>

[ColumnType](../types/ColumnType.md)

</td><td>

_(Optional)_ 列数据类型，默认 'text'。决定默认排序类型（sortType）和筛选匹配模式（filterMatchMode）

</td></tr>
<tr><td>

[width?](./ColumnDef.md)

</td><td>

</td><td>

number \| string

</td><td>

_(Optional)_ 列宽：number = 像素值，string = CSS 值（如 "50%"、"auto"、"200px"）

</td></tr>
</tbody></table>

---

## 属性详情

### align

# ColumnDef.align property

对齐方式

## Signature

```typescript
align?: Align;
```

### editable

# ColumnDef.editable property

是否可编辑，默认 false（不传 = 不可编辑）

## Signature

```typescript
editable?: boolean | ColumnEditTrigger;
```

### ellipsis

# ColumnDef.ellipsis property

单元格文本溢出省略号：true 时单行截断（…）+ hover 显示完整文本 tooltip。 默认 false —— 单元格默认换行完整显示，省略号需显式开启。

⚠️ 虚拟滚动约束：本组件虚拟滚动为「固定行高」方案（非动态测量）， 换行会撑高 `<tr>` 导致可见行定位错位。因此开启 `virtualScroll` 时， 所有可能超长换行的列必须显式 `ellipsis: true`<!-- -->（或使用 `$truncate` 插槽）保证单行。

## Signature

```typescript
ellipsis?: boolean;
```

### filterable

# ColumnDef.filterable property

是否可筛选

## Signature

```typescript
filterable?: boolean;
```

### filtermatchmode

# ColumnDef.filterMatchMode property

筛选匹配模式，默认由 type 推断：text=contains，其余（number/select/checkbox/date/boolean）=exact

## Signature

```typescript
filterMatchMode?: FilterMatchMode;
```

### fixed

# ColumnDef.fixed property

固定列位置

## Signature

```typescript
fixed?: 'left' | 'right';
```

### hidden

# ColumnDef.hidden property

是否隐藏

## Signature

```typescript
hidden?: boolean;
```

### key

# ColumnDef.key property

列 key（对应数据字段名）

## Signature

```typescript
key: keyof T & string;
```

### mergebyfield

# ColumnDef.mergeByField property

按字段分组自动合并：相同值的连续行合并为一个 cell

## Signature

```typescript
mergeByField?: keyof T & string;
```

### minwidth

# ColumnDef.minWidth property

最小列宽（px），默认 50

## Signature

```typescript
minWidth?: number;
```

### resizable

# ColumnDef.resizable property

是否可拖拽调整列宽

## Signature

```typescript
resizable?: boolean;
```

### rules

# ColumnDef.rules property

声明式校验规则（纯数据，可序列化）

## Signature

```typescript
rules?: ValidationRule[];
```

### selectlist

# ColumnDef.selectList property

内置下拉渲染：显示选项 text 而非原始值

## Signature

```typescript
selectList?: SelectOption[];
```

### slot

# ColumnDef.slot property

单元格内置插槽名（$ 前缀），从 Main 侧内置目录解析；非 $ 前缀或未命中则回退默认渲染

## Signature

```typescript
slot?: string;
```

### slotprops

# ColumnDef.slotProps property

传给插槽组件的纯数据（Serializable，可跨广播）

## Signature

```typescript
slotProps?: Serializable;
```

### sortable

# ColumnDef.sortable property

是否可排序

## Signature

```typescript
sortable?: boolean;
```

### sortkey

# ColumnDef.sortKey property

排序字段（默认取 key，可指定字段名或字段路径数组）

## Signature

```typescript
sortKey?: string | string[];
```

### sorttype

# ColumnDef.sortType property

排序类型（默认由 type 推断）

## Signature

```typescript
sortType?: 'string' | 'number' | 'date';
```

### title

# ColumnDef.title property

列标题

## Signature

```typescript
title: string;
```

### type

# ColumnDef.type property

列数据类型，默认 'text'。决定默认排序类型（sortType）和筛选匹配模式（filterMatchMode）

## Signature

```typescript
type?: ColumnType;
```

### width

# ColumnDef.width property

列宽：number = 像素值，string = CSS 值（如 "50%"、"auto"、"200px"）

## Signature

```typescript
width?: number | string;
```
