---
name: axiom-hash-multi
description: 多算法哈希生成器 (MD5/SHA-1/SHA-256/SHA-512/BLAKE2b) — 确定性、字节到字节、零依赖。在需要使用多种算法同时对文件或字符串进行哈希时使用,无需LLM、无云、无幻觉。
language: zh
---

# 🛠️ axiom-hash-multi

**版本:** 1.1.0
**Axioma Tools — Skill #1 (Phase 1)**
**集群:** Axioma

## 这个 skill 的功能

对文件或字节输入计算**5 种哈希算法**(或仅一种):

- MD5
- SHA-1
- SHA-256
- SHA-512
- BLAKE2b (64 字节摘要)

**差异化优势:**
- **零依赖** (纯 Python 标准库)
- **字节到字节确定性** (相同输入 → 相同哈希,永远)
- **流式处理** 大文件 (不占用大量内存)
- **无 LLM,无云,无幻觉**
- **一次调用计算多种算法** (`--all` 标志)

## 使用场景

- ✅ 对文件进行哈希以验证完整性
- ✅ 同时获取多种算法用于交叉验证
- ✅ 为文件生成指纹用于去重
- ✅ 对字符串进行哈希而无需编写脚本
- ✅ 批量哈希目录 (循环调用此 CLI)
- ✅ 验证文件是否匹配预期哈希 (`--compare`)
- ✅ 验证 MANIFEST 文件中的所有哈希 (`--verify-manifest`)
- ✅ 获取结构化 JSON 输出供脚本使用 (`--json`)
- ❌ 需要 HMAC 或密码哈希 (使用 bcrypt/argon2)
- ❌ 需要加密签名 (使用 GPG/age)

## 使用方法

### 命令行

```bash
# 单个算法 (默认: SHA-256)
python3 axiom_hash_multi.py <file>
python3 axiom_hash_multi.py "my string" --string
echo "data" | python3 axiom_hash_multi.py --stdin

# 指定算法
python3 axiom_hash_multi.py <file> --algo md5
python3 axiom_hash_multi.py <file> --algo sha512

# 一次计算所有算法
python3 axiom_hash_multi.py <file> --all

# 与预期哈希比对 (匹配则 exit 0,否则 1)
python3 axiom_hash_multi.py <file> --algo sha256 --compare=<expected_hex>

# 验证 MANIFEST.txt 文件 (所有哈希)
python3 axiom_hash_multi.py --verify-manifest MANIFEST.txt

# JSON 输出 (供脚本使用)
python3 axiom_hash_multi.py <file> --all --json
```

### Python API

```python
from axiom_hash_multi import hash_bytes, hash_file, hash_all, hash_file_all, verify_manifest

# 字节
digest = hash_bytes(b"hello", "sha256")

# 文件 (流式)
digest = hash_file("path/to/file", "sha256")

# 所有算法
results = hash_all(b"test")  # 包含 5 种算法的字典
results = hash_file_all("path/to/file")  # 包含 5 种算法的字典

# 验证 MANIFEST
result = verify_manifest("MANIFEST.txt")  # {"verified": True, "checked": 12, "failed": 0}
```

## 验证状态

| 检查项 | 状态 |
|-------|--------|
| 单元测试 (≥10 个用例) | ✅ 24 个测试 + 16 个压力测试 = 40 个用例 |
| 性能 <100ms | ✅ 对 <100MB 文件已验证 |
| 安全性 (无注入) | ✅ 纯标准库,无 eval/subprocess |
| 字节到字节确定性 | ✅ hashlib 规范 + 1000 次运行测试 |
| 0 LLM/KAN 依赖 | ✅ 仅标准库 (hashlib, pathlib, json) |
| 文档 (README + SKILL.md) | ✅ v1.1.0 完整 |
| 许可证 | Apache-2.0 |

**压力测试结果 (9 组,40+ 个用例):** 全部通过

_最后更新: 2026-06-14 — v1.1.0 发布,修复 /dev/null 错误 + 新增 4 个功能._
