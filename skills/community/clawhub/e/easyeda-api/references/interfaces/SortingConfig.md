# SortingConfig interface

排序配置

## Signature

```typescript
interface SortingConfig
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

[defaultState?](./SortingConfig.md)

</td><td>

</td><td>

[SortState](./SortState.md)<!-- -->\[\]

</td><td>

_(Optional)_ 非受控：初始排序状态

</td></tr>
<tr><td>

[multiple?](./SortingConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否支持多列排序，默认 false

</td></tr>
<tr><td>

[onChange?](./SortingConfig.md)

</td><td>

</td><td>

(state: [SortState](./SortState.md)<!-- -->\[\]) =&gt; void

</td><td>

_(Optional)_ 排序变更通知

</td></tr>
<tr><td>

[remote?](./SortingConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 远端排序：true 时仅触发 onChange，不本地排序，默认 false

</td></tr>
<tr><td>

[state?](./SortingConfig.md)

</td><td>

</td><td>

[SortState](./SortState.md)<!-- -->\[\]

</td><td>

_(Optional)_ 受控：外部维护的排序状态

</td></tr>
</tbody></table>

---

## 属性详情

### defaultstate

# SortingConfig.defaultState property

非受控：初始排序状态

## Signature

```typescript
defaultState?: SortState[];
```

### multiple

# SortingConfig.multiple property

是否支持多列排序，默认 false

## Signature

```typescript
multiple?: boolean;
```

### onchange

# SortingConfig.onChange property

排序变更通知

## Signature

```typescript
onChange?: (state: SortState[]) => void;
```

### remote

# SortingConfig.remote property

远端排序：true 时仅触发 onChange，不本地排序，默认 false

## Signature

```typescript
remote?: boolean;
```

### state

# SortingConfig.state property

受控：外部维护的排序状态

## Signature

```typescript
state?: SortState[];
```
