# ClipboardCellData interface

剪贴板单元格数据

## Signature

```typescript
interface ClipboardCellData
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

[contentType](./ClipboardCellData.md)

</td><td>

</td><td>

[CellContentType](../types/CellContentType.md)

</td><td>

内容类型

</td></tr>
<tr><td>

[subType?](./ClipboardCellData.md)

</td><td>

</td><td>

string

</td><td>

_(Optional)_ 子类型（预留）

</td></tr>
<tr><td>

[text](./ClipboardCellData.md)

</td><td>

</td><td>

string

</td><td>

纯文本表示

</td></tr>
<tr><td>

[value](./ClipboardCellData.md)

</td><td>

</td><td>

any

</td><td>

原始值

</td></tr>
</tbody></table>

---

## 属性详情

### contenttype

# ClipboardCellData.contentType property

内容类型

## Signature

```typescript
contentType: CellContentType;
```

### subtype

# ClipboardCellData.subType property

子类型（预留）

## Signature

```typescript
subType?: string;
```

### text

# ClipboardCellData.text property

纯文本表示

## Signature

```typescript
text: string;
```

### value

# ClipboardCellData.value property

原始值

## Signature

```typescript
value: any;
```
