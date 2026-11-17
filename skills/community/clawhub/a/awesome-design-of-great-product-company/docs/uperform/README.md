# UPerform 优普丰 设计系统

[DESIGN.md](https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/uperform/DESIGN.md) 提取自 UPerform（优普丰）官方视觉设计规范。适用于敏捷/Scrum 培训材料、企业咨询演示等场景。

## 文件说明

| 文件 | 说明 |
|------|------|
| `DESIGN.md` | 完整设计系统文档（9 个章节） |
| `preview.html` | 交互式设计令牌目录（亮色主题） |
| `preview-dark.html` | 交互式设计令牌目录（暗色主题） |

使用 [DESIGN.md](https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/uperform/DESIGN.md) 作为 AI 代理（Claude、Cursor 等）的参考，生成符合 UPerform 品牌视觉的内容。

## 预览

基于 DESIGN.md 构建的示例页面，展示实际的颜色、字体、按钮、卡片、间距和深度效果。

### 暗色主题
![UPerform Design System — Dark Mode](https://pub-2e4ecbcbc9b24e7b93f1a6ab5b2bc71f.r2.dev/designs/uperform/preview-dark-screenshot.png)

### 亮色主题
![UPerform Design System — Light Mode](https://pub-2e4ecbcbc9b24e7b93f1a6ab5b2bc71f.r2.dev/designs/uperform/preview-screenshot.png)

## 品牌特点 — 4 层色彩体系

按国际设计标准（Material Design / IBM Carbon / Figma）采用 **PRIMARY / NEUTRALS / SECONDARY / ACCENT** 4 层结构，各司其职：

| 层级 | 色系 | 代表色 | 视觉量 | 职责 |
|------|------|--------|--------|------|
| **PRIMARY** | 蓝色 (5色) | 海洋蓝 `#1E4976` | 60–70% | 品牌识别 |
| **NEUTRALS** | 灰色 (5色) | 碳黑/石板/钢铁/银/雾白 | 功能性 | 文字/边/底 |
| **SECONDARY** | 金色 (2色,**必须渐变**) | 尊贵金 `#D4AF37` + 香槟金 `#F2D492` | 装饰性 / 强调性 | 高级感 + 强调点缀（≤ 3 处,橙色的优先替代）|
| **ACCENT** | 橙色 (2色) | 活力橙 `#FF6B35` | 行动性(极度克制) | CTA 按钮（≤ 1 处,尽可能不采用）|

**4 条使用铁律**：
- 🔴 橙色是"放大镜"，全场 ≤ 1 处（尽可能不采用,默认用金色替代）
- 🟡 金色永远搭配深色，不放冰川蓝上；金色已承担强调与点缀职责
- ⚪ 文字层级只走灰阶，蓝/橙/金不参与正文
- 🆕 🟨 **金色一律使用渐变，禁止纯色** —— 尊贵金/香槟金是金属色，纯色 = 廉价 = 油漆感。所有金色（背景/底色/按钮/描边/文字）100% 渐变；金字用 `background-clip: text` 渐变技术，绝不写 `color: #D4AF37`

**🆕 标志性奢华组合：海洋蓝背景 + 尊贵金字**

深邃的海洋蓝铺底，金属质感的金色文字浮于其上，营造"深海藏金"的视觉张力——这是 UPerform 的标志性奢华组合，用于高端封面、Hero 标题、奖项大数字、VIP 标识、限量版标签。

| 变体 | 背景 | 文字 | 适用场景 |
|------|------|------|---------|
| 海洋蓝 + 尊贵金字 | 海洋蓝 `#1E4976` 纯色 | 尊贵金渐变文字（`#E8C547`→`#F2D492`→`#D4AF37`，`background-clip: text`） | 高端封面、Hero 标题、奖项大数字 |
| 深海蓝 + 香槟金字 | 深海蓝渐变 `#0A2540`→`#1E4976` | 香槟金渐变文字（`#FFF4D6`→`#F2D492`→`#D9BC6E`） | 章节封面、引用金句、长标题 |

**典型场景组合**：
- 商务场景：深海蓝 + 尊贵金渐变 + 金色 CTA(优先,渐变) + 金字渐变
- 数字产品：雾白 + 香槟金渐变 + 海洋蓝底白字按钮
- 🆕 标志性奢华：海洋蓝 + 金字渐变（深海藏金）
- 营销物料：天空蓝 + 尊贵金渐变 + 金字渐变
- 风格：深邃、尊贵、活力，适合企业培训、咨询与高端场景