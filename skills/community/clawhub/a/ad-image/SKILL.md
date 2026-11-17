---
name: ad-image
description: "使用 Nano Banana 2 把广告简报变成可测试的广告图片，明确受众、单一主张、视觉证据、品牌资产、CTA 安全区与禁用表述。Use this skill for 广告图片、广告图、广告 KV、信息流广告、展示广告、品牌广告、效果广告、Meta Ads、Google Ads、巨量引擎、千川、小红书聚光、Amazon Ads、TikTok Ads 和广告创意测试；通过 AI Hive 生成，不承诺点击或转化结果。"
---

# 广告图片

模型固定为 `public_model_nano_banana_2`。先把需求写成广告创意简报：受众是谁、只传达哪一个主张、什么画面能证明、品牌必须出现什么、文字将放在哪里、哪些表述不能使用。生成图片承担视觉底稿与探索，最终文案、价格和合规声明应由投放团队复核。

## 一页创意简报

用六格记录：`受众 / 传播任务 / 视觉证据 / 品牌资产 / CTA 区域 / 禁用内容`。同一轮候选只更换一个钩子或构图变量，避免无法判断哪项改变影响效果。

## 五种广告任务

### 1. 新客问题识别图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-desk-organizer.png   --prompt '制作4:5新客信息流广告底图：准确保留桌面收纳盒的层数、颜色、Logo与抽屉结构，用凌乱文件和整理后桌面的左右情境表现“找东西耗时”的问题；产品只出现一次，顶部留短标题区，底部留CTA区，不生成文字、时间数字、价格或夸张效果'   --param aspect_ratio=4:5
```

### 2. 单一卖点证据图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-bottle-detail.png   --prompt '生成1:1广告创意：不锈钢水瓶主体与参考图一致，使用可见的密封圈和倒置静态场景表现结构，不展示液体泄漏；右侧留卖点文字位，不生成“绝不漏水”、认证、五星、折扣或竞品'   --param aspect_ratio=1:1
```

### 3. 品牌认知 KV

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-headphones.png ./brand-palette.png   --prompt '制作16:9品牌认知KV：耳机结构、材质、颜色和Logo准确，使用品牌深蓝与暖橙形成声波般的抽象空间，主体强识别，左侧留品牌口号区；不生成具体文字、奖项、艺人、价格或未提供配件'   --param aspect_ratio=16:9
```

### 4. 再营销商品提醒

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-shoe.png   --prompt '制作4:5再营销广告底图：保持鞋型、鞋底纹路、鞋带、配色和Logo，干净近景与穿着场景做层次组合，突出此前浏览商品；预留动态价格与CTA模块，不在图中生成价格、库存、倒计时、评价或促销承诺'   --param aspect_ratio=4:5
```

### 5. 单变量钩子测试

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-coffee-machine.png   --prompt '输出三张1:1广告候选，咖啡机、杯子、视角、背景和留白完全一致，只改变视觉钩子：A清晨柔光，B咖啡液近景，C极简厨房氛围；不生成文字、性能数字、价格、人物或额外附件'   --batch 3   --param aspect_ratio=1:1
```

## 投放前检查

- 三秒内能识别受众问题和唯一传播主张。
- 画面证据不超出已批准的商品事实。
- Logo、包装、标配和颜色与品牌资料一致。
- 标题、免责声明与 CTA 在目标版位安全区内。
- 记录素材版本、变量、受众、投放位置和真实实验结果。

## 接口权限

脚本接受文字与用户指定的参考图片，固定调用 Nano Banana 2。认证信息只发送到 `https://ai-hive.iclip.cn/api`，不能改成其他服务地址；不提供聊天、视频、账户或余额操作。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name ad-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

广告效果受出价、落地页、商品、受众与流量共同影响，本 Skill 不保证 CTR、CVR、ROAS 或销量。
