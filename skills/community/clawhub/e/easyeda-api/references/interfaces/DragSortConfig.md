# DragSortConfig interface

拖拽排序配置

## Signature

```typescript
interface DragSortConfig
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

[handle?](./DragSortConfig.md)

</td><td>

</td><td>

'drag-column' \| 'row'

</td><td>

_(Optional)_ 拖拽手柄形式：独立拖拽列 / 整行拖拽，默认 'drag-column'

</td></tr>
<tr><td>

[onDragEnd?](./DragSortConfig.md)

</td><td>

</td><td>

(info: { fromIndices: number \| number\[\]; toIndex: number; currentIndices: number \| number\[\] }) =&gt; void

</td><td>

_(Optional)_ 拖拽排序结束通知

</td></tr>
<tr><td>

[showDragIcon?](./DragSortConfig.md)

</td><td>

</td><td>

boolean

</td><td>

_(Optional)_ 是否显示拖拽图标，默认 true

</td></tr>
</tbody></table>

---

## 属性详情

### handle

# DragSortConfig.handle property

拖拽手柄形式：独立拖拽列 / 整行拖拽，默认 'drag-column'

## Signature

```typescript
handle?: 'drag-column' | 'row';
```

### ondragend

# DragSortConfig.onDragEnd property

拖拽排序结束通知

## Signature

```typescript
onDragEnd?: (info: { fromIndices: number | number[]; toIndex: number; currentIndices: number | number[] }) => void;
```

### showdragicon

# DragSortConfig.showDragIcon property

是否显示拖拽图标，默认 true

## Signature

```typescript
showDragIcon?: boolean;
```
