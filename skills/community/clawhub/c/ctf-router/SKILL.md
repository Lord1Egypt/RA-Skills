---
name: ctf-router
description: "CTF题目分诊路由：拿到新题目时先判断题型（pwn/crypto/misc/web/reverse/forensics），给出解题入口与换技能指引。所有 CTF 解题请求的第一步，任何 ctf、做题、拿flag、解题请求都先用它分诊。"
---

# CTF 题目分诊路由

拿到题目先分诊，再进专项技能。这是所有 CTF 解题的统一入口。

## 环境约定（跨平台）

- **解题 Python（记作 `$PY`）**：必须是 **64 位** Python 3.10+ 虚拟环境，装有
  `pwntools z3-solver sympy pycryptodome gmpy2 requests volatility3 flask-unsign
  pillow numpy pyzbar python-magic-bin dnspython`。
  首次使用时若不确定环境状态，运行本技能的 `scripts/env-check.py`
  （`python scripts/env-check.py`，脚本只用标准库），它会列出缺失项和一键安装命令。
  没有环境就按它的指引建一个：`python -m venv ctf-venv` 然后装上述包。
- **Windows 用户**：强烈建议装 WSL（`wsl --install kali-linux`），
  Linux 专属工具（gdb/ltrace/binwalk/foremost/strings/john/checksec/ROPgadget/upx/nmap）
  在 Kali 里执行：`wsl -d kali-linux -- bash -lc "<cmd>"`，文件路径换成 `/mnt/c/...`。
  Linux/macOS 用户直接用系统包管理器装。
- **外部工具**：tshark（Wireshark）、hashcat、semgrep、sqlmap、ffuf、Ghidra（绿色版+Java 17+）、
  Burp Suite（可选，复杂 Web 流量）。`env-check.py` 会报告缺失项与安装方式。
- **本套技能自带知识库**：各专项技能目录下的 `references/` 收录了上百个真题解法参考文件
  （攻击手法 + 完整代码），遇到对应题型时按需读取。

## 分诊决策树

按附件与题面特征判断：

1. **有可执行文件/二进制 + 提示要"打穿/拿 shell/控制流"** → ctf-pwn-exploit
2. **有源码/密文/数学参数 (n, e, c)/加密服务** → ctf-crypto-solver
3. **pcap/流量/内存镜像/磁盘镜像/图片音频文档/编码串** → ctf-misc-forensics
4. **给了 URL/Web 应用** → ctf-web-reverse-audit（Web 部分）
5. **有可执行文件但要求"分析它做了什么/找校验逻辑"** → ctf-web-reverse-audit（逆向部分）
6. **题目涉及 AI/大模型/提示词/智能体** → 先按 Web 侦察摸清接口；考点多为提示词注入、
   越狱、模型参数/训练数据泄露，结合 Web 侦察与编码能力

拿不准时：先跑通用三板斧——识别类型、搜字符串、查嵌入文件——再按结果二次分诊。

## 通用三板斧

```powershell
# 用 $PY 做类型识别（避免依赖 file 命令）
$PY -c "import magic; print(magic.from_file('attachment'))"
# Linux/WSL 内搜字符串与嵌入文件
strings -n 6 attachment | grep -iE "flag|ctf|key"
binwalk attachment
```

## 解题纪律

- flag 格式优先用题面给的（常见 `flag{}`），正则搜索时把 `flag\{` 和 `ctf\{` 都试。
- 远程题先手动交互摸清协议，再写 pwntools/requests 脚本。
- 每个假设都要用一次实际运行验证，不要凭猜继续堆代码。
- WriteUp 素材随手记：赛后可能要交。
- 比赛若规定禁用 AI 辅助，遵守规则——本技能仅用于训练与赛后复盘。
