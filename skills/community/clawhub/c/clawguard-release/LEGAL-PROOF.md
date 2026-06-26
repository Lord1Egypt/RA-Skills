# ⚖️ Legal Validity / 法律效力说明

## Core Principles / 核心原理

ClawGuard uses **triple technology** to ensure evidence chain integrity:  
龙虾卫士通过**三重技术**确保证据链完整：

### 1. SHA256 Hash (Content Uniqueness) / SHA256 哈希（内容唯一性）

**Features / 特性**:
- **Uniqueness / 唯一性**: Same file = same hash, different files = different hashes
- **Irreversibility / 不可逆**: Cannot reverse-engineer file from hash
- **Sensitivity / 敏感性**: 1-byte change = completely different hash
- **International Standard / 国际认可**: ISO/IEC standard algorithm

**Legal Verification / 法律验证**:
```
1. Present certificate (hash H1) / 出示存证凭证（哈希 H1）
2. Extract original file / 提取原文件
3. Calculate SHA256(original) = H2 / 当庭计算 SHA256(原文件) = H2
4. Compare: H1 == H2 → Same file confirmed / 对比：H1 == H2 → 确认同一文件
```

### 2. ISO 8601 Timestamp (Proof Time) / ISO 8601 时间戳（存证时间）

- **Standard / 标准**: ISO 8601 international format
- **Authority / 权威**: NTP network time sync (pool.ntp.org)
- **Precision / 精度**: Second-level precision with timezone
- **Format / 格式**: `2026-03-16T17:00:14+08:00`

### 3. Local Blockchain (Tamper-proof) / 本地区块链（不可篡改）

- **Structure / 结构**: Hash-linked blockchain
- **Verification / 验证**: Tamper detection supported
- **Independence / 独立**: Local storage, no third-party dependency

## Legal Validity / 法律效力

### Complies with PRC Copyright Law / 符合《中华人民共和国著作权法》

- ✅ **Authenticity / 真实性**: SHA256 hash verification
- ✅ **Legality / 合法性**: Complies with legal requirements
- ✅ **Relevance / 关联性**: One-to-one hash-file correspondence

### Use Cases / 适用场景

- Personal digital assets / 个人数字资产确权
- SME IP protection / 中小企业 IP 保护
- E-commerce rights / 电商平台维权
- Academic priority / 学术论文优先权
- Collaborative works / 合作创作权属

## Recommendations / 使用建议

### Low-Medium Value Cases (<1M CNY) / 中低价值案件

Direct use of ClawGuard certificate is sufficient.  
直接使用龙虾卫士存证凭证即可。

### High Value Cases (>1M CNY) / 高价值案件

Recommended to use with notary office:  
建议配合公证处使用：
1. First prove with ClawGuard (get timestamp) / 先用龙虾卫士确权
2. Then notarize at notary office (enhance validity) / 再到公证处公证

## Technical Specifications / 技术规格

| Item / 项目 | Specification / 规格 |
|------------|---------------------|
| Hash Algorithm / 哈希算法 | SHA256 |
| Time Standard / 时间标准 | ISO 8601 |
| Time Source / 时间源 | NTP / Local fallback |
| Storage / 存储 | Local blockchain / 本地区块链 |
| Formats / 格式 | 25+ types |

---

**Version / 版本**: V1.5  
**License / 许可证**: MIT License  
**Author / 作者**: Xinjiang Baoheng Info Tech / 新疆宝恒信息科技有限公司
