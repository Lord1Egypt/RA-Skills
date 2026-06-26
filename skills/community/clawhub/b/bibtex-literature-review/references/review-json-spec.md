# Review JSON Specification

Use this JSON format with `scripts/build_docx_from_review_json.py`.

## Top-Level Fields

```json
{
  "title": "文献综述",
  "paragraphs": [],
  "references": [],
  "style": {}
}
```

- `title`: document title. Defaults to `文献综述`.
- `paragraphs`: required list of paragraph part lists.
- `references`: required list of bibliography entries in citation-number order.
- `style`: optional style settings.

## Paragraph Parts

Each paragraph is a list. Each item is either a string or a citation object.

```json
[
  "刘颖认为数字化转型推动人力资源管理创新",
  {"cite": 1},
  "。"
]
```

## Citation Objects

Single citation:

```json
{"cite": 1}
```

Multiple citations with default compression:

```json
{"cite": [3, 4, 5]}
```

Default display: `[3-5]`.

Multiple citations without compression:

```json
{"cite": [10, 11], "collapse": false}
```

Display: `[10,11]`.

Two-number ranges are not compressed by default because many thesis examples prefer `[4,5]` rather than `[4-5]`. To force a range:

```json
{"cite": [4, 5], "collapse": true, "min_range": 2}
```

Display: `[4-5]`.

## References

Each reference should include `gbt`, `formatted`, or `text`. `gbt` is retained as the backwards-compatible field name even when the bibliography text is APA, MLA, IEEE, or another requested style.

```json
{
  "gbt": "刘颖. 数字化转型背景下企业人力资源管理模式创新研究[J]. 知识经济, 2025(33): 157-159, 163."
}
```

Equivalent:

```json
{"text": "Liu, Y. (2025). Digital transformation and HRM innovation. Knowledge Economy, (33), 157-159."}
```

Optional `anchor` may be provided. If omitted, anchors are generated as `_RefBib001`, `_RefBib002`, etc.

```json
{"anchor": "_RefBib001", "gbt": "..."}
```

Reference objects may also carry source metadata (`key`, `type`, `fields`) produced by `sources_to_json.py`; the DOCX builder ignores unknown fields.

## Style Fields

Optional:

```json
{
  "style": {
    "body_font": "SimSun",
    "east_asia_font": "宋体",
    "body_size_pt": 12,
    "reference_size_pt": 10.5,
    "line_spacing": 1.5
  }
}
```

`body_east_asia_font` is accepted as a backwards-compatible alias, but new JSON should use `east_asia_font`.

The builder defaults are tuned for Chinese thesis-style literature reviews.
