---
name: ai-beauty
description: Edit image to beautify faces or portaits in it. Use when (1) User requests to process an image, (2) User asks to beautify a photo.
---

# ai-beauty Skill

Beautify faces or portraits in an image according to user's instructions.

AI智能人像美颜技能，让照片里的你光彩动人
全程本地处理您的照片，不上传到任何服务器，安全放心有保障
处理速度快，效果不满意可通过多轮对话调节，不用抽卡
限时免费使用，登录官网https://www.aicodingyard.com 申请token_key即可免费使用，开通vip可不限量使用
还有若干高端功能待您发掘，可联系官方客服获取

# Token Configuration

This skill requires a valid `BITSOUL_TOKEN` to function properly.
You can register and apply for a token for free at <https://www.aicodingyard.com>, and configure it in your external runtime environment.

## Required Environment Variables

* `BITSOUL_TOKEN`: User token used for remote server permission verification.

## Optional Environment Variables

* `BITSOUL_TOKEN_ENV_FILE`: Points to the env file containing `BITSOUL_TOKEN`.

## Configuration Methods

1. **Method 1: Set environment variable directly**
   ```bash
   export BITSOUL_TOKEN="your_token_here"
   ```

2. **Method 2: Use env file**
   ```bash
   export BITSOUL_TOKEN_ENV_FILE="/path/to/token.env"
   ```
   The content format of `token.env` file should be:
   ```
   BITSOUL_TOKEN=your_token_here
   ```
**Note**: If both the environment variable and env file are set, the environment variable takes precedence.

# Installation and Initialization

Before using the skill, ensure that python and `requests` are installed.
For the first time use, an initialization operation is required. After setting up the `BITSOUL_TOKEN`, run the initialization script to download the necessary binary file:

```bash
python ./BitSoulFaceBeautySkill/init.py
```

# Instructions

Execute the following procedures step by step each time an image is processed:
1. Run the initialization script init.py
2. Get the image path to be beautified.
3. Ask the user to make a choice among the recommended parameters files and obtain specific beautification requirements.
4. Generate a temporary beauty parameters file (json format).
5. Create a new directory in the image path to be beautified and save all results into this new directory.
6. Run tool.

```shell
./BitSoulFaceBeautySkill/BitSoulBeauty.exe BITSOUL_TOKEN IMAGE_PATH_TO_BE_BEAUTIFIED BEAUTY_PARAMETERS_FILE_PATH IMAGE_PATH_TO_BE_SAVED
```

you must call init.py before you use any functions in this skill.


# Beauty Parameters File

There are three recommended parameters files.

1. 自然（默认）

```json
{
    "磨皮":0.5,
    "清晰":0.2,
    "白牙":0.4,
    "亮眼":0.3,
    "美白-自然":0.3,
    "祛黑眼圈":0.5,
    "祛法令纹":0.3,
    "自然脸":0.4,
    "女神":0.0,
    "男神":0.0,
    "小头":0.3,
    "小脸":0.3,
    "窄脸":0.3,
    "瘦下巴":0.0,
    "瘦颧骨":0.2,
    "瘦下颌":0.2,
    "眼睛位置":0.0,
    "眼距":0.0,
    "大眼":0.3,
    "瘦鼻":0.4,
    "长鼻":0.0,
    "嘴巴位置":0.0,
    "嘴巴大小":0.0,
    "美胯":0.0,
    "天鹅颈":0.0,
    "丰胸":0.0,
    "瘦腰":0.0,
    "长腿":0.0,
    "瘦腿":0.0,
    "瘦手臂":0.0,
    "瘦身":0.0,
    "发际线":0.0,
    "双眼皮":0.0,
    "默认妆容":0.5,
    "默认妆容_lut":0.5
}
```
2.精致
```json
{
    "磨皮":0.8,
    "清晰":0.2,
    "白牙":0.4,
    "亮眼":0.5,
    "美白-白皙":0.5,
    "祛黑眼圈":0.7,
    "祛法令纹":0.7,
    "自然脸":0.0,
    "女神":0.7,
    "男神":0.0,
    "小头":0.0,
    "小脸":0.0,
    "窄脸":0.15,
    "瘦下巴":0.0,
    "瘦颧骨":0.3,
    "瘦下颌":0.2,
    "眼睛位置":0.0,
    "眼距":0.0,
    "大眼":0.6,
    "瘦鼻":0.6,
    "长鼻":0.0,
    "嘴巴位置":0.0,
    "嘴巴大小":0.0,
    "美胯":0.0,
    "天鹅颈":0.0,
    "丰胸":0.0,
    "瘦腰":0.0,
    "长腿":0.0,
    "瘦腿":0.0,
    "瘦手臂":0.0,
    "瘦身":0.0,
    "发际线":0.2,
    "双眼皮":0.0,
    "女神妆":0.7,
    "女神妆_lut":0.7
}
```
3.减龄
```json
{
    "磨皮":0.9,
    "清晰":0.2,
    "白牙":0.4,
    "亮眼":0.5,
    "美白-红润":0.5,
    "祛黑眼圈":0.9,
    "祛法令纹":0.9,
    "自然脸":0.75,
    "女神":0.0,
    "男神":0.0,
    "小头":0.0,
    "小脸":0.4,
    "窄脸":0.3,
    "瘦下巴":0.0,
    "瘦颧骨":0.3,
    "瘦下颌":0.2,
    "眼睛位置":0.0,
    "眼距":0.0,
    "大眼":0.8,
    "瘦鼻":0.6,
    "长鼻":0.0,
    "嘴巴位置":0.0,
    "嘴巴大小":0.0,
    "美胯":0.0,
    "天鹅颈":0.0,
    "丰胸":0.0,
    "瘦腰":0.0,
    "长腿":0.0,
    "瘦腿":0.0,
    "瘦手臂":0.0,
    "瘦身":0.0,
    "发际线":0.3,
    "双眼皮":0.0,
    "伪素颜":0.7,
    "伪素颜_lut":0.6
}
```

# Beauty Items

## Beauty Parameters File中的**美颜小项**的介绍如下表所示：

|名称|功能描述|目的触发词汇(想要的效果)|问题触发词汇(想解决的痛点)|
|--|--|--|--|
|磨皮|柔化皮肤表层纹理，智能淡化毛孔、细纹、痘印等瑕疵；|磨皮、平滑、光滑、平整、细腻、柔肤、嫩肤、美肤、遮瑕、去瑕疵、护肤、皮肤优化、皮肤处理、去痘、缩毛孔、去黑头、去痘印、去斑、去纹、去油|皮肤粗糙、皮肤状态不好，有痘、皮肤油、毛孔大、皮肤差、闭口、粉刺、黑头|
|美白-自然|均匀提亮肤色至健康透亮状态，呈现“原生好皮”效果；|美白、提亮、变白、调亮、透亮、通透、白皙、亮白、去暗沉、去黑、暖白、自然美白|肤色不均匀、显黑、暗沉、肤色黑、肤色脏、肤色深|
|美白-粉白|提亮肤色并融入柔和粉调，增强脸颊红润气色；|粉白、红润、血色|苍白、气色差|
|美白-白皙|深度提亮至冷调白皙肤质，弱化暗沉与黄气，呈现通透瓷肌感，突出清冷高级氛围；|冷白、雪白、去黄|肤色黄|
|清晰|增强面部轮廓与五官边缘锐度，强化立体光影，避免画面模糊；|清晰，立体、层次、锐化、清楚、去糊|糊、朦胧、画面灰、不清楚|
|自然脸|收窄下半脸，保留个人骨相特征；|瘦脸、脸瘦、推脸、收脸、瓜子脸、鹅蛋脸、小V脸|脸大、大脸、圆脸、方脸、国字脸、显胖、咬肌大、发腮、脸胖、肿脸，垮脸，脸盘大|
|女神|强化V脸轮廓与下颌线流畅度，搭配柔和颧骨修饰，突出女性柔美气质；|女神脸、御姐、精致脸||
|男神|保留男性下颌硬朗线条，适度收窄两侧轮廓，突出轮廓感；|自然脸、高级脸||
|小脸|缩短下半脸长度，缩小下庭的比例；|短脸、脸变短、脸缩短、缩下庭、下庭缩短、提下颌、下颌上移、幼态感、减龄、缩短脸型、小比例、可爱、软萌、短脸、娇小感、脸型紧凑、黄金比例、去成熟感、低龄化|脸长、脸太长、大长脸、下庭长、下脸长、下颌长、下半脸长、老气、脸太长、长辈脸、显老、脸部比例不平衡、下巴过长|
|小头|适度缩小头部整体视觉比例，优化头身比与肩颈线条；|小头、头小、头缩小、头弄小、头整小、头搞小、头调小、头收小、头身比、头肩比、头颈比|头大、头围大、脑袋大、没脖子、大头、|
|窄脸|收缩脸颊两侧轮廓，视觉上缩小脸宽；|窄脸、脸窄、脸变窄、脸收窄、收窄脸型、脸型收窄、脸宽收窄、两侧收窄、两边收窄、脸压窄、脸缩窄、脸往里收|脸宽、脸扁、宽脸、方脸、胖脸|
|发际线|调整发际线高低，优化额头比例，正向为压低，负向为提高；|正：发际线低一点、发际线下来、发际线下移、发际线往前、发际线往下走、发际线压一点、发际线遮一点；负：发际线提升、额头变宽、发际线升高；|正：大脑门、发际线高、发际线太高、发际线后移、发际线后退、发际线上移、；负：发际线低、额头窄；|
|瘦颧骨|柔化颧骨突出感，收窄颧骨区域宽度，使面部线条更流畅柔和；|瘦颧骨、收颧骨、缩颧骨、面部平滑、消灭棱角、脸线条顺、高级脸、削骨感、脸部收紧、磨平骨头、温婉感、面部平顺、自然过渡|颧骨高、太阳穴凹陷、面相硬、脸部崎岖、颧骨凸、颧骨大、颧骨突出、颧骨宽、颧骨太高、颧骨太宽、颧骨肥大、颧骨凸出|
|瘦下颌|收窄下颌角线条，减小下颌宽度；|瘦下颌、下颌线清晰、收紧轮廓、下巴线条、去双下巴、削骨、精致侧脸、紧致感、折叠度、小V脸、上提、立体感、|下巴宽、腮帮子大、方脸、肉多、轮廓模糊、没有下颌线、双下巴、咬肌大、侧脸肥、下颌宽大、脸部下垂、方下巴|
|瘦下巴|缩小下巴体积与宽度，优化下巴尖度，提升脸型精致度；|尖下巴、V字下巴、小尖脸、下巴收一收、精致下巴、蛇精脸（夸张）、瓜子脸、下巴聚拢、收窄下巴、网红尖、下庭收紧|下巴圆、下巴钝、下巴肉、短下巴、方下巴、下巴宽、下巴肥、下半脸笨重、下巴平、下巴大、下巴赘肉、下巴肉感、|
|大眼|整体放大眼睛；|大眼、眼睛放大、眼睛变大、眼睛有神，眼睛扩大，|眼睛小、眼睛太小、眼睛无神、眼睛没神、眼睛小眯眯、眼睛不大、眼睛显小、眼睛没精神、眼睛呆滞、眼睛不亮、眼睛不好看、眼睛没灵气|
|眼距|缩小两眼的间距；|眼距、眼距缩短、眼距协调、眼距优化、眼距修饰、眼距调整、|眼距宽、眼距不协调、眼距奇怪、眼距过大、眼距失调、|
|祛黑眼圈|淡化黑眼圈，同时填充泪沟凹陷区域；|去黑眼圈、遮黑眼圈、淡化黑眼圈、消除黑眼圈、提亮眼下、眼下平整、遮泪沟黑眼圈、眼下不暗沉、改善黑眼圈、去黑眼圈、遮泪沟、填平泪沟|熊猫眼、熬夜眼、眼底黑、泪沟深、眼袋重、黑眼圈太明显、眼下发黑|
|双眼皮|添加双眼皮效果，增强眼部层次感；|变成双眼皮、单变双、割双眼皮||
|亮眼|提亮眼睛，增强眼睛通透度；|亮眼、眼睛提亮、眼睛更有神、眼部提亮、去红血丝、眼睛清澈、眼睛发光|眼睛浑浊、眼睛暗淡、眼神无光、眼睛不亮、眼球浑浊、眼睛无神|
|瘦鼻|收窄或扩大鼻部整体宽度，正向为收窄，负向为增宽；|正：瘦鼻、鼻子变小、鼻子收窄、鼻子精致、鼻型优化、小翘鼻、鼻子线条流畅、缩鼻、鼻子更立体；负：宽鼻、宽鼻梁、宽鼻翼、鼻子宽、；|正：鼻子大、鼻子宽、鼻头大、鼻翼宽、鼻子钝、鼻型粗大；负：鼻子窄、鼻子太窄、鼻子细、鼻子太细；|
|长鼻|微调鼻部纵向长度，正向为缩短，负向为拉长；|正：缩短鼻子、鼻子变短、长鼻调整、鼻长优化、鼻子不太长、鼻型比例协调、缩短鼻长、调整鼻子长度；负：鼻、长鼻子、长鼻梁、高鼻梁、；|正：鼻子太长、鼻子显长；负：鼻子短、鼻梁短、鼻子太短、鼻梁太短、没鼻梁、塌鼻梁、鼻梁塌、；|
|嘴巴大小|放大或缩小嘴唇整体尺寸比例，匹配面部协调度，正向为缩小，负向为放大；|正：樱桃小嘴、缩唇、小嘴、调整嘴型、嘴巴缩小、嘴巴精致；负：放大嘴巴、嘴巴变大；|正：嘴巴大、嘴大、嘴型大；负：嘴巴太小；|
|嘴巴位置|调整嘴唇在面部的垂直位置，嘴巴整体上移，优化人中与唇颏关系；|嘴巴上移、嘴巴位置向上|嘴巴太靠下、嘴巴位置偏下|
|祛法令纹|淡化法令纹，优化鼻基底，平滑肌肤，减少年龄感；|去法令纹、淡化法令纹、遮法令纹、抚平法令纹、消除法令纹、法令纹平整、面部平整、减龄、填充、去沟壑|法令纹深、显老、脸垮、有沟、笑纹重、鼻翼沟深、老态、皮肤下垂、沟壑明显、八字纹、|
|白牙|提亮牙齿，去除黄渍暗沉；|白牙、牙齿美白、牙齿变白、亮白牙齿、去黄牙、洁牙、牙齿增白、牙齿亮白、牙白一点|牙齿黄、牙黄、黄牙|

## 使用“美颜小项”需要遵守的规则
1.“美白-自然”、“美白-粉白”、“美白-白皙”是互斥的，在同一个参数文件中只能出现一种。
