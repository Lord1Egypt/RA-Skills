---
name: dlazy-ecommerce-main-image
version: 1.0.2
description: 电商爆款主图生成与编辑。上传已批准的商品图，生成搜索列表里能被认出、商品事实准确、卖点有画面证据、符合渠道规则的主图候选，并按单变量原则产出 A/B 测试组。覆盖白底基线图、可视差异图、内容电商场景图、配色 SKU 组、单变量背景测试五种场景，适用于淘宝天猫京东拼多多抖音小红书 Amazon TikTok Shop Shopify 的主图与首图。当用户需要「做主图」「爆款主图」「白底图」「主图测款」「测图」「A/B 测试主图」「一个 SKU 铺多个配色」时使用本技能。转化受价格、评价、库存与流量共同影响，图片不单独构成爆款保证。
metadata: {"clawdbot":{"emoji":"🛍️","requires":{"bins":["npm","npx"],"env.optional":["DLAZY_API_KEY"]},"install":"npm install -g @dlazy/cli@1.2.3","installAlternative":"npx @dlazy/cli@1.2.3","homepage":"https://dlazy.com","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"When invoking this skill, run `dlazy banana-pro -h` to confirm the current flags before building a command."}}
---

# bestseller-main-image — 电商爆款主图生成与编辑

主图的作用是**在列表页把点击换回来**，不是把商品拍好看。

「爆款」不可控，但它拆开之后每一项都可控：列表缩略图里能不能认出这是什么、商品事实有没有被改掉、卖点有没有画面证据、渠道规则允不允许、这一版和上一版是不是只差一个变量。这五件事做到了，剩下的交给数据。

---

## 1、能力边界

| 能做 | 说明 |
| --- | --- |
| 白底基线图 | 纯白背景、商品完整、占比可控、自然接地阴影 |
| 可视差异图 | 同一商品的两个真实状态并置（折叠/展开、正面/背面） |
| 内容电商场景图 | 商品放进真实使用环境，留标题安全区 |
| 配色 SKU 组 | 同款多配色，除颜色外全部一致 |
| 单变量测试组 | 两版候选只差一个变量，可解释归因 |

**不做**：不改商品的外形、结构、配件数量、颜色和 Logo；不生成原图没有的部件或赠品；不伪造功效、容量、倍数、续航等无法从画面证明的数字；不生成价格、低价角标、平台 Logo、活动文案；不用特效制造「看起来像但实际没有」的卖点。

主图证明不了的卖点，放详情页或文案，不要在主图上编。

---

## 2、主图证据地图

生成前先把这张表填掉。填不出来的项，说明还不能开始生成。

| 项 | 要确定的事 |
| --- | --- |
| SKU | 具体到颜色和规格，不是「这款包」 |
| 核心差异 | 和同类竞品最不一样的那一点 |
| 可视证据 | 这个差异靠画面里的什么能被看到 |
| 商品占比 | 占画面多少（白底基线一般 75%–80%） |
| 背景 | 纯白 / 浅灰 / 真实场景 |
| 道具 | 有没有，用来做什么（尺度参照？使用联想？） |
| 标题安全区 | 平台会在哪压文字，那块不能放关键结构 |
| 平台规则 | 目标平台当日的主图规范 |
| 禁止主张 | 这个类目不能说的话 |
| 唯一测试变量 | 这一版相对基线只改了什么 |

最后一行最容易被跳过。跳过了，测出来的数据就没法归因。

---

## 3、输入素材规则

- **必须传已批准的商品实拍图**（`--images`），不要让模型凭文字想象商品。文字描述出来的商品，结构一定和真货对不上。
- 传多张时在提示词里逐张说明角色（「图 1 是折叠状态，图 2 是展开状态」），否则模型会把它们混成一个。
- `banana-pro` 最多接 14 张参考图。
- 商品图背景越干净、光线越均匀，生成结果越稳。

---

## 4、五个主图场景

命令可直接执行。所有场景都基于「传入已批准商品图 + 明确写出不许动什么」。

### 4.1 搜索白底基线

先有基线，才谈得上测试。基线的唯一目标是**在列表里被正确识别**。

```bash
dlazy banana-pro \
  --images ./approved-toolbox.png \
  --prompt '生成 1:1 电商白底基线图：工具箱箱体、卡扣、提手、分隔、颜色、Logo 和标配数量保持不变，三分之二角度，商品完整不裁切，占画面约 78%，自然接触阴影；不生成工具、文字、低价角标、平台 Logo 或额外隔层' \
  --aspectRatio 1:1 --imageSize 2K
```

### 4.2 可视差异图

把「和别人不一样」变成一眼能看见的画面，而不是写在文案里。

```bash
dlazy banana-pro \
  --images ./approved-lamp-folded.png ./approved-lamp-open.png \
  --prompt '制作折叠阅读灯差异主图：只展示同一产品折叠与展开两个已批准状态，图 1 为折叠、图 2 为展开，结构、转轴、底座、颜色和 Logo 完全一致，浅灰背景，两个状态各出现一次；不生成角度数字、护眼功效文案、文字、赠品或第三个状态' \
  --aspectRatio 1:1 --imageSize 2K
```

### 4.3 内容电商场景图

抖音、小红书这类内容场，商品需要出现在真实使用环境里。

```bash
dlazy banana-pro \
  --images ./approved-spice-rack.png \
  --prompt '生成竖版内容电商主图：保持调料架层数、尺寸、颜色、Logo 和标配挂钩不变，放在家庭厨房台面正常摆放，放入少量无品牌调料瓶作为尺度参照，顶部留出标题安全区；不生成容量数字、收纳倍数、价格、人物或额外配件' \
  --aspectRatio 3:4 --imageSize 2K
```

> `banana-pro` 的比例只有 `auto / 1:1 / 4:3 / 3:4 / 16:9 / 9:16 / 21:9`，**没有 4:5**。内容电商常用的 4:5 用 `3:4` 代替，或先出 `1:1` 再按平台要求裁切。

### 4.4 配色 SKU 组

同款多配色。除了颜色，其他一切都必须一致——不然用户会以为是不同的商品。

`banana-pro` 一次只出一张，多配色靠循环，每次只改颜色词：

```bash
for c in 雾蓝 砂白 陶土红; do
  dlazy banana-pro \
    --images ./approved-mug.png \
    --prompt "为同款马克杯生成${c}配色 SKU 主图：杯型、把手、Logo、相机角度、白背景、商品占比和阴影与参考图完全一致，画面只有一个杯子；不生成文字、饮品、道具或其他颜色" \
    --aspectRatio 1:1 --imageSize 2K
done
```

### 4.5 单变量背景测试

A/B 的关键是**只差一个变量**。下面两条命令除了背景描述，其余逐字相同。

```bash
dlazy banana-pro --images ./approved-earbuds.png \
  --prompt '无线耳机主图，背景纯白。耳机与充电盒结构、颜色、Logo、角度、占比和阴影保持不变，不改变指示灯状态；不生成文字、续航数字、人物或配件' \
  --aspectRatio 1:1 --imageSize 2K

dlazy banana-pro --images ./approved-earbuds.png \
  --prompt '无线耳机主图，背景浅蓝渐变。耳机与充电盒结构、颜色、Logo、角度、占比和阴影保持不变，不改变指示灯状态；不生成文字、续航数字、人物或配件' \
  --aspectRatio 1:1 --imageSize 2K
```

---

## 5、提示词结构

主图提示词按这个顺序写，缺哪项模型就自己发挥哪项：

```
商品与必须保持不变的部分 → 角度与构图 → 占画面比例 → 背景 → 光线与阴影 → 安全区 → 禁止项
```

**禁止项要具体**。「不要文字」比「保持简洁」有效得多；「不生成价格、角标、平台 Logo」又比「不要文字」更管用。

`banana-pro` 的提示词上限是 2000 字符，够用。真写不下时优先砍形容词——「精美的」「高质量的」这类词对模型几乎没有作用，只是在占配额。

---

## 6、单变量 A/B 测试

| 规则 | 说明 |
| --- | --- |
| 一次一个变量 | 背景、角度、占比、道具，每轮只动一个 |
| 其余逐字相同 | 提示词其他部分不要顺手润色，改了就不是单变量了 |
| 控制外部因素 | 同价格、同时段、同流量位，否则数据归因不到图 |
| 看真实指标 | 点击、加购、转化，不是「哪张好看」 |
| 基线要留着 | 每轮和基线比，不是和上一轮比 |

主图能影响的只是点击环节。加购和转化还受价格、评价、库存、详情页影响——测图的时候别把这些也算到图头上。

---

## 7、发布前核验

- [ ] 缩略图尺寸下，商品类别、数量、核心差异还能不能认出
- [ ] 商品结构、配件数量、颜色、Logo 与实物一致
- [ ] 画面里没有无法证明的功效、数字、赠品
- [ ] 没有价格、角标、平台 Logo、活动文案
- [ ] 标题安全区没压住关键结构
- [ ] 符合目标平台**当日**的主图规范（规则会变，按当天的查）

---

## 8、dLazy 工具调用

本技能使用 dLazy 的 **`banana-pro`**（即 Nano Banana Pro）。选它的原因是产品质感和光影最接近实拍棚拍，而电商主图的成败很大程度上取决于「看起来像不像真的拍出来的」。

积分：`--imageSize 1K` 和 `2K` 都是 18，`4K` 是 30。主图用 2K 足够，4K 留给需要放大精修的详情图。

### Authentication

All requests require a dLazy API key. The recommended way to authenticate is:

```bash
dlazy login
```

This runs a device-code flow (also works in remote shells) and **automatically saves your API key** to the local CLI config — no manual copy/paste required.

#### Alternative: Set the Key Manually

```bash
dlazy auth set YOUR_API_KEY
```

The CLI saves the key in your user config directory (`~/.dlazy/config.json` on macOS/Linux, `%USERPROFILE%\.dlazy\config.json` on Windows), with file permissions restricted to your OS user account. You can also supply the key per-invocation via the `DLAZY_API_KEY` environment variable.

#### Getting Your API Key Manually

1. Sign in or create an account at [dlazy.com](https://dlazy.com)
2. Go to [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. Copy the key shown in the API Key section

Each key is scoped to your dLazy organization and can be **rotated or revoked at any time** from the same dashboard.

### About & Provenance

- **CLI source code**: [github.com/dlazy-ai/cli](https://github.com/dlazy-ai/cli)
- **Maintainer**: dlazyai
- **npm package**: `@dlazy/cli` (pinned to `1.2.3` in this skill's install spec)
- **Homepage**: [dlazy.com](https://dlazy.com)

```bash
npx @dlazy/cli@1.2.3 <command>
```

### How It Works

This skill is a thin client over the dLazy hosted API. When you invoke it:

- Prompts and parameters you provide are sent to the dLazy API endpoint (`api.dlazy.com`) for inference.
- Any local file paths you pass to image fields are uploaded to dLazy's media storage (`files.dlazy.com`) so the model can read them — the same flow as any cloud-based generation API.
- Generated output URLs returned by the API are hosted on `files.dlazy.com`.

### Usage

```bash
dlazy banana-pro -h

Options:
  --prompt [prompt]              Prompt
  --images [images...]           Images [image: url or local path] (max 14)
  --aspectRatio [aspectRatio]    Aspect Ratio [default: auto] (choices: "auto",
                                 "1:1", "4:3", "3:4", "16:9", "9:16", "21:9")
  --imageSize [imageSize]        Image Size [default: 1K] (choices: "1K", "2K", "4K")
  --dry-run                      Print payload + cost estimate without calling API
  --no-wait                      Return generateId immediately for async tasks
  --timeout <seconds>            Max seconds to wait for async completion (default: "1800")
  -h, --help                     display help for command
```

默认 `--imageSize 1K` 对电商主图偏低，**主图务必显式写 `2K`**。

### Output Format

```json
{
  "ok": true,
  "result": {
    "tool": "banana-pro",
    "outputs": [
      { "type": "image", "url": "https://files.dlazy.com/result.png" }
    ]
  }
}
```

批量铺 SKU 时用 `--no-wait` 先全部提交，再用 `dlazy status <generateId> --wait` 统一取回，比串行等待快得多。

### 先估价不真跑

```bash
dlazy banana-pro --images ./approved-mug.png --prompt '...' --aspectRatio 1:1 --imageSize 2K --dry-run
```

打印将要发送的参数和积分估算，不产图、不扣费。铺整组 SKU 之前先跑一次，一个参数写错乘以 20 个 SKU 就是 20 次白花。

### Error Handling

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `unauthorized` | key 缺失或失效 | `dlazy login` 或 `dlazy auth set` |
| `insufficient_balance` | 积分不足 | 去 dashboard 充值，不要重试 |
| `invalid choice: '4:5'` | 该比例不支持 | 用 `3:4`，或出 `1:1` 后裁切 |
| 商品结构被改了 | 提示词没写「保持不变」 | 把不许动的部分逐项列出来重生成 |
| 出图很糊 | 用了默认 `1K` | 显式 `--imageSize 2K` |

---

## 9、执行流程

1. 收齐已批准的商品实拍图，确认可以商用
2. 填完第 2 节的证据地图，确定唯一测试变量
3. 出白底基线图，过 SKU 核验和平台规则
4. 按需要出场景图 / 差异图 / 配色组
5. 每轮只改一个变量，产出 A/B 候选
6. 按第 7 节清单核验后上架
7. 用真实点击、加购、转化数据迭代

---

## 10、常见问题

**生成的商品和实物对不上？**
多半是没传 `--images`，或提示词里没写「保持不变」。模型不会主动保守，必须逐项点名。

**配色组里几张图的杯型不一样？**
循环时提示词有别的地方也变了。除颜色词外必须逐字相同。

**能不能直接生成带价格和促销角标的主图？**
不建议。价格和活动会变，图会过期；多数平台也禁止主图出现价格与角标。促销信息交给平台的活动组件。

**4:5 怎么办？**
`banana-pro` 不支持。用 `3:4`，或出 `1:1` 再按平台尺寸裁切。

**测出来数据没差异？**
先确认变量是不是真的只有一个，以及样本量够不够。图之外的价格、流量位、时段没控住的话，测的就不是图。
