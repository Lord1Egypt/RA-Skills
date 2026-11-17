---
name: ctf-crypto-solver
description: "Crypto密码学解题助手：RSA/AES/ECC/格/PRNG/哈希/签名攻击的识别与求解脚本开发。遇到 crypto、RSA、AES、CBC、padding oracle、格、LWE、PRNG、签名伪造类题目时使用。"
---

# CTF Crypto 解题

识别密码体制 → 定位弱点 → 写求解脚本拿明文。

## 环境约定

- `$PY` = 64 位解题 Python（含 pycryptodome/z3/sympy/gmpy2）。
  环境不确定时先运行 ctf-router 技能的 `scripts/env-check.py` 自检。
- **hashcat**：哈希爆破；字典建议 rockyou（Kali 自带 `/usr/share/wordlists/`）。
- **SageMath（可选）**：格攻击与高级数论（Coppersmith、离散对数）。
  本机没有时用 `pip install fpylll` 替代格归约，或装 Sage：
  Linux `sudo apt install sagemath`；Windows 建议走 WSL。

## 识别速查

```powershell
$PY -c "n=<N>; print('bits=', n.bit_length())"      # RSA 模数位宽
$PY -c "from sympy import factorint; print(factorint(<n>))"  # 小因子？
# 哈希识别：看长度（32=MD5, 40=SHA1, 64=SHA256 hex）；hashcat --example-hashes 对照
# XOR 试探
$PY -c "from pwn import xor; print(xor(bytes.fromhex('<hex>'), b'flag{'))"
```

## 按体制的攻击清单

### RSA（最高频）
- 小 e + 小消息：直接开 e 次方
- 共模攻击：同一 m 两个 (n, e) → 扩展欧几里得
- Wiener：小 d（d < n^0.25 / 3）
- Fermat：p q 接近
- Pollard p-1：p-1 光滑
- Hastad 广播：e 组同明文（含线性填充用 Coppersmith）
- 已知 phi(n) 的倍数（如 e*d-1）：Miller-Rabin 平方根法分解
- dp/dq/qinv 部分泄露：遍历 k 还原素数
- 同态性绕过解密预言机：查 `c*r^e` 再除 r
- 先跑自动攻击组合：写脚本批量试（小e/共模/Wiener/Fermat/多素数）

### 对称加密
- **ECB**：块重排、逐字节选择明文（每字节 256 次查询）、cut-and-paste 伪造字段
- **CBC**：位翻转改明文；padding oracle 逐字节解密（每块约 4096 次查询）；IV 位翻转改第一块
- **GCM nonce 重用**：CTR 密钥流复用 + GHASH 密钥恢复
- **CBC-MAC/线性 MAC**：XOR 差分伪造签名
- **哈希长度扩展**：`hash(SECRET||msg)` 用 `hashpumpy`（pip 可装）
- **CRC32**：GF(2) 线性 → 追加 4 字节强制目标 CRC，伪造签名

### 流密码与 PRNG
- LFSR：Berlekamp-Massey 从 2L bit 密钥流恢复反馈多项式
- RC4：第二字节偏置识别
- MT19937：624 个输出克隆状态；float 输出用 GF(2) 矩阵恢复（not_random 库）
- LCG：已知部分输出 → 模逆回退 / 格恢复截断状态
- C `srand(time(NULL))`：用 ctypes 调 libc 的 srand/rand 同步序列（Windows 无 libc 时走 WSL）

### ECC / DLP
- 检查曲线阶的小因子 → Pohlig-Hellman
- 异常曲线（阶= p）→ Smart 攻击
- 无效曲线：服务端不校验点是否在曲线上
- ECDSA/DSA nonce 重用：同 r 直接解私钥
- 小 k 空间：暴力遍历

### 格 / LWE
- 判据：模线性方程组 + 未知量小/稀疏/偏置/部分泄露 → 格问题
- 工具顺序：LLL → BKZ → Babai 近似 CVP
- HNP：ECDSA 部分 nonce 泄露的标准归约
- 无 Sage 时：`pip install fpylll`（C 扩展，Windows 装不上就转 WSL）

### 经典与杂项
- 维吉尼亚：已知 `flag{` 前缀直接推 key；未知长度用 Kasiski（重复串距离 GCD）
- 多字节 XOR：按 key 位置分列做频率分析
- OTP 重用：`C1 xor C2 xor P_known = P_unknown`，crib dragging
- 约束求解：Z3（BitVec/Int）解自定义变换、S-box、方程组

## Z3 通用骨架

```python
from z3 import *
flag = [BitVec(f'f{i}', 8) for i in range(N)]
s = Solver()
# 按题目逻辑加约束（异或、乘、模、比较）
# 可加 Printables 约束: And(f>=32, f<=126)
if s.check() == sat:
    m = s.model()
    print(bytes(m[f].as_long() for f in flag))
```

## 何时换技能

- 要先逆向出算法实现 → 逆向技能。
- 数据要从流量/文件里先挖出来 → 取证技能。
- 其实是编码谜题而非密码分析 → Misc 技能。

## 深度知识库（按需读取）

本技能目录 `references/ctf-crypto/` 下参考文件（含完整攻击代码）：

| 文件 | 内容 |
|---|---|
| rsa-attacks.md / rsa-attacks-2.md | RSA 全攻击目录（含 Coppersmith、故障攻击、同态绕过） |
| modern-ciphers.md / -2 / -3 | AES 各模式攻击、padding oracle、MAC 伪造、GCM |
| classic-ciphers.md | 经典密码与 XOR 变体、文件格式头恢复密钥 |
| ecc-attacks.md | ECC/DSA 攻击全集 |
| lattice-and-lwe.md | 格攻击分诊、嵌入构造、失败模式 |
| advanced-math.md | LLL/BSGS/Coppersmith/同态等数学攻击代码 |
| prng.md / prng-attacks.md | MT/LCG/V8 random/ctypes 同步等 PRNG 攻击 |
| stream-ciphers.md | LFSR/RC4 |
| zkp-and-advanced.md | Z3 模式、Shamir、ZKP 伪造 |
| exotic-crypto*.md | 冷门代数结构（Paillier、热带半环等） |
