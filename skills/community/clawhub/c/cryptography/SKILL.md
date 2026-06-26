# Cryptography / 密码学

## 概念→原理→公式→代码→应用 结构化参考

---

## 1. 对称加密

### 概念
加密和解密使用同一密钥。速度快，适合大量数据。

### AES（Advanced Encryption Standard）

**原理**：SPN 结构，分组大小 128 bit，密钥 128/192/256 bit。轮数：10/12/14。
**操作**：SubBytes → ShiftRows → MixColumns → AddRoundKey

```
密文 = E_K(明文)    明文 = D_K(密文)
```

**工作模式**：

| 模式 | 特点 | 需要填充 | 并行 |
|------|------|---------|------|
| ECB | 相同明文块→相同密文块（不安全） | 是 | 加密可 |
| CBC | 每块 XOR 前一密文块 | 是 | 解密可 |
| CTR | 计数器模式，流式加密 | 否 | 是 |
| GCM | CTR + 认证标签 (AEAD) | 否 | 是 |

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = os.urandom(12)
ct = aesgcm.encrypt(nonce, plaintext, associated_data)
pt = aesgcm.decrypt(nonce, ct, associated_data)
```

### ChaCha20-Poly1305

Google 推荐替代 AES-GCM（无硬件加速时更快）。流密码 + MAC。

### SM4（国密）

中国国家标准，128 bit 密钥，32 轮。用于金融/政务。

---

## 2. 非对称加密

### RSA

**原理**：基于大整数分解困难性。

```
n = p × q,  φ(n) = (p-1)(q-1)
e（通常 65537）,  d = e^(-1) mod φ(n)
加密：c = m^e mod n    解密：m = c^d mod n
签名：s = m^d mod n    验证：m = s^e mod n
```

密钥 ≥2048 bit。使用 OAEP（加密）/ PSS（签名）填充。

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

private_key = rsa.generate_private_key(65537, 4096)
ct = private_key.public_key().encrypt(
    msg, padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))
```

### ECC（椭圆曲线密码学）

基于 ECDLP。同等安全密钥更短。

```
y² = x³ + ax + b (mod p)
私钥 d ∈ [1, n-1],  公钥 Q = d × G
ECDH 共享密钥: d_A × Q_B = d_B × Q_A
```

| 曲线 | 应用 |
|------|------|
| P-256 | TLS 通用 |
| secp256k1 | 比特币/以太坊 |
| Curve25519 | ECDH（推荐） |
| Ed25519 | 签名（推荐） |

### SM2（国密）

中国国家标准 ECC，配套 SM3 哈希。

---

## 3. 哈希函数

单向性、抗碰撞性、雪崩效应。

| 算法 | 输出 | 状态 |
|------|------|------|
| SHA-256 | 256 bit | ✅ 安全 |
| SHA-3 | 可变 | ✅ 安全 |
| SM3 | 256 bit | ✅ 安全（国密） |
| MD5/SHA-1 | 128/160 bit | ❌ 已破解 |

### HMAC

```
HMAC(K, m) = H((K' ⊕ opad) || H((K' ⊕ ipad) || m))
```

### 密码哈希

慢哈希 + 盐，抗暴力/彩虹表。**Argon2**（推荐）> scrypt > bcrypt。

### 生日攻击

SHA-256 碰撞需要 ≈2¹²⁸ 次尝试。

---

## 4. 数字签名与 PKI

| 算法 | 特点 |
|------|------|
| RSA-PSS | RSA + 概率签名 |
| ECDSA | 椭圆曲线签名 |
| EdDSA (Ed25519) | 确定性，推荐 |

### PKI

根 CA → 中间 CA → 终端证书。CRL/OCSP 吊销检查。

### Let's Encrypt / ACME

自动签发免费 TLS 证书。HTTP-01 / DNS-01 域名验证。

---

## 5. 密钥管理

- **密钥派生**：HKDF / PBKDF2
- **密钥封装**：HPKE（RFC 9180，推荐）
- **前向保密**：临时 ECDH 密钥对

---

## 6. 协议安全

### TLS 1.3（1-RTT）

ClientHello + KeyShare → ServerHello + KeyShare + Cert + Finished → Finished
ECDHE 协商共享密钥，前向保密。

### JWT

```
Header.Payload.Signature
alg: none 攻击需防范；不加密敏感数据
```

### 双因素认证

- **TOTP**：`Truncate(HMAC-SHA1(K, ⌊time/30⌋))` → 6 位数字
- **WebAuthn/FIDO2**：公钥密码学 + 硬件安全密钥

---

## 7. 侧信道攻击

- **时序攻击**：通过操作耗时推断密钥。防护：恒定时间比较。
- **功耗分析**：DPA/SPA 分析设备功耗。防护：掩码、盲化。
- **缓存攻击**：Spectre/Meltdown 类。防护：恒定时间实现、缓存刷新。

---

## 8. 密码学应用

### 区块链

- **Merkle 树**：`H(H(a)||H(b))` 二叉哈希树，高效验证数据完整性
- **PoW**：找到 `nonce` 使得 `H(block_header) < target`
- **PoS**：权益证明，按持币量选验证者

### 零知识证明（ZKP）

证明者不泄露信息的情况下证明某个陈述为真。

```
zk-SNARK：简洁非交互知识论证
  特点：证明小（~200B）、验证快、需可信设置
zk-STARK：透明、无需可信设置、证明较大
```

应用：Zcash 隐私交易、以太坊 zkRollup 扩容。

### 同态加密

对密文直接计算，解密结果等于对明文计算的结果。

```
E(a) ⊕ E(b) = E(a + b)    （加法同态：Paillier）
E(a) ⊗ E(b) = E(a × b)    （全同态：Gentry 方案，CKKS/BFV）
```

### 安全多方计算（MPC）

多方各自持有私密输入，联合计算函数结果，不泄露各自输入。

应用：隐私集合求交（PSI）、联合建模、密钥分片托管。
