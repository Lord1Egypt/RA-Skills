---
name: china-auth-integration
description: "Implement Chinese authentication systems including WeChat Login, Alipay Login, phone SMS verification, and real-name verification (实名认证). Teach AI agents how to integrate OAuth2 flows for Chinese platforms, implement phone verification with Chinese SMS providers, handle real-name verification requirements, and build unified auth interfaces. Covers: WeChat OAuth2 login (web/mini program/app), phone SMS verification (Alibaba Cloud SMS/Tencent Cloud SMS), real-name verification (ID card + face recognition), unified multi-method auth interface, and session management with Chinese compliance. Triggers on: 微信登录, wechat login, 支付宝登录, alipay login, 手机验证码, SMS verification china, 实名认证, real-name verification, 中国身份验证, china authentication, 微信OAuth, wechat oauth2, 短信验证码, SMS code verification, 统一登录, unified login, 中国用户认证, china user auth"
---

# China Auth Integration - 中国认证集成专家

You are an expert at implementing authentication systems for Chinese applications. You handle WeChat Login, Alipay Login, phone SMS verification, and real-name verification — the four pillars of Chinese user authentication.

## Core Philosophy

**In China, email/password login is secondary.** Users expect WeChat scan-to-login or phone SMS verification. If you don't support these, you lose 80% of potential users.

## Auth Method Priority

| Method | User Preference | Implementation Complexity | Trust Level |
|--------|---------------|------------------------|-------------|
| WeChat Login | ⭐⭐⭐⭐⭐ | Medium | High (verified identity) |
| Phone SMS | ⭐⭐⭐⭐ | Low | Medium (SIM-based) |
| Alipay Login | ⭐⭐⭐ | Medium | High (real-name verified) |
| Email/Password | ⭐⭐ | Low | Low (anonymous) |

## Workflow 1: WeChat OAuth2 Login

### Web Application (PC)
```
Step 1: Redirect to WeChat
  GET https://open.weixin.qq.com/connect/qrconnect?
    appid=APPID&
    redirect_uri=REDIRECT_URI&
    response_type=code&
    scope=snsapi_login&
    state=STATE

Step 2: User scans QR code with WeChat

Step 3: WeChat redirects back with code
  REDIRECT_URI?code=CODE&state=STATE

Step 4: Exchange code for access_token
  GET https://api.weixin.qq.com/sns/oauth2/access_token?
    appid=APPID&
    secret=SECRET&
    code=CODE&
    grant_type=authorization_code

Step 5: Get user info
  GET https://api.weixin.qq.com/sns/userinfo?
    access_token=ACCESS_TOKEN&
    openid=OPENID&
    lang=zh_CN
```

### Mini Program Login
```javascript
// Frontend (Mini Program)
wx.login({
  success: (res) => {
    // res.code → send to your backend
    wx.request({
      url: 'https://your-api.com/auth/wechat/miniprogram',
      method: 'POST',
      data: { code: res.code }
    })
  }
})

// Backend (Node.js)
const axios = require('axios')
async function wechatMiniProgramLogin(code) {
  // Step 1: Exchange code for session_key + openid
  const { data } = await axios.get(
    'https://api.weixin.qq.com/sns/jscode2session',
    {
      params: {
        appid: process.env.WX_APPID,
        secret: process.env.WX_SECRET,
        js_code: code,
        grant_type: 'authorization_code'
      }
    }
  )
  // data: { openid, session_key, unionid? }
  
  // Step 2: Find or create user by openid
  let user = await User.findOne({ wechatOpenid: data.openid })
  if (!user) {
    user = await User.create({ wechatOpenid: data.openid })
  }
  
  // Step 3: Generate JWT
  const token = jwt.sign({ userId: user._id }, JWT_SECRET, { expiresIn: '7d' })
  return { token, user }
}
```

### Mobile App Login
```javascript
// iOS/Android → WeChat SDK → get code → backend exchange
// Same flow as web, but uses SDK instead of QR code
// User taps "微信登录" → WeChat app opens → auto-redirect back with code
```

## Workflow 2: Phone SMS Verification

### Provider Comparison
| Provider | Price/条 | Reliability | Speed | Best For |
|----------|---------|-------------|-------|----------|
| 阿里云SMS | ¥0.045 | ⭐⭐⭐⭐⭐ | <3s | Production |
| 腾讯云SMS | ¥0.045 | ⭐⭐⭐⭐⭐ | <3s | Production |
| 华为云SMS | ¥0.04 | ⭐⭐⭐⭐ | <5s | Alternative |
| 容联云 | ¥0.04 | ⭐⭐⭐ | <5s | Budget |

### Implementation (Alibaba Cloud SMS)
```javascript
const Core = require('@alicloud/pop-core')

const client = new Core({
  accessKeyId: process.env.ALI_ACCESS_KEY,
  accessKeySecret: process.env.ALI_ACCESS_SECRET,
  endpoint: 'https://dysmsapi.aliyuncs.com',
  apiVersion: '2017-05-25'
})

async function sendSMS(phone, code) {
  const result = await client.request('SendSms', {
    PhoneNumbers: phone,        // +8613800138000
    SignName: '你的应用名',      // Must be approved
    TemplateCode: 'SMS_123456',  // Must be approved
    TemplateParam: JSON.stringify({ code })
  }, { method: 'POST' })
  
  return result.Code === 'OK'
}

// Rate limiting: 1 SMS per minute per phone, 5 per hour
const smsLimiter = {
  window: 60,        // seconds
  maxPerWindow: 1,
  maxPerHour: 5,
  maxPerDay: 10
}
```

### Verification Flow
```javascript
// 1. Generate 6-digit code
function generateCode() {
  return Math.floor(100000 + Math.random() * 900000).toString()
}

// 2. Store in Redis with TTL
await redis.setex(`sms:${phone}`, 300, code)  // 5 min TTL

// 3. Verify
async function verifyCode(phone, inputCode) {
  const storedCode = await redis.get(`sms:${phone}`)
  if (!storedCode) return { valid: false, reason: 'expired' }
  if (storedCode !== inputCode) return { valid: false, reason: 'wrong' }
  await redis.del(`sms:${phone}`)  // One-time use
  return { valid: true }
}
```

## Workflow 3: Real-Name Verification (实名认证)

### Two-Factor Verification
```
Level 1: ID card number + name (基础实名)
  → Check against public security database
  → Cost: ¥0.8-2.0 per check
  → Providers: 阿里云/腾讯云/百度云

Level 2: ID card + face recognition (增强实名)
  → ID check + liveness detection + face comparison
  → Cost: ¥1.5-5.0 per check
  → Required for: financial, healthcare, education apps
```

### Implementation
```javascript
// Level 1: ID Card Verification (阿里云)
async function verifyIdCard(name, idNumber) {
  const client = new Core({ /* ... */ })
  const result = await client.request('VerifyIdCard', {
    Name: name,        // 张三
    IdCardNumber: idNumber  // 110101199001011234
  })
  return result.Result === '1'  // 1=match, 0=no match
}

// Level 2: Face Recognition (腾讯云)
async function verifyFace(idCardImage, selfieImage) {
  const result = await tencentCloudClient.request('CompareFace', {
    ImageA: idCardImage,  // Base64 ID card photo
    ImageB: selfieImage,  // Base64 selfie
    QualityControl: 1     // Enable quality check
  })
  return result.Similarity > 80  // >80 = same person
}
```

### When Real-Name is Required
| Scenario | Level Required | Regulation |
|----------|---------------|------------|
| Social features (comment/post) | Level 1 | 网络安全法 |
| Financial services | Level 2 | 金融监管 |
| Healthcare | Level 2 | 医疗法规 |
| Education | Level 1 | 教育部规定 |
| E-commerce (seller) | Level 1 | 电商法 |
| Live streaming (host) | Level 2 | 网信办规定 |
| Gaming (anti-addiction) | Level 1 | 版署规定 |

## Workflow 4: Unified Multi-Method Auth Interface

```javascript
// Unified auth endpoint
router.post('/auth/:method', async (req, res) => {
  const { method } = req.params
  
  switch (method) {
    case 'wechat':
      // WeChat OAuth2 flow
      return handleWechatLogin(req, res)
    
    case 'phone':
      // SMS verification
      return handlePhoneLogin(req, res)
    
    case 'alipay':
      // Alipay OAuth2 flow
      return handleAlipayLogin(req, res)
    
    default:
      return res.status(400).json({ error: 'Unsupported method' })
  }
})

// Account linking: same user can have multiple auth methods
// User schema:
{
  phone: '+8613800138000',
  wechatOpenid: 'oXXXX',
  wechatUnionid: 'uXXXX',   // Cross-app identity
  alipayUserId: '2088XXXX',
  realNameVerified: false,
  realNameLevel: 0           // 0=none, 1=ID, 2=ID+face
}
```

## Safety Rules

1. **Never store SMS codes in database** — use Redis with TTL only
2. **Rate limit SMS** — 1/min, 5/hour, 10/day per phone number
3. **Encrypt ID numbers** — never store in plaintext
4. **Session security** — use httpOnly + secure + sameSite cookies
5. **WeChat session_key** — never expose to frontend, use for data decryption only
6. **Phone format** — always include country code (+86) for international compatibility
7. **Compliance** — PIPL requires separate consent for collecting ID/phone data
8. **Audit log** — log all auth events for security review

## Quick Reference

| Auth Method | Prerequisites | Key API | User Data Returned |
|-------------|-------------|---------|-------------------|
| WeChat Web | MP account + 网页授权 | open.weixin.qq.com/connect/qrconnect | openid, nickname, avatar |
| WeChat Mini | Mini Program | jscode2session | openid, unionid |
| Phone SMS | SMS provider account | SendSms API | phone number only |
| Alipay | 支付宝开放平台 | alipay.system.oauth.token | user_id, avatar |
| Real-name L1 | Cloud provider | VerifyIdCard | match/no-match |
| Real-name L2 | Cloud provider | CompareFace | similarity score |
