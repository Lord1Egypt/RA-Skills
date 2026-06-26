---
name: compliance-check
description: 违规词·与多個免費齊全持續更新的詞庫對比，通過再上架；開箱即用，不用自己加詞。Use when user asks 合规检查, 敏感词, 违规词, 发帖前检查, 内容审核.
---

# 违规词·发帖前合规检查

跟多個免費、齊全、持續更新的詞庫對比，**沒問題才上架**。開箱即用，**不用用戶自己增加詞庫**，付費就是省事。

## When to use

- User says 检查这段文案、违规词、敏感词、发前合规、上架前检查
- User pastes draft and wants to know if it’s safe to post / compliant

## How to run

```bash
python scripts/check.py "待检查的文案内容"
python scripts/check.py --file path/to/draft.txt
python scripts/check.py "文案" --format report
```

**用戶無需**執行 sync、無需自己添加詞庫；技能自帶多詞庫，直接檢查即可。

## 詞庫（開箱即用）

- 內建：廣告法（絕對化/誇張、迷信與醫療）、平台通用（辱罵與違禁、拼音與變體等）。
- 已同步的免費詞庫：英文違禁、中文違禁、廣告類型、補充詞庫、色情類型、反動、暴恐、其他等（見 `config/wordlists/`）。全部參與對比，無需用戶維護。
- 自訂（可選）：`config/sensitive_words.txt` 可加自己想擋的詞，非必須。

## Output

- **JSON**：`pass`、`report_short`、`summary_zh`、`hits_by_source`、`compliance_tips`、可選 `suggestions`。
- **--format report**：Markdown 報告，可直接展示。

## Permissions / SkillPay

僅讀取用戶傳入文案與技能內詞庫；不寫用戶系統、不代發。可接 SkillPay 按次計費，每次執行計 1 次。
