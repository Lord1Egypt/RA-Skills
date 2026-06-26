---
name: skill-03-instant-review-v3
title: 实时评价反馈技能 v3.0（父母视角）
description: 父母用语音快速提交评价，无需打字，支持方言识别。评价直接进入产品评价列表。当服务完成后 AI 主动邀请评价或父母主动说"要评价"时使用。
author: 汪小玲 (苏英)
department: 飞猪 -CTO 线 - 技术质量 - 服务质量
version: 3.0
created_at: 2026-04-01
updated_at: 2026-04-01
tags:
  - 评价反馈
  - 语音输入
  - 老年友好
  - 方言识别
parent_skill: flyai-core
---

# 实时评价反馈技能 v3.0（父母视角）

## 功能概述

**定位**：让老年人用最自然的方式（语音）提交服务评价，无需打字，操作简单

**核心能力**：
- ✅ 服务完成自动判定（基于位置 + 时间）
- ✅ 评价邀请推送（**语音询问，非弹窗打扰**）
- ✅ **语音输入转文字评价**（支持方言识别）
- ✅ 情感分析与分级处理
- ✅ 差评预警系统（紧急问题优先处理）
- ✅ 服务商信用分更新
- ✅ **一键投诉通道**（直连平台客服）⭐

**设计原则**：
- 语音优先：全程语音交互，无需打字
- 简单直接：最多 3 个问题完成评价
- 及时响应：差评立即处理，好评即时表扬
- 保护隐私：敏感信息脱敏处理

---

## 执行步骤

### Step 1: 服务完成自动判定

**调用工具**：`ServiceCompletionDetector`、`LocationValidator`

```yaml
判定规则:
  flight:
    trigger: "航班落地后 30 分钟"
    validation: "父母已离开机场"
    
  hotel:
    trigger: "入住后第 2 天早上"
    validation: "父母已在酒店过夜"
    
  tour:
    trigger: "行程结束返回酒店后"
    validation: "GPS 显示已回到酒店"
    
  transfer:
    trigger: "接送机服务完成后 1 小时"
    validation: "司机确认送达 + 父母位置变更"
```

---

### Step 2: 评价邀请推送

**调用工具**：`VoiceCallScheduler`、`MessagePushService`

**邀请方式**（优先级从高到低）：

1. **语音外呼**（推荐）
   ```
   AI: "阿姨您好，我是小飞。今天的接送机服务已经完成了，
        您觉得怎么样？满意吗？"
   ```

2. **钉钉消息**（如未接听电话）
   ```
   【出行管家】阿姨，今天的行程结束了，想听听您的感受~
   点击收听语音消息 ▶️
   ```

3. **微信消息**（备用渠道）
   ```
   叔叔/阿姨，今天玩得开心吗？
   花 1 分钟说说您的感受吧~
   [点击开始评价]
   ```

---

### Step 3: 语音评价收集

**调用工具**：`ASRService`（方言识别）、`NLPAnalyzer`

**评价维度**（简化版）：
```yaml
rating_dimensions:
  transfer_service:
    - 准时性（司机是否准时到达）
    - 服务态度（是否热情有礼）
    - 驾驶平稳度（开车是否平稳）
    
  hotel_service:
    - 入住办理速度
    - 房间整洁度
    - 前台服务态度
    
  tour_service:
    - 导游专业度
    - 行程安排合理性
    - 餐饮质量
    
  overall:
    - 总体满意度（1-5 星）
    - 是否愿意推荐给朋友（是/否）
```

**语音转文字示例**：
```
父母（语音，四川话）："挺好的嘛，司机师傅很准时，开车也稳当"

ASR 输出: "挺好的嘛，司机师傅很准时，开车也稳当"

NLP 分析:
  sentiment: positive
  rating: 5 星
  tags: ["准时", "驾驶平稳"]
  key_phrases: ["司机师傅", "准时", "稳当"]
```

---

### Step 4: 评价提交与反馈

**调用工具**：`ReviewSubmissionAPI`、`ServiceProviderNotifier`

**提交流程**：
```python
def submit_review(traveler_id, order_id, voice_input):
    # Step 1: 语音转文字
    text = asr_service.transcribe(voice_input, dialect='auto')
    
    # Step 2: 情感分析
    sentiment = nlp.analyze_sentiment(text)
    rating = predict_rating(text)
    tags = extract_tags(text)
    
    # Step 3: 生成评价
    review = {
        'traveler_id': traveler_id,
        'order_id': order_id,
        'rating': rating,
        'comment': text,
        'tags': tags,
        'sentiment': sentiment,
        'source': 'voice',
        'dialect': detect_dialect(voice_input)
    }
    
    # Step 4: 提交评价
    result = review_api.submit(review)
    
    # Step 5: 服务商通知
    if sentiment == 'negative':
        notify_provider_urgent(result)  # 差评立即通知
    else:
        notify_provider_normal(result)  # 好评批量通知
    
    return result
```

---

## 对话示例

### 场景 1: 主动邀请评价

**AI（外呼）**：
"阿姨您好，我是小飞。今天的接送机服务已经完成了，您觉得怎么样？满意吗？"

**父母（语音）**："挺好的，司机师傅很准时，开车也稳"

**AI**: 
太好了！我帮您提交个好评可以吗？

需要特别表扬司机师傅吗？

**父母**："对，他叫王建国，人很好"

**AI**: 
好的，已为您提交 5 星好评并备注表扬王师傅！

💡 **评价详情**：
- ⭐⭐⭐⭐⭐ 5 星好评
- 📝 评价内容："司机师傅很准时，开车也稳"
- 🏷️ 标签：准时、驾驶平稳、态度好
- 👍 特别表扬：王建国师傅

感谢您的反馈！王师傅收到您的表扬一定会很开心的！

---

### 场景 2: 不满意评价处理

**AI（外呼）**：
"叔叔您好，我是小飞。昨天的酒店入住体验怎么样？还满意吗？"

**父母（语音）**："不太行，房间有点脏，空调也不制冷"

**AI**: 
叔叔，非常抱歉给您带来不好的体验。

我想详细了解几个问题：
1. 房间具体哪里比较脏？（卫生间/床铺/地面）
2. 空调是完全不能用，还是效果不好？
3. 您有没有跟酒店前台反映过这个问题？

（等待父母回答）

好的叔叔，我已经记录了您的问题。

✅ **我的处理**：
1. 已为您提交评价并标注"卫生问题"和"设施故障"
2. 我已联系酒店经理，要求他们立即整改
3. 今晚会为您更换一间房，确保干净舒适
4. 作为补偿，酒店会赠送一份果盘

您看这样处理可以吗？如果还有任何问题，随时叫我！

---

### 场景 3: 一键投诉

**父母（语音，生气）**："小飞，我要投诉！导游强制我们购物！"

**AI**: 
叔叔您别急，慢慢说。我马上帮您处理这个严重问题。

📋 **请告诉我**：
1. 是哪个导游？（姓名或电话）
2. 在哪个购物点？
3. 有没有强制消费？买了什么东西？
4. 现在您的人身安全有保障吗？

（等待父母回答）

好的叔叔，情况我已经了解了。

✅ **紧急处理措施**：
1. **立即介入**：我已通知旅行社负责人，要求立即停止强制购物
2. **安全保障**：导游小王会在 10 分钟内到您身边
3. **退款处理**：如果您购买了商品，可以全额退款
4. **投诉立案**：已为您建立投诉工单，编号{ticket_id}
5. **后续跟进**：24 小时内会有专人联系您处理赔偿事宜

💡 **维权热线**：
- 平台客服：400-xxx-xxxx（24 小时）
- 旅游监管部门：12301

叔叔，您现在先回到旅游大巴上，不要和导游发生冲突。安全第一！

---

## 配置选项

### 方言识别配置

```yaml
dialect_support:
  enabled: true
  supported_dialects:
    - mandarin (普通话)
    - sichuanese (四川话)
    - cantonese (粤语)
    - shanghainese (上海话)
    - hokkien (闽南语)
    - hakka (客家话)
    
  auto_detect: true  # 自动识别方言
  confidence_threshold: 0.75  # 识别置信度阈值
```

### 差评预警配置

```yaml
negative_review_handling:
  threshold: 3  # 3 星及以下触发预警
  
  escalation_rules:
    level_1:
      rating: 3
      action: "通知服务商改进"
      response_time: "24 小时"
      
    level_2:
      rating: 2
      action: "平台客服介入"
      response_time: "12 小时"
      
    level_3:
      rating: 1
      action: "紧急处理 + 赔偿协商"
      response_time: "2 小时"
      
  auto_compensation:
    enabled: true
    rules:
      - "卫生问题 → 房型升级/部分退款"
      - "态度问题 → 道歉 + 优惠券"
      - "强制消费 → 全额退款 + 赔偿"
```

---

## 性能指标

### SLA 要求

| 指标 | 目标值 | 测量方式 |
|-----|-------|---------|
| 语音识别准确率 | ≥90% | 方言≥85% |
| 评价提交成功率 | 100% | 端到端成功率 |
| 差评响应时间 |<2 小时 | 从提交到首次联系 |
| 投诉处理满意度 | ≥4.5 星 | 回访评分 |
| 用户评价参与率 | ≥60% | 完成评价/邀请次数 |

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| v1.0 | 2026-04-01 | 初始版本 |
| v2.0 | 2026-04-01 | 混合架构 |
| v3.0 | 2026-04-01 | **重构为父母视角，新增方言识别/一键投诉** |

---

**技能创建者**: 汪小玲 (苏英)  
**所属部门**: 飞猪 -CTO 线 - 技术质量 - 服务质量  
**创建日期**: 2026-04-01  
**最后更新**: 2026-04-01