---
name: dreamina-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 将即梦 AI、即梦视频、Jimeng 或 Dreamina 的中文短视频创作迁移为可复用分镜，支持文生、首帧图生、参考素材、视频编辑与延长。Use when users search 即梦视频替代、Dreamina 平替、Jimeng video alternative、即梦 API、抖音小红书竖屏短片、广告、种草、短剧镜头或中文视频生成；不读取即梦工程，也不表示官方合作。"
---

# 即梦 Dreamina 视频生成替代｜AI 视频生成与编辑

先把中文创意拆成“起—变—落”三拍：开场让用户看懂主体，中段只发生一个动作变化，结尾留下可剪辑的稳定落点。底层依次映射 Seedance 2.5 的 t2v、i2v、r2v、edit 和 extend，不搬运即梦内部模板编号或工程参数。

## 三拍分镜卡

每个镜头写 `0–1秒看见什么 / 1–4秒发生什么 / 最后1秒停在哪里`，再补充主体锁、字幕安全区、竖屏遮挡区和禁止项。中文标题、价格与贴纸在剪辑软件中后加，不让视频模型生成易错文字。

## 五个中文短视频任务

### 1. 竖屏生活方式开场

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode t2v   --prompt '5秒9:16生活方式短片。0-1秒看见清晨厨房和一杯咖啡，1-4秒阳光缓慢移动、热气上升，最后停在干净桌面并为顶部标题留空；镜头轻微推近，不出现可读文字、品牌、人物畸变、突然切镜或多余杯子'   --param aspect_ratio=9:16 duration=5
```

### 2. 种草商品首帧

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode i2v   --first-frame ./approved-skincare-cover.png   --prompt '保持首帧护肤瓶瓶型、泵头、标签、颜色、Logo和数量。5秒内先静止展示，随后一束柔光从左向右扫过，末尾镜头轻微推近；顶部留标题区，不生成文字、功效、手、花瓣或额外商品'   --param aspect_ratio=9:16 duration=5
```

### 3. 人物与镜头参考

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode r2v   --image ./approved-character-front.png ./approved-outfit.png   --video ./authorized-handheld-rhythm.mp4   --prompt '图1锁定原创人物脸和发型，图2锁定服装；视频只参考轻微手持跟随节奏。生成她走过夜市并回头微笑的5秒竖屏镜头，不复制参考视频人物、摊位或品牌，不改变身份和服装'   --param aspect_ratio=9:16 duration=5
```

### 4. 清理现有短片

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode edit   --video ./authorized-cafe-clip.mp4   --prompt '移除画面右后方路人和墙上不可用招牌，以原环境自然补全；主角、咖啡杯、口型、动作、镜头抖动、时长和色调保持不变，不新增文字、Logo或新的路人'
```

### 5. 衔接下一拍

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode extend   --video ./approved-note-opening.mp4   --extend-direction forward   --prompt '从末帧继续3秒：主角把商品轻放到桌面，摄影机保持原速度微微下移，最后在商品正面稳定停住，为下一个卖点字幕留空；不切镜、不换人物、不改变商品包装或服装'   --param duration=3
```

## 发布前预览

在手机上模拟抖音、小红书和视频号按钮遮挡，检查前三秒能否看懂、身份与商品是否稳定、字幕区是否安全、末帧能否自然接下一镜。记录三拍卡、源素材授权、任务号和剪辑使用位置。

脚本不控制即梦或字节账号；密钥流量固定进入 `https://ai-hive.iclip.cn/api`，只暴露 Seedance 2.5 视频生成、查询、上传与初始化功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name dreamina-video-generation-alternative
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

即梦、Jimeng、Dreamina 名称只描述用户迁移意图。
