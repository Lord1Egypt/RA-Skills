# 🎨 视觉风格指南 (FableForge Visual Style Bible)

本指南是 FableForge 视频生成流水线的官方视觉规范，提供各题材、文化背景下的生图公式与排除规则，确保 AI 生成图像的风格自洽和文化准确度。

---

## 1. 风格决策原则

- **动态适配**：视觉风格必须完全服务于故事。可选国风写意、现代极简、蒸汽朋克、赛博朋克或电影感实拍风格。
- **自洽性**：全片所有图片的色调、光影和元素必须统一，严禁跨时空混搭（除非剧情要求）。
- **文化锚点优先于美感**：当「好看」和「文化准确」冲突时，选文化准确。一张唐代故事里出现的日式庭院，再好看也是错误。

---

## 2. 常见文化与体裁锚点速查表

| 文化/体裁设定 | 场景/建筑关键词 | 元素/服饰关键词 | 常见误导（必须排除） |
|-------------|---------------|---------------|-------------------|
| **现代商务 (Analytical)** | Modern glass office, boardroom, high-rise, minimalist workspace | Business suit, smart casual, laptop, abstract charts | 奇幻元素, 杂乱背景, 古代物品 |
| **极简数据 (Analytical)** | Abstract data visualization, glowing nodes, dark background | Neon lines, geometric shapes, HUD elements | 具体人物, 复杂实景建筑 |
| 唐宋中国 (Narrative)| Dougong brackets, grey tiles, wooden beams, moon gate | Round-collar robe, Hanfu, Mingguang armor | 鸟居, 和服, 榻榻米, 哥特尖拱 |
| 明清中国 (Narrative)| Upturned eaves, red lacquer columns, courtyard houses | Changshan, Qipao, Mandarin collar | 和服, 韩服, 维多利亚裙 |
| 日本和风 (Narrative)| Torii gate, tatami, shoji screens, engawa | Kimono, hakama, geta sandals | 斗拱, 汉服, 旗袍 |
| 中世纪欧洲 (Narrative)| Gothic arches, stone castle, stained glass | Chainmail, surcoat, leather boots | 东方建筑, 丝绸长袍 |
| 赛博朋克 (Narrative)| Neon signs, holographic ads, megastructures | LED-trimmed jacket, visor, cybernetic limbs | 古典建筑, 自然光 |

---

## 3. 图片提示词工程

- **公式**：`[画幅指令] + [文化锚点] + [本幕内容] + [色调光影] + [质量后缀] + [排除清单]`
- **质量后缀**：`hyper-realistic details, cinematic lighting, masterpiece, 8K`
- **排除清单格式**：`No [culture A] elements, no [culture B] elements, no modern objects.`
- **中文文字生成**（架构图/概念图专用）：`A [style] visualization with Chinese labels. Main node: "核心词". Sub-nodes: "关联词1", "关联词2". Professional design, glowing connections.`

---

## 4. 风格圣经模板示例

### 4.1 古代中国唐代水墨风提示词
```
Cinematic vertical shot, 9:16 aspect ratio. Ancient Chinese Tang Dynasty style.
A young monk in grey round-collar robes holds a bronze oil lamp in a temple courtyard
with Dougong bracket architecture and grey tile roofing.
Ink-wash atmosphere, warm golden lamplight against dark shadows, subtle rice-paper texture.
hyper-realistic details, cinematic lighting, 8K.
No Japanese elements, no Western elements, no modern objects.
```
