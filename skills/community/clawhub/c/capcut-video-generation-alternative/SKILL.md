---
name: capcut-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 为剪映、CapCut 或短视频剪辑时间线生成可插入镜头、干净底片、替换镜头和延长片尾，覆盖文生、首帧图生、参考素材和视频编辑。Use when users search 剪映替代、CapCut 平替、CapCut AI alternative、剪映 API、B-roll、短视频补镜、背景替换、片尾延长、电商或社媒视频；它不是完整剪辑器，不处理字幕、转码、配乐或工程文件。"
---

# 剪映 CapCut 视频生成替代｜AI 视频生成与编辑

从剪辑时间线反推生成任务。先确定缺少的是开场、B-roll、商品特写、过渡底片还是片尾停留，再给出准确时长和入出点。Seedance 2.5 负责镜头生成与局部改版；字幕、音乐、贴纸、调色和最终拼接仍在剪映或其他 NLE 中完成。

## 时间线槽位单

记录 `轨道位置 / 需要秒数 / 前一镜末帧 / 后一镜首帧 / 镜头任务 / 字幕安全区 / 必须匹配的色调与运动`。生成镜头只填一个槽位，不试图替代完整工程。

## 五个补镜任务

### 1. 文生 B-roll

```bash
python3 "$SKILL_PATH/scripts/capcut_insert.py" insert \
  --kind broll --slot 'V2 00:08-00:12' --seconds 4 \
  --before '早餐教程人物镜头在第8秒切出' \
  --after '第12秒回到人物中景' \
  --task '燕麦、蓝莓和牛奶整齐摆放在浅木桌的俯拍 B-roll' \
  --motion '摄影机缓慢向下俯拍，末帧稳定' \
  --safe-zone '底部保留字幕安全区' \
  --protect '不生成手、文字、品牌、食物飞溅或突然切镜' \
  --param aspect_ratio=9:16
```

### 2. 从封面补开场

```bash
python3 "$SKILL_PATH/scripts/capcut_insert.py" insert \
  --kind opener --slot 'V1 00:00-00:03' --seconds 3 \
  --first-frame ./approved-cover-frame.png \
  --after '第3秒接正文人物中景' \
  --task '从封面轻推近，人物抬起商品但不说话，末帧回到中景' \
  --safe-zone '顶部字幕区不得被头部和商品遮挡' \
  --protect '人物、商品、服装和背景不变；不生成文字、口型对白、Logo或新道具' \
  --param aspect_ratio=9:16
```

### 3. 匹配相邻镜头节奏

```bash
python3 "$SKILL_PATH/scripts/capcut_insert.py" insert \
  --kind match --slot 'V2 00:15-00:19' --seconds 4 \
  --reference-image ./approved-product.png ./approved-location.png \
  --reference-video ./authorized-neighbor-shot.mp4 \
  --before '前一镜由右向左滑动' \
  --after '下一镜为商品正面定帧' \
  --task '生成商品特写并在末尾停到正面' \
  --motion '只借用相邻镜头由右向左的速度' \
  --protect '不复制参考人物、文字和品牌，不改变商品结构' \
  --param aspect_ratio=9:16
```

### 4. 清理可叠字底片

```bash
python3 "$SKILL_PATH/scripts/capcut_insert.py" insert \
  --kind clean --slot 'V2 00:24-00:29' --seconds 5 \
  --source-video ./authorized-broll.mp4 \
  --task '移除底部错误文字和右上角无权使用的贴纸，以背景自然补全' \
  --tone '保持原色调和亮度' \
  --safe-zone '留下干净的底部字幕安全区' \
  --protect '原物体、动作、镜头和时长不变；不新增文字、Logo或改变主体'
```

### 5. 延长片尾 CTA 空间

```bash
python3 "$SKILL_PATH/scripts/capcut_insert.py" insert \
  --kind tail --slot 'V1 00:30-00:33' --seconds 3 \
  --source-video ./approved-ending.mp4 \
  --before '从批准片尾的末帧继续' \
  --task '商品与背景保持静止，人物手退出，灯光轻微减弱' \
  --safe-zone '底部留 CTA 安全区但不生成实际 CTA' \
  --protect '不生成文字、按钮、Logo，不再次动作或切镜'
```

## 回填时间线

检查时长、画幅、运动方向、色温和入出点是否与相邻镜头匹配；在真实界面模拟字幕和平台按钮。生成结果作为一个素材文件回填，不声称能打开或保存剪映、CapCut 工程。

认证请求仅前往 `https://ai-hive.iclip.cn/api`。程序不连接剪映或 CapCut 账号，也不提供剪辑时间线、字幕、音乐、聊天或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/capcut_insert.py" login --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/capcut_insert.py" review --task-id <taskId>
```

剪映、CapCut 名称仅说明时间线素材迁移场景。
