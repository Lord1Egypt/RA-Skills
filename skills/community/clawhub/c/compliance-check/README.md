# 违规词·发帖前合规检查

**跟多個免費、齊全、持續更新的詞庫對比，沒問題再上架——開箱即用，不用自己加詞，付費就是省事。**

## 一句話

發帖前跑一次檢查，自動對比多份內建 + 同步的免費詞庫（中英、廣告法、平台違禁等）；通過就安心發，未通過就按報告改。你不用懂詞庫從哪來、也不用自己維護，省心。

## 使用（就兩步）

```bash
# 1. 檢查一段文案
python scripts/check.py "你要發的內容"

# 2. 或檢查檔案、或要 Markdown 報告
python scripts/check.py --file 文案.txt
python scripts/check.py "內容" --format report
```

**詞庫從哪來？** 技能自帶多份內建詞庫，並已預拉多個免費、持續更新的外部詞庫（見 `config/wordlists/`）。你**不用自己新增**，直接檢查即可。維護者若想更新詞庫，可執行一次 `python scripts/sync_wordlists.py`（一般用戶可忽略）。

## 可選

- **AI 修改建議**：設定 `DEEPSEEK_API_KEY` 後，命中時會給簡短修改建議。
- **自訂詞**：有特殊詞想一併擋，可編輯 `config/sensitive_words.txt`（非必須）。

## 權限與收費

僅讀取你傳入的文案與技能內詞庫，不寫盤、不代發。可接 SkillPay 按次計費，每次執行計 1 次。
