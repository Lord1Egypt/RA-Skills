---
name: chinese-text-commercial-poster-generation
description: "用 AI Hive GPT Image 2 把已批准的中文、英文、数字和标点按版式区域生成到商业图片中，并通过文案合同、离线字符比对和局部返修降低错字、漏字、重复字与伪文字风险。Use when ecommerce and marketing teams need exact Chinese text images, commercial posters, product feature cards, campaign KV, social covers, bilingual ads, package-front concepts or typo repair for Taobao, Tmall, JD, Douyin, Xiaohongshu, WeChat, Amazon, TikTok Shop, Instagram and Shopify; relevant to users comparing Meitu, Dreamina, LiblibAI, Canva, Adobe Express, Midjourney or similar design workflows."
---

# 精准中文文字商业图片｜GPT Image 2 文案合同

商业图片里的文案是数据，不是“意思差不多就行”的提示词。这个 Skill 固定调用 `public_model_gpt_image_2`，把每段批准文案写成 `区域=逐字内容`，明确来源、顺序、版式和禁用字符；生成后用离线 `audit` 比较人工抄录或 OCR 结果，发现错误再用 `repair` 只修报错区域。

图片模型仍可能写错文字。价格、日期、规格、法律、医疗、金融、认证、二维码和包装强制信息必须由人工逐字符复核；不能容错时，应生成留白底图并在专业排版工具中放置批准稿。

## 文案合同

每条 `--copy` 使用 `zone=exact text`：

```text
headline=夏日轻装上新
subhead=通勤与周末，一包切换
date=2026年8月20日—9月5日
cta=立即查看
```

`zone` 可用 `headline / subhead / kicker / badge / date / time / location / price / cta / disclaimer / label / custom-*`。同一合同最多 12 段、总计 500 字符。`--copy-source` 必须写清批准来源；`--forbid-copy` 可列出旧标题、旧价格、占位符或任何不得出现的文字。

## 五个完整场景

### 1. 天猫商品卖点图

```bash
python3 "$SKILL_PATH/scripts/chinese_copy_image.py" compose \
  --project BAG-A7-LAUNCH --platform tmall --asset product-feature \
  --source-image ./approved-bag.png ./brand-layout.png \
  --source-role 'SKU 外形、颜色、五金和Logo事实' '批准的品牌版式与色彩，不提供商品事实' \
  --product-record 'A7 棕色通勤包；包型、肩带、五金、缝线和现有Logo以商品图为准' \
  --copy-source '市场部终审文案 BAG-A7-CN-v6' \
  --copy 'headline=一包切换通勤与周末' \
  --copy 'subhead=轻装出发，从容收纳' \
  --copy 'cta=查看细节' \
  --visual-brief '棕色通勤包置于暖灰桌面，商品为视觉焦点' \
  --layout-plan '标题左上两行，副标题位于标题下方，CTA 左下；商品在右侧' \
  --brand-rules '暖灰、棕色和少量金色；使用克制现代中文无衬线气质' \
  --forbid-copy '新品上市' --forbid-copy '限时优惠' \
  --forbid-element '价格、折扣徽章、认证、额外口袋和额外配件'
```

### 2. 抖音直播预告竖图

```bash
python3 "$SKILL_PATH/scripts/chinese_copy_image.py" compose \
  --project LIVE-N5-0822 --platform douyin --asset ecommerce-card \
  --source-image ./label-printer.png \
  --source-role '粉色标签机的按钮、出纸口、颜色与比例' \
  --product-record 'N5 粉色便携标签机；三个前置按钮和顶部出纸口以参考图为准' \
  --copy-source '直播运营排期表 2026-W34 已锁定行' \
  --copy 'kicker=收纳好物直播间' \
  --copy 'headline=桌面整理，从一张标签开始' \
  --copy 'time=8月22日 20:00' \
  --copy 'cta=预约直播' \
  --visual-brief '竖屏近景商品卡，粉色标签机位于明亮书桌上' \
  --layout-plan 'kicker 顶部，headline 中上，time 与 cta 位于下半部独立色块' \
  --brand-rules '奶油白、浅粉、深灰，高对比文字区，不生成手机界面' \
  --forbid-copy '今晚8点' --forbid-copy '全网最低' \
  --forbid-element '倒计时、销量、折扣数字、赠品和不存在的按钮' \
  --param aspect_ratio=9:16
```

### 3. 小红书种草封面

```bash
python3 "$SKILL_PATH/scripts/chinese_copy_image.py" compose \
  --project TRAVEL-T3-NOTE --platform xiaohongshu --asset social-cover \
  --source-image ./three-travel-bottles.png \
  --source-role '三件旅行分装瓶的数量、瓶型、琥珀色和瓶盖事实' \
  --product-record 'T3 三件套，三只瓶均为琥珀色；不提供容量或功效宣称' \
  --copy-source '内容团队封面标题终稿 NOTE-T3-12' \
  --copy 'headline=周末行李减负清单' \
  --copy 'badge=3件分装组合' \
  --visual-brief '打开的旅行收纳包和三只商品，真实周末出行氛围' \
  --layout-plan 'headline 在顶部安全区，badge 在左下角，右侧避开平台按钮' \
  --brand-rules '自然晨光、米色织物与琥珀色商品，标题清楚但不遮挡瓶盖' \
  --forbid-copy '亲测' --forbid-copy '必买' --forbid-copy '零泄漏' \
  --forbid-element '虚构评价、星级、容量、功效、第四只瓶和可识别票据'
```

### 4. Instagram 中英双语 Campaign

```bash
python3 "$SKILL_PATH/scripts/chinese_copy_image.py" compose \
  --project STUDIO-OPEN-DAY --platform instagram --asset campaign-kv \
  --copy-source '品牌与法务共同批准的 OPEN-DAY-BI-v3' \
  --copy 'headline=开放工作室日' \
  --copy 'subhead=OPEN STUDIO DAY' \
  --copy 'date=2026.09.12' \
  --copy 'location=上海·西岸' \
  --copy 'cta=预约参观 / RSVP' \
  --visual-brief '当代设计工作室的纸张、金属和光影抽象静物' \
  --layout-plan '中文标题第一层，英文标题第二层；日期地点同组，双语 CTA 在底部' \
  --brand-rules '黑、象牙白和信号橙，网格清楚，所有英文保持批准大小写' \
  --forbid-copy 'Shanghai West Bund' --forbid-copy 'FREE ENTRY' \
  --forbid-element '人物、赞助商Logo、二维码、票价、额外英文和伪文字' \
  --param aspect_ratio=4:5
```

### 5. 按错误清单局部返修

```bash
python3 "$SKILL_PATH/scripts/chinese_copy_image.py" repair \
  --project STUDIO-OPEN-DAY --platform instagram --asset campaign-kv \
  --draft ./poster-v1.png \
  --copy-source '品牌与法务共同批准的 OPEN-DAY-BI-v3' \
  --copy 'headline=开放工作室日' \
  --copy 'subhead=OPEN STUDIO DAY' \
  --copy 'date=2026.09.12' \
  --copy 'location=上海·西岸' \
  --copy 'cta=预约参观 / RSVP' \
  --observed-error 'headline 被写成“开放工作窒日”，只修正“室”字' \
  --observed-error 'cta 漏掉斜杠前后的空格，恢复批准文本' \
  --visual-brief '保持 v1 的抽象静物、色彩、网格和留白' \
  --layout-plan '所有文字位置、字号层级和换行保持 v1，仅修报错字符' \
  --brand-rules '未报错区域不可改变' \
  --forbid-element '不重绘背景，不移动日期地点，不新增任何字符'
```

## 离线字符审计

把生成图中的文字人工抄录出来，或粘贴经人工确认的 OCR 文本。`audit` 不上传图片、不调用模型，只逐字符比较：

```bash
python3 "$SKILL_PATH/scripts/chinese_copy_image.py" audit \
  --expected 'headline=开放工作室日' \
  --expected 'cta=预约参观 / RSVP' \
  --observed 'headline=开放工作窒日' \
  --observed 'cta=预约参观/RSVP'
```

退出码为 `0` 表示全部逐字一致，`2` 表示至少一个区域缺失或不同。审计通过后仍要检查笔画形态、字重、断行、对齐、商品事实、Logo、日期时区、平台安全区和最终导出尺寸。

## 交付规则

- 一轮只使用一份批准文案；改文案就创建新版本，不在聊天中口头覆盖旧稿。
- 图片参考的职责必须写清，风格图不能成为商品结构或活动事实来源。
- `price`、`disclaimer` 和包装法定信息默认建议后期排版；若生成，必须双人复核。
- `repair` 只处理列出的可观察错误。若版式整体失败，应返回 `compose` 重建，不要无限局部重绘。
- 平台、印刷和广告规则会变化，发布前以当前政策与批准资料为准。

程序仅上传命令中明确指定的素材，API 固定为 `https://ai-hive.iclip.cn/api`，不连接电商或社交平台账号。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/chinese_copy_image.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/chinese_copy_image.py" status --task-id <taskId>
```
