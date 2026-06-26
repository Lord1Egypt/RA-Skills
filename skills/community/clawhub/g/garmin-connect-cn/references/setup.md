# Garmin Connect 技能配置详解

## 为什么需要 JWT Token？

Garmin Connect 使用 HTTP Bearer Token 认证，而非传统的用户名密码 API Key。每个 Token 绑定你的账号，有效期约 1 个月。

## 获取 JWT Token 步骤

### 第一步：登录 Garmin Connect

1. 打开 Chrome/Safari 浏览器
2. 访问 https://connect.garmin.cn
3. 点击右上角「登录」
4. 输入账号密码 + 手机验证码完成 MFA

### 第二步：打开开发者工具

- **macOS**: `Cmd + Option + I`
- **Windows/Linux**: `F12` 或 `Ctrl + Shift + I`

### 第三步：找到 Cookies

1. 在开发者工具顶部找到 **Application** 标签（Chrome）
2. 左侧菜单展开 **Cookies**
3. 点击 `https://connect.garmin.cn`

### 第四步：复制 JWT_WEB

1. 在 cookie 列表中找到 `JWT_WEB`
2. 点击 Value 列，会变成可编辑状态
3. 复制完整内容（以 `eyJ...` 开头）

### 第五步：验证 Token

```bash
curl --noproxy '*' -s \
  -H "Authorization: Bearer 你的Token" \
  -H "nk: NT" \
  -H "Accept: application/json" \
  "https://connect.garmin.cn/userprofile-service/userprofile/user-settings"
```

返回 JSON 数据即成功。

## Token 有效期

- JWT exp 字段标注了过期时间
- 一般有效期 **30 天**左右
- 过期后重新登录获取新 Token

## 安全提示

- ✅ JWT 是你的账号访问凭证，**不要分享给他人**
- ✅ 建议定期更换 Token
- ✅ 公开分享技能配置时，**抹掉 Token 真实值**

## 常见问题

**Q: 为什么不能直接用账号密码？**  
A: Garmin 使用 OAuth2，不支持密码模式。

**Q: httpOnly cookies 是什么？**  
A: Garmin session cookie 是 httpOnly，只能在浏览器 JS 中使用，无法通过 Python/curl 直接使用。所以用 JWT 替代。

**Q: 登录失败怎么办？**  
A: 确保使用 garmin.cn 中国站，garmin.com 国际站 API 不同。

**Q: MFA 收不到验证码？**  
A: 确保手机号与 Garmin 账号绑定一致，或尝试邮件验证码。
