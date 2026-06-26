---
name: ecommerce-bundle
version: 1.0.0
description: |
  电商运营套装 - 智能电商助手，让店铺运营更轻松。整合竞品监控、自动回复、评价管理、选品分析四大能力。24小时在线客服，数据驱动选品。定价¥199/套。
---

# 电商运营套装 (E-commerce Bundle)

> 智能电商助手，让店铺运营更轻松

## 💼 套装定位

专为电商卖家、运营人员和 dropshipper 打造，整合竞品监控、自动回复、评价管理和选品分析四大核心能力，实现店铺智能化运营。

---

## 🎯 包含技能

### 1. 竞品监控 (spider / firecrawl-search / browser-automation)
- **功能**：价格监控、库存追踪、活动监测
- **适用场景**：竞品动态追踪、市场变化预警
- **价值**：第一时间掌握竞品动向

### 2. 自动回复 (wechat-management / message / qqbot-cron)
- **功能**：客户咨询自动回复、常见问题解答、售后处理
- **适用场景**：客服减负、快速响应
- **价值**：24小时在线客服

### 3. 评价管理 (browser-automation / agent-browser)
- **功能**：评价抓取、情感分析、差评预警
- **适用场景**：口碑监控、问题及时发现
- **价值**：维护店铺评分

### 4. 选品分析 (tavily-search / research / akshare-stock)
- **功能**：市场趋势分析、热销商品发现、利润测算
- **适用场景**：选品决策、市场进入
- **价值**：数据驱动选品

---

## 📦 套装内容

```
ecommerce-bundle/
├── SKILL.md                      # 本文件 - 套装总览
├── config/
│   ├── competitors.yaml          # 竞品监控配置
│   ├── auto-reply.yaml           # 自动回复话术
│   ├── review-monitor.yaml       # 评价监控配置
│   └── product-research.yaml     # 选品分析配置
├── examples/
│   ├── competitor-alert.md       # 竞品监控示例
│   ├── customer-service.md       # 客服场景示例
│   └── product-analysis.md       # 选品分析示例
└── README.md                     # 快速上手指南
```

---

## 🚀 快速开始

### 第一步：安装技能

```powershell
# 竞品监控
py -m clawhub install spider
py -m clawhub install firecrawl-search
py -m clawhub install browser-automation

# 自动回复
py -m clawhub install wechat-management
py -m clawhub install qqbot-cron

# 评价管理
py -m clawhub install agent-browser

# 选品分析
py -m clawhub install tavily-search
py -m clawhub install research
```

### 第二步：配置监控目标

编辑 `config/competitors.yaml`：

```yaml
competitors:
  - name: "竞品店铺A"
    platform: "taobao"
    shop_id: "123456"
    products:
      - id: "prod-001"
        name: "竞品爆款商品"
        url: "https://item.taobao.com/item.htm?id=xxx"
        monitor:
          - price
          - stock
          - sales
          - promotions
    alert_channels:
      - "wechat"
      - "email"
  
  - name: "竞品店铺B"
    platform: "jd"
    shop_id: "789012"
    monitor_frequency: "hourly"
```

---

## 💡 典型使用场景

### 场景1：竞品价格监控

```
用户：监控竞品A的价格变化

电商助手：
✅ 已设置竞品监控

📊 监控目标：
   店铺：竞品店铺A
   平台：淘宝
   监控商品：5款
   监控频率：每小时

🔔 预警规则：
   • 价格下降超过5% → 立即通知
   • 库存低于100件 → 预警
   • 新活动上线 → 通知

📈 当前数据快照：
   商品1：¥199（库存：523件）
   商品2：¥299（库存：189件）⚠️
   商品3：¥159（库存：892件）

监控已启动，有变动会第一时间通知您！
```

### 场景2：智能客服回复

```
用户：帮我设置自动回复

电商助手：
✅ 已配置智能客服系统

💬 自动回复场景：

1. 欢迎语
   触发：客户首次咨询
   回复："您好！欢迎光临XX店铺，我是您的专属客服小助手。请问有什么可以帮您？"

2. 发货时间
   触发：包含"多久发货"
   回复："亲，我们承诺48小时内发货，一般下单后24小时就能发出哦~"

3. 尺码咨询
   触发：包含"尺码""大小"
   回复："亲可以参考详情页的尺码表，建议按平时尺码选择。不确定的话告诉我身高体重，我帮您推荐~"

4. 售后问题
   触发：包含"退货""换货"
   回复："亲，我们支持7天无理由退换货。如有问题请联系人工客服，会第一时间为您处理~"

5. 催单
   触发：包含"还没发货"
   回复："亲，我帮您查一下订单状态...[自动查询] 您的订单已经在打包中，预计今天发出！"

📊 今日客服数据：
   • 自动回复：47次
   • 转人工：12次
   • 平均响应时间：3秒
```

### 场景3：评价监控预警

```
用户：查看最近的评价情况

电商助手：
📊 评价监控报告（最近7天）

━━━━━━━━━━━━━━━━━━━━━
📈 数据概览
━━━━━━━━━━━━━━━━━━━━━

总评价数：+156条
好评率：94.2% ⬆️ (+2.1%)
平均评分：4.8/5.0

━━━━━━━━━━━━━━━━━━━━━
⭐ 好评亮点（TOP 3）
━━━━━━━━━━━━━━━━━━━━━

1. "质量很好，物流很快！"（32次提及）
2. "客服态度好，解决问题快"（28次提及）
3. "性价比高，会回购"（24次提及）

━━━━━━━━━━━━━━━━━━━━━
⚠️ 差评预警（3条需关注）
━━━━━━━━━━━━━━━━━━━━━

🔴 紧急处理（1条）
   用户：@买家XXX
   评分：⭐
   内容："收到商品破损，客服不理人"
   时间：2小时前
   建议：立即联系客户，安排补发

🟡 需关注（2条）
   • 物流慢问题（2条类似反馈）
   • 尺码偏小（3条类似反馈）

━━━━━━━━━━━━━━━━━━━━━
💡 改进建议
━━━━━━━━━━━━━━━━━━━━━

1. 加强包装防护，减少破损率
2. 详情页增加尺码对照说明
3. 与物流沟通提升配送速度

需要我帮您回复差评吗？
```

### 场景4：选品分析

```
用户：帮我分析这个品类是否值得做

电商助手：
📊 选品分析报告：智能家居

━━━━━━━━━━━━━━━━━━━━━
🔍 市场概况
━━━━━━━━━━━━━━━━━━━━━

市场规模：¥2,500亿（年增长率23%）
竞争程度：中等偏高
进入门槛：中等

━━━━━━━━━━━━━━━━━━━━━
📈 趋势分析
━━━━━━━━━━━━━━━━━━━━━

🔥 上升品类：
   • 智能门锁（+45%）
   • 扫地机器人（+38%）
   • 智能窗帘（+52%）

📉 下降品类：
   • 智能音箱（-12%）
   • 普通插座（-8%）

━━━━━━━━━━━━━━━━━━━━━
💰 利润分析
━━━━━━━━━━━━━━━━━━━━━

品类              毛利率    竞争度    建议
智能门锁          35-45%    高        ⭐⭐⭐
扫地机器人        25-35%    极高      ⭐⭐
智能窗帘          40-50%    中        ⭐⭐⭐⭐
智能开关          30-40%    中高      ⭐⭐⭐

━━━━━━━━━━━━━━━━━━━━━
🎯 推荐选品
━━━━━━━━━━━━━━━━━━━━━

**首选：智能窗帘**
理由：
✓ 增长率高（+52%）
✓ 利润率好（40-50%）
✓ 竞争相对较小
✓ 售后问题少

**备选：智能门锁**
理由：
✓ 市场需求大
✓ 客单价高
⚠️ 但竞争激烈，需要差异化

━━━━━━━━━━━━━━━━━━━━━
⚠️ 风险提示
━━━━━━━━━━━━━━━━━━━━━

• 需要3C认证
• 安装服务要求高
• 售后维护成本

需要我深入分析某个具体品类吗？
```

---

## ⚙️ 配置模板

### 竞品监控配置

```yaml
# config/competitors.yaml
monitoring:
  enabled: true
  frequency: "hourly"  # hourly, daily, weekly
  
competitors:
  - name: "竞品店铺A"
    platform: "taobao"
    shop_url: "https://shop123456.taobao.com"
    products:
      - name: "爆款商品1"
        url: "https://item.taobao.com/item.htm?id=xxx"
        monitor_fields:
          - price
          - stock
          - sales_count
          - promotion
        alert_rules:
          - type: "price_drop"
            threshold: 5  # 降价5%预警
            channel: "wechat"
          - type: "stock_low"
            threshold: 100
            channel: "email"
  
  - name: "竞品店铺B"
    platform: "jd"
    shop_url: "https://mall.jd.com/index-xxx.html"
    monitor_fields:
      - price
      - reviews
```

### 自动回复话术配置

```yaml
# config/auto-reply.yaml
auto_reply:
  enabled: true
  working_hours:
    start: "09:00"
    end: "23:00"
  outside_hours_message: "您好，当前为非工作时间，您的留言会在上班后第一时间处理~"
  
rules:
  - name: "欢迎语"
    priority: 1
    triggers:
      - "首次咨询"
      - "hello"
      - "在吗"
    response: |
      您好！欢迎光临{shop_name}🎉
      
      我是您的智能客服助手，可以帮您：
      • 查询商品信息
      • 了解优惠活动
      • 处理售后问题
      
      请问有什么可以帮您？
  
  - name: "发货时间"
    priority: 2
    triggers:
      - "多久发货"
      - "什么时候发货"
      - "发货时间"
    response: |
      亲，我们承诺48小时内发货📦
      
      • 16:00前下单，当天发出
      • 16:00后下单，次日发出
      • 预售商品以页面标注时间为准
      
      您可以点击"我的订单"查看物流信息~
  
  - name: "退换货"
    priority: 3
    triggers:
      - "退货"
      - "换货"
      - "退款"
    response: |
      亲，我们支持7天无理由退换货✅
      
      退换货流程：
      1. 点击"申请售后"
      2. 选择退货/换货原因
      3. 等待审核（24小时内）
      4. 按地址寄回商品
      
      如有疑问，可以转人工客服处理~
```

---

## 💰 定价与价值

| 项目 | 传统方案 | 电商套装 |
|------|----------|----------|
| 竞品监控 | 人工查看3小时/天 | 自动监控实时预警 |
| 客服回复 | 2名客服¥6000/月 | AI客服24小时在线 |
| 评价管理 | 人工统计2小时/天 | 自动分析实时预警 |
| 选品分析 | 购买数据¥2000/月 | AI分析即时生成 |
| 月度成本 | ¥8000+ | **¥199** |

**套装定价：¥199/套（一次性购买，终身使用）**

---

## 🛠️ 技术要求

- OpenClaw >= 2.0
- Windows 10/11 或 macOS 或 Linux
- 电商平台账号权限
- 网络连接

---

## 📞 售后支持

- 文档：https://docs.clawhub.com/ecommerce
- 社区：加入飞书群获取更新
- 更新：购买后终身免费更新

---

*让AI成为你的电商运营合伙人。*
