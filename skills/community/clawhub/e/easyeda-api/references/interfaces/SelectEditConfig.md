# SelectEditConfig interface

## Signature

```typescript
interface SelectEditConfig
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

[disabled?](./SelectEditConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_

</td></tr>
<tr><td>

[multiple?](./SelectEditConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否多选

</td></tr>
<tr><td>

[onChange?](./SelectEditConfig.md)

</td><td>

</td><td>

(value: string \| number \| Array&lt;string \| number&gt;) =&gt; void

</td><td>

_(Optional)_

</td></tr>
<tr><td>

[options](./SelectEditConfig.md)

</td><td>

</td><td>

[SelectOption](./SelectOption.md)<!-- -->\[\]

</td><td>

下拉选项

</td></tr>
<tr><td>

[placeholder?](./SelectEditConfig.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
<tr><td>

[searchable?](./SelectEditConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否可搜索过滤

</td></tr>
<tr><td>

[type](./SelectEditConfig.md)

</td><td>

</td><td>

'select'

</td><td>

</td></tr>
</tbody></table>

---

## 属性详情

### disabled

# SelectEditConfig.disabled property

## Signature

```typescript
disabled?: boolean;
```

### multiple

# SelectEditConfig.multiple property

是否多选

## Signature

```typescript
multiple?: boolean;
```

### onchange

# SelectEditConfig.onChange property

## Signature

```typescript
onChange?: (value: string | number | Array<string | number>) => void;
```

### options

# SelectEditConfig.options property

下拉选项

## Signature

```typescript
options: SelectOption[];
```

### placeholder

# SelectEditConfig.placeholder property

## Signature

```typescript
placeholder?: string;
```

### searchable

# SelectEditConfig.searchable property

是否可搜索过滤

## Signature

```typescript
searchable?: boolean;
```

### type

# SelectEditConfig.type property

## Signature

```typescript
type: 'select';
```
