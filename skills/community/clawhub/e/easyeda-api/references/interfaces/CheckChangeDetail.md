# CheckChangeDetail interface

勾选变更详情

## Signature

```typescript
interface CheckChangeDetail
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

[row?](./CheckChangeDetail.md)

</td><td>

</td><td>

Record&lt;string, any&gt;

</td><td>

_(Optional)_ 相关行数据

</td></tr>
<tr><td>

[trigger](./CheckChangeDetail.md)

</td><td>

</td><td>

'rowsUpdate' \| 'checkListUpdate' \| 'user'

</td><td>

变更来源

</td></tr>
</tbody></table>

---

## 属性详情

### row

# CheckChangeDetail.row property

相关行数据

## Signature

```typescript
row?: Record<string, any>;
```

### trigger

# CheckChangeDetail.trigger property

变更来源

## Signature

```typescript
trigger: 'rowsUpdate' | 'checkListUpdate' | 'user';
```
