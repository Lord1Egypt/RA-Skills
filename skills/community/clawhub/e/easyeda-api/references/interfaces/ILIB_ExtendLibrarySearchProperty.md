# ILIB\_ExtendLibrarySearchProperty interface

External library search property

## Signature

```typescript
interface ILIB_ExtendLibrarySearchProperty<T>
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

[page?](./ILIB_ExtendLibrarySearchProperty.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ Page count

</td></tr>
<tr><td>

[pageSize?](./ILIB_ExtendLibrarySearchProperty.md)

</td><td>

</td><td>

number

</td><td>

_(Optional)_ Number of entries per page

</td></tr>
<tr><td>

[query](./ILIB_ExtendLibrarySearchProperty.md)

</td><td>

</td><td>

T &amp; { wd?: string; listByTitles?: Array&lt;string&gt;; classification?: [ILIB\_ExtendLibraryClassificationIndex](./ILIB_ExtendLibraryClassificationIndex.md) \| Array&lt;string&gt; }

</td><td>

Query parameter

</td></tr>
</tbody></table>

---

## 属性详情

### page

# ILIB\_ExtendLibrarySearchProperty.page property

Page count

## Signature

```typescript
page?: number;
```

### pagesize

# ILIB\_ExtendLibrarySearchProperty.pageSize property

Number of entries per page

## Signature

```typescript
pageSize?: number;
```

### query

# ILIB\_ExtendLibrarySearchProperty.query property

Query parameter

## Signature

```typescript
query: T & { wd?: string; listByTitles?: Array<string>; classification?: ILIB_ExtendLibraryClassificationIndex | Array<string> };
```
