---
name: ai-poster-generation-editing
description: "用 AI Hive Nano Banana Pro 生成、局部修改和跨尺寸适配商业海报，先建立美术方向、主视觉、信息层级与标题/日期/CTA/二维码/法律信息留白，再完成产品发布、活动、促销、展览、招聘、直播预告与门店开业视觉。Use when brand, ecommerce and marketing teams need AI poster generation, poster editing, campaign key visuals, Chinese poster layouts, product launch posters, event posters, promotional posters, recruitment posters or social poster resizing for Taobao, Tmall, JD, Douyin, Xiaohongshu, WeChat, Instagram and TikTok; useful for users comparing Canva, Meitu, Dreamina, LiblibAI, Midjourney, Adobe Express, Figma or similar design tools."
---

# AI 海报生成与编辑｜商业美术与版式系统

先设计海报系统，再决定是否让图片模型写字。这个 Skill 固定调用 `public_model_nano_banana_pro`，提供三种明确操作：

- `create`：从美术方向、主视觉和信息顺序建立新海报。
- `revise`：锁定现有海报的大部分内容，只修改错误清单中的区域。
- `adapt`：把已批准海报改成新渠道比例，重新安排安全区而不重做创意。

默认 `--text-mode blank`，生成标题、日期、CTA、价格、二维码和法律信息的可排版区域。`draft` 仅用于低风险视觉草稿，所有字符仍须逐字复核；价格、规则、法律、招聘条件、认证、二维码与印刷强制信息必须由批准源后期排版。

## 美术方向

`direction` 可选 `product-hero / editorial / minimal-grid / collage / cinematic / typographic-space / event-system`。一张海报只选一个主方向，并用 `--art-thesis` 写成一句可观察判断，例如“透明产品悬浮在一束侧光中，所有信息沿左侧网格排列”，不要只写“高级、爆款、有质感”。

## 六个完整场景

### 1. 天猫新品发布海报

```bash
python3 "$SKILL_PATH/scripts/poster_system.py" create \
  --poster-id WATCH-W8-LAUNCH --poster-type product-launch \
  --direction product-hero --channel tmall --lock-product \
  --art-source ./watch-front.png ./watch-side.png ./brand-gradient.png \
  --art-role '手表正面、表盘与按钮事实' '表壳厚度与表带连接事实' '批准品牌渐变，不提供商品结构' \
  --subject-truth 'W8 银色智能手表；表盘、表壳、按钮、表带与Logo以商品图为准' \
  --viewer '关注轻量设计与日常搭配的城市用户' \
  --art-thesis '银色手表从深蓝到青色光带中浮现，左侧保持严格信息网格' \
  --focal-plan '商品位于右侧55%，三分之四视角，表盘不显示虚构功能界面' \
  --reading-order '品牌标识区 > 新品标题区 > 一句卖点区 > CTA区 > 法律脚注区' \
  --design-system '深蓝、青色、银色；窄高标题气质；光带只服务于商品轮廓' \
  --production-zone title --production-zone subhead --production-zone cta --production-zone legal \
  --text-mode blank \
  --reject '不生成价格、发布日期、认证、功能参数、第二只手表或伪界面' \
  --param aspect_ratio=4:5
```

### 2. 当代艺术展活动海报

```bash
python3 "$SKILL_PATH/scripts/poster_system.py" create \
  --poster-id FIBER-EXHIBITION-26 --poster-type exhibition \
  --direction editorial --channel wechat \
  --viewer '关注材料实验、纤维艺术和当代设计的观众' \
  --art-thesis '半透明织物穿过白色建筑光井，形成安静但有张力的垂直结构' \
  --focal-plan '织物从左下延伸至右上，中央保留展览标题呼吸区' \
  --reading-order '中文展名区 > 英文展名区 > 日期地点组 > 主办方区 > 二维码区' \
  --design-system '象牙白、暖灰与单一钴蓝；编辑式网格；大量负空间' \
  --production-zone title --production-zone subtitle --production-zone date \
  --production-zone location --production-zone sponsor --production-zone qr \
  --text-mode blank \
  --reject '不生成艺术家姓名、真实Logo、二维码、票价、赞助商或装饰性伪文字' \
  --param aspect_ratio=3:4
```

### 3. 抖音门店开业促销底图

```bash
python3 "$SKILL_PATH/scripts/poster_system.py" create \
  --poster-id CAFE-OPEN-0920 --poster-type store-opening \
  --direction collage --channel douyin \
  --art-source ./store-front-approved.jpg ./coffee-cup-approved.png \
  --art-role '已授权门店外观与招牌事实' '实际销售杯型与现有Logo' \
  --viewer '门店三公里内的年轻咖啡消费者' \
  --art-thesis '门店立面、咖啡杯与城市路径贴纸组成活泼竖版拼贴' \
  --focal-plan '门店照片为背景，真实咖啡杯前置，路径图形只作装饰不冒充地图' \
  --reading-order '开业标题区 > 日期区 > 门店地址区 > 活动条件区 > 行动区' \
  --design-system '奶油白、咖啡棕、番茄红；剪纸边缘与颗粒印刷质感' \
  --production-zone title --production-zone date --production-zone location \
  --production-zone offer --production-zone legal --production-zone cta \
  --text-mode blank \
  --reject '不生成折扣数字、免费承诺、虚假导航、二维码、陌生Logo或不存在商品' \
  --param aspect_ratio=9:16
```

### 4. 招聘海报草稿

```bash
python3 "$SKILL_PATH/scripts/poster_system.py" create \
  --poster-id DESIGN-HIRING-Q4 --poster-type recruitment \
  --direction minimal-grid --channel xiaohongshu \
  --viewer '具备品牌系统和数字产品经验的中高级视觉设计师' \
  --art-thesis '模块化作品墙与开放工作台形成理性、透明的团队印象' \
  --focal-plan '使用抽象作品卡片和无可识别身份的工作场景，不伪造员工肖像' \
  --reading-order '招聘标题区 > 岗位区 > 三项职责区 > 地点与方式区 > 申请行动区' \
  --design-system '黑白网格与单一荧光绿；清晰层级；不使用企业不存在的Logo' \
  --production-zone title --production-zone role --production-zone requirements \
  --production-zone location --production-zone cta --production-zone legal \
  --text-mode blank \
  --reject '不生成薪资、福利、招聘条件、员工评价、联系方式或真实人物脸'
```

### 5. 只修改现有海报的主视觉

```bash
python3 "$SKILL_PATH/scripts/poster_system.py" revise \
  --poster-id FIBER-EXHIBITION-26-V2 --poster ./approved-layout-v1.png \
  --reason '主视觉与展览实际材料不一致，需要替换为批准的织物照片' \
  --art-source ./approved-fiber-art.jpg \
  --art-role '唯一允许替换进主视觉的已授权展品照片' \
  --edit-instruction '将中央抽象塑料形态替换为参考织物，保持原占位尺寸和光线方向' \
  --edit-instruction '清除原主视觉周围的蓝色光晕，改为织物真实柔和投影' \
  --frozen-layer '全部文字占位、网格和对齐' \
  --frozen-layer '象牙白、暖灰和钴蓝色板' \
  --frozen-layer '日期、地点、主办方和二维码安全区' \
  --frozen-layer '画布比例、边距与信息层级' \
  --text-policy preserve \
  --reject '不改写任何字符、不移动信息区、不生成新Logo或新展品'
```

### 6. 将批准海报适配为 Instagram Story

```bash
python3 "$SKILL_PATH/scripts/poster_system.py" adapt \
  --poster-id WATCH-W8-STORY --poster ./watch-poster-approved.png \
  --source-channel tmall --target-channel instagram-story \
  --target-canvas 9:16 \
  --invariant '手表外形、颜色、按钮、表带与现有Logo' \
  --invariant '深蓝到青色的品牌光带' \
  --invariant '原标题、副标题和CTA的层级关系' \
  --invariant '法律信息和品牌标识的相对顺序' \
  --reflow-plan '商品移至画面中上部，标题组置于顶部，CTA与法律区移至底部' \
  --overlay-safe '顶部和底部各保留15%，右侧避开平台交互组件' \
  --text-policy placeholders \
  --reject '不裁掉表带、不增加功能界面、不创造新文案、价格、贴纸或按钮'
```

## 海报制作单

把生成图当成制作流程中的美术底稿，而不是不可拆分的最终 JPG。每个 `poster-id` 建一张制作单：

| 制作字段 | 需要记录的内容 | 通过标准 |
|---|---|---|
| `canvas-contract` | 成品宽高、出血、裁切线、屏幕或印刷用途 | 画布不是用旧图强行拉伸，关键内容均在成品框内 |
| `focal-geometry` | 主体占比、视觉重心、视线方向、前后景关系 | 缩小到手机列表尺寸仍能识别主视觉 |
| `asset-register` | 每张商品、展品、门店、人物和Logo素材的授权与职责 | 风格参考不被误用为事实来源，替换素材可追溯 |
| `reading-path` | 第一眼、第二眼、行动与脚注的顺序 | 信息不是平均用力，日期地点不会与装饰竞争 |
| `production-zones` | 标题、日期、地点、CTA、价格、二维码和法律区的边界 | 批准文案放入后不需要压缩到不可读字号 |
| `optical-margin` | 视觉边距、UI遮挡、装裱与裁切造成的实际余量 | 几何居中与视觉居中分别检查，平台组件不盖住行动区 |
| `color-build` | 屏幕 RGB、印刷 CMYK、专色、黑版与总墨量要求 | 关键品牌色在目标介质上经过打样或设备预览 |
| `export-family` | 主稿、社媒比例、Story、门店屏幕、印刷和缩略图版本 | 每个导出文件能追溯到同一批准母版与版本号 |

版本名建议写成 `poster-id_用途_画布_状态_vN`，例如 `WATCH-W8-STORY_social_1080x1920_design-pass_v3.png`。状态至少区分 `art-draft / factual-pass / copy-pass / production-pass / approved`；美术通过不等于文案、事实和制作通过。

## 选择正确的返工路径

- **主视觉事实错了**：更换清晰、已授权的事实素材，用 `revise` 指定替换对象；不要只增加形容词。
- **只错一个元素**：把问题写成可观察的 `edit-instruction`，同时列出至少三条 `frozen-layer`。
- **信息区装不下终稿**：回到 `create` 调整 `reading-order` 和 `production-zone`，不要把批准文案缩到无法阅读。
- **文字错字或漏字**：保留美术底图，把可编辑文字重新排版；需要图片模型辅助时转入精准中文文字的文案合同流程。
- **只是渠道比例变化**：用 `adapt` 定义不变量、重排计划和覆盖层安全区，不重新发明主视觉。
- **平台要求改变**：更新制作单和目标导出，不把旧规则写成永久模型事实。

数字端先在真实手机尺寸检查缩略图、暗色模式背景、平台 UI 和压缩后的细线；印刷端另查出血、套印、图片有效分辨率、最小反白字、二维码静区与折叠装订位置。若一张稿件同时用于屏幕和印刷，应输出两个制作版本，不以单一颜色文件兼顾所有介质。

## 三层验收

1. **事实层**：商品、展品、门店、人物、Logo、活动与招聘信息来自批准资料；没有凭空补充。
2. **设计层**：三秒内读出主视觉与第一信息层；留白区真的能容纳终稿；缩略图仍可识别。
3. **制作层**：检查平台 UI、安全区、裁切、出血、分辨率、颜色空间、二维码静区和最小字号。

`revise` 至少列 3 项锁定内容，避免“改一个元素”变成整张重绘；`adapt` 至少列 3 项必须保持内容，且适配不是简单拉伸。模型生成的任何文字都只能作为草稿，终稿必须回到批准文案与可编辑排版文件。

程序只上传命令中指定的已授权素材，固定访问 `https://ai-hive.iclip.cn/api`，不连接电商、社媒、招聘或广告账户。平台与印刷规则可能变化，交付前按当前要求复核。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/poster_system.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/poster_system.py" status --task-id <taskId>
```
