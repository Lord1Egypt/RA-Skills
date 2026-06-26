# 工程扫描使用说明（Project Scan）

> 由 SKILL.md 步骤 2.5 引用。在已有扫描报告时阅读本文。

## 运行扫描

在技能目录的 `scripts/` 下执行：

```bash
cd scripts
node src/project-scan.js /path/to/project --json --output scan-report.json
```

当前实现：**Android** 会解析 `res/values/*.xml` 中的颜色、字符串、尺寸，并列出 `drawable` 资源名；**iOS** 为轻量占位（见报告 `notes`）。报告含 `indices`，便于按 hex、文案做快速匹配。

## 在代码生成阶段使用扫描结果（步骤 3）

**颜色匹配：**

1. 从 Figma 节点取 hex → 规范化为 `#RRGGBB`
2. 在 `indices.colors` 中查找 → 命中则使用工程引用（Android：`@color/名称`，iOS：按项目习惯，如 `UIColor` 扩展或 Asset）
3. iOS 动态色：Figma 多为浅色稿。若扫描到 `light:#2965FF dark:#4D88FF`，与 Figma 的 `#2965FF` 对齐时按浅色值匹配
4. 未命中 → 可写死 hex，并注释 `// TODO: 无匹配工程色`

**字符串匹配：**

1. 从 Figma TEXT 节点取文案
2. 在 `indices.strings` 中查找 → 命中则使用多语言引用（Android：`@string/key`，iOS：依项目本地化格式）
3. 未命中 → 可写死文案，并注释 `// TODO: 未在 i18n 中`

**文本样式匹配：**

1. 从 Figma TEXT 取 fontSize + fontWeight
2. 构造查找键：`"{fontSize}sp_{weight}"`（如 `"16sp_bold"`）
3. 在 `indices.text_styles` 中查找 → 命中则使用样式引用（Android：`style="@style/..."`）
4. 未命中 → 使用行内属性（`android:textSize`、`android:textStyle` 等）

**fontWeight 映射（Figma 数值 → Android 关键字）：**

- 400 及以下 → `normal`
- 500 → `medium`
- 600 → `semibold`
- 700 及以上 → `bold`

**图片匹配：**

1. 图标类元素 → 按语义名在扫描结果中找 drawable（如 Figma `icon/back` → `icon_back`）
2. 命中 → `UIImage(named:)` / `@drawable/name`
3. 未命中 → 从 Figma API 导出

**基类检测（iOS）：**

- 扫描若发现 `BaseViewController`、`BaseTableViewCell` 等 → 优先作为父类，而不是裸用 UIKit 类

## 无扫描报告时的降级

若无项目扫描报告，则按步骤 3 中「写死值 + 资源匹配」的约定生成代码。
