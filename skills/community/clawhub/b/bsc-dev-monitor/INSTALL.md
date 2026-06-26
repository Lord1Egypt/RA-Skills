# BSC Dev Monitor Skill - 安装指南

## 📦 快速安装

### 通过 ClawHub 安装

```bash
# 使用 ClawHub CLI
clawhub install bsc-dev-monitor

# 或者直接在 https://clawhub.com 上搜索安装
```

## 🧪 本地测试

### 1. 安装依赖

```bash
cd /root/.openclaw/workspace/bsc-dev-monitor-skill
npm install
```

### 2. 运行测试

```bash
# 测试监控 60 秒
npm test

# 或
node index.js 0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4 60
```

### 3. 查看输出

```
📥 收到请求: {"action":"monitor","address":"0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4","duration":60}
🔍 开始监控地址: 0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4
⏱️  监控时长: 60 秒
🌐 网络: BSC
📦 起始区块: 84770000
✅ 监控已启动，按 Ctrl+C 停止
```

## 💰 支付测试

### 模拟支付流程

```javascript
// 生成支付链接
const { generatePaymentLink } = require('./index.js');

const paymentLink = generatePaymentLink('user123', 'http://localhost:3000/callback');
console.log('支付链接:', paymentLink);
```

### 验证支付

```javascript
// 验证支付状态
const { verifyPayment } = require('./index.js');

verifyPayment('user123', 'payment_id_here')
  .then(result => console.log('验证成功:', result))
  .catch(error => console.error('验证失败:', error));
```

## 📊 使用示例

### 基本使用

```javascript
const { handleRequest } = require('./index.js');

// 发起监控请求
handleRequest({
  action: 'monitor',
  address: '0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4',
  duration: 3600,
  payment_verified: true,
  user_id: 'your_user_id',
  callback_url: 'http://your-server.com/callback'
});
```

### 处理支付请求

```javascript
const response = await handleRequest({
  action: 'monitor',
  address: '0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4',
  user_id: 'user123',
  callback_url: 'http://your-server.com/callback'
});

if (response.status === 'payment_required') {
  // 返回支付链接给用户
  console.log('请支付:', response.payment_link);
}
```

## ⚙️ 配置说明

### SkillPay API Key

当前使用的 API Key:
```
sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5
```

### 价格设置

- 每次调用: 0.001 USDT
- 支持的货币: USDT

## 🔧 故障排查

### 常见问题

1. **无法连接到 BSC RPC**
   - 检查网络连接
   - 尝试更换 RPC 节点
   - 参考 BSC 官方文档

2. **支付验证失败**
   - 检查 API Key 是否正确
   - 确认 SkillPay 服务状态
   - 查看 SkillPay 文档

3. **监控无响应**
   - 检查目标地址是否正确
   - 确认网络类型（BSC）
   - 查看日志文件

## 📞 获取帮助

- 查看 README.md 了解详细说明
- 查看 DEPLOY.md 了解部署流程
- 访问 https://clawhub.com 获取社区支持

---

祝使用愉快！🎉
