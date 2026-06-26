# GB/T 7714 from BibTeX

Use this file when formatting selected references from BibTeX metadata.

## General Rules

- Use only metadata present in BibTeX unless the user explicitly permits external lookup.
- Do not invent missing volume, issue, pages, publisher, place, DOI, or URL.
- Preserve author order.
- For Chinese references, keep Chinese punctuation and names as provided.
- For English references, uppercase family-name/initial style is acceptable when metadata is already in English.
- Use `et al.` when the entry has many English authors and the target style allows abbreviation.
- Use `等` only when appropriate for Chinese author lists and the user/style expects it.

## Common Formats

### Journal Article

Chinese:

```text
作者. 题名[J]. 刊名, 年, 卷(期): 起止页.
```

Without volume:

```text
作者. 题名[J]. 刊名, 年(期): 起止页.
```

Without pages:

```text
作者. 题名[J]. 刊名, 年, 卷(期).
```

English:

```text
AUTHOR A, AUTHOR B. Title[J]. Journal, Year, Volume(Issue): Pages.
```

### Book

```text
作者. 书名[M]. 出版地: 出版者, 年.
```

If place or publisher is missing, omit the missing segment rather than fabricate it.

### Conference Paper

```text
作者. 题名[C]//会议名. 出版地: 出版者, 年: 起止页.
```

### Thesis

```text
作者. 题名[D]. 保存地: 保存单位, 年.
```

### Online / Report / Misc

Use the most complete honest form available. Include access date only if present or requested.

## BibTeX Field Mapping

- `author` -> authors.
- `editor` -> editors when author is absent.
- `title` -> title.
- `journal` or `journaltitle` -> journal.
- `booktitle` -> conference or chapter source.
- `year` or `date` -> year.
- `volume` -> volume.
- `number` or `issue` -> issue.
- `pages` -> pages. Normalize double hyphens to single hyphen for display.
- `publisher` -> publisher.
- `address` or `location` -> publication place.
- `doi`, `url` -> append only when the requested style includes them or when necessary.

## Quality Checks

- Every cited item has a bibliography entry.
- No bibliography item is unused.
- Number order follows first citation order unless another sort order is requested.
- Reference punctuation is consistent.
- English journal titles and article titles are not accidentally lowercased by code.
- Chinese `(文)` or source annotations from metadata are preserved only if they are actually part of the author field or user-provided metadata.
