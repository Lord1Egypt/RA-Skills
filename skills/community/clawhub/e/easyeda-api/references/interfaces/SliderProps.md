# SliderProps interface

滑杆组件：基于浏览器原生 range 输入

## Signature

```typescript
interface SliderProps
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

[max?](./SliderProps.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 最大值（默认 1）

</td></tr>
<tr><td>

[min?](./SliderProps.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 最小值（默认 0）

</td></tr>
<tr><td>

[onChange?](./SliderProps.md)

</td><td>

</td><td>

(value: number) =&gt; void

</td><td>

_(Optional)_ 值变化时触发，参数为最新值

</td></tr>
<tr><td>

[value?](./SliderProps.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 当前值（受控）

</td></tr>
</tbody></table>

---

## 属性详情

### max

# SliderProps.max property

最大值（默认 1）

## Signature

```typescript
max?: number;
```

### min

# SliderProps.min property

最小值（默认 0）

## Signature

```typescript
min?: number;
```

### onchange

# SliderProps.onChange property

值变化时触发，参数为最新值

## Signature

```typescript
onChange?: (value: number) => void;
```

### value

# SliderProps.value property

当前值（受控）

## Signature

```typescript
value?: number;
```
