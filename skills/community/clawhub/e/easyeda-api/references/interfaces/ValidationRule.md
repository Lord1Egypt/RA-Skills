# ValidationRule interface

校验规则（声明式，纯数据，可序列化）

## Signature

```typescript
interface ValidationRule
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

[max?](./ValidationRule.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 最大值（数字）

</td></tr>
<tr><td>

[maxLength?](./ValidationRule.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 最大长度（字符串）

</td></tr>
<tr><td>

[message?](./ValidationRule.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_ 校验失败时的提示文案

</td></tr>
<tr><td>

[min?](./ValidationRule.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 最小值（数字）

</td></tr>
<tr><td>

[minLength?](./ValidationRule.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 最小长度（字符串）

</td></tr>
<tr><td>

[pattern?](./ValidationRule.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_ 正则表达式字符串（匹配失败即校验失败）

</td></tr>
<tr><td>

[required?](./ValidationRule.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否必填（空值 = null/undefined/空白字符串）

</td></tr>
</tbody></table>

---

## 属性详情

### max

# ValidationRule.max property

最大值（数字）

## Signature

```typescript
max?: number;
```

### maxlength

# ValidationRule.maxLength property

最大长度（字符串）

## Signature

```typescript
maxLength?: number;
```

### message

# ValidationRule.message property

校验失败时的提示文案

## Signature

```typescript
message?: string;
```

### min

# ValidationRule.min property

最小值（数字）

## Signature

```typescript
min?: number;
```

### minlength

# ValidationRule.minLength property

最小长度（字符串）

## Signature

```typescript
minLength?: number;
```

### pattern

# ValidationRule.pattern property

正则表达式字符串（匹配失败即校验失败）

## Signature

```typescript
pattern?: string;
```

### required

# ValidationRule.required property

是否必填（空值 = null/undefined/空白字符串）

## Signature

```typescript
required?: boolean;
```
