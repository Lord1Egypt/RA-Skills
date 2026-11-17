# 🛡️ ccpa-guard — CCPA 合规护栏

在 AI 应用输入/输出链路中实时检测 CCPA/CPRA 语境下的个人信息：US SSN、加州驾照、加州 ID、信用卡（Luhn）、US 电话等模式，以及 CCPA 分类（商业信息/生物识别/地理位置/就业/教育等）。按风险分级脱敏或阻断，供 Agent 主动调用。

纯本地运行，零网络请求，零动态执行。

## 安装

```bash
openclaw skill install ccpa-guard
```

## 用法

```bash
# 检测并脱敏（默认 ccpa 规则）
python3 scripts/guard.py --text "my SSN 987-65-4320, DL A1234567"

# 敏感个人信息检测
python3 scripts/guard.py --text "has a purchase history and biometric data"

# 高危阻断
python3 scripts/guard.py --text "credit card 4532015112830366" --action block

# 列出规则包
python3 scripts/guard.py --list-profiles
```

## 动作

| 动作 | 行为 |
|------|------|
| `detect` | 仅检测并报告，不改动文本 |
| `mask` | 脱敏后放行（默认） |
| `block` | 命中达阈值则阻断，否则脱敏 |

## 检测范围（ccpa v1.0.0）

**结构性模式**：US SSN、加州驾照、加州 ID、US 电话（NANPA）、信用卡（Luhn）、US 银行路由号、IPv4、MAC、邮箱。

**关键词线索**：CCPA/CPRA 分类：敏感 PI、商业信息、生物识别、地理位置、受保护分类、互联网活动、就业/教育。

## 架构

```
scripts/
  guard.py          检测内核
  rules/
    ccpa.py         CCPA 规则包（自包含）
```

## 系列规划

- `ccpa-guard`（CCPA版）— 本项目
- `gdpr-guard`（GDPR版）
- `pipl-guard`（中国PIPL版）

## 许可证与声明

MIT 许可证。本工具仅为防护辅助手段，不构成法律建议或合规证明，检测不保证 100% 完整。
