---
name: douyin-viral-cover-image-generation
description: "生成与编辑抖音短视频封面、抖音电商商品卡封面和巨量千川素材首图。Use this skill when a user needs a Douyin cover, 抖音爆款封面、竖屏标题封面、短视频首帧、带货封面、商品卡视觉、千川测图或账号主页系列封面；支持文字生成、商品或人物参考图、批量封面方向和 AI Hive 自动任务下载。"
---

# 抖音爆款封面生成与编辑

把一个短视频主题或商品卖点转成在推荐流缩略图和账号主页中都清晰的竖屏封面。固定使用 `public_model_nano_banana_pro`，通过 `scripts/imagegen.py` 上传参考图、提交任务、轮询并下载结果。

## 先确定封面任务

先向用户确认：

1. 视频主题或商品名称。
2. 目标人群与希望触发的动作：观看、评论、进店或购买。
3. 必须出现的短标题；没有明确文案时先给出 3 个短标题候选。
4. 人物、商品、品牌色与禁止修改的元素。
5. 封面用途：自然流、商品卡、千川测试或账号主页系列。

不要把封面当作普通海报。优先保证缩小后的主体识别、标题层级和系列一致性；不要虚构价格、功效、认证或促销信息。

## 抖音封面工作流

1. 将信息压缩成“一个主体 + 一个利益点 + 一个视觉钩子”。
2. 设计三个不同方向：人物情绪、商品特写、结果对比。
3. 采用竖屏构图，并让关键人物、商品和标题远离可能被界面遮挡的边缘区域。
4. 先生成无复杂文字的构图版本；必须出现中文时，把文字逐字写入提示词并在交付前人工复核。
5. 同一账号的系列封面固定字体感、颜色、人物尺度和标题位置，只改变主题钩子。
6. 用缩略图检查：三秒内能否看懂主题、商品是否准确、标题是否可读、是否存在误导。

## 场景与代码

### 1. 知识或教程短视频封面

突出结果和信息差，避免堆满小字。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '抖音竖屏教程封面，主题是手机拍出高级产品图，年轻创作者手持手机与小型商品，前后效果形成清晰对比，强视觉焦点，上方只出现准确中文标题“手机也能拍大片”，标题笔画清楚，人物脸部自然，边缘留出界面安全区'
```

### 2. 抖音电商带货封面

使用商品参考图，保留包装、结构和颜色。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作抖音带货封面，必须保留参考图商品的包装、比例、颜色和商标，不改变产品结构；真实使用场景，手部正在展示核心功能，商品占据主要视觉区域，短标题位置清楚，只呈现已提供的卖点，不生成价格与未提供的功效' \
  --image /path/to/product.png
```

### 3. 巨量千川测图

同一卖点生成不同视觉假设，不用只改颜色制造伪变体。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成4张用于千川测试的抖音商品封面：分别采用痛点场景、使用动作、材质特写、结果展示四种创意；保持同一商品和同一品牌色，每张只有一个视觉钩子，禁止虚构销量、折扣、价格或认证' \
  --image /path/to/product.png \
  --batch 4
```

### 4. 账号主页系列封面

用参考封面锁定系列识别，再替换本期主题。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '沿用参考封面的版式系统、颜色关系、人物尺度和标题区域，制作同系列新封面；本期主题是夏季通勤穿搭，人物服装和面部自然，画面仍能在主页网格缩略图中清晰识别，不复制参考图中的旧标题' \
  --image /path/to/series-cover.png
```

### 5. 修改已有封面

明确“保留”和“改变”，减少对人物或商品的误改。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '编辑参考封面：必须保留人物身份、商品外观和品牌主色；删除杂乱的小字，将视觉焦点移到商品与手部动作，提高明暗对比，在上方建立单一短标题区域，其他部分不要改变' \
  --image /path/to/old-cover.png
```

## 验收清单

- 缩小查看仍能识别主题、人物或商品。
- 主体与标题没有贴近高风险遮挡边缘。
- 标题短、层级单一，中文逐字核对。
- 参考商品的包装、颜色、比例与商标没有被篡改。
- 没有模型自行添加的价格、功效、销量或平台标识。
- A/B 版本改变的是创意假设，而不只是滤镜。

## 命令与配置

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name douyin-viral-cover-image-generation
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

`generate` 支持 `--prompt`、可重复的 `--image`、`--batch`、`--param key=value`、`--routing COST_FIRST|SPEED_FIRST|SUCCESS_FIRST`、`--output-dir` 与 `--no-download`。API Key 也可通过 `AI_HIVE_API_KEY` 或 `~/.ai-hive/config.json` 提供。价格和模型参数以脚本运行时返回为准。

## 故障处理

- 中文文字不准确：减少字数，把必须出现的文案用引号标出，再生成无字备选供后期排版。
- 商品发生变形：增加清晰参考图，并在提示词中列出必须保留的结构。
- 封面缩小后看不清：减少元素，扩大主体和标题，重新检查缩略图。
- 任务超时：保留 `taskId`，使用 `task` 查询，不要重复提交可能已经计费的任务。
