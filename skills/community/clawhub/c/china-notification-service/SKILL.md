---
name: china-notification-service
description: "Implement multi-channel notification services for Chinese applications using WeChat Template Messages, WeChat Subscription Messages, SMS (Alibaba Cloud/Tencent Cloud), DingTalk Bot, Feishu Bot, and Email. Teach AI agents how to build unified notification dispatch systems, handle rate limits, implement priority-based routing, and ensure delivery compliance. Covers: unified notification dispatch interface, WeChat template/subscription messages, SMS via Chinese cloud providers, enterprise IM bot notifications (DingTalk/Feishu), and notification compliance and rate limiting. Triggers on: 中国通知服务, china notification service, 微信模板消息, wechat template message, 微信订阅消息, wechat subscription message, 短信通知, SMS notification china, 钉钉机器人通知, dingtalk bot notification, 飞书机器人通知, feishu bot notification, 多渠道通知, multi-channel notification, 通知分发, notification dispatch, 消息推送, message push china, 通知合规, notification compliance"
---

# China Notification Service - 中国通知服务专家

You are an expert at building multi-channel notification systems for Chinese applications. You handle the unique challenges of notification delivery in China: WeChat message limits, SMS provider integration, and enterprise IM bot configuration.

## Core Philosophy

**One notification, multiple channels, smart routing.** Different messages need different delivery channels. Urgent → SMS + DING. Important → WeChat + Feishu. Informational → Email + DingTalk. You build the routing logic.

## Channel Comparison

| Channel | Delivery Guarantee | Speed | Cost | Best For |
|---------|-------------------|-------|------|----------|
| SMS | ⭐⭐⭐⭐⭐ | <5s | ¥0.04/条 | Verification codes, urgent alerts |
| WeChat Template | ⭐⭐⭐⭐ | <10s | Free | Order updates, status changes |
| WeChat Subscribe | ⭐⭐⭐ | <10s | Free | Content updates, reminders |
| DingTalk Bot | ⭐⭐⭐⭐ | <3s | Free | Team notifications, alerts |
| Feishu Bot | ⭐⭐⭐⭐ | <3s | Free | Team notifications, reports |
| Email | ⭐⭐ | <30s | Free | Reports, newsletters, receipts |

## Workflow 1: Unified Notification Dispatch

### Architecture
```
App Event → Notification Service → Channel Router → Channel Adapter → User
                                      ↓
                              Priority Check
                              Rate Limiter
                              Compliance Check
                              Template Engine
```

### Implementation
```javascript
class NotificationService {
  constructor() {
    this.channels = {
      sms: new SMSChannel(),
      wechat_template: new WeChatTemplateChannel(),
      wechat_subscribe: new WeChatSubscribeChannel(),
      dingtalk: new DingTalkBotChannel(),
      feishu: new FeishuBotChannel(),
      email: new EmailChannel()
    }
  }

  async send(notification) {
    const { userId, type, priority, channels, template, data } = notification
    
    // 1. Check rate limits
    await this.checkRateLimit(userId, type)
    
    // 2. Resolve user channel preferences
    const targetChannels = this.resolveChannels(userId, priority, channels)
    
    // 3. Render template with data
    const rendered = await this.renderTemplate(template, data)
    
    // 4. Send to each channel
    const results = await Promise.allSettled(
      targetChannels.map(ch => this.channels[ch].send(userId, rendered))
    )
    
    // 5. Log delivery status
    await this.logDelivery(userId, type, results)
    
    return results
  }

  resolveChannels(userId, priority, preferredChannels) {
    // Priority-based routing
    if (priority === 'urgent') return ['sms', 'dingtalk', 'feishu']
    if (priority === 'high') return ['wechat_template', 'dingtalk']
    if (priority === 'normal') return preferredChannels || ['wechat_template', 'email']
    if (priority === 'low') return ['email']
    
    return preferredChannels || ['wechat_template']
  }
}
```

## Workflow 2: WeChat Template Messages

### Setup
1. 登录 mp.weixin.qq.com → 模板消息
2. 选择或创建模板（需审核）
3. 获取 template_id

### Send Template Message
```javascript
async function sendWeChatTemplate(openid, templateId, data) {
  const accessToken = await getAccessToken()
  
  const result = await axios.post(
    `https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=${accessToken}`,
    {
      touser: openid,
      template_id: templateId,
      // url: 'https://your-app.com/order/123',  // Optional click URL
      // miniprogram: { appid: 'xxx', pagepath: 'pages/index' },  // Or mini program
      data: {
        first: { value: '您有一笔新订单', color: '#173177' },
        keyword1: { value: data.orderId },
        keyword2: { value: data.productName },
        keyword3: { value: data.amount },
        keyword4: { value: data.time },
        remark: { value: '点击查看详情' }
      }
    }
  )
  
  return result.data.errcode === 0
}
```

### WeChat Subscription Messages (Mini Program)
```javascript
// 1. Request user subscription (frontend)
wx.requestSubscribeMessage({
  tmplIds: ['template_id_1', 'template_id_2'],
  success: (res) => {
    // res['template_id_1'] === 'accept' | 'reject'
  }
})

// 2. Send subscription message (backend)
async function sendSubscribeMessage(openid, templateId, page, data) {
  const accessToken = await getAccessToken()
  
  return axios.post(
    `https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=${accessToken}`,
    {
      touser: openid,
      template_id: templateId,
      page: page,  // 'pages/order/detail?id=123'
      data: {
        thing1: { value: data.productName },  // 20 chars max
        amount2: { value: data.amount },
        time3: { value: data.time },
        thing4: { value: data.remark }        // 20 chars max
      }
    }
  )
}
```

### ⚠️ WeChat Limits
- Template messages: No limit on count, but users must have interacted in last 48h
- Subscription messages: User must explicitly subscribe (one-time consent)
- Each subscription = one message send (must re-subscribe for next)

## Workflow 3: SMS via Chinese Cloud Providers

### Alibaba Cloud SMS
```javascript
const Core = require('@alicloud/pop-core')

const client = new Core({
  accessKeyId: process.env.ALI_ACCESS_KEY,
  accessKeySecret: process.env.ALI_ACCESS_SECRET,
  endpoint: 'https://dysmsapi.aliyuncs.com',
  apiVersion: '2017-05-25'
})

async function sendSMS(phone, signName, templateCode, templateParam) {
  return client.request('SendSms', {
    PhoneNumbers: phone,
    SignName: signName,           // Must be pre-approved
    TemplateCode: templateCode,   // Must be pre-approved
    TemplateParam: JSON.stringify(templateParam)
  }, { method: 'POST' })
}

// Examples
await sendSMS('+8613800138000', '我的应用', 'SMS_123456', { code: '123456' })
await sendSMS('+8613800138000', '我的应用', 'SMS_789012', { name: '张三', amount: '99.00' })
```

### Tencent Cloud SMS
```javascript
const tencentCloud = require('tencentcloud-sdk-nodejs')
const smsClient = tencentCloud.sms.v20210111.Client

const client = new smsClient({
  credential: {
    secretId: process.env.TC_SECRET_ID,
    secretKey: process.env.TC_SECRET_KEY
  },
  region: 'ap-guangzhou'
})

async function sendSMS(phone, templateId, params) {
  return client.SendSms({
    SmsSdkAppId: process.env.TC_SMS_APP_ID,
    SignName: '我的应用',
    TemplateId: templateId,
    TemplateParamSet: params,
    PhoneNumberSet: [`+86${phone}`]
  })
}
```

## Workflow 4: Enterprise IM Bot Notifications

### DingTalk Bot (Webhook)
```javascript
async function sendDingTalk(webhookUrl, message) {
  // Text message
  await axios.post(webhookUrl, {
    msgtype: 'text',
    text: { content: message }
  })
  
  // Markdown message
  await axios.post(webhookUrl, {
    msgtype: 'markdown',
    markdown: {
      title: 'Alert Title',
      text: '## Alert\n\n**Service**: API Server\n**Status**: Down\n**Time**: 2026-05-26 18:00'
    }
  })
  
  // ActionCard message
  await axios.post(webhookUrl, {
    msgtype: 'actionCard',
    actionCard: {
      title: 'Order Alert',
      text: 'New order received!',
      btnOrientation: '1',
      singleTitle: 'View Order',
      singleURL: 'https://your-app.com/orders/123'
    }
  })
}
```

### Feishu Bot (Webhook)
```javascript
async function sendFeishu(webhookUrl, message) {
  // Text message
  await axios.post(webhookUrl, {
    msg_type: 'text',
    content: { text: message }
  })
  
  // Rich text (post) message
  await axios.post(webhookUrl, {
    msg_type: 'post',
    content: {
      post: {
        zh_cn: {
          title: 'Alert Title',
          content: [
            [{ tag: 'text', text: 'Service: ' }, { tag: 'text', text: 'API Server' }],
            [{ tag: 'text', text: 'Status: ' }, { tag: 'text', text: 'Down' }],
            [{ tag: 'a', text: 'View Details', href: 'https://your-app.com' }]
          ]
        }
      }
    }
  })
}
```

## Workflow 5: Notification Compliance & Rate Limiting

### Rate Limit Rules
```javascript
const RATE_LIMITS = {
  sms: {
    per_user_per_minute: 1,
    per_user_per_hour: 5,
    per_user_per_day: 10,
    per_app_per_second: 50
  },
  wechat_template: {
    per_user_per_day: 100,    // WeChat limit
    per_app_per_day: 100000   // Account-level limit
  },
  wechat_subscribe: {
    per_user_per_template: 1, // One per subscription
    per_template_per_day: 100000
  },
  dingtalk: {
    per_bot_per_minute: 20,
    per_bot_per_hour: 500
  },
  feishu: {
    per_bot_per_minute: 50,
    per_bot_per_hour: 1000
  },
  email: {
    per_user_per_day: 5,
    per_app_per_minute: 100
  }
}
```

### Compliance Checklist
- [ ] SMS content pre-approved by provider (签名+模板审核)
- [ ] WeChat templates pre-approved by platform
- [ ] Unsubscribe mechanism for marketing messages
- [ ] No marketing SMS before 8:00 or after 21:00
- [ ] User consent recorded before sending
- [ ] Delivery status logged for audit
- [ ] Rate limits enforced per channel per user

## Safety Rules

1. **Never send marketing SMS without consent** — PIPL requirement
2. **Always check rate limits** — exceeding limits gets your account suspended
3. **Template approval first** — WeChat and SMS templates must be pre-approved
4. **Fallback channels** — if primary channel fails, try secondary
5. **Idempotency** — same notification should not be sent twice
6. **Sensitive data** — never include full ID/phone in notification content
7. **Test with sandbox** — always test in sandbox before production

## Quick Reference

| Channel | Setup Time | Cost | Limit | Best For |
|---------|-----------|------|-------|----------|
| SMS | 1-3 days | ¥0.04/条 | 1/min/user | Verification, urgent |
| WeChat Template | 1-3 days | Free | 100/day/user | Status updates |
| WeChat Subscribe | 1-3 days | Free | 1/sub | Reminders |
| DingTalk Bot | 5 min | Free | 20/min | Team alerts |
| Feishu Bot | 5 min | Free | 50/min | Team reports |
| Email | 1 day | Free | 100/min | Reports, receipts |
