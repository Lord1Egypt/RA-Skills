# Plan schema

`build_figures.py` reads one JSON file describing the whole insertion pass. Paths may be absolute or relative to the working directory. `output` must differ from `source`; the source file is never modified.

```json
{
  "source": "report.docx",
  "output": "report_with_exhibits.docx",

  "style": {
    "cn_font": "宋体",
    "en_font": "Times New Roman",
    "table_font_pt": 9,
    "table_caption_pt": 10.5,
    "figure_caption_pt": 12,
    "note_pt": 9,
    "figure_width_cm": 14.5,
    "caption_bold": true,
    "note_align": "left",
    "normalize_image_width_cm": 14.5
  },

  "references": [
    { "anchor": "印度尼西亚、巴基斯坦、赞比亚在可再生能源发展目标", "text": "（见表1）" },
    { "anchor": "截至 2025 年 6 月底，巴基斯坦全国装机约", "text": "（见图2）" }
  ],

  "tables": [
    {
      "number": 1,
      "title": "三国可再生能源发展目标与执行进展",
      "anchor": "印度尼西亚、巴基斯坦、赞比亚在可再生能源发展目标",
      "header": ["国家", "目标设定", "实际进展", "与目标的差距"],
      "rows": [
        ["印度尼西亚", "2025 年可再生能源占一次能源 23%", "2025 年底约 15.75%", "低约 7.3 个百分点"],
        ["巴基斯坦", "2030 年可再生能源发电占比 60%", "2025 年 9 月约 46%", "低约 14 个百分点"]
      ],
      "widths_cm": [2.0, 4.0, 5.9, 2.6],
      "aligns": ["center", "left", "left", "left"],
      "align_first": "center",
      "note": "注：差距为文中目标值与实际值之差。资料来源：根据本节正文数据整理。"
    }
  ],

  "figures": [
    {
      "number": 2,
      "title": "巴基斯坦装机容量与峰值负荷对比（2025 年 6 月底）",
      "anchor": "截至 2025 年 6 月底，巴基斯坦全国装机约",
      "image": "figs/fig2_pak_capacity.png",
      "width_cm": 14.5,
      "note": "注：名义备用容量为全国装机容量与系统峰值负荷之差。资料来源：根据本节正文数据整理。"
    }
  ]
}
```

## Field notes

- **anchor** — the first ~20–30 characters of the existing paragraph the exhibit follows. Must match exactly (leading whitespace is stripped). Make it long enough to be unique; the builder stops at the first match and exits if there is none.
- **references** — inserted before the last `。` of the anchor paragraph, inheriting the surrounding run formatting. The anchor for a reference and for the exhibit it points to is normally the same paragraph.
- **number** — integer used for `表N`/`图N` in caption and reference. Number across the whole document in reading order; continue an existing series instead of restarting.
- **rows** — strings only; numbers may be given as strings to control formatting (`"41 121"`, `"93.2%"`, `"1.889 万亿"`).
- **widths_cm** — one value per column; the sum is the real table width. Keep the sum ≤ usable text width (usually 14.65 cm). Very narrow first columns break country names; 2.0 cm is about the minimum for a 5-character Chinese name at 9 pt.
- **aligns** — per column, used for body cells; `align_first` overrides column 0. Numbers look best `center`, prose `left`.
- **style** — omit entirely to use the defaults above. `normalize_image_width_cm` scales any pre-existing inline image wider than that value, keeping its aspect ratio.
- **figures.width_cm** — defaults to `style.figure_width_cm`. Draw the PNG at that physical width so 9 pt chart text stays 9 pt after insertion (see `scripts/fig_style.py`).

## Ordering rule

Tables are inserted after figures in the file only if the plan lists them that way; the builder processes `references`, then `tables`, then `figures`. Anchors are searched on the current document, so anchor paragraphs must still be findable after earlier insertions — use body paragraphs, never a caption the builder itself created.
