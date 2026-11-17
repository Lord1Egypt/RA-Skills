# VirtualScrollConfig interface

虚拟滚动配置

## Signature

```typescript
interface VirtualScrollConfig
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

[onScrollToEnd?](./VirtualScrollConfig.md)

</td><td>

</td><td>

() =&gt; void

</td><td>

_(Optional)_ 滚动到底部通知

</td></tr>
<tr><td>

[overscan?](./VirtualScrollConfig.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 预渲染行数（上下各），默认 10

</td></tr>
<tr><td>

[scrollEndThreshold?](./VirtualScrollConfig.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ 触发 onScrollToEnd 的距底阈值，默认 200

</td></tr>
</tbody></table>

---

## 属性详情

### onscrolltoend

# VirtualScrollConfig.onScrollToEnd property

滚动到底部通知

## Signature

```typescript
onScrollToEnd?: () => void;
```

### overscan

# VirtualScrollConfig.overscan property

预渲染行数（上下各），默认 10

## Signature

```typescript
overscan?: number;
```

### scrollendthreshold

# VirtualScrollConfig.scrollEndThreshold property

触发 onScrollToEnd 的距底阈值，默认 200

## Signature

```typescript
scrollEndThreshold?: number;
```
