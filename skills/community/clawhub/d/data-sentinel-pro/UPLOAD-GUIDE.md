# 📤 Data Sentinel Pro - 上传指南

## ✅ 已准备好的文件

**发布包：** `/home/admin/.openclaw/workspace/skills/data-sentinel-pro-v1.0.0.zip`  
**大小：** 6.2 KB  
**内容：**
```
SKILL.md              - 技能文档（已更新为你的邮箱和官网）
package.json          - 包配置（作者：Anson <ai.agent.anson@qq.com>）
crontab-example.txt   - Cron 示例
scripts/monitor.py    - 核心监控脚本
```

## 🔧 已修改内容

| 项目 | 原值 | 新值 |
|------|------|------|
| 📧 支持邮箱 | support@datascntinel.pro | ai.agent.anson@qq.com |
| 🌐 官网 | https://datascntinel.pro | https://asmartglobal.com |
| 👤 作者 | OpenClaw Skills | Anson <ai.agent.anson@qq.com> |
| 📚 文档链接 | docs.datascntinel.pro | github.com/anson125chen/data-sentinel-pro |

---

## 📤 上传步骤（ClawHub 网页）

### 1️⃣ 登录 ClawHub
打开 https://clawhub.com 并登录你的 GitHub 账号

### 2️⃣ 创建新技能
- 点击右上角 **"Create Skill"** 或 **"New Skill"**
- 或者访问：https://clawhub.com/skills/new

### 3️⃣ 填写基本信息

| 字段 | 填写内容 |
|------|----------|
| **Name** | `data-sentinel-pro` |
| **Display Name** | `Data Sentinel Pro` |
| **Version** | `1.0.0` |
| **Description** | `7x24 小时监控网页、商品价格、竞对动态，变化即通知` |
| **Tags** | `monitoring, alert, web-scraper, price-tracker` |

### 4️⃣ 上传文件
- 点击 **"Upload ZIP"** 或拖拽文件
- 选择：`/home/admin/.openclaw/workspace/skills/data-sentinel-pro-v1.0.0.zip`

### 5️⃣ 提交审核
- 点击 **"Publish"** 或 **"Submit for Review"**
- 等待安全扫描（1-2 分钟）

---

## 🔍 上传后验证

上传成功后检查：
- ✅ VirusTotal 扫描：应该是 "Clean"
- ✅ OpenClaw 扫描：无 "Suspicious" 警告
- ✅ 技能页面正常显示
- ✅ 可以复制安装命令

---

## 📋 安装命令（上传成功后）

用户安装你的技能：
```bash
openclaw skills install anson125chen/data-sentinel-pro
```

---

## ⚠️ 如果安全扫描仍有警告

1. 点击警告中的 **"Details"** 查看具体问题
2. 常见问题：
   - 缺少依赖声明 → 更新 package.json
   - 脚本路径不匹配 → 检查 SKILL.md 中的路径
   - 明文凭据 → 确保使用 `<YOUR_XXX>` 占位符

3. 修复后重新上传新版本（v1.0.1）

---

## 📞 需要帮助？

- ClawHub 文档：https://docs.clawhub.com
- Discord 社区：https://discord.com/invite/clawd
- 技能作者：Anson <ai.agent.anson@qq.com>

---

**准备时间：** 2026-04-04 13:45  
**技能版本：** v1.0.0  
**作者：** Anson @ Jiufang Intelligent (Shenzhen)
