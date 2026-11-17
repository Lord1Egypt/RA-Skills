# Verbatim subset: procedure and pitfalls

## Why verbatim

A rewritten “slim” edition can contain more conditional markers than the original while covering less. Once text is paraphrased, the marker count stops being evidence. Verbatim cuts keep the measurement honest.

Allowed changes: deleting a whole block, inserting a pointer line, inserting a separator.

Forbidden: rewording, merging sentences, adding emphasis, changing punctuation.

## Procedure

1. **Record line ranges.** For each block you intend to move, note `[start, end]` in the original.
2. **Extract mechanically.** Write the moved file by slicing those ranges; never retype.
3. **Compare bytes.** For every moved slice, assert the extracted text equals the original slice, character for character.
4. **Insert a pointer.** One line, containing: the trigger condition, the target file, and what it covers.
5. **Remove the block** from the slim file. Leave only the pointer.
6. **Run `subset_check.py`.** Zero missing non-pointer lines is the pass condition.
7. **Run `cond_count.py` on slim and moved.** Compute both inequalities.

## Pointer line requirements

A pointer must answer: **when** should the reader follow it, and **what** will they find. “See references/x.md” fails the when test and will never be followed.

Good:

```
> See references/pdf-export.md when producing a PDF or embedding fonts.
```

Bad:

```
> More details in references/pdf-export.md
```

## Joint accounting example

| Version | Markers |
|---|---|
| original | 36 |
| slim | 29 |
| moved | 24 |

- `slim <= original` → 29 <= 36 ✅ (no rewrite)
- `slim + moved >= original` → 53 >= 36 ✅ (coverage retained)

Reporting only the first number would look like a loss; reporting only the second would hide a rewrite. Both are required.

## Pitfalls

- **Marker counts rise after rewriting.** Treat any increase in the slim file as a rewrite signal and inspect it.
- **Section attribution matters.** A total that holds while one section falls is still a regression; name the section.
- **Pointer without trigger equals deletion.** The rule will never be read.
- **Stale snapshots.** Replace “there are N items” with the command that answers it, or it will silently drift.
