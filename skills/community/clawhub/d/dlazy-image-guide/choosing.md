# 按场景选型

每个场景给首选和备选，并说明为什么。命令都是可直接执行的完整形式。

## 图里要有准确的中文文字

海报、封面、幻灯片、带标注的示意图。这是最考验模型的场景，多数模型会把中文画成似是而非的字形。

**首选 `gpt-image-2`** —— 中文字形准确率最高，且能听懂"标题写「注意力机制」"这类指令。

```bash
dlazy gpt-image-2 \
  --prompt "16:9 演示幻灯片，主标题「季度增长报告」，副标题「2026 Q3」，左侧三个要点：营收、用户、留存。极简商务风，白底，蓝色主色，中文字形必须准确" \
  --size 2048x1152 --quality medium
```

**备选 `qwen-image-2-pro`**（20 积分）—— 中文同样扎实，排版风格更偏国内审美。提示词上限 1300，比 gpt-image-2 紧。

**不要用** seedream 系和 mj-imagine 做大段中文——前者提示词上限 500 不够描述文字内容，后者中文字形不可靠。

## 产品图 / 电商主图

**首选 `banana-pro`**（18 积分，2K）—— 质感和光影最好，适合需要"看起来像摄影棚拍的"场景。

```bash
dlazy banana-pro \
  --prompt "白色陶瓷马克杯产品图，纯白背景，柔和顶光，轻微反射，居中构图，电商主图风格" \
  --imageSize 2K --aspectRatio 1:1
```

要 4K 精修图时加 `--imageSize 4K`（30 积分）。

**备选 `seedream-5.0-pro`**（7 积分）—— 便宜一半以上，质量够用于详情页次图。

**配套**：出图后用 `imageseg`（1 积分）抠掉背景，比让模型直接画透明背景可靠得多。

## 矢量图 / Logo / 图标

**只有 recraft 系能出真正的矢量**，其余模型都是位图。

```bash
dlazy recraft-v4-vector --prompt "极简咖啡杯 logo，单色，几何构成，粗线条" --aspect_ratio 1:1
```

- `recraft-v4-vector`（11）：日常够用
- `recraft-v4-pro-vector`（22）：细节更干净，商用交付选这个
- `recraft-v3-svg`（11）：老版本，支持 `--style` 指定风格预设

**已有位图想转矢量**：用 `vectorize`（2 积分），不要重新生成。

## 写实人像 / 摄影感

**首选 `seedream-5.0-pro`**（7 积分）—— 人脸结构稳定，皮肤质感自然，性价比高。

**备选 `kling-image-o1`**（11 积分）—— 提示词上限 2500，是全部模型里最宽松的，适合需要长段描述精确控制人物特征、服装、场景的情况。

```bash
dlazy kling-image-o1 --prompt "<长达 2000 字的详细人物设定>" --aspect_ratio 3:4 --clarity 2k
```

## 艺术性 / 风格化

**`mj-imagine`**（5 积分）—— 构图和氛围最有想法，适合概念图、插画、封面。代价是可控性差，同样的提示词每次差异大，不适合需要精确复现的场景。

## 批量铺量 / 极致性价比

**`seedream-5.0-lite`** 或 **`mj-imagine`**，都是 5 积分——生成 100 张只要 500 积分。

批量时务必用 `--no-wait` 提交、再统一轮询：

```bash
for p in "prompt1" "prompt2" "prompt3"; do
  dlazy seedream-5.0-lite --prompt "$p" --size 16:9 --no-wait
done
# 拿到各 generateId 后统一 dlazy status <id> --wait
```

## 4K 大图

| 方案 | 积分 | 说明 |
|---|---|---|
| `seedream-5.0 --resolution 4k` | 8 | **最便宜的 4K** |
| `banana-pro --imageSize 4K` | 30 | 质感最好 |
| `gpt-image-2 --size 3840x2160` | 37 | 需要 4K + 准确中文时的唯一选择 |
| 先出 2K 再 `superres` | 5 + 10 = 15 | 中间路线，且能挑好图再放大 |

最后一种常常最划算：先用便宜模型出几张 2K 挑选，只把选中的那张放大。

## 改一张已有的图

**`gpt-image-2 --images`** 是唯一能稳定按指令做局部修改的：

```bash
dlazy gpt-image-2 --images ./slide.png \
  --prompt "把标题从「注意力机制」改成「自注意力机制」，其余版式、配色、风格全部保持不变" \
  --size 2048x1152
```

带参考图时积分翻倍（medium 33）。详见 `editing.md`。

## 一句话速查

| 需求 | 用 |
|---|---|
| 中文文字准确 | `gpt-image-2` |
| 产品质感 | `banana-pro` |
| 矢量 | `recraft-v4-vector` |
| 人像 | `seedream-5.0-pro` |
| 艺术感 | `mj-imagine` |
| 最便宜 | `seedream-5.0-lite` / `mj-imagine`（5） |
| 最便宜的 4K | `seedream-5.0 --resolution 4k`（8） |
| 改图 | `gpt-image-2 --images` |
| 长提示词（>2000） | `kling-image-o1`（2500） |
