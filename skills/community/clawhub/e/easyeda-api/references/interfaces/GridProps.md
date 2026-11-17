# GridProps interface

布局容器：固定列数的网格布局容器

## Signature

```typescript
interface GridProps extends StyleProps
```
**Extends:** [StyleProps](./StyleProps.md)

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

[children?](./GridProps.md)

</td><td>

</td><td>

any

</td><td>

_(Optional)_ Child node

</td></tr>
<tr><td>

[colGap?](./GridProps.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ Column gap (pixels)

</td></tr>
<tr><td>

[columns](./GridProps.md)

</td><td>

</td><td>

number \| (number \| string)\[\]

</td><td>

列数（必填）。 - number：等宽 n 列（repeat(n, 1fr)） - number\[\]：数组长度 = 列数，元素 = 各列宽度（像素） - string\[\]：数组长度 = 列数，元素 = 各列宽度（CSS 值，如 '1fr' / 'auto'）

</td></tr>
<tr><td>

[rowGap?](./GridProps.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ Row gap (pixels)

</td></tr>
</tbody></table>

---

## 属性详情

### children

# GridProps.children property

Child node

## Signature

```typescript
children?: any;
```

### colgap

# GridProps.colGap property

Column gap (pixels)

## Signature

```typescript
colGap?: number;
```

### columns

# GridProps.columns property

列数（必填）。 - number：等宽 n 列（repeat(n, 1fr)） - number\[\]：数组长度 = 列数，元素 = 各列宽度（像素） - string\[\]：数组长度 = 列数，元素 = 各列宽度（CSS 值，如 '1fr' / 'auto'）

## Signature

```typescript
columns: number | (number | string)[];
```

### rowgap

# GridProps.rowGap property

Row gap (pixels)

## Signature

```typescript
rowGap?: number;
```
