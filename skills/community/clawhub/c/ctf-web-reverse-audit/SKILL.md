---
name: ctf-web-reverse-audit
description: "Web攻击与逆向审计助手：HTTP应用漏洞（SQLi/SSRF/SSTI/XXE/JWT/文件上传）利用，以及 Ghidra 无头反汇编与 semgrep 源码审计。遇到 web 题、源码审计、逆向分析、JWT、注入类题目时使用。"
---

# CTF Web 攻击与逆向审计

两半能力：① Web 应用攻击（第一战场是 CTF Web 题）；② 逆向与源码审计（Ghidra 无头分析 + semgrep）。

## 环境约定

- `$PY` = 64 位解题 Python（含 requests/flask-unsign 等）。
  环境不确定时先运行 ctf-router 技能的 `scripts/env-check.py` 自检。
- **sqlmap**：`pip install sqlmap` 后 `sqlmap -u ...`。
- **ffuf**：目录爆破，`winget install ffuf`（Windows）或系统包管理器。
- **curl**：Windows 自带 `curl.exe`；Linux/macOS 自带。
- **Burp Suite**（可选）：复杂流量拦截/重放时人工配合。
- **Ghidra**：绿色版解压 + Java 17+；无头入口是 `support/analyzeHeadless`
  （Windows 为 .bat，Linux/macOS 为无后缀脚本）。
- **semgrep**：源码审计，`pip install semgrep` 或独立 venv。
- **gdb/ltrace/strace/upx**：动态分析，Windows 走 WSL。

## Web：第一遍工作流（先侦察后动手）

1. **抓一对正常请求/响应**再模糊测试；每个主要功能都抓。
2. **枚举隐藏面**：`/robots.txt`、`/.git/`、`/.env`、`/admin`、`/debug`、JS bundle 里的路由与 API。
3. **判定漏洞族**：注入 / 越权 / 解析差异 / 上传 / 信任代理 / 状态机 / 客户端。
4. **先拿最小原语**：读一个文件、伪造一个 token、打一个内部接口；再链接成完整利用。

```powershell
# 侦察
curl -sI https://target/
curl -s https://target/robots.txt
ffuf -u https://target/FUZZ -w wordlist.txt -mc 200,301,302,403

# SQLi
sqlmap -u "https://target/page?id=1" --batch --dbs

# JWT 解码（不验签）
$PY -c "import base64,json,sys; p=sys.argv[1].split('.')[1]; p+='='*(-len(p)%4); print(json.dumps(json.loads(base64.urlsafe_b64decode(p)),indent=2))" "<token>"

# Flask cookie 解码/爆破密钥
flask-unsign --decode --cookie "<cookie>"
flask-unsign --unsign --cookie "<cookie>" --wordlist rockyou.txt

# SSTI 探针
curl "https://target/?name={{7*7}}"
curl "https://target/?name={{config}}"
```

### 常见链型
- 侦察 → 隐藏路由 → 认证绕过 → 读内部文件 → 拿 token/flag
- XSS → 管理员 bot → 特权操作 → 泄露机密
- 穿越/上传 → 配置/源码泄露 → 密钥 → 会话伪造
- SSRF → 元数据/内网 → 凭据 → RCE

### flag 常见位置
`/flag*`、`/proc/self/environ`、环境变量、数据库 `flag(s)` 表、响应头、隐藏路由、DOM `data-*`。

## 逆向：工作流（先快赢再深挖）

```powershell
# 1. 快赢：字符串与动态（WSL/Linux）
strings bin | grep -iE 'flag\{|correct|success'
ltrace ./bin        # 直接抓 strcmp 参数
strace -f -s 500 ./bin

# 2. Ghidra 无头反编译（路径按实际安装位置调整）
analyzeHeadless <proj_dir> rev_tmp -import bin -postScript DecompileAll.py

# 3. 关键洞见：让程序自己算答案——断在最后一次比较处，dump 算好的值
#    两个模式: transform(flag)==stored（逆变换）或 transform(stored)==flag（直接变换）
```

常用套路：单字节 XOR（暴破 256）、已知前缀 `flag{` 推 key、RC4 硬编码 key、位置异或、
PyInstaller（`pyinstxtractor`）、UPX 壳（`upx -d`）。

## 源码审计（semgrep）

```powershell
# 通用漏洞规则集扫描
semgrep scan --config auto <src_dir>
# 安全审计规则集
semgrep scan --config "p/security-audit" <src_dir>
# 危险函数快速兜底（以 PHP 为例，其他语言同理）
grep -rnE "eval|system|exec|passthru|unserialize|sql|include" <src_dir>
```

## 何时换技能

- 拿到代码执行后变成内存破坏 → PWN 技能。
- Web 的本质难点在密码学（JWT 数学、自定义 MAC）→ Crypto 技能。
- 要分析日志/pcap/备份文件 → 取证技能。

## 深度知识库（按需读取）

本技能目录 `references/` 下三套参考文件（只读复用）：

| 目录 | 内容 |
|---|---|
| references/ctf-web/ | SQLi（sql-injection.md）、服务端（server-side*.md）、反序列化（server-side-deser.md）、客户端/XSS（client-side*.md）、认证与 JWT（auth-*.md）、CVE 速查（cves.md）、实战长链（field-notes.md） |
| references/ctf-reverse/ | 工具用法（tools*.md）、反分析绕过（anti-analysis*.md）、常见模式（patterns*.md）、语言专项（languages*.md）、平台专项（platforms*.md） |
| references/security-arsenal/ | XSS/SSRF/SQLi/XXE/命令注入等 payload 弹药库 |
