# Project Scan Usage Guide
> Referenced by SKILL.md Step 2.5. Read this file when a project scan is available.

## Running the Scan

```bash
python scripts/project_scan.py /path/to/project --json --output scan-report.json
```

The scan auto-detects Android or iOS, and produces a report with:
- All colors, strings, images, custom views in the project
- Lookup indices for fast matching (hex → color resource, text → string resource)
- Semantic labels: which resources map to design system roles (primary, surface, body, etc.)

## How to Use Scan Results in Code Generation (Step 3)

### Color matching (with semantic labels)

The scan report includes `semantic_labels` — annotations that tell you which
resources play which role in the design system:

```json
{
  "semantic_labels": [
    {"name": "#FF6200EE", "resource_type": "color", "semantic_role": "primary",
     "source": "theme_mapping", "confidence": "high"},
    {"name": "#FF1C1B1F", "resource_type": "color", "semantic_role": "on_primary",
     "source": "theme_mapping", "confidence": "high"}
  ]
}
```

**Process:**
1. Extract hex from Figma node → normalize to `#RRGGBB`
2. Look up in `indices.colors` → if hit, use project reference
3. Also check `semantic_labels` for role → if Figma has a color labeled
   "Primary" and the project has one, map them even if hex differs
4. For iOS dynamic colors: Figma is light mode. A scanned `light:#2965FF dark:#4D88FF`
   matches Figma `#2965FF`
5. No match → hardcode hex, but comment `// TODO: no matching project color`

**When to use semantic labels over exact hex match:**
- Figma uses a design system color (primary, secondary, surface) → prefer semantic
  label mapping even if hex values differ slightly
- Project has theme variables (`?attr/colorPrimary`) → use theme reference,
  not the resolved hex

### String matching

1. Extract text from Figma TEXT node
2. Look up in `indices.strings` → if hit, use i18n reference
   (Android: `@string/key`, iOS: depends on project i18n format)
3. No match → hardcode text, but comment `// TODO: not in i18n`

### Text style matching

1. Extract fontSize + fontWeight from Figma TEXT node
2. Build lookup key: "{fontSize}sp_{weight}" (e.g. "16sp_bold")
3. Look up in `indices.text_styles` → if hit, use style reference
   (Android: `style="@style/TextAppearance.App.Body"`)
4. Also check `semantic_labels` for text style roles — if Figma labels a text
   as "Body" and the project has a matching style, use it
5. No match → use inline attributes (android:textSize, android:textStyle, etc.)

fontWeight mapping (Figma numeric → Android key):
- 400 or below → "normal"
- 500 → "medium"
- 600 → "semibold"
- 700+ → "bold"

### Image matching

1. Icon elements → search scan images by semantic name
   (Figma `icon/back` → `icon_back`)
2. If matched: `UIImage(named:)` / `@drawable/name`
3. If not matched: export from Figma API

### Base class detection (iOS)

- Scan reveals `BaseViewController`, `BaseTableViewCell`, etc.
  → use as parent class instead of raw UIKit classes

## Semantic Labels Reference

The scanner produces three levels of semantic annotation:

| Source | Confidence | Example |
|--------|-----------|---------|
| **Theme mapping** (Android themes.xml) | high | `colorPrimary` → primary |
| **Asset naming** (iOS .colorset names) | high | `AccentColor` → primary |
| **Resource naming** (color names like "primary") | medium | `brand_primary_color` → primary |
| **Dimen naming** (spacing_*) | medium | `spacing_16` → spacing_md |
| **Text style naming** (style name heuristics) | medium | `TextAppearance.Body1` → body |

Use high-confidence labels first. Medium-confidence labels are hints —
validate against the Figma design before making assumptions.

## Fallback (No Scan Available)

If no scan report is available, fall back to the hardcoded resource matching
described in Step 3.

## Presenting Scan Results

Keep it brief and useful — not a JSON dump:

> ✓ 扫描完成：找到 3 个模块、24 个颜色、18 条文案。
> 其中有 6 个颜色映射到了主题色（primary、surface 等），生成代码时会用项目资源引用。

If scan found issues, tell the user naturally:

> 扫描完了，找到 N 个资源。不过 [具体问题，如某个模块没找到资源文件]，
> 你项目里这部分是怎么组织的？
