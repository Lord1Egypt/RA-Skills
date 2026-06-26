# BCE-Cert: 百度智能云 DNS 自动证书申请工具

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

纯 Python 实现的 SSL 证书自动申请和续期工具，通过 Let's Encrypt (ACME v2) 获取免费证书，使用百度云 DNS API 进行域名验证。

## ✨ 特性

- 🔐 **免费证书** - 通过 Let's Encrypt 获取免费 SSL 证书
- 🔄 **自动续期** - 证书到期前自动续期（默认提前 30 天）
- 🌐 **通配符支持** - 自动申请 `example.com` 和 `*.example.com`
- 🪟 **纯 Windows** - 无需 WSL、Cygwin 或 acme.sh
- ⏰ **计划任务** - 支持 Windows 计划任务，每天自动检查
- 🔧 **可扩展** - 支持续期后执行自定义命令

## 📁 项目结构

```
bce-cert/
├── config.conf.example   # 配置文件模板（复制为 config.conf 使用）
├── main.py               # 主入口：申请/续期/状态查看
├── acme_client.py        # ACME v2 协议客户端
├── bce_dns.py            # 百度云 DNS API 操作
├── scheduler.py          # 定时检查调度器
├── setup_task.py         # Windows 计划任务注册
├── requirements.txt      # Python 依赖
└── README.md             # 本文件
```

## 🚀 快速开始

### 前置条件

1. **Python 3.8+** - 确保已安装 Python
2. **百度云账号** - 域名需在百度智能云 DNS 托管
3. **API 密钥** - 从百度云控制台获取 Access Key

### 第一步：克隆项目

```bash
git clone https://github.com/你的用户名/bce-cert.git
cd bce-cert
```

### 第二步：安装依赖

```bash
pip install -r requirements.txt
```

或使用国内镜像加速：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 第三步：配置

```bash
# 复制配置模板
copy config.conf.example config.conf  # Windows
# cp config.conf.example config.conf  # Linux/macOS

# 编辑配置文件，填入真实信息
notepad config.conf  # Windows
# nano config.conf   # Linux/macOS
```

配置项说明：

| 参数 | 必填 | 说明 |
|------|:----:|------|
| `BCE_ACCESS_KEY_ID` | ✅ | 百度云 Access Key ID |
| `BCE_SECRET_ACCESS_KEY` | ✅ | 百度云 Secret Access Key |
| `DOMAIN` | ✅ | 主域名（如 `example.com`） |
| `EMAIL` | ✅ | 邮箱（Let's Encrypt 账号） |
| `CERT_DIR` | ✅ | 证书保存目录 |
| `RENEW_DAYS` | — | 提前多少天续期（默认 30） |
| `DNS_TTL` | — | TXT 记录 TTL（默认 300） |
| `DNS_PROPAGATION_WAIT` | — | DNS 传播等待时间（默认 30） |
| `RENEW_HOOK` | — | 续期后执行的命令 |

### 第四步：申请证书

```bash
# 首次申请
python main.py issue

# 查看证书状态
python main.py status
```

申请成功后，证书文件保存在 `CERT_DIR` 目录：

| 文件 | 用途 |
|------|------|
| `example.com.key` | 私钥 |
| `example.com.crt` | 证书 |
| `example.com.fullchain.crt` | 完整证书链（推荐使用） |

### 第五步：配置自动续期

**方式 A：Windows 计划任务（推荐）**

```bash
# 以管理员身份运行
python setup_task.py install

# 查看任务状态
python setup_task.py status

# 删除任务
python setup_task.py uninstall
```

任务将在每天凌晨 3:00 自动检查并续期，日志保存在 `logs/cert-renew.log`。

**方式 B：后台持续运行**

```bash
python scheduler.py
```

**方式 C：配合外部调度器**

```bash
python scheduler.py --once
```

## 📖 命令参考

```bash
# 证书管理
python main.py issue    # 申请证书（已有且未到期则跳过）
python main.py renew    # 同 issue
python main.py force    # 强制重新申请
python main.py status   # 查看证书状态

# 计划任务
python setup_task.py install    # 注册 Windows 计划任务
python setup_task.py uninstall  # 删除计划任务
python setup_task.py status     # 查看任务状态

# DNS API 独立测试
python bce_dns.py list - -                    # 列出所有 DNS Zone
python bce_dns.py add _acme-challenge.example.com test123
python bce_dns.py del _acme-challenge.example.com test123
```

## 🔧 Nginx 配置示例

```nginx
server {
    listen 443 ssl http2;
    server_name example.com *.example.com;

    ssl_certificate     C:/certs/example.com.fullchain.crt;
    ssl_certificate_key C:/certs/example.com.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # ... 其他配置
}
```

续期后自动重载 Nginx（在 `config.conf` 中配置）：

```ini
RENEW_HOOK=nginx -s reload
```

## ❓ 常见问题

### `BCE DNS API 错误 403`

检查 AK/SK 是否正确，以及该账号是否有 DNS 操作权限（控制台 → IAM → 权限策略）。

### `找不到域名对应的 DNS Zone`

确认域名已在百度云 DNS 托管（控制台 → DNS 解析 → 域名列表中能看到该域名）。

### ACME 验证失败（DNS 记录未找到）

增大 `DNS_PROPAGATION_WAIT`（如改为 60 或 120），等待 DNS 传播更充分。

### `Rate limit exceeded`

Let's Encrypt 对同一域名每周限制 5 次申请。测试时可在 `acme_client.py` 中将 `staging=False` 改为 `staging=True` 使用测试环境。

## ⚠️ 安全提示

- **config.conf 包含敏感信息**（API 密钥），已加入 `.gitignore`
- **切勿将 config.conf 上传到 GitHub 或任何公开仓库**
- **定期轮换 API 密钥**以提高安全性

## 📜 License

[MIT License](LICENSE)

## 🙏 致谢

- [Let's Encrypt](https://letsencrypt.org/) - 免费证书颁发机构
- [百度智能云](https://cloud.baidu.com/) - DNS API 支持
- [acme-tiny](https://github.com/diafygi/acme-tiny) - ACME 协议参考实现
