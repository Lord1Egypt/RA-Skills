# Code Generation Rules
> Referenced by SKILL.md Step 3. Read this file before generating code.

## Output Rules (absolute — never break these)

**Project scan availability check:**
- If a project scan report is available (Step 2.5 was run): match Figma values against project resources first, then hardcode unmatched values.
- If NO project scan was run: hardcode ALL values directly (hex colors, literal strings, dp dimensions). Do not use `@color/placeholder` or `@string/placeholder` — write real values for instant visual preview.

- **Colors**: Before hardcoding, search `res/values/colors.xml` (and `res/values/colors_*.xml` if present) for a matching hex value. If found, use the resource reference (e.g. `@color/primary`). If not found, write hex directly (`android:textColor="#0F0F0F"` / `Color(0xFF0F0F0F)`).
- **Strings**: Before hardcoding, search `res/values/strings.xml` for matching text content. If found, use the resource reference (e.g. `@string/notification_settings`). If not found, write text directly (`android:text="通知设置"`).
- **Dimensions**: write values directly (`android:textSize="17sp"`). Dimension resources are rarely worth matching.
- **Lists**: output main layout + separate item layout file. Do NOT generate Adapter/ViewHolder.
- **Resource matching priority**: Use project-defined `@color/` and `@string/` when an exact match exists. Hardcode everything else for instant preview. Never create new resource definitions — only reference existing ones.

## Drawable Resources — Generate, Don't Placeholder

- **Shape drawables** (backgrounds, outlines, tracks): Generate the actual XML shape drawable code based on Figma data (color, cornerRadius, stroke, gradient). Output each as a separate file with `📄 drawable/filename.xml` header.
- **Icons/vectors**: Use `figma_fetch.py --export-svg <node-ids>` to export SVG from Figma API, then convert to Android Vector Drawable XML. The simplified JSON includes an `"id"` field on every node — use these IDs for export. Output each as `📄 drawable/ic_name.xml`.
- **Photos/bitmaps**: These cannot be generated — use `@drawable/placeholder` and note what image is needed.
- **Goal**: The generated code should be copy-pasteable and immediately render a close approximation of the design, not a blank screen with placeholders.

## Unmatched Resource Suggestions (when project scan is available)

After all code output, if any colors or strings were hardcoded because they didn't match existing project resources, append a **"Suggested Resources"** block. This helps the user add them to the project in one go:

```
📝 Suggested Resources (unmatched — copy to your project if needed)

// colors.xml
<color name="text_primary">#0F0F0F</color>
<color name="bg_card">#F7F7F7</color>

// strings.xml
<string name="btn_submit">提交</string>
<string name="hint_nickname">请输入昵称</string>
```

Rules for this block:
- Only include when project scan was used and there are unmatched resources
- Name suggestions should follow the project's existing naming convention (observe scan results for patterns like `color_xxx` vs `xxx_color` vs `colorXxx`)
- Group by resource type (colors first, then strings)
- Skip dimensions — they're rarely worth extracting into resources
- This is a **suggestion**, not auto-creation. The user decides whether to add them

## Platform Guidelines

The agent already knows these — this is a reminder to follow them strictly:

- **Android XML**: Material Design 3. ConstraintLayout as default for any non-trivial layout. 8dp grid. Min touch target 48dp. MaterialCardView/MaterialSwitch over legacy.
- **Android Compose**: Material3 composables. Modifier chains. LazyColumn for lists. Scaffold for pages.
- **iOS SwiftUI**: Apple HIG. NavigationStack, List, VStack/HStack/ZStack. Safe areas. System fonts.
- **iOS UIKit**: Apple HIG. AutoLayout (NSLayoutConstraint or StackView). UITableView/UICollectionView for lists. Safe areas.

## Handling Special Visual Properties

- **Gradients**: generate platform-appropriate gradient code (GradientDrawable / Brush.linearGradient / LinearGradient / CAGradientLayer). If gradient is complex, add a comment noting it may need visual tuning.
- **Shadows**: use platform shadow APIs. Note if the design shadow differs from default elevation shadow.
- **Per-corner radius**: use platform-specific per-corner APIs when radii differ.

## Platform-Specific Mapping Details

Read platform-specific mapping details from:
- Android Compose → references/compose-patterns.md
- Android XML → references/xml-patterns.md
- iOS SwiftUI → references/swiftui-patterns.md
- iOS UIKit → references/uikit-patterns.md
