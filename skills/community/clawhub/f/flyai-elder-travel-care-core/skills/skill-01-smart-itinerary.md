---
name: skill-01-smart-itinerary-v3
title: 智能行程单生成技能 v3.0（父母视角）
description: 子女预定后自动生成结构化行程单，支持父母语音询问查看、大字体显示、语音播报。当父母询问"明天几点出发"、"航班是几点"、"司机到了吗"时使用。
author: 汪小玲 (苏英)
department: 飞猪 -CTO 线 - 技术质量 - 服务质量
version: 3.0
created_at: 2026-04-01
updated_at: 2026-04-01
tags:
  - 行程单
  - 老年友好
  - 语音交互
  - 大字体
parent_skill: flyai-core
dependencies:
  - skill-02-active-companion
---

# 智能行程单生成技能 v3.0（父母视角）

## 功能概述

**定位**：为老年人提供友好的行程查询体验，支持语音询问、大字体显示、语音播报

**核心能力**：
- ✅ 订单信息聚合（机票/酒店/当地游/接送机/旅拍）
- ✅ 行程时间轴组装与冲突检测
- ✅ **语音播报版行程单**（适合老年人收听，语速慢 20%）
- ✅ H5/长图/PDF 行程单生成（**大字体版本 18-32px 可调**）
- ✅ 子女寄语模块（支持语音转文字）
- ✅ 电子授权书生成（授权父母联系服务商）
- ✅ **一键拨打紧急联系人**（子女/服务商）
- ✅ **方言识别支持**（四川话/粤语/上海话等）

**目标用户**：**父母（老年人）**直接使用

---

## 执行步骤

### Step 1: 订单信息聚合

**调用工具**：`OrderQueryTool`、`OrderDetailParser`

```yaml
输入:
  traveler_names: array (必填，父母姓名)
  trip_status: enum (待出行/进行中/已完成)
  
输出:
  orders: array
    - order_id: string
    - type: enum (flight/hotel/tour/transfer/photo)
    - service_time: datetime
    - contact_info: object (包含服务商电话)
    - status: enum
```

**提取关键信息**：
- 机票：航班号、起降时间、航站楼、**值机柜台**
- 酒店：入住/离店时间、地址、联系电话、**附近医院**
- 当地游：集合时间地点、导游联系方式、行程安排、**紧急集合点**
- 接送机：司机姓名、车牌号、**上车地点描述**
- 其他服务：旅拍预约、租车服务等

---

### Step 2: 行程时间轴组装

**调用工具**：`ItineraryBuilder`、`WeatherForecastAPI`、`HealthFacilityLocator`

```python
# 伪代码示例
def build_elder_friendly_timeline(orders):
    timeline = []
    
    # Day 0: 出发前提醒（提前 3 天开始推送）
    timeline.append({
        'day': 0,
        'title': '出发前准备',
        'activities': [{
            'time': '出发前 1 天',
            'type': 'reminder',
            'content': get_packing_list(destination),
            'weather': get_weather_forecast(destination),
            'health_tips': get_health_tips(traveler_age),  # 新增健康提示
            'emergency_contact': get_emergency_contacts(destination)  # 新增紧急联系人
        }]
    })
    
    # 按时间顺序排列所有行程节点
    sorted_orders = sort_by_time(orders)
    
    for order in sorted_orders:
        activity = convert_to_activity(order)
        # 新增：添加安全提示
        activity['safety_tips'] = generate_safety_tips(order.type)
        timeline.append(activity)
    
    # 检测时间冲突
    conflicts = detect_conflicts(timeline)
    if conflicts:
        suggest_adjustments(conflicts)
    
    return timeline
```

---

### Step 3: 生成可分享行程单

**调用工具**：`H5PageGenerator`、`DocumentRenderer`、`QRCodeGenerator`、`VoiceSynthesizer`

**行程单内容结构**：
```yaml
Itinerary:
  basic_info:
    destination: string
    duration: string (如"5 天 4 晚")
    travelers: array (父母姓名)
    child_message: string (子女寄语，支持语音播放)
    
  daily_schedule:
    - day: integer
      date: string
      weather: object
      activities:
        - time: string
          title: string
          location: string
          description: string
          contact: string
          safety_tips: string[]
          emergency_exit: string (紧急出口/集合点)
          
  emergency_contacts:
    - name: string (子女)
      relation: string
      phone: string
    - name: string (地接社)
      role: string
      phone: string
      available_24h: boolean
    - name: string (保险公司)
      policy_no: string
      hotline: string
      
  health_facilities:
    - hospital_name: string
      distance: string (距离最近酒店)
      address: string
      phone: string
```

**老年友好设计**：
- 字体大小：默认 18px，最高 32px
- 对比度：高对比模式（黑底白字/白底黑字）
- 语音播报：每段行程可点击播放，语速比正常慢 20%
- 一键呼叫：每个联系人旁边有"打电话"按钮
- 简化布局：避免复杂图表，使用清晰的时间轴

---

### Step 4: 电子授权书生成

**调用工具**：`AuthorizationLetterGenerator`、`DigitalSignatureService`

**授权书模板**：
```
自由行服务授权书

授权人（子女）：{child_name}
身份证号：{child_id_no}

被授权人（父母）：{traveler_names}
关系：父子/母女等

授权事项：
1. 授权父母在旅行过程中直接联系机票/酒店/当地游等服务提供商
2. 授权父母在紧急情况下代表家庭做出合理决策
3. 授权 AI 助手协助父母处理行程变更、服务协调等事宜

授权有效期：{start_date} 至 {end_date}

授权人签名：{digital_signature}
日期：{current_date}

（本授权书具有法律效力，服务提供商应予以配合）
```

**生成方式**：
- 子女在行程前通过飞猪 APP 确认授权
- 生成 PDF 版本，发送至父母钉钉/微信
- 服务商可通过扫描二维码验证授权真实性

---

## 对话示例

### 场景 1：父母语音询问行程

**父母（语音）**："小飞小飞，我明天的航班是几点？"

**AI**: 
叔叔您好！您明天的航班信息如下：

✈️ **MU5801 杭州→昆明**
- 起飞时间：早上 8:30
- 到达时间：11:20
- 出发机场：杭州萧山机场 T4 航站楼
- 到达机场：昆明长水机场 T1 航站楼

🚗 **接送机安排**
- 司机王师傅会在**早上 6:30**到您家楼下等候
- 车牌号：浙 A·D12345（白色比亚迪宋）
- 上车地点：您家小区南门

💡 **温馨提示**
- 明天杭州晴天，气温 15-22℃，建议穿薄外套
- 飞机上会有点冷，建议带件厚衣服
- 早餐可以吃点清淡的，不要喝太多水

需要我再重复一遍吗？或者您想听我慢慢说？

---

### 场景 2：父母查看完整行程

**父母（语音）**："小飞，把我们这次旅行的安排说一遍"

**AI**: 
好的阿姨，我来给您详细介绍一下这次云南之旅的安排：

📅 **总共 5 天 4 晚，4 月 10 日到 4 月 14 日**

**第一天（4 月 10 日）今天**
- 早上 6:30 司机王师傅接您去机场
- 8:30 杭州飞昆明，11:20 到
- 中午在昆明吃午饭
- 下午游览石林风景区
- 晚上住昆明翠湖酒店

**第二天（4 月 11 日）明天**
- 早上 8:00 酒店大堂集合
- 坐高铁去大理，2 小时到
- 下午游览大理古城
- 晚上住大理洱海边的民宿

**第三天（4 月 12 日）**
- 上午游览洱海
- 下午参观崇圣寺三塔
- 晚上继续住大理

**第四天（4 月 13 日）**
- 早上返回昆明
- 下午自由活动
- 晚上住昆明

**第五天（4 月 14 日）回家**
- 上午在酒店休息
- 下午 15:30 昆明飞杭州
- 18:20 到家

阿姨，有什么不清楚的地方随时问我！

---

### 场景 3：子女远程查看父母行程

**子女**："帮我看看我爸妈现在到哪里了"

**AI**: 
好的，正在查询您父母的实时位置...

📍 **当前位置**：云南省大理市大理古城
🕐 **更新时间**：10 分钟前

📅 **今日行程进度**：
- ✅ 08:30 酒店出发（已完成）
- ✅ 10:00 到达大理古城（已完成）
- 🔄 10:00-12:30 游览古城（进行中）
- ⏰ 12:30 午餐（未开始）
- ⏰ 14:00 崇圣寺三塔（未开始）

👨‍🦰 **陪同人员**：
- 导游：李导游 138****5678
- 团友：8 人小团

💡 **状态**：一切正常，父母心情很好，刚才在古城拍了很多照片。

需要我帮您联系父母吗？

---

## 配置选项

### 字体设置

```yaml
font_settings:
  default_size: 18px
  max_size: 32px
  min_size: 14px
  high_contrast: true
  font_family: "PingFang SC, Heiti SC"
```

### 语音播报设置

```yaml
voice_settings:
  speed: 0.8  # 比正常慢 20%
  volume: 1.0
  dialect: "mandarin"  # 支持：mandarin/sichuanese/cantonese/shanghainese
  repeat_count: 2  # 重要信息重复 2 遍
```

### 紧急联系人配置

```yaml
emergency_contacts:
  priority_order:
    - child_primary (子女主联系人)
    - local_guide (地接导游)
    - hotel_front_desk (酒店前台)
    - insurance_hotline (保险热线)
    - emergency_services (120/110)
```

---

## 异常处理

### 常见异常场景

| 异常类型 | 处理方式 | 降级方案 |
|---------|---------|---------|
| **订单信息不完整** | 提示子女补充 | 从历史记录推断，标注"待确认" |
| **父母不会用智能手机** | 发送纸质版行程单 | 电话热线 + 短信通知 |
| **网络信号差** | 缓存离线版行程单 | 提前下载 PDF 到本地 |
| **听力障碍** | 调大音量 + 文字显示 | 子女代为接听 AI 电话 |
| **视力障碍** | 自动启用语音播报 | 超大字体（32px）+ 高对比度 |

### 错误回复模板

**信息不完整**：
```
叔叔/阿姨，我发现您的行程中有些信息还不太完整：

⚠️ 缺失信息：{missing_fields}

我已经先基于已有信息生成了行程单，不确定的地方标注了"待确认"。

我会继续联系旅行社确认详细信息，确认后第一时间告诉您。

现在您可以先看已确认的部分，好吗？
```

**网络不佳**：
```
叔叔/阿姨，现在网络信号不太好，我可能说得有点慢。

建议您：
1. 找个信号好的地方（窗边或室外）
2. 或者我可以把行程单发到您的微信，您有空的时候再看
3. 也可以让您的孩子帮您查看

您看哪种方式方便？
```

---

## 性能指标

### SLA 要求

| 指标 | 目标值 | 测量方式 |
|-----|-------|---------|
| 行程单生成时间 |<10 秒 | 端到端延迟 |
| 语音响应时间 | <2 秒 | ASR+NLP+TTS总耗时 |
| 方言识别准确率 | ≥85% | 抽样评测 |
| 大字体模式加载速度 | <3 秒 | 前端渲染时间 |
| 用户满意度 | ≥4.8 星 | 评价收集 |

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| v1.0 | 2026-04-01 | 初始版本，子女视角 |
| v2.0 | 2026-04-01 | 混合架构，增加路由 |
| v3.0 | 2026-04-01 | **重构为父母视角，新增语音交互/大字体/方言支持** |

---

**技能创建者**: 汪小玲 (苏英)  
**所属部门**: 飞猪-CTO 线 - 技术质量 - 服务质量  
**创建日期**: 2026-04-01  
**最后更新**: 2026-04-01