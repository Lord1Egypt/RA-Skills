# 账户管理（account.py）

## 命令

```bash
python3 scripts/account.py add    # 新建账户（交互式）
python3 scripts/account.py list   # 列出所有账户
python3 scripts/account.py edit --id 1 --nickname "建行储蓄卡"
python3 scripts/account.py delete --id 1
python3 scripts/account.py default --id 2   # 设为默认账户
```

## 账户字段

| 字段 | 说明 | 必填 |
|------|------|------|
| nickname | 用户昵称，如"招行信用卡" | ✅ |
| type | debit（借记）/ credit（信用）/ wallet（电子钱包） | ✅ |
| last4 | 卡号尾号 | ❌ |
| currency | 货币，默认 CNY | ❌ |
| balance | 初始余额，默认 0 | ❌ |

## 余额更新规则

- 支出（expense）：`balance -= amount`（仅 debit/wallet 类型账户）
- 收入（income）：`balance += amount`
- 信用卡（credit）：`balance += amount`（负数 = 已用额度）
- transfer：从源账户扣，向目标账户加

## 常见账户类型示例

```
招行储蓄卡    debit    尾号 1234
浦发信用卡    credit   尾号 5678
微信钱包      wallet
支付宝        wallet
现金          wallet
```
