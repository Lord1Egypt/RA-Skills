---
name: bce-cert
description: 百度智能云 DNS 自动申请/续期 Let's Encrypt SSL 证书技能。支持申请证书、查看状态、自动续期、Windows 计划任务配置。
metadata:
  openclaw:
    emoji: "🔐"
---

# BCE-Cert 技能

百度智能云 DNS 自动证书申请工具技能。

## 功能

- 使用百度云 DNS API 自动申请 Let's Encrypt 免费 SSL 证书
- 支持通配符证书（*.domain.com）
- 自动续期（证书到期前自动续期）
- Windows 计划任务配置
- DNS 记录自动清理

## 快速开始

### 1. 配置

复制 `config.conf.example` 为 `config.conf`，填入以下信息：

```ini
BCE_ACCESS_KEY_ID=你的AccessKey
BCE_SECRET_ACCESS_KEY=你的SecretKey
DOMAIN=你的域名（如 example.com）
EMAIL=你的邮箱
CERT_DIR=证书保存目录
```

### 2. 申请证书

```bash
python main.py issue  # 申请证书
python main.py status # 查看证书状态
python main.py renew  # 续期
python main.py force  # 强制重新申请
```

### 3. 配置自动续期

```bash
python setup_task.py install   # 注册 Windows 计划任务
python setup_task.py status    # 查看任务状态
python setup_task.py uninstall # 删除任务
```

## 代码位置

项目代码：https://gitee.com/x-hower/bce-cert

## 注意事项

1. 域名必须在百度云 DNS 托管
2. API 密钥保存在 `config.conf` 中，**不要**上传到 Git
3. Let's Encrypt 有速率限制（每周最多 5 次重复申请）
4. 测试时可设置 `STAGING=true` 使用测试环境
