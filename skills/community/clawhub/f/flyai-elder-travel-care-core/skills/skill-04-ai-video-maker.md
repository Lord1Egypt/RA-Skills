---
name: skill-04-ai-video-maker-v3
title: AI 旅行视频制作技能 v3.0（父母视角）
description: 父母无需操作，AI 自动收集旅拍照片 + 行程中的精彩瞬间，一键生成纪念视频。支持语音旁白、大字版相册。当旅行结束时 AI 主动制作并发送给父母。
author: 汪小玲 (苏英)
department: 飞猪 -CTO 线 - 技术质量 - 服务质量
version: 3.0
created_at: 2026-04-01
updated_at: 2026-04-01
tags:
  - AI 视频
  - 老年友好
  - 自动制作
  - 语音旁白
parent_skill: flyai-core
---

# AI 旅行视频制作技能 v3.0（父母视角）

## 功能概述

**定位**：父母无需任何操作，AI 自动收集素材、智能剪辑、生成纪念视频，让老年人轻松拥有美好回忆

**核心能力**：
- ✅ **素材自动聚合**（旅拍成片 + 服务商提供的照片 + 公开天气/景点素材）
- ✅ 模板推荐引擎（**老年友好：经典怀旧风格优先**）
- ✅ 人脸识别与质量筛选
- ✅ AI 智能剪辑（叙事结构 + 配乐）
- ✅ **语音旁白自动生成**（子女录制或 AI 合成）⭐
- ✅ 多平台一键分享（微信/抖音/钉钉）
- ✅ 旅行足迹地图生成
- ✅ **大字版相册**（方便父母在手机上反复观看）⭐

**设计原则**：
- 零操作：父母无需上传任何照片
- 自动推送：视频完成后主动发送给父母
- 简单分享：一键转发到微信群/朋友圈
- 情感优先：突出温馨、感动、成就感

---

## 执行步骤

### Step 1: 素材自动聚合

**调用工具**：`MaterialCollector`、`PhotoQualityAnalyzer`

**素材来源**（按优先级排序）：

```yaml
material_sources:
  professional_photos:
    source: "旅拍摄影师"
    expected_count: 30-100 张
    quality: "高清专业级"
    examples:
      - "机场出发合影"
      - "景点打卡照"
      - "全家福"
      - "活动抓拍"
      
  service_provider_photos:
    source: "地接社/导游/司机"
    expected_count: 10-50 张
    quality: "手机拍摄"
    examples:
      - "团集合照"
      - "用餐场景"
      - "活动花絮"
      
  public_materials:
    source: "公开素材库"
    type: "景点官方图片/天气预报图/地图轨迹"
    examples:
      - "大理古城航拍图"
      - "洱海风景照"
      - "行程足迹地图"
      
  user_uploaded (可选):
    source: "父母自己拍的照片"
    note: "非必需，如有则自动同步"
```

**智能筛选规则**：
```python
def filter_photos(all_photos):
    selected = []
    
    for photo in all_photos:
        # 质量检查
        if not check_quality(photo):  # 模糊/过曝/过暗
            continue
            
        # 人脸检测
        faces = detect_faces(photo)
        if not faces:
            continue
            
        # 确保包含父母
        if not recognize_traveler(faces):
            continue
            
        # 去重（相似照片只选最佳）
        if is_duplicate(photo, selected):
            continue
            
        selected.append(photo)
    
    return selected[:50]  # 精选 50 张
```

---

### Step 2: 模板推荐

**调用工具**：`TemplateRecommender`、`MusicSelector`

**推荐策略**：
```yaml
template_recommendation:
  factors:
    - destination (目的地风格匹配)
    - season (季节色彩匹配)
    - traveler_age (老年友好：经典怀旧优先)
    - trip_type (休闲/探险/文化)
    
  recommended_templates:
    classic_nostalgic:
      name: "岁月如歌"
      style: "经典怀旧"
      music: "《光阴的故事》《童年》"
      transition: "缓慢柔和"
      suitable_for: "60 岁以上"
      
    warm_family:
      name: "温馨时光"
      style: "家庭温馨"
      music: "《相亲相爱一家人》"
      transition: "温暖治愈"
      suitable_for: "全家出游"
      
    scenic_beauty:
      name: "大美中国"
      style: "风光纪录片"
      music: "《彩云之南》《青藏高原》"
      transition: "大气磅礴"
      suitable_for: "自然风光"
```

**老年友好设计**：
- 字体大：字幕最小 24px
- 节奏慢：每个镜头 3-5 秒
- 配色暖：避免过于刺眼的颜色
- 音乐熟：选择耳熟能详的经典老歌

---

### Step 3: AI 智能剪辑

**调用工具**：`VideoEditor`、`VoiceSynthesizer`、`SubtitleGenerator`

**叙事结构**：
```yaml
video_structure:
  opening:
    duration: "10 秒"
    content: "封面 + 标题 + 出行人员"
    example: "「彩云之南」张父李母的云南之旅 2026.4.10-4.14"
    
  chapter_1_departure:
    title: "出发啦"
    duration: "30 秒"
    content: "机场合影、登机、到达"
    
  chapter_2_highlights:
    title: "精彩瞬间"
    duration: "2-3 分钟"
    content: "按时间顺序展示各景点游玩"
    chapters:
      - "昆明·石林"
      - "大理·洱海"
      - "丽江·古城"
      
  chapter_3_emotions:
    title: "感动时刻"
    duration: "30 秒"
    content: "笑容特写、温馨互动、全家福"
    
  closing:
    title: "期待下次旅行"
    duration: "15 秒"
    content: "返程 + 子女祝福语音 + 结束语"
```

**语音旁白生成**：
```python
def generate_voiceover(template, child_id):
    # 方式 1: 子女录制
    if child_records_voice():
        audio = get_child_recording(child_id)
        
    # 方式 2: AI 合成（用子女声音克隆）
    elif child_cloned_voice_exists(child_id):
        script = generate_script(template)
        audio = tts_synthesize(script, voice_clone=child_id)
        
    # 方式 3: AI 合成（标准播音腔）
    else:
        script = generate_script(template)
        audio = tts_synthesize(script, voice='warm_female')
    
    return audio
```

---

### Step 4: 视频发布与分享

**调用工具**：`VideoPublisher`、`SocialShareService`

**发布流程**：
```python
def publish_video(video):
    # Step 1: 生成多个版本
    versions = {
        'full': video,  # 完整版 3-5 分钟
        'highlights': trim_to_1min(video),  # 精华版 1 分钟
        'photo_album': generate_photo_book(video)  # 静态相册版
    }
    
    # Step 2: 发送给父母
    send_to_travelers(versions)
    
    # Step 3: 发送给子女
    send_to_children(versions)
    
    # Step 4: 提供分享入口
    share_links = {
        'wechat': generate_wechat_link(video),
        'douyin': generate_douyin_link(video),
        'dingtalk': generate_dingtalk_link(video)
    }
    
    return share_links
```

**分享文案模板**：
```
【我的云南之旅】🌈

我和老伴的云南自由行圆满结束啦！
感谢儿女的精心安排，玩得特别开心！

📍 去了：昆明·大理·丽江
📸 拍了：200+ 张照片
🎬 制作了：精美纪念视频

点击观看我们的旅行故事 👇
[视频链接]

#自由行 #云南旅行 #退休生活
```

---

## 对话示例

### 场景 1: AI 主动推送视频

**AI（外呼）**：
"叔叔阿姨您好，我是小飞。告诉您一个好消息！

🎉 **您的云南之旅纪念视频已经制作完成啦！**

视频包含了：
- 📸 旅拍摄影师拍的 45 张精美照片
- 🎥 地接社提供的 12 张活动花絮
- 🗺️ 您的旅行足迹地图
- 🎵 配乐《月光下的凤尾竹》
- 🎙️ 还有您儿子录制的祝福语音

视频时长 4 分 30 秒，已经发送到您的微信和钉钉。

现在方便看一下吗？我可以教您怎么观看和分享。"

---

### 场景 2: 指导父母观看视频

**父母**："小飞，我怎么打开看啊？"

**AI**: 
叔叔别急，我一步步教您：

**如果您用微信**：
1. 打开微信
2. 找到"飞猪出行管家"公众号
3. 点击最新推送的消息
4. 就能看到的视频啦！

**如果您用钉钉**：
1. 打开钉钉
2. 找到"小飞"的聊天窗口
3. 点击我发给您的视频卡片
4. 就能播放了

您先试试看，如果找不到，我让您的孩子远程帮您。

看到了吗？视频开头就是您二人在机场的合影呢！

---

### 场景 3: 指导父母分享视频

**父母**："我想把这个发到朋友圈，怎么弄？"

**AI**: 
太好了！我来教您：

1. 在视频播放页面，找到右下角的"..."三个点
2. 点击后选择"分享到朋友圈"
3. 我已经帮您写好了一段文字，您可以直接用
4. 然后点击"发表"就完成啦！

需要我让孙女远程教您吗？她可以跟您视频通话，一步一步带着您操作。

或者您也可以直接回复"好的"，我自动帮您分享到微信朋友圈。

---

## 配置选项

### 视频模板配置

```yaml
video_templates:
  elderly_friendly:
    font_size: 24px  # 大字体
    pace: "slow"  # 慢节奏
    music_style: "classic"  # 经典老歌
    color_scheme: "warm"  # 暖色调
    
  default_duration: "3-5 分钟"
  highlight_version: "1 分钟"
  
  aspect_ratios:
    - 16:9 (横屏，适合电视播放)
    - 9:16 (竖屏，适合手机观看)
    - 1:1 (正方形，适合朋友圈)
```

### 音乐库配置

```yaml
music_library:
  classic_chinese:
    - "《月光下的凤尾竹》"
    - "《彩云之南》"
    - "《青藏高原》"
    - "《茉莉花》"
    
  nostalgic:
    - "《光阴的故事》"
    - "《童年》"
    - "《外婆的澎湖湾》"
    
  family_warm:
    - "《相亲相爱一家人》"
    - "《常回家看看》"
    - "《让爱住我家》"
```

---

## 性能指标

### SLA 要求

| 指标 | 目标值 | 测量方式 |
|-----|-------|---------|
| 视频生成时间 | <10 分钟 | 从素材收集到完成 |
| 人脸识别准确率 | ≥95% | 确保包含父母 |
| 音乐版权合规率 | 100% | 使用正版授权音乐 |
| 用户满意度 | ≥4.8 星 | 评价收集 |
| 分享率 | ≥70% | 分享视频/收到视频 |

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| v1.0 | 2026-04-01 | 初始版本 |
| v2.0 | 2026-04-01 | 混合架构 |
| v3.0 | 2026-04-01 | **重构为父母视角，新增零操作/语音旁白/大字版** |

---

**技能创建者**: 汪小玲 (苏英)  
**所属部门**: 飞猪 -CTO 线 - 技术质量 - 服务质量  
**创建日期**: 2026-04-01  
**最后更新**: 2026-04-01