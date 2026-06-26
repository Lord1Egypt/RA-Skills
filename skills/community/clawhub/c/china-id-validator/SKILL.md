---
name: China ID Validator
description: "Validate and extract info from Chinese ID card numbers (身份证). 身份证号码验证、归属地查询、出生日期提取、性别判断、年龄计算、15位转18位。China mainland ID card validator and parser."
tags: china, id, card, validator, identity, 身份证, chinese, utility, tool
---

# China ID Validator 🪪

中国居民身份证号码验证与信息提取工具。

## Features | 功能

- **号码验证**：15位/18位身份证合法性校验
- **信息提取**：省份、出生日期、性别、年龄
- **格式转换**：15位↔18位互转
- **校验码验证**：18位末位校验位验证

## Usage | 使用

```bash
# 验证身份证号
python3 scripts/id_validator.py 110101199003079

# 提取信息
python3 scripts/id_validator.py validate 110101199003079

# 生成测试号码（仅供测试）
python3 scripts/id_validator.py generate 11 1990 3 7 男
```

---

*免责声明：本工具仅供学习参考，不构成任何投资或商业建议。*
