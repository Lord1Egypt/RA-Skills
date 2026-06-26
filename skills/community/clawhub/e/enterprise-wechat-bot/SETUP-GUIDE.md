# 企业微信开发者账号注册指南

**目标**: 获取测试环境 Webhook Key  
**预计时间**: 15-30 分钟

---

## 📋 注册步骤

### 步骤 1: 访问企业微信

网址：https://work.weixin.qq.com

### 步骤 2: 立即注册

1. 点击"立即注册"
2. 选择"企业创建"
3. 填写企业信息:
   - 企业名称 (可用个人名义)
   - 管理员姓名
   - 手机号
   - 验证码

### 步骤 3: 登录管理后台

1. 使用管理员账号登录
2. 进入管理后台

### 步骤 4: 创建自建应用

1. 管理后台 → 应用管理
2. 点击"应用" → "自建"
3. 点击"创建应用"
4. 填写应用信息:
   - 名称：WeChat Automation
   - 图标：默认即可
   - 描述：自动化消息推送

### 步骤 5: 添加机器人

1. 进入创建的应用
2. 找到"机器人"功能
3. 点击"添加机器人"
4. 填写机器人信息:
   - 名称：AutoBot
   - 描述：自动回复机器人

### 步骤 6: 获取 Webhook Key

1. 机器人创建成功后
2. 复制 Webhook URL
3. 提取 Key 参数

**URL 格式**:
```
https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                              这就是 Key
```

---

## 🧪 测试连接

```bash
# 测试消息发送
curl -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "测试消息，如果收到说明配置成功"
    }
  }'
```

**预期响应**:
```json
{
  "errcode": 0,
  "errmsg": "ok"
}
```

---

## 📝 记录认证信息

创建 `.env` 文件保存:

```bash
# 企业微信配置
WECHAT_CORPID=your_corpid
WECHAT_CORPSECRET=your_corpsecret
WECHAT_AGENT_ID=your_agent_id
WECHAT_WEBHOOK_KEY=your_webhook_key
```

**⚠️ 安全提示**: 不要将 `.env` 文件提交到 Git!

---

## 🔧 开发环境准备

### 必需工具
- [x] curl (已安装)
- [ ] jq (可选，JSON 处理)
- [ ] Node.js (可选，高级功能)

### 可选工具
```bash
# 安装 jq (JSON 处理)
sudo apt-get install -y jq

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## 📚 下一步

1. ✅ 完成账号注册
2. ✅ 获取 Webhook Key
3. ⏳ 测试消息发送
4. ⏳ 开发 MVP 原型

---

**创建时间**: 2026-03-29 18:30  
**状态**: 准备执行
