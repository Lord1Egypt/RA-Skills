# InputEditConfig interface

## Signature

```typescript
interface InputEditConfig
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

[inputType?](./InputEditConfig.md)

</td><td>

</td><td>

'text' \| 'number'

</td><td>

_(Optional)_ 原生 input 类型，默认 'text'

</td></tr>
<tr><td>

[maxLength?](./InputEditConfig.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_

</td></tr>
<tr><td>

[onChange?](./InputEditConfig.md)

</td><td>

</td><td>

(value: string) =&gt; void

</td><td>

_(Optional)_

</td></tr>
<tr><td>

[onConfirm?](./InputEditConfig.md)

</td><td>

</td><td>

(value: string) =&gt; void

</td><td>

_(Optional)_

</td></tr>
<tr><td>

[placeholder?](./InputEditConfig.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
<tr><td>

[type](./InputEditConfig.md)

</td><td>

</td><td>

'input'

</td><td>

</td></tr>
</tbody></table>

---

## 属性详情

### inputtype

# InputEditConfig.inputType property

原生 input 类型，默认 'text'

## Signature

```typescript
inputType?: 'text' | 'number';
```

### maxlength

# InputEditConfig.maxLength property

## Signature

```typescript
maxLength?: number;
```

### onchange

# InputEditConfig.onChange property

## Signature

```typescript
onChange?: (value: string) => void;
```

### onconfirm

# InputEditConfig.onConfirm property

## Signature

```typescript
onConfirm?: (value: string) => void;
```

### placeholder

# InputEditConfig.placeholder property

## Signature

```typescript
placeholder?: string;
```

### type

# InputEditConfig.type property

## Signature

```typescript
type: 'input';
```
