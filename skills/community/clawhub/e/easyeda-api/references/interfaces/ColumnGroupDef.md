# ColumnGroupDef interface

列分组：多级表头

## Signature

```typescript
interface ColumnGroupDef<T = any>
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

[align?](./ColumnGroupDef.md)

</td><td>

</td><td>

[Align](../types/Align.md)

</td><td>

_(Optional)_ 分组对齐（子列未指定时继承）

</td></tr>
<tr><td>

[children](./ColumnGroupDef.md)

</td><td>

</td><td>

[ColumnDef](./ColumnDef.md)<!-- -->&lt;T&gt;\[\]

</td><td>

子列

</td></tr>
<tr><td>

[fixed?](./ColumnGroupDef.md)

</td><td>

</td><td>

'left' \| 'right'

</td><td>

_(Optional)_ 分组固定列位置（子列未指定时继承）

</td></tr>
<tr><td>

[key](./ColumnGroupDef.md)

</td><td>

</td><td>

string

</td><td>

分组标识（表头渲染用）

</td></tr>
<tr><td>

[title](./ColumnGroupDef.md)

</td><td>

</td><td>

string

</td><td>

分组标题

</td></tr>
<tr><td>

[type](./ColumnGroupDef.md)

</td><td>

</td><td>

'group'

</td><td>

</td></tr>
</tbody></table>

---

## 属性详情

### align

# ColumnGroupDef.align property

分组对齐（子列未指定时继承）

## Signature

```typescript
align?: Align;
```

### children

# ColumnGroupDef.children property

子列

## Signature

```typescript
children: ColumnDef < T > [];
```

### fixed

# ColumnGroupDef.fixed property

分组固定列位置（子列未指定时继承）

## Signature

```typescript
fixed?: 'left' | 'right';
```

### key

# ColumnGroupDef.key property

分组标识（表头渲染用）

## Signature

```typescript
key: string;
```

### title

# ColumnGroupDef.title property

分组标题

## Signature

```typescript
title: string;
```

### type

# ColumnGroupDef.type property

## Signature

```typescript
type: 'group';
```
