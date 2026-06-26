# 部署到 ClawHub - 指南

## 🚀 方式 1：通过 Web 界面部署（推荐）

由于当前环境无法打开浏览器，请手动通过 Web 界面部署：

### 步骤

1. **访问 ClawHub**
   ```
   https://clawhub.com/publish
   ```

2. **准备上传文件**
   将整个文件夹打包：
   ```bash
   cd /root/.openclaw/workspace
   zip -r bsc-dev-monitor-skill.zip bsc-dev-monitor-skill/
   ```

3. **填写 Skill 信息**

   - **名称**: bsc-dev-monitor
   - **描述**: BSC Dev Wallet Monitor - 监控指定地址的代币转出
   - **版本**: 1.0.0
   - **价格**: 0.01 USDT / 次
   - **分类**: Crypto / Trading / Monitor

4. **上传文件**
   - 上传 `bsc-dev-monitor-skill.zip` 或整个文件夹

5. **提交审核**
   - 填写完成后点击提交
   - 等待审核通过（通常 1-2 小时）

6. **发布成功**
   - 审核通过后 Skill 将自动发布
   - 用户可以搜索安装

---

## 🔧 方式 2：通过 CLI 部署（需要登录）

### 步骤 1：登录 ClawHub

```bash
clawhub login
```

这会打开浏览器进行认证。请：

1. 复制浏览器地址栏的链接
2. 在你的本地电脑上打开该链接
3. 完成登录
4. 将登录凭证复制回服务器

或者使用手动 token 登录：
```bash
clawhub login --token YOUR_TOKEN_HERE
```

### 步骤 2：发布 Skill

```bash
cd /root/.openclaw/workspace/bsc-dev-monitor-skill
clawhub publish .
```

### 步骤 3：验证发布

```bash
clawhub list
```

查找 `bsc-dev-monitor` 是否在列表中。

---

## 📦 方式 3：使用 API 部署（高级）

```bash
# 1. 打包
cd /root/.openclaw/workspace
zip -r bsc-dev-monitor-skill.zip bsc-dev-monitor-skill/

# 2. 上传到服务器
curl -X POST https://api.clawhub.com/v1/skills \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -F "file=@bsc-dev-monitor-skill.zip" \
  -F "name=bsc-dev-monitor" \
  -F "version=1.0.0" \
  -F "price=0.01" \
  -F "currency=USDT"
```

---

## 🎯 推荐操作

### 在 Web 界面操作（最简单）

1. 访问 https://clawhub.com/publish
2. 下载 `/root/.openclaw/workspace/bsc-dev-monitor-skill/` 文件夹
3. 在浏览器中上传
4. 填写 Skill 信息
5. 提交审核

### 使用本地 CLI

如果你有本地环境：

```bash
# 1. 在服务器上打包
cd /root/.openclaw/workspace
tar -czf bsc-dev-monitor-skill.tar.gz bsc-dev-monitor-skill/

# 2. 下载到本地
# 使用 scp、rsync 或其他方式下载

# 3. 在本地发布
tar -xzf bsc-dev-monitor-skill.tar.gz
cd bsc-dev-monitor-skill
clawhub publish .
```

---

## 📝 Skill 信息

准备好以下信息：

| 项目 | 内容 |
|------|------|
| **名称** | bsc-dev-monitor |
| **版本** | 1.0.0 |
| **描述** | BSC Dev Wallet Monitor - 监控指定地址的代币转出行为 |
| **价格** | 0.01 USDT / 次 |
| **支付** | SkillPay.me |
| **分类** | Crypto / Trading / Monitor |
| **适用人群** | 跟投 Dev 的用户 |

---

## ✅ 部署前检查

- [x] 所有文件已准备完毕
- [x] SKILL.md 配置正确
- [x] 支付设置正确（0.01 USDT）
- [x] 代码测试通过
- [x] 文档完整

---

## 🔗 相关链接

- **ClawHub 发布页面**: https://clawhub.com/publish
- **Skill 文档**: https://docs.clawhub.com/publish
- **SkillPay 文档**: https://docs.skillpay.me

---

**准备就绪，可以发布到 ClawHub！** 🚀
