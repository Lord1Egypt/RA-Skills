# Project Scan Usage Guide
> Referenced by SKILL.md Step 2.5. Read this file when a project scan is available.

## Running the Scan

```bash
python scripts/project_scan.py /path/to/project --json --output scan-report.json
```

The scan auto-detects Android or iOS, and produces a report with:
- All colors, strings, images, custom views in the project
- Lookup indices for fast matching (hex → color resource, text → string resource)

## How to Use Scan Results in Code Generation (Step 3)

**Color matching:**
1. Extract hex from Figma node → normalize to `#RRGGBB`
2. Look up in `indices.colors` → if hit, use project reference (Android: `@color/name`, iOS: `UIColor.df.name`)
3. For iOS dynamic colors: Figma is light mode. A scanned `light:#2965FF dark:#4D88FF` matches Figma `#2965FF`
4. No match → hardcode hex, but comment `// TODO: no matching project color`

**String matching:**
1. Extract text from Figma TEXT node
2. Look up in `indices.strings` → if hit, use i18n reference (Android: `@string/key`, iOS: depends on project i18n format)
3. No match → hardcode text, but comment `// TODO: not in i18n`

**Text style matching:**
1. Extract fontSize + fontWeight from Figma TEXT node
2. Build lookup key: "{fontSize}sp_{weight}" (e.g. "16sp_bold")
3. Look up in `indices.text_styles` → if hit, use style reference (Android: `style="@style/TextAppearance.App.Body"`)
4. No match → use inline attributes (android:textSize, android:textStyle, etc.)

fontWeight mapping (Figma numeric → Android key):
- 400 or below → "normal"
- 500 → "medium"
- 600 → "semibold"
- 700+ → "bold"

**Image matching:**
1. Icon elements → search scan images by semantic name (Figma `icon/back` → `icon_back`)
2. If matched: `UIImage(named:)` / `@drawable/name`
3. If not matched: export from Figma API

**Base class detection (iOS):**
- Scan reveals `BaseViewController`, `BaseTableViewCell`, etc. → use as parent class instead of raw UIKit classes

## Fallback (No Scan Available)

If no scan report is available, fall back to the hardcoded resource matching described in Step 3.
