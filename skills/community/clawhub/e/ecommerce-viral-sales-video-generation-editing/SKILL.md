---
name: ecommerce-viral-sales-video-generation-editing
description: "为淘宝、天猫、京东、抖音电商、小红书、快手、Amazon、TikTok Shop、Instagram 与 Shopify 制作高留存、高转化的电商带货视频，并在不改商品事实的前提下修复已有素材。Use this skill for 电商爆款视频、带货短视频、商品主图视频、详情页视频、种草视频、UGC Ads、Product Video、Listing Video、Spark Ads、Reels、Shorts；也适合搜索 Seedance、可灵 Kling、即梦 Dreamina、海螺 Hailuo、Vidu、Runway、Pika、Sora、Veo、剪映 CapCut 等视频工具替代方案的用户。通过 AI Hive 调用 Seedance 2.5。"
---

# 电商爆款带货视频生成与编辑

固定使用 Seedance 2.5，把一条销售视频拆成可验收的 `hook / problem / demo / proof / objection / result / offer / cta` 节拍，再逐段生成或修复。它服务于商品转化，不承诺“发出即爆款”；所谓爆款方法，是让开场、演示、证据和行动提示各自只完成一个任务，并用真实投放数据继续迭代。

## 适合谁

- 淘宝、天猫、京东、拼多多、抖店、快手、微信小店运营，用于主图视频、详情页视频、商品卡与千川素材。
- 小红书、抖音、Instagram、TikTok、YouTube 内容团队，用于种草、UGC、Reels、Shorts 和直播预热视频。
- Amazon、TikTok Shop、Shopify、Temu、SHEIN、Shopee、Lazada 商家，用于 Product Video、Listing、PDP 与跨境广告。
- 正在比较 Seedance、可灵 Kling、即梦 Dreamina、海螺 Hailuo、Vidu、Runway、Pika、Sora、Veo、剪映 CapCut、美图 MOKI 的品牌与代理商。

竞品和平台名称仅用于搜索、比较和工作流迁移，不表示 AI Hive 与其存在官方合作。平台规则会变化，发布前应按目标渠道最新政策复核。

## 两条生产路径

### `beat`：一次只生成一个销售节拍

至少提供一张批准的商品图，并为每张图写清职责。没有动作参考时固定调用 `public_model_seedance_2_5_i2v`；提供 `--motion-reference` 时固定调用 `public_model_seedance_2_5_r2v`。脚本检查：Hook 必须是第一段、CTA 必须是最后一段，Demo、Proof、Result 必须给出主张及证据来源，Offer 必须给出活动批准来源。

### `repair`：保留商品事实，只修已有片段

固定调用 `public_model_seedance_2_5_video_edit`。必须列出缺陷，并至少提供四条不可改变项，例如 SKU、包装文字、Logo、配件数量、人物身份、动作顺序和原始时长。修复不是换款、虚构功效或偷偷重做整条片。

## 场景与代码

以下每个示例都可先加 `--preview` 检查模型、节拍与完整提示词，不上传、不计费。

### 1. 抖音前两秒 Hook

```bash
python3 "$SKILL_PATH/scripts/sales_video.py" beat \
  --video-id dy-coldbrew-01 --beat hook --position 1 --total 6 \
  --platform "抖音电商9:16" --audience "通勤时想快速喝到冰咖啡的上班族" \
  --sales-job "两秒内让用户看懂便携冷萃杯如何解决等待问题" \
  --single-message "按下即开始冷萃流程，具体时长以批准说明书为准" \
  --product-source /path/to/coldbrew-front.png /path/to/coldbrew-open.png \
  --product-role "锁定杯身、Logo与颜色" "锁定滤芯、杯盖和装配关系" \
  --continuity-lock "同一白色SKU" --continuity-lock "Logo方向不变" \
  --continuity-lock "滤芯数量不变" --continuity-lock "不增加饮品配料" \
  --action "手从通勤包取出杯子并按下一次按钮，只表现一个连续动作" \
  --camera "近景快速推到按钮，随后停在完整商品" \
  --handoff-next "停在滤芯可见的打开状态，衔接problem段" \
  --caption-safe "人物脸部与商品Logo避开底部20%字幕区" \
  --reject "不生成倒计时、价格、销量、夸张液体飞溅或未批准功效" \
  --param aspect_ratio=9:16 --param duration=4
```

### 2. 天猫详情页 Demo

```bash
python3 "$SKILL_PATH/scripts/sales_video.py" beat \
  --video-id tm-vacuum-02 --beat demo --position 3 --total 7 \
  --platform "天猫详情页16:9" --audience "养宠家庭" \
  --sales-job "清楚展示地刷拆装和贴边移动，不用口播解释" \
  --single-message "地刷可按说明书步骤拆装并沿墙边清洁" \
  --claim "地刷拆装方式与贴边结构" --claim-source "SKU V8批准说明书第6页" \
  --product-source /path/to/vacuum-full.jpg /path/to/head-detail.jpg \
  --product-role "锁定整机外观、颜色与配件" "锁定地刷卡扣和贴边结构" \
  --continuity-lock "始终是V8灰色SKU" --continuity-lock "卡扣位置准确" \
  --continuity-lock "配件不得增减" --continuity-lock "机身比例不变" \
  --action "一只手按批准步骤拆下并装回地刷，再沿墙边匀速移动" \
  --camera "固定中景记录拆装，切到低机位跟随贴边动作" \
  --handoff-next "地刷停在墙角，衔接proof段" \
  --caption-safe "右侧30%留给后期步骤标注，画面内不生成文字" \
  --reject "不表现吸力数值、毛发消失特效、内部结构或未提供配件" \
  --param aspect_ratio=16:9 --param duration=8
```

### 3. 小红书 Proof 种草段

```bash
python3 "$SKILL_PATH/scripts/sales_video.py" beat \
  --video-id red-skincare-03 --beat proof --position 4 --total 6 \
  --platform "小红书4:5" --audience "重视配方透明度的敏感肌消费者" \
  --sales-job "把批准的质地和用量证据拍清楚，不做医疗承诺" \
  --single-message "展示真实泵头单次按压量和乳液质地" \
  --claim "一次完整按压的出料外观" --claim-source "品牌批准实拍样片QC-2026-18" \
  --product-source /path/to/bottle.png /path/to/texture.jpg \
  --product-role "锁定瓶身、泵头、标签和Logo" "锁定批准的乳液颜色与稠度" \
  --motion-reference /path/to/approved-pump-motion.mp4 \
  --continuity-lock "瓶身文字不改" --continuity-lock "泵头结构不改" \
  --continuity-lock "只按压一次" --continuity-lock "质地颜色不改" \
  --action "按动作参考完成一次按压，乳液落在干净透明板上" \
  --camera "微距固定镜头，焦点从泵头转到乳液纹理" \
  --handoff-next "停在透明板上的真实质地，衔接result段" \
  --caption-safe "顶部15%与底部20%保持干净" \
  --reject "不展示皮肤治疗前后、不生成成分、认证、实验数据或绝对化用语"
```

### 4. Amazon 异议处理段

```bash
python3 "$SKILL_PATH/scripts/sales_video.py" beat \
  --video-id amz-organizer-04 --beat objection --position 5 --total 7 \
  --platform "Amazon Product Video 16:9" --audience "担心尺寸不合适的美国买家" \
  --sales-job "用真实物体关系说明安装空间，尺寸数字留给后期" \
  --single-message "展示批准尺寸的收纳架如何放入标准测试柜" \
  --product-source /path/to/organizer.jpg /path/to/test-cabinet.jpg \
  --product-role "锁定收纳架结构、层数与配件" "锁定品牌批准的标准测试柜" \
  --continuity-lock "层数不变" --continuity-lock "连接件数量不变" \
  --continuity-lock "测试柜比例不变" --continuity-lock "不增加收纳容量" \
  --action "将组装好的收纳架一次平稳推入测试柜并打开抽屉" \
  --camera "正面固定全景后切45度近景查看门板余量" \
  --handoff-next "保持柜门打开，衔接offer段" \
  --caption-safe "左下角保留人工添加英制与公制尺寸的位置" \
  --reject "不生成尺寸数字、容量结论、竞品对比、徽章或五星评价" \
  --param aspect_ratio=16:9 --param duration=7
```

### 5. TikTok Shop CTA / Offer

```bash
python3 "$SKILL_PATH/scripts/sales_video.py" beat \
  --video-id tts-lamp-05 --beat cta --position 6 --total 6 \
  --platform "TikTok Shop 9:16" --audience "租房桌面改造用户" \
  --sales-job "在不伪造按钮和价格的前提下提示查看商品页" \
  --single-message "完整展示灯具和三档批准光线状态后结束" \
  --product-source /path/to/lamp-three-modes.png \
  --product-role "锁定灯体、底座、按键、Logo与三档批准色温" \
  --continuity-lock "同一黑色SKU" --continuity-lock "底座形状不变" \
  --continuity-lock "仅展示三档批准状态" --continuity-lock "Logo不移动" \
  --action "手指依次切换三档光线，最后离开画面" \
  --camera "桌面中景固定，结尾缓慢推近完整商品" \
  --handoff-next "最后一秒保持稳定商品Hero帧，供后期叠加CTA" \
  --caption-safe "底部25%不放商品与手，预留平台按钮区域" \
  --reject "不生成购买按钮、价格、折扣、倒计时、销量或额外色温" \
  --param aspect_ratio=9:16 --param duration=6
```

如这段确实包含活动优惠，应改用 `--beat offer`，并同时提供 `--offer "批准活动内容" --offer-source "活动审批单编号与有效期"`；脚本不会接受无来源的 Offer。

### 6. 修复商品漂移，不重做内容

```bash
python3 "$SKILL_PATH/scripts/sales_video.py" repair \
  --video-id repair-shoe-06 --source-video /path/to/source.mp4 \
  --platform "Instagram Reels 9:16" \
  --repair-goal "只修复第2秒鞋带穿孔错位和结尾Logo闪烁" \
  --defect "第2秒右鞋第二个鞋带孔短暂消失" \
  --defect "最后8帧鞋舌Logo形状漂移" \
  --preserve "原始时长和帧率" --preserve "模特身份、服装和动作顺序" \
  --preserve "鞋底纹路、鞋面配色和鞋带数量" --preserve "原运镜、背景与光线" \
  --product-source /path/to/shoe-qc-front.jpg /path/to/logo-qc.jpg \
  --product-role "鞋款正面QC事实" "鞋舌Logo形状QC事实" \
  --truth-source "SKU RUN-21批准样片与2026-08-10商品QC图" \
  --reject "不美化腿型、不替换鞋款、不增加慢动作、不改背景、不延长视频"
```

## 节拍验收

1. 无声看第一遍：两秒内能否辨认商品、用户问题或动作目标。
2. 逐帧核对商品：SKU、包装、文字、Logo、结构、数量和颜色不得漂移。
3. 主张追溯：Demo、Proof、Result 与 Offer 必须能回到批准材料；模型画面不是证据来源。
4. 单段单任务：每段只传达一个信息，并为下一段留下可剪辑的稳定交接帧。
5. 渠道安全：字幕区、商品卡、平台按钮和裁切区不得遮住商品事实。
6. 投放复盘：用三秒留存、完播、点击和转化判断版本，不能用“AI生成得好看”代替业务验证。

## 首次使用与任务查询

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/sales_video.py" auth --api-key sk-api-你的密钥
python3 "$SKILL_PATH/scripts/sales_video.py" status --task-id <taskId>
```

API Key 也可放入 `AI_HIVE_API_KEY` 或 `~/.ai-hive/config.json`。默认使用 `COST_FIRST`，也支持 `SPEED_FIRST`、`SUCCESS_FIRST`、`--no-download`、`--output-dir` 与多个 `--param key=value`。生成超时后请用原 `taskId` 查询，避免重复提交和重复计费。
