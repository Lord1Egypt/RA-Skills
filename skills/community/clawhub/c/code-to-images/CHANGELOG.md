# 更新日志 / Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。
All notable changes are documented here following [Semantic Versioning](https://semver.org/).

## [v2.3.0] — 2026-10-27

### 新增 / Added

- **按编辑器主题配色（11 族）**：把原来"按扩展名套单一色表"升级为"按语言 key 归族"。49 种语言各自归到 11 个「编辑器亮色族」，全白底（打印省墨），贴近各语言主流编辑器的观感。
  - 新增 `FAMILY_PALETTES`（11 套族色表）与 `LANG_TO_FAMILY`（49 语言 → 族映射）。
  - 新增 `detect_lang_key()`，main 循环改为按语言 key 选族，不再按扩展名。
  - 11 个族：VS Code（Light+）、IntelliJ、Xcode、Visual Studio、Keil μVision、Chrome DevTools、MATLAB、RStudio、TeXstudio、Arduino IDE、微信暖色。
- **WXML / WXSS 微信暖色**：微信小程序 `.wxml` 与 `.wxss` 统一走「微信开发者工具」暖色配色（标签红粉 `#d6336c`、属性名紫 `#7048e8`、字符串蓝 `#1d4ed8`、表达式/数字橙 `#e8590c`、注释绿 `#4e9a06`、正文橙 `#b05000`）。
  - 新增 `wxml`、`wxss` 两个语言规则（继承 HTML/CSS，独立 key）。
  - 分词层新增 `attr`（标签内属性名）、`expr`（`{{...}}` 数据绑定表达式）两个 token，并加跨行 `in_tag` 状态以正确识别标签内属性名。
- **HTML Chrome 配色**：`.html` / `.htm` / `.xhtml` 走 Chrome DevTools 源码视图配色（标签深蓝 `#062e6f`、属性名蓝 `#0b57d0`、字符串红 `#dc362e`、注释绿 `#146c2e`、十六进制色码/数字品红 `#b90063`、正文近黑 `#1c1e21`），颜色取自真实截图采样。
- **HTML 内嵌 CSS/JS 逐行分区**：`.html` 文件中 `<style>` 块按 CSS 规则、`<script>` 块按 JS 规则逐行分词，块外走 HTML 规则，三块共用 Chrome 色表，还原 Chrome 源码视图"整页一套配色"。独立 `.css` / `.js` 文件不受影响。
  - 新增 `_classify_zones()`（按行判 css/js/html）与 `tokenize_full_zoned()`（按行切规则）。

### 改进 / Improved

- 扩展名识别补充：`.wxml → wxml`、`.wxss → wxss`、`.html/.htm/.xhtml → chrome`，`.xml/.svg/.vue` 维持默认 `html` 规则不变。
- 分词器 `tokenize_line` 返回值统一为 4 元组（含 `in_tag`），所有早退 return 点与 `wrap_line_tokens` 内部调用同步更新。

### 兼容性 / Compatibility

- 默认冷色系（C 关键字粉、寄存器橙、字符串绿、注释灰）仍保留，仅在语言被明确归族后按族配色。
- 其它语言（未在 11 族中单独指定的）回退到默认 VS Code 族，不影响出图。

---

## [v2.2.0]

- 49 种语言自动识别 · 忠实缩进 · 自动换行 · 双语文档。
