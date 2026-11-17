# ClipboardConfig interface

剪贴板配置

## Signature

```typescript
interface ClipboardConfig
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

[onCopy?](./ClipboardConfig.md)

</td><td>

</td><td>

(data: [ClipboardCellData](./ClipboardCellData.md)<!-- -->\[\]\[\]) =&gt; void

</td><td>

_(Optional)_ 复制通知（注意：复制走浏览器原生，此回调仅作通知，不接管复制）

</td></tr>
<tr><td>

[onPaste?](./ClipboardConfig.md)

</td><td>

</td><td>

(data: [ClipboardCellData](./ClipboardCellData.md)<!-- -->\[\]\[\], targetCell: [CellCoord](./CellCoord.md)<!-- -->) =&gt; void

</td><td>

_(Optional)_ 粘贴通知

</td></tr>
<tr><td>

[shortcuts?](./ClipboardConfig.md)

</td><td>

</td><td>

\{ copy?: string; paste?: string; cut?: string \}

</td><td>

_(Optional)_ 自定义快捷键

</td></tr>
</tbody></table>

---

## 属性详情

### oncopy

# ClipboardConfig.onCopy property

复制通知（注意：复制走浏览器原生，此回调仅作通知，不接管复制）

## Signature

```typescript
onCopy?: (data: ClipboardCellData[][]) => void;
```

### onpaste

# ClipboardConfig.onPaste property

粘贴通知

## Signature

```typescript
onPaste?: (data: ClipboardCellData[][], targetCell: CellCoord) => void;
```

### shortcuts

# ClipboardConfig.shortcuts property

自定义快捷键

## Signature

```typescript
shortcuts?: { copy?: string; paste?: string; cut?: string };
```
