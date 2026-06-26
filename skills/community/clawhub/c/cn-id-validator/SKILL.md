---
slug: cn-id-validator
name: Cn Id Validator
version: "1.0.0"
description: "cn id validator"
keywords: tool, utility
license: MIT-0
tags:
  - tools
---


# Chinese ID Validator

Validate Chinese ID numbers (18-digit and 15-digit formats) and extract information.

## Features

- Validate 18-digit ID numbers (with checksum verification)
- Validate 15-digit ID numbers (with birth date check)
- Extract birth date from ID number
- Extract gender from ID number
- Extract region code from ID number
- Pure Python, no external dependencies

## ID Number Format

### 18-digit Format (1999-present)
- 1-6: Region code
- 7-14: Birth date (YYYYMMDD)
- 15-17: Sequential code (odd=male, even=female)
- 18: Check digit (0-10, where 10=X)

### 15-digit Format (1985-1999)
- 1-6: Region code
- 7-12: Birth date (YYMMDD, assumed 19xx)
- 13-15: Sequential code (odd=male, even=female)

## Usage

```bash
python3 scripts/id_validator.py --id 110101199003074416
```

## Example Output

```json
{
  "valid": true,
  "region": "110101",
  "birthday": "1990-03-07",
  "gender": "男"
}
```

## Validation Rules

1. Length must be 15 or 18 digits
2. Birth date must be a valid calendar date
3. For 18-digit IDs: checksum must be correct
4. Region code must be a valid Chinese administrative region

## Common Region Codes

| Code | Region |
|------|--------|
| 110000 | 北京市 |
| 310000 | 上海市 |
| 440000 | 广东省 |
| 320000 | 江苏省 |
| 330000 | 浙江省 |

## Use Cases

- User registration form validation
- Identity verification in business processes
- Age-based access control
- Demographic data analysis

## Notes

- This tool validates format and checksum only
- It does not verify against government databases
- Region codes are not fully validated (only format checked)
- Results are for reference only

## Technical Details

- Language: Python 3
- Dependencies: None (standard library only)
- License: MIT-0

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
