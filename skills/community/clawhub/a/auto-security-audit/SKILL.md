---
name: auto-security-audit
description: "一键自动化安全审计：nmap 端口扫描 + nuclei 12000+ CVE 漏洞检测（内外网双扫）+ SSL/TLS 检查 + SSH/防火墙/fail2ban 系统审计 + Markdown 报告生成。支持 cron 定时扫描 + 飞书推送。"
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: [nmap, nuclei, sslscan]
author: nashbuaa-ops
---

# Auto Security Audit 🛡️

一键全套安全扫描 + 结构化报告，开箱即用。

## 能力

| 检测项 | 工具 | 说明 |
|--------|------|------|
| 端口 & 服务 | nmap | top 1000 TCP 端口 + 服务版本识别 |
| 已知漏洞 | nmap --script vuln | 内置漏洞脚本检测 |
| CVE/Web 漏洞 | nuclei | 12000+ 模板，内网+外网双扫，覆盖 CVE/XSS/SQLi/RCE |
| SSL/TLS | sslscan | 证书 & 加密协议检查 |
| SSH 加固 | sshd -T | root 登录、密码认证、最大尝试次数 |
| 防火墙 | ufw + iptables | 规则审计 |
| 暴力破解防护 | fail2ban | 状态 & 封禁记录 |
| 系统补丁 | apt | 待更新包检查 |
| 登录审计 | lastlog | 近 7 天登录记录 |

## 安装依赖

```bash
apt install -y nmap sslscan
# nuclei
curl -sL https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_$(curl -s https://api.github.com/repos/projectdiscovery/nuclei/releases/latest | grep tag_name | cut -d'"' -f4 | tr -d v)_linux_amd64.zip -o /tmp/nuclei.zip
unzip /tmp/nuclei.zip -d /tmp && mv /tmp/nuclei /usr/local/bin/
nuclei -update-templates
```

## 使用

### 一键扫描
```bash
python3 scripts/security_scan.py
```

输出：
- 终端打印风险摘要（🔴/🟡/🟢）
- `reports/security-scan-{日期}.md` — 完整 Markdown 报告
- `reports/latest-scan-summary.txt` — 摘要（供 cron 推送）

### 定时扫描 + 飞书推送
```bash
openclaw cron add --name "weekly-security-scan" \
  --cron "0 10 * * 1" \
  --message "执行安全扫描：python3 /path/to/scripts/security_scan.py，扫描完成后把报告摘要私聊发给我。" \
  --tz "Asia/Shanghai"
```

## 风险等级判定

- 🔴 **CRITICAL**: 危险端口对外开放 / nuclei 发现漏洞 / nmap 发现已知 CVE
- 🟡 **WARN**: SSH 配置弱 / 防火墙未启用 / fail2ban 未安装
- 🟢 **SAFE**: 未发现问题

## 授权声明

仅扫描你拥有或被授权测试的目标。
