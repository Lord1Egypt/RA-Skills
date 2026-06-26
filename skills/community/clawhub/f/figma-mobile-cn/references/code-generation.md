# 代码生成规则

> 由 SKILL.md 步骤 3 引用。生成代码前必读。

## 输出规则（必须遵守）

- **颜色**：写死前先在 `res/values/colors.xml`（及若存在的 `colors_*.xml`）中按 hex 查找。找到则用资源引用（如 `@color/primary`）。找不到则直接写 hex（`android:textColor="#0F0F0F"` / `Color(0xFF0F0F0F)`）。
- **字符串**：写死前先在 `res/values/strings.xml` 按文案查找。找到则用 `@string/...`。找不到则直接写字符串（如 `android:text="通知设置"`）。
- **尺寸**：直接写数值（如 `android:textSize="17sp"`）。尺寸资源一般不必强行匹配。
- **列表**：输出主布局 + 独立 item 布局文件。**不要**生成 Adapter / ViewHolder。
- **资源匹配优先级**：若存在完全一致的 `@color/`、`@string/`，优先引用。其余为便于预览可写死。**不要**新建资源定义——只引用已有项。

## Drawable — 生成真实资源，避免占位

- **Shape drawable**（背景、描边、轨道）：根据 Figma（颜色、圆角、描边、渐变）生成完整 XML。每个文件单独输出，带 `📄 drawable/文件名.xml` 标题。
- **图标/矢量**：在 `scripts/` 下执行 `node src/figma-fetch.js "<url>" --export-svg [--nodes "id1,id2"]`（或 `npm run figma-fetch --`）从 Figma API 导出 SVG，再转为 Android Vector Drawable。简化 JSON 中每个节点有 `"id"`，供 `--nodes` 使用。导出文件带 `📄 drawable/ic_名称.xml`。
- **照片/位图**：无法凭空生成 → 使用 `@drawable/placeholder` 并说明需补素材。
- **目标**：代码可复制粘贴即可大致还原设计，而不是满屏占位。

## 未匹配资源的建议块（在已有工程扫描时）

全部代码输出后，若有因未匹配而写死的颜色/字符串，**追加**「建议资源」块，便于用户一次性补进工程：

```
📝 建议资源（未匹配 — 可按需复制到工程）

// colors.xml
<color name="text_primary">#0F0F0F</color>
<color name="bg_card">#F7F7F7</color>

// strings.xml
<string name="btn_submit">提交</string>
<string name="hint_nickname">请输入昵称</string>
```

规则：

- 仅在使用了工程扫描且仍有未匹配项时附带
- 命名建议遵循工程现有风格（从扫描结果观察 `color_xxx` / `xxx_color` 等）
- 按类型分组（先颜色后字符串）
- 尺寸一般不必单独抽资源
- 本块为**建议**，是否落库由用户决定

## 平台约定（提醒）

模型已具备平台知识，此处仅作硬性对齐：

- **Android XML**：Material 3；非平凡布局默认 **ConstraintLayout**；8dp 网格；最小触控约 48dp；优先 `MaterialCardView` / `MaterialSwitch` 等。
- **Android Compose**：Material3；`Modifier` 链；列表用 `LazyColumn`；页面骨架用 `Scaffold`。
- **iOS SwiftUI**：遵循 HIG；`NavigationStack`、`List`、`VStack`/`HStack`/`ZStack`；安全区；系统字体。
- **iOS UIKit**：HIG；Auto Layout（约束或 StackView）；列表用 `UITableView`/`UICollectionView`；安全区。

## 特殊视觉效果

- **渐变**：按平台生成对应渐变代码（GradientDrawable / `Brush.linearGradient` / `LinearGradient` / `CAGradientLayer`）。若很复杂，注释说明可能需微调。
- **阴影**：使用平台阴影 API；若设计阴影与默认 elevation 差异大，注明。
- **分角圆角**：四角不一致时使用各平台分角 API。

## 平台细映射表

请结合对应参考文档：

- Android Compose → `references/platform-compose.md`
- Android XML → `references/platform-xml.md`
- iOS SwiftUI → `references/platform-swiftui.md`
- iOS UIKit → `references/platform-uikit.md`
