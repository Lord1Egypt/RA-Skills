# 🔒 安全承诺书

## 我们的承诺

**我们靠订阅赚钱，不卖用户数据。**

这不是口号，是写入代码的原则。

---

## 📋 安全审计清单

### ✅ 代码透明

- [x] 全部代码开源在 GitHub
- [x] 无隐藏的后门或恶意代码
- [x] 无未声明的外部 API 调用
- [x] 接受社区审计

### ✅ 数据安全

- [x] 用户百度 Token 本地加密存储
- [x] 不上传任何用户文件到我们的服务器
- [x] 不收集用户使用数据
- [x] 不追踪用户行为

### ✅ 网络安全

- [x] 仅调用百度官方 API（pan.baidu.com）
- [x] 使用 HTTPS 加密传输
- [x] 无第三方 SDK 或跟踪代码
- [x] 无广告或推广内容

---

## 🔍 数据流向说明

```
用户电脑 ←→ 百度网盘 API (pan.baidu.com)
    ↑
    └── 本 Skill（仅转发，不存储）
```

**我们看不到**：
- 你的百度网盘内容
- 你的百度账号密码
- 你的文件下载/上传记录

**我们只知道**（如果你选择分享）：
- 订阅状态（是否付费用户）
- 基础使用统计（可选，用于改进产品）

---

## 📂 本地存储详情

### Token 存储位置
```
~/.config/configstore/baidu-netdisk-skill.json
```

### 加密方式
- **算法**：AES-256-CBC
- **密钥来源**：使用 `crypto-js` 内置密钥派生
- **存储格式**：加密后的 Base64 字符串

### 验证方法
```bash
# 查看存储文件（Token 已加密）
cat ~/.config/configstore/baidu-netdisk-skill.json

# 监控网络请求（确认只调用百度 API）
mitmproxy -p 8080
npx baidu-netdisk-skill list /
# 应该只看到 pan.baidu.com 的请求
```

---

## 🛡️ 技术安全措施

### 1. Token 加密存储

用户的百度 Access Token 使用 AES-256 加密，存储在本地配置文件中。

```javascript
// 加密存储，密钥由用户密码派生
const encrypted = crypto.encrypt(token, userPassword);
```

### 2. 最小权限原则

我们只申请必要的 API 权限：
- `basic` - 获取用户信息
- `netdisk` - 文件读写

**不申请**：
- 百度账号的其他权限
- 通讯录、消息等无关权限

### 3. 代码签名

每个 Release 版本都有 GPG 签名，用户可以验证：

```bash
gpg --verify baidu-netdisk-skill-0.1.0.tar.gz.sig
```

### 4. 依赖审计

所有 npm 依赖都经过安全扫描：

```bash
npm audit
```

无高危漏洞才发布。

---

## 📢 如何验证我们的承诺

### 方法 1：自己审计代码

```bash
# 克隆代码
git clone https://github.com/你的用户名/baidu-netdisk-skill

# 查看核心逻辑
cat src/baidu-api.js
cat src/auth.js

# 检查外部调用
grep -r "http" src/
```

### 方法 2：自己编译

```bash
# 不信任我们发布的包？自己 build
npm install
npm run build
```

### 方法 3：网络监控

```bash
# 运行抓包，看 Skill 调用了哪些域名
mitmproxy -p 8080
npx baidu-netdisk-skill list /
```

应该只看到 `pan.baidu.com` 的请求。

---

## 🚨 安全事件响应

如果发现任何安全问题：

1. **立即邮件**：security@yourdomain.com
2. **24 小时内**：我们回复确认
3. **72 小时内**：修复并发布公告
4. **公开致谢**：给发现者（如果愿意）

---

## 📜 法律承诺

本 Skill 受 MIT License 保护，但附加以下条款：

1. **不得用于非法目的**（盗版、侵权等）
2. **不得逆向工程我们的付费验证逻辑**
3. **不得转售 API 额度**

违反者我们将追究法律责任。

---

## 🙋 常见问题

**Q: 你们能看到我的文件吗？**  
A: 不能。所有操作都在你的本地完成，我们只是调用百度官方 API。

**Q: 我的百度账号安全吗？**  
A: 安全。我们使用 OAuth 2.0 授权，不存储你的账号密码。

**Q: 如果百度 API 改了怎么办？**  
A: 我们会及时更新 Skill，订阅用户免费升级。

**Q: 你们怎么赚钱？**  
A: 订阅费。用户付月费，我们提供技术支持和 API 额度管理。

---

**最后更新**：2026-03-12  
**版本**：0.1.0
