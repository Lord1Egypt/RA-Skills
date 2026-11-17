# 编辑与后处理

## 参考图能做什么

支持 `--images` 的模型：`gpt-image-2`、banana 系、seedream 全系、`jimeng-t2i`、`qwen-image-2-pro`、`kling-image-o1`、`viduq2-t2i`。

传参考图的用途分三类，说清用途模型才知道怎么用：

| 用途 | 提示词里怎么说 |
|---|---|
| 保留内容 | "保持图中产品的外观、比例和标签不变" |
| 沿用风格 | "参考这张图的配色、笔触和构图密度，画一个新场景" |
| 局部修改 | "只把标题改成 X，其余全部保持不变" |

传多张时**逐张说明角色**，否则模型会混淆：

```bash
dlazy gpt-image-2 --images ./product.png ./style-ref.png \
  --prompt "图 1 是必须保留的产品实拍，图 2 是风格参考。按图 2 的配色和光影，把图 1 的产品放进新场景" \
  --size 2048x2048
```

`gpt-image-2` 最多 5 张。

## 局部修改

**`gpt-image-2` 是唯一能稳定按指令做局部改的**。关键是把"不要动的部分"写清楚——不写模型会顺手重画：

```bash
dlazy gpt-image-2 --images ./slide.png \
  --prompt "把左上角主标题从「注意力机制」改成「自注意力机制」，其余内容、版式、配色、手绘风格全部保持不变" \
  --size 2048x1152 --quality medium
```

带图调用积分翻倍（low 25 / medium 33 / high 60）。改一次比重新生成整张贵，但比重画一遍再对齐风格便宜。

改完**必须肉眼验收再替换原图**——模型可能会顺带改掉你没提的地方。

## 后处理链

这四个工具只吃图片，接在生成之后，比重新生成便宜一个数量级：

| 工具 | 积分 | 什么时候用 |
|---|---|---|
| `imageseg` | 1 | 要透明背景 |
| `vectorize` | 2 | 要 SVG，但图已经是位图 |
| `superres` | 10 | 图对了但不够清晰 |
| `image-replicate` | 6 | 要同一张图的变体 |

### 要透明背景

**不要让模型直接画透明背景**——多数模型不支持 alpha 通道，会画出灰白格子的"假透明"。正确做法是画纯色背景再抠：

```bash
dlazy banana-pro --prompt "产品正面图，纯白背景，无阴影" --imageSize 2K --aspectRatio 1:1
dlazy imageseg --image <上一步的URL或本地路径>
```

纯白或纯绿背景抠得最干净。

### 省钱的放大路线

```bash
# 用便宜模型多出几张
dlazy seedream-5.0-lite --prompt "..." --size 16:9   # 5 积分 × N
# 挑中一张再放大
dlazy superres --image ./picked.png                   # 10 积分
```

总价常低于直接出 4K，而且能先挑再放大，不会为废图付高价。

### 要 SVG

已经有位图就用 `vectorize`（2 积分）。只有从零开始画时才用 `recraft-v4-vector`（11 积分）。

## 组成链条

管道引用可以把上一步的输出直接喂给下一步，不用手工拷 URL：

```bash
dlazy banana-pro --prompt "产品图，纯白背景" --imageSize 2K \
  | dlazy imageseg --image @1
```

`@1` 表示上一步的第 1 个输出。语法详见 `dlazy --help`。

## 验收清单

替换或交付前逐条检查——这些是模型最常出问题的地方：

- 文字有没有错字、变形字、多余的字
- 手指、四肢数量对不对
- 要求保留的元素有没有被改动
- 尺寸和比例是不是你要的（尤其没显式写尺寸时）
- 有没有意外的水印、签名、边框
