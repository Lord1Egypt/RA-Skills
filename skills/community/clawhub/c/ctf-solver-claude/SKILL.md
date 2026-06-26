---
name: ctf-solver
description: >
  仅在用户明确使用 /ctf-solver 指令或显式说"调用CTF技能/skill"时才触发，不自动响应任何CTF相关关键词。
  本技能以夺取flag为唯一目标，调用大量工具、深度分析题目，给出完整的解题过程和可执行的攻击链。
---

# CTF Solver — 专业夺旗技能

## 核心原则

1. **以夺取 flag 为唯一目标**，不惜调用任何工具、执行任何命令。
2. **深度优先**：先穷举所有可能向量，再逐步缩小范围。
3. **工具驱动**：优先用 bash_tool 执行命令、安装工具、运行 exploit。
4. **迭代调试**：每一步都验证输出，遇到错误立即调整策略。
5. **完整输出**：给出从题目分析到 flag 提交的完整攻击链。

---

## Step 0 — 题目类型判断

在调用子技能之前，先判断题目类型。按以下优先级匹配：

| 判断依据 | 类型 |
|---------|------|
| 给了 URL / IP:Port，有登录页、表单、API | **WEB** |
| 给了 ELF/PE 二进制，提示"nc"连接，有 libc | **PWN** |
| 给了压缩包、图片、流量包、音频、文本加密 | **MISC** |
| 给了可执行文件但无"nc"连接，提示分析逻辑 | **REVERSE** |
| 同时满足多个 | 分别处理，优先级 WEB > PWN > REVERSE > MISC |

判断完成后，**立即阅读对应子技能文件**，然后按其流程执行。

---

## 子技能文件索引

| 类型 | 文件路径 | 触发条件 |
|------|---------|---------|
| WEB | `references/web.md` | HTTP 服务、Web 漏洞利用 |
| PWN | `references/pwn.md` | 二进制漏洞、内存利用 |
| MISC | `references/misc.md` | 编解码、隐写、取证、密码学 |
| REVERSE | `references/reverse.md` | 静态/动态逆向分析 |

**用法**：判断类型后，用 `view` 工具读取对应文件，按其步骤执行。

---

## 通用工具速查

```bash
# 环境准备（优先在沙箱运行）
pip install pwntools requests flask --break-system-packages
apt-get install -y binutils file strings xxd gdb radare2 2>/dev/null

# 基础识别
file <binary>
strings <binary> | grep -i flag
xxd <binary> | head -50
binwalk <file>           # 文件嵌套检测

# 网络
curl -v 'http://target/...'
python3 -c "import requests; r=requests.get('http://...'); print(r.text)"
```

---

## Flag 格式速查

大多数 CTF 的 flag 格式：
- `flag{...}`、`CTF{...}`、`XXXXCTF{...}`（赛事名+大括号）
- Base64/hex 编码后的上述格式
- 纯 MD5/SHA1 哈希（题目会说明）

找到 flag 后，**立即输出完整 flag 字符串**，并说明是如何得到的。

---

## 遇到困难时的 escalation 路径

1. 尝试所有已知向量 → 仍无进展
2. 用 `web_search` 搜索题目关键词 + "CTF writeup"
3. 搜索具体漏洞/技术点的 PoC
4. 在 bash 中安装专用工具后重试
5. 如仍无法解题，输出当前分析结果和下一步建议
