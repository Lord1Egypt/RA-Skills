# BCE-Cert 技能

百度智能云 DNS 自动证书申请工具技能包。

## 功能

- 🔐 自动申请 Let's Encrypt 免费 SSL 证书
- 🌐 支持通配符证书（*.domain.com）
- 🔄 自动续期
- ⏰ Windows 计划任务
- 🧹 DNS 记录自动清理

## 安装

将本目录复制到 OpenClaw 的 skills 目录即可。

## 配置

1. 复制 `config.conf.example` 为 `config.conf`
2. 填入百度云 API 密钥和域名信息
3. 运行 `python main.py issue` 申请证书

## 使用

- "帮我申请证书"
- "查看证书状态"  
- "配置自动续期"
- "检查 DNS 记录"

## 源代码

https://gitee.com/x-hower/bce-cert

## 安全提示

- `config.conf` 包含敏感信息，请勿上传到 Git
- 建议将敏感配置放在 `.gitignore` 中
