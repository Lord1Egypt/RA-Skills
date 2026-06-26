# email-163-com v1.0.4 发布指南

**创建日期**: 2026-04-11  
**目标平台**: ClawHub

---

## 📦 准备文件

**位置**: `/tmp/email-163-com-1.0.4-fixed.zip`

**包含文件**:
```
email-163-com/
├── main.py                 # 主程序
├── email-163-com          # CLI wrapper ✅ 新增
├── INSTALL.sh             # 安装脚本 ✅ 新增
├── package.json           # 添加凭证声明 ✅ 更新
├── _meta.json             # 添加来源信息 ✅ 更新
├── SECURITY.md            # 安全说明 ✅ 新增
├── SKILL.md               # 技能说明
├── README.md              # 使用指南
├── INSTALL.md             # 安装指南
└── TEST-REPORT.md         # 测试报告 ✅ 更新
```

---

## 🚀 发布步骤

### 方法 1: 使用 ClawHub CLI（推荐）

#### 步骤 1: 登录 ClawHub

```bash
# 启动浏览器登录
clawhub login

# 浏览器会自动打开 https://clawhub.ai/cli/auth
# 完成认证后返回终端
```

#### 步骤 2: 验证登录

```bash
clawhub whoami
# 应显示你的用户信息
```

#### 步骤 3: 发布技能

```bash
cd /tmp/email-163-com
clawhub publish .
```

或者从压缩包发布：

```bash
# 解压到临时目录
cd /tmp
unzip email-163-com-1.0.4-fixed.zip
cd email-163-com
clawhub publish .
```

#### 步骤 4: 填写发布信息

系统会提示填写：
- **版本**: 1.0.4
- **发布说明**: 使用 `PUBLISH-NOTES.md` 中的内容
- **分类**: email, productivity, tools
- **标签**: 163, email, imap, smtp, netease

#### 步骤 5: 确认发布

```bash
# 查看发布状态
clawhub skill list

# 查看技能详情
clawhub inspect email-163-com
```

---

### 方法 2: 通过 ClawHub 网站

#### 步骤 1: 访问 ClawHub

打开浏览器访问：https://clawhub.com/skills/publish

#### 步骤 2: 登录

使用你的 ClawHub 账号登录

#### 步骤 3: 上传技能包

- 点击 "Upload New Skill"
- 选择文件：`/tmp/email-163-com-1.0.4-fixed.zip`
- 填写发布信息

#### 步骤 4: 填写元数据

```yaml
Name: email-163-com
Version: 1.0.4
Description: 163 邮箱完整邮件管理工具
Author: OpenClaw
License: MIT
Category: Productivity
Tags:
  - email
  - 163
  - netease
  - imap
  - smtp
  - mail
```

#### 步骤 5: 填写发布说明

复制 `PUBLISH-NOTES.md` 的内容

#### 步骤 6: 提交审核

- 确认所有信息正确
- 点击 "Submit for Review"
- 等待审核通过（通常 24-48 小时）

---

## 📋 发布清单

发布前检查：

- [x] 所有文件已更新
- [x] Security Scan 问题已修复
- [x] 测试通过
- [x] 文档完整
- [ ] ClawHub 登录
- [ ] 提交发布
- [ ] 审核通过

---

## 🔍 发布后验证

### 验证 1: 搜索技能

```bash
clawhub search email-163-com
```

### 验证 2: 安装测试

```bash
# 在新环境中安装
clawhub install email-163-com

# 验证安装
email-163-com --help
email-163-com read --count 5
```

### 验证 3: 查看 Security Scan

访问 ClawHub 上的技能页面，检查 Security Scan 状态：
- VirusTotal: 应显示扫描结果
- OpenClaw: 应显示 "Verified" 或 "Safe"

---

## ⚠️ 常见问题

### 问题 1: 发布失败 - "Not logged in"

**解决**:
```bash
clawhub login
# 完成浏览器认证
```

### 问题 2: 发布失败 - "Skill already exists"

**解决**:
```bash
# 更新现有技能
clawhub publish . --update
```

### 问题 3: Security Scan 仍然显示 Suspicious

**解决**:
1. 等待 VirusTotal 扫描完成（约 5-10 分钟）
2. 检查 `package.json` 中的 `security` 字段
3. 确保 `SECURITY.md` 已包含

### 问题 4: 安装后 CLI 不工作

**解决**:
```bash
# 检查软链接
ls -la ~/.local/bin/email-163-com

# 重新安装
clawhub uninstall email-163-com
clawhub install email-163-com
```

---

## 📞 支持

- **ClawHub 文档**: https://docs.clawhub.com
- **GitHub Issues**: https://github.com/openclaw/skills/issues
- **Discord**: https://discord.gg/clawhub

---

**准备完成时间**: 2026-04-11 19:36  
**等待操作**: 登录 ClawHub 并发布  
**预计审核时间**: 24-48 小时
