# AI秘书套装 - 快速上手指南

## 🚀 5分钟快速开始

### 1. 安装 OpenClaw

确保你已经安装了 OpenClaw CLI：

```powershell
# Windows
pip install openclaw

# 验证安装
openclaw --version
```

### 2. 一键安装套装

```powershell
# 克隆套装仓库
git clone https://github.com/clawhub/ai-secretary-bundle.git
cd ai-secretary-bundle

# 安装所有依赖技能
./install.ps1
```

### 3. 配置你的信息

复制配置模板并填写：

```powershell
cp config/email-config.yaml.template config/email-config.yaml
notepad config/email-config.yaml
```

### 4. 启动你的AI秘书

```
openclaw run ai-secretary --config ./config
```

---

## 📋 常用命令速查

| 命令 | 功能 |
|------|------|
| `查看邮件摘要` | 获取未读邮件智能摘要 |
| `设置提醒 明天下午3点开会` | 创建定时提醒 |
| `今天有什么AI新闻` | 获取AI领域最新动态 |
| `我的待办` | 查看当前任务列表 |
| `开始我的一天` | 执行晨间例行流程 |

---

## 🔧 故障排除

### 邮件连接失败
- 检查邮箱服务器地址
- 确认IMAP/SMTP已开启
- 使用应用专用密码（非登录密码）

### 定时任务不执行
- 检查 cron 服务是否运行
- 确认时区设置正确
- 查看日志文件排查

### 新闻获取为空
- 检查网络连接
- 确认新闻源配置正确
- 尝试更换关键词

---

## 📚 进阶配置

详见 `SKILL.md` 获取完整配置说明和高级用法。

---

**开始使用AI秘书，让效率翻倍！** 💪
