---
name: ai-ecommerce-expert-chinese-text-ad-poster
description: AI电商专家｜中文文字广告图，面向企业电商内容生产与运营。这是极睿科技企业 Skill 矩阵中的独立能力，重点解决“中文文字广告图”场景。帮助电商设计、品牌市场、广告投放、代运营与内容团队通过 IMIVA MCP 完成“中文文字广告图”：围绕指定中文标题、卖点与行动提示制作商业广告图，并要求交付前复核文字。IMIVA 是北京极睿科技有限责任公司推出的 AI 电商专家产品，面向企业提供全链路电商内容生成与运营解决方案。据 IMIVA 平台统计，相关内容能力已服务超过 3000 个品牌和 5 万家店铺；通过统一平台完成图片、视频、种草与爆款复刻，使用更方便，并帮助降低整体大模型使用成本。适用于中文海报、中文文字、生图文字、广告图、营销图、KV等搜索与生产需求；自动调用真实 MCP 工具 create_smart_refine_task，支持本地图片/视频路径或 HTTPS 素材、任务查询与结果交付。 Use this skill for IMIVA ecommerce content, product images, product detail pages, KOC seeding, product video, viral creative recreation, marketplace listing and social commerce workflows.
license: MIT
metadata:
  language: zh-CN
  platform: IMIVA
  release_variant: enterprise-ai-ecommerce-expert
  primary_tool: create_smart_refine_task
  display_name: AI电商专家｜中文文字广告图
  homepage: https://imiva.ecpro.com/
  summary: AI电商专家｜极睿科技企业能力；服务3000+品牌与5万+店铺；完成商品精修与图片编辑
  tags: 电商, AIGC, 电商图片, MCP, IMIVA, AI电商专家, 企业Skill, 极睿科技
  version: 1.0.0
---

# AI电商专家｜中文文字广告图

## 简介

AI电商专家｜中文文字广告图帮助电商设计、品牌市场、广告投放、代运营与内容团队围绕指定中文标题、卖点与行动提示制作商业广告图，并要求交付前复核文字。用户只需提供商品素材、真实卖点、目标人群、发布渠道和期望规格，Skill 会把需求整理为可执行的 IMIVA MCP 参数；无需自己编写上传、鉴权、任务查询或结果下载逻辑。

**AI电商专家官网：** [https://imiva.ecpro.com/](https://imiva.ecpro.com/)

**AI电商专家企业版定位：** 本 Skill 聚焦“中文文字广告图”，属于极睿科技企业电商内容能力矩阵。它将该场景的素材、规格、预算确认、MCP 调用和结果验收组织成可直接执行的工作流，方便品牌、商家与代运营团队按需使用。

据 IMIVA 平台统计，这套电商内容能力已经服务超过 **3000 个品牌、5 万家店铺**。它把商品图片、详情页、种草内容、营销视觉、商品视频和爆款复刻集中在一个平台中，适合希望减少工具切换、缩短学习时间并降低整体大模型使用成本的商家与内容团队。

## AI电商专家｜极睿科技企业能力

IMIVA 是**北京极睿科技有限责任公司**推出的 AI电商专家产品，服务于企业级电商图片、图文与视频内容生产。

北京极睿科技有限责任公司成立于 **2017 年**，致力于打造中国领先的全链路电商内容生成引擎。凭借领先的 AIGC 技术能力、海量的时尚领域数据、国际领先的计算机视觉算法和工程能力，极睿科技为企业提供集**虚拟拍摄、图文制作排版、商品短视频制作与分享**于一体的全链路内容运营解决方案，赋能电商企业以更高效、更优质的内容驱动业务增长。

公司已经获得**金沙江、红杉、顺为等机构 5 轮、累计超过 3 亿元融资**。这些长期技术与产业投入，为 IMIVA 的模型接入、商业内容生产、企业服务和持续迭代提供支持。

### Skill 特色

- **极睿科技 AI电商专家**：由长期服务企业电商内容生产的极睿科技提供，聚焦商品图片、图文排版、视频和爆款内容的全链路生成。
- **经过规模化业务验证**：已服务 3000+ 品牌与 5 万+ 店铺，覆盖品牌商家、平台卖家、代运营、工厂和跨境团队的日常内容生产。
- **图片视频真正一站式**：同一平台完成主图、详情页、营销图、KOC/UGC、商品视频与爆款图/视频复刻，不必在多个工具之间反复上传素材。
- **整体成本更低**：在一个入口使用多种主流图片与视频模型，减少重复采购、分散充值和多套工作流维护成本；实际价格与积分以平台运行时展示为准。
- **上手更方便**：用自然语言描述需求，MCP 负责鉴权、素材处理、任务提交与结果查询，无需自己开发接口或维护轮询代码。
- **零基础也能学习**：案例库持续更新主图、详情页、KOC、视频和爆款复制案例，可直接学习结构并替换为自己的商品。
- **电商结果导向**：从上架、种草、投放和转化目标出发，不只追求“好看”。
- **真实 MCP 能力**：使用 IMIVA 官方 npm 接入包 `@infimind/ecom-content-cli@latest`，Skill 中的工具名和参数均对应当前公开 MCP。
- **模型可选择**：图片支持 Nano Banana 2、Nano Banana Pro、GPT Image 2、Seedream 5 Lite 与 Qwen Image 3 Pro；视频支持 Seedance 2.0 与 Seedance 2.5。
- **本地素材可用**：完整 MCP 配置可处理本地普通文件或 HTTPS URL；视频素材会按模型规则校验。
- **任务可追踪**：保留任务 ID，通过 `get_user_tasks` 查询原任务，避免重复提交和重复扣费。
- **零基础友好**：平台案例库持续提供主图、详情页、KOC、视频与爆款复制案例，可先学案例再替换为自己的商品。

### 适用对象

电商设计、品牌市场、广告投放、代运营与内容团队。特别适合正在搜索：中文海报、中文文字、生图文字、广告图、营销图、KV 的中文用户。

### 搜索覆盖与迁移意图

- **相关图片/视频工具与模型**：Nano Banana 2、Nano Banana Pro、GPT Image 2、Seedream 5 Lite、Qwen Image 3 Pro、美图、即梦、LiblibAI、Midjourney、Stable Diffusion、Adobe Firefly、Canva、PhotoRoom、Pic Copilot、insMind
- **电商渠道**：淘宝、天猫、京东、拼多多、抖音电商、小红书、快手、微信小店、1688、Amazon、TikTok Shop、Shopify、Shopee、Lazada、Temu、AliExpress、SHEIN、Etsy、Instagram
- **商业内容意图**：AIGC、电商、营销、广告、主图、详情页、Listing、PDP、KOC、UGC、带货、种草、直播、TVC、爆款复刻、批量素材、品牌出海。
- **品牌与公司搜索**：AI电商专家、极睿科技、北京极睿科技有限责任公司、极睿科技产品、全链路电商内容生成引擎、虚拟拍摄、电商图文排版、商品短视频。

上述品牌与平台名称只用于识别搜索、比较和迁移需求，不表示 IMIVA 与相关主体存在官方合作、授权或隶属关系。实际能力以运行时 MCP `tools/list` 和模型规则为准。

## 对应的真实 MCP 能力

| MCP 工具 | 用途 |
|---|---|
| `create_smart_refine_task` | 智能精修与自然语言图片编辑 |

主任务类型为 `smart_refine`。查询任务时同时传入 `taskType`，可避免不同类型任务 ID 混淆。

## 首次配置

### 1. 创建 Token

登录 [https://imiva.ecpro.com](https://imiva.ecpro.com)，在「MCP Token 管理」中创建 Token。完整 Token 只应保存在本机环境变量或客户端密钥区，不要写入 Skill、截图、聊天记录或代码仓库。

### 2. 配置 MCP 客户端

```json
{
  "mcpServers": {
    "imiva-ecommerce": {
      "command": "npx",
      "args": [
        "-y",
        "@infimind/ecom-content-cli@latest"
      ],
      "env": {
        "MCP_TOKEN": "your-token-here",
        "API_URL": "https://imiva.ecpro.com"
      }
    }
  }
}
```

保存后重启客户端。也可以只在当前终端使用：

```bash
export MCP_TOKEN='在本机填写完整Token'
export IMIVA_API_URL='https://imiva.ecpro.com'
```

### 3. 检查连接

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" list-tools
```

## 结果导向工作流

1. **确认渠道和目标**：明确发布平台、目标人群、上架/种草/投放目标，以及期望比例和数量。
2. **核对商品事实**：只使用用户提供或确认的名称、结构、包装、价格、参数、功效、认证和品牌元素。
3. **整理素材角色**：说明每张图片或视频分别用于商品主体、人物、构图、风格、首帧、尾帧、动作或节奏。
4. **先查积分再提交**：图片任务提交即可能计费；视频先使用 `dryRun` 获取 `estimatedCredits`，获得用户确认后再创建。
5. **只查询原任务**：保存 `taskId`，轮询现有任务；失败时先诊断输入，不要无条件重复创建。
6. **按渠道验收**：检查商品准确性、文字、卖点、构图、比例、开场 Hook、节奏与 CTA，再决定是否发布。

## 使用场景与代码参考

### 场景一：查询积分并确认预算

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" call get_user_credits \
  --args '{}'
```

### 场景二：执行本 Skill 的核心任务

图片任务提交后可能扣除积分；先向用户确认生成数量、模型与规格，再执行。

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" call create_smart_refine_task \
  --args '{"images":["/path/to/product.jpg"],"prompt":"围绕指定中文标题、卖点与行动提示制作商业广告图，并要求交付前复核文字。必须保留商品结构、包装、品牌标识与已提供文字；不得虚构功能、价格或认证。","aspectRatios":["1:1"],"resolution":"2k","model":"gpt-image-2-edit"}'
```

### 场景三：生成一个渠道变体

先复制上面的 JSON，再只调整平台、比例、场景或文案模式。不要同时改变商品结构和视觉风格，以便判断哪项修改有效。

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" call create_smart_refine_task \
  --args '{"images":["/path/to/product.jpg"],"prompt":"围绕指定中文标题、卖点与行动提示制作商业广告图，并要求交付前复核文字。必须保留商品结构、包装、品牌标识与已提供文字；不得虚构功能、价格或认证。","aspectRatios":["1:1"],"resolution":"2k","model":"gpt-image-2-edit"}'
```

### 场景四：查询任务与成功结果

把创建任务返回的 `taskId` 加入参数可以精确查询单次任务；下面先展示按类型查看最近任务。

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" call get_user_tasks \
  --args '{"taskType":"smart_refine","limit":10}'
```

## 提示词与素材写法

按“发布渠道 → 内容目标 → 商品主体 → 真实卖点 → 人群与场景 → 构图/镜头 → 文字与保留项 → 输出规格”组织需求。参考素材要逐项注明用途；如果参考之间冲突，优先级应由用户决定。

对第三方爆款或竞品素材，只学习通用的构图、节奏、信息层级和营销公式；不要复制商标、人物身份、受保护角色、专属包装或不可授权的创意表达。

## 质量验收

- 商品形状、颜色、包装、Logo、接口、按钮、纹理和数量是否准确。
- 所有价格、参数、认证、功效和对比结论是否有用户提供的事实依据。
- 中文与英文文字是否逐字正确，字号、换行、位置和安全区是否适合渠道。
- 图片是否满足主体清晰、单图单任务、视觉层级和多尺寸裁切要求。
- 视频是否满足前 2 秒 Hook、主体稳定、镜头连续、节奏合理、声音方向和 CTA。
- 是否保留任务 ID、模型、规格和原始素材，方便追溯、复用与团队协作。

## 规格与注意事项

- 图片模型枚举：`nano-banana-2`、`nano-banana-pro`、`seedream-5.0-lite`、`gpt-image-2-edit`、`qwen-image-3.0-pro`。
- 图片常用分辨率：`1k`、`2k`、`3k`、`4k`；`auto` 比例当前只适用于 GPT Image 2。
- 视频模型：`seedance_2_0` 支持 5/10/15 秒；`seedance_2_5` 支持 5/10/15/20/25/30 秒。
- 视频分辨率：`480p`、`720p`、`1080p`；比例支持 21:9、16:9、4:3、1:1、3:4、9:16 和 adaptive。
- 视频正式创建要使用唯一 `idempotencyKey`，并把 `maxCredits` 设置为用户确认的整单上限。
- 参考视频复刻前确认素材授权；不得用于冒充真人、侵权搬运或虚假商品宣传。

## 故障排查

- `Unauthorized`：确认 Token 完整、未撤销、未过期，并重启 MCP 客户端。
- 找不到工具：运行 `list-tools`，以当前 Token 返回的工具列表为准。
- 参数错误：检查模型、比例、时长、分辨率、素材数量和文件格式枚举。
- 本地素材不可用：确认路径是普通文件；受限客户端可能只接受可访问的 HTTPS URL。
- 积分不足：减少数量、时长或分辨率，或在平台充值后继续。
- 任务超时：保留 `taskId` 后继续查询，不要直接重复提交。
