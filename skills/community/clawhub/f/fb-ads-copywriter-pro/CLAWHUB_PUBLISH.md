# 🚀 ClawHub 技能包上架指南

## ✅ 準備完成

**技能包：** FB Ads Copywriter Pro  
**版本：** 1.0.0  
**位置：** `/home/admin/.openclaw/workspace/skills/fb-ads-copywriter-pro/`

**已完成文件：**
- [x] SKILL.md (17KB) - 完整技能描述
- [x] _meta.json (2.9KB) - 元數據配置
- [x] README.md (1.9KB) - 使用說明
- [x] requirements.txt - Python 依賴
- [x] scripts/copy-generator.py (16.6KB) - 核心腳本
- [x] references/api-docs.md - API 文檔
- [x] references/examples.md - 示例文案

---

## 📋 上架步驟

### 步驟 1：登錄 ClawHub

```bash
clawhub login
```

**預期輸出：**
```
? Email: victor@vic-ai.com
? Password: ********
✅ Login successful!
```

---

### 步驟 2：發布技能包

```bash
cd /home/admin/.openclaw/workspace/skills
clawhub publish fb-ads-copywriter-pro
```

**預期輸出：**
```
📦 Publishing fb-ads-copywriter-pro v1.0.0...
✅ Published successfully!
🔗 https://clawhub.com/skills/fb-ads-copywriter-pro
```

---

### 步驟 3：驗證上架

**檢查清單：**
- [ ] 技能包頁面可以訪問
- [ ] 安裝命令正常
- [ ] 文檔顯示正確
- [ ] 價格設置正確

---

## 🎯 技能包信息

### 基本信息

| 項目 | 內容 |
|------|------|
| **Name** | fb-ads-copywriter-pro |
| **Display Name** | FB Ads Copywriter Pro |
| **Version** | 1.0.0 |
| **Author** | Vic AI Company |
| **License** | MIT |

### 定價

| 版本 | 價格 | 功能 |
|------|------|------|
| 基礎版 | $29 | 6 個廣告版本，基礎 A/B 測試 |
| 專業版 | $99 | 無限生成，進階 A/B 測試，受眾分析 |
| 企業版 | $299 | 定制語氣，批量生成，API 訪問 |

### 關鍵詞

```
facebook-ads, copywriting, marketing, ai, advertising, social-media, 
ab-testing, audience-analysis, openclaw, clawhub
```

### 分類

```
marketing
```

---

## 📸 截圖建議

**建議準備以下截圖：**

1. **技能包封面** - 展示 6 個廣告風格
2. **使用示例** - 命令行生成過程
3. **交付包示例** - Markdown 交付包預覽
4. **A/B 測試建議** - 測試組合表格
5. **受眾分析** - 3 個細分群組

**截圖位置：** `/home/admin/.openclaw/workspace/skills/fb-ads-copywriter-pro/assets/`

---

## 🔧 故障排除

### 問題 1：登錄失敗

**錯誤：** `Error: Not logged in`

**解決：**
```bash
# 清除舊登錄
clawhub logout

# 重新登錄
clawhub login
```

### 問題 2：發布失敗

**錯誤：** `Error: Skill already exists`

**解決：**
```bash
# 更新版本號
# 編輯 _meta.json，修改 version 為 1.0.1

# 重新發布
clawhub publish fb-ads-copywriter-pro --changelog "Initial release"
```

### 問題 3：驗證失敗

**錯誤：** `Error: Missing required fields`

**解決：**
```bash
# 檢查 _meta.json 是否完整
cat /home/admin/.openclaw/workspace/skills/fb-ads-copywriter-pro/_meta.json

# 確保包含所有必填字段
```

---

## 📞 需要幫助？

**聯絡方式：**
- Email: support@vic-ai.com
- Telegram: @vicaimonitor_bot
- ClawHub: https://clawhub.com/support

---

## ✅ 上架後檢查

- [ ] 技能包頁面正常顯示
- [ ] 安裝命令可用：`clawhub install fb-ads-copywriter-pro`
- [ ] 文檔完整
- [ ] 價格正確
- [ ] 示例代碼可運行

---

**準備完成！隨時可以上架！** 🚀

**最後更新：** 2026-03-15 17:15  
**狀態：** ✅ 等待上架
