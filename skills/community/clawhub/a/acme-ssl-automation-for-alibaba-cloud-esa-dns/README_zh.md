# ali-esa-acme-ssl-skill

[English](README.md)

OpenClaw 技能：使用 **阿里云 ESA DNS + acme.sh** 自动申请/续期 HTTPS 证书，支持泛域名，可按需安装到 Nginx。

## 解决什么问题

AI 模型总是解析到错误的地方，它到传统的云解析 DNS 那边解析，正确的应该是解析 ESA DNS，这两者是独立的。

也就是说，当域名托管在 ESA（`*.atrustdns.com`）时，DNS-01 验证记录必须写入 ESA DNS，而不是传统的云解析 DNS。

## 环境兼容性

- ✅ Linux 主机（Ubuntu 已测试）
- ✅ 系统级 Nginx（LNMP 已测试）
- ❌ 容器环境（不支持 Docker）
- ❌ 没有测试 Windows/macOS

## 项目结构

- `SKILL.md` – Agent 触发规则和使用指南
- `scripts/esa_acme_issue.py` – 自动化脚本
- `scripts/i18n/` – 脚本输出的语言文件（en.json、zh.json 等）
- `evals/evals.json` – 基础评估用例

## acme.sh 前置要求

使用本技能前，请先按 `acme.sh` 官方项目的说明完成安装，并先审查你选择的安装方式，不要直接把远程脚本无审查地管道给 shell：

- https://github.com/acmesh-official/acme.sh

本技能要求 `acme.sh` 可从 `PATH` 找到；脚本也兼容直接从 `~/.acme.sh/acme.sh` 位置查找。

## 快速开始

### 1) 导出凭证

```bash
export ALIYUN_AK='你的AK'
export ALIYUN_SK='你的SK'
export ALIYUN_SECURITY_TOKEN='YOUR_STS_TOKEN'  # 可选，推荐 STS 临时凭证
```

脚本也兼容 Alibaba Cloud 风格的变量名：

```bash
export ALIBABACLOUD_ACCESS_KEY_ID='你的AK'
export ALIBABACLOUD_ACCESS_KEY_SECRET='你的SK'
export ALIBABACLOUD_SECURITY_TOKEN='YOUR_STS_TOKEN'  # 可选
```

### 2) 单域名

```bash
python3 scripts/esa_acme_issue.py -d test.example.com --lang zh
```

### 3) 主域 + 泛域名

```bash
python3 scripts/esa_acme_issue.py -d example.com -d '*.example.com' --lang zh
```

### 3.1) 仅通配符

```bash
python3 scripts/esa_acme_issue.py -d '*.example.com' --lang zh
```

脚本会保持“仅通配符”申请意图，不会再隐式补一个 `example.com`。

## 默认行为

- 默认不安装证书到 Nginx；如需安装请显式传 `--install-cert`
- `--dns-timeout` 默认 600 秒
- 区域自动发现为尽力而为；如果 ESA 不支持 `DescribeRegions`，请传 `--region` 作为站点探测提示，脚本会继续探测内置候选区域
- 可选 IPv4/IPv6 记录管理：`--ensure-a-record host=ip`（会校验权威 NS 生效）

- 如果使用 `--install-cert`，请在可控 Linux 主机上执行，并确保当前用户有权限写入目标证书路径并重载 Nginx

## 安装自动续期 cron

使用 `scripts/install_cron.sh` 可以一键安装 root 持有的环境文件、wrapper 脚本和 cron 任务。

示例：

```bash
sudo bash scripts/install_cron.sh \
  --wrapper-name dogeow \
  --domains "dogeow.com,*.dogeow.com" \
  --ak 你的AK \
  --sk 你的SK \
  --region cn-hangzhou \
  --with-nginx-reload
```

它会创建：
- `/root/.config/` 下的 env 文件
- `/usr/local/sbin/` 下的 wrapper 脚本
- 写日志到 `/var/log/` 的 cron 任务

你也可以通过 `--schedule` 自定义 cron 表达式，例如：

```bash
sudo bash scripts/install_cron.sh \
  --domains "example.com,*.example.com" \
  --ak 你的AK \
  --sk 你的SK \
  --schedule "17 3 * * 0"
```

如果希望续期后由 acme.sh 安装证书到 nginx 管理路径，请传 `--cert-path`、`--key-path`，以及可选的 `--reload-cmd`。

示例：

```bash
python3 scripts/esa_acme_issue.py \
  -d test.example.com \
  --ensure-a-record test.example.com=1.2.3.4 \
  --lang zh
```

显式安装到 Nginx：

```bash
python3 scripts/esa_acme_issue.py \
  -d test.example.com \
  --install-cert \
  --lang zh
```

## 完成判定标准（防误报）

在声明"DNS 记录已完成"之前，必须同时满足：

1. ESA `ListRecords` 确认了精确的 `RecordName + Type + Value`
2. 权威 NS 查询（`dig @ns TXT`）返回了预期的 token

如果仅 CreateRecord API 返回成功，应报告为"请求已接受"（非已完成）。

## 常见故障排查

- `No TXT record found`：增大 `--dns-timeout`，验证权威 NS 传播
- `InvalidRecordNameSuffix`：域名不属于当前 ESA 站点后缀

## 常见问题

### Q: 我给 AccessKey 设置了 IP 白名单，应该检查什么？

A: 这是"权限"类错误的常见原因。

- 确保服务器当前的 **公网出口 IP** 在白名单中
- 如果使用代理/NAT，白名单应放行 **实际出口 NAT IP**，而非内网 IP
- 先确认出口 IP：

  ```bash
  curl -s ifconfig.me
  ```

## 安全说明

每次执行前，始终提醒用户以下 1/2/3：

1. 使用最小权限 RAM 子账号密钥，避免长期使用主账号密钥
2. 尽可能优先使用 STS 临时凭证
3. 为 AccessKey 开启 IP 白名单，只放行实际出口 NAT IP

- 不要在脚本中硬编码 AK/SK
- 优先使用环境变量
- 一旦 AK/SK 在聊天或日志中暴露，立即轮换
