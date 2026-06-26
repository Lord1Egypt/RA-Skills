---
name: fb-ads-copywriter-pro
description: Facebook 廣告文案專家 - 生成 6 個高轉化率廣告版本，包含 A/B 測試建議和受眾分析
author: Vic AI Company
version: 2.1.0
metadata: {"emoji": "📝", "category": "marketing", "tags": ["facebook-ads", "copywriting", "marketing", "ai", "clawhub"]}
clawhub_pricing:
  single: $3 USD/次（6 文案 +6 圖片 +UTM+ 第 7 日報告，無試用）
  subscription: $29-199 USD/月
---

# FB Ads Copywriter Pro - Facebook 廣告文案專家

**專業級 Facebook 廣告文案生成工具，6 個廣告版本 + A/B 測試建議 + 受眾分析 + 投放策略**

---

## 🎯 功能特點

### 核心功能

- 📝 **6 個廣告版本生成** - FOMO/社交證明/權威背書/痛點營銷/優惠促銷/故事營銷
- 🧪 **A/B 測試建議** - 3 個測試組合，科學優化廣告效果
- 🎯 **目標受眾分析** - 3 個細分群組，精準定位目標客戶
- 📊 **投放策略建議** - 預算分配、版位建議、KPI 目標
- ✍️ **粵語口語化創作** - 地道香港廣東話，符合本地市場
- ✅ **符合廣告政策** - 自動避免違規詞語，降低被封鎖風險

### 進階功能

- 🔍 **關鍵詞優化** - SEO 友好，提升廣告質量得分
- 📈 **ROI 預測** - 根據行業基準預測廣告回報
- 🎨 **Emoji 智能配對** - 適當使用 Emoji，提升吸引力
- 🏷️ **Hashtag 生成** - 3-5 個相關標籤，增加曝光
- 📧 **Email 交付** - 自動發送交付包畀客戶
- 💬 **Telegram 通知** - 即時通知客戶已交付

---

## 🚀 快速開始

### 安裝

```bash
# 使用 ClawHub 安裝
clawhub install fb-ads-copywriter-pro

# 或手動克隆
git clone https://github.com/vic-ai/fb-ads-copywriter-pro.git
cd fb-ads-copywriter-pro
pip install -r requirements.txt
```

### 配置 API Key

```bash
# 設置 GLM API Key
export GLM_API_KEY="your-glm-api-key"

# 或創建 .env 文件
echo "GLM_API_KEY=your-glm-api-key" > .env
```

### 基礎用法

```bash
# 生成廣告文案（交互式）
python scripts/copy-generator.py generate

# 使用問卷數據生成
python scripts/copy-generator.py generate --questionnaire memory/questionnaire-sub_123456.md

# 指定產品生成
python scripts/copy-generator.py generate \
  --product "維 C 亮白精華素" \
  --audience "25-45 歲女性" \
  --budget "5000-8000 HKD/月"
```

---

## 📋 使用場景

### 場景 1：客戶提交問卷後生成文案

```bash
# 1. 客戶提交問卷（已保存到 memory/）
# 2. 自動生成文案
python scripts/copy-generator.py generate --questionnaire memory/questionnaire-sub_123456.md

# 3. 查看生成的文案
cat memory/ad-delivery-sub_123456.md

# 4. 發送畀客戶
python scripts/copy-generator.py send --email client@example.com --telegram
```

### 場景 2：快速生成特定產品文案

```bash
python scripts/copy-generator.py generate \
  --product "無線耳機" \
  --audience "18-35 歲，音樂愛好者" \
  --budget "3000-5000 HKD/月" \
  --style "casual" \
  --output json
```

### 場景 3：批量生成多個產品文案

```bash
# 準備產品列表
cat > products.json << EOF
[
  {"name": "維 C 精華", "audience": "25-45 歲女性"},
  {"name": "保濕面霜", "audience": "20-35 歲女性"},
  {"name": "防曬噴霧", "audience": "18-40 歲男女"}
]
EOF

# 批量生成
python scripts/copy-generator.py batch --input products.json --output ads/
```

---

## 🎨 6 個廣告風格

### 1️⃣ FOMO（恐懼錯過）🔥

**特點：** 強調限時優惠、庫存緊張、錯過就沒有了

**適用場景：**
- 限時促銷活動
- 清庫存
- 新品上市（限量）
- 節日營銷

**示例標題：**
```
⏰ 最後 3 日！香港女生瘋搶嘅亮白秘密
🚨 庫存告急！下次到貨要等 3-4 週
```

### 2️⃣ 社交證明 👥

**特點：** 強調用戶評價、銷量、推薦人數

**適用場景：**
- 新產品推廣
- 建立信任
- 高單價產品
- 競爭激烈市場

**示例標題：**
```
🌟 超過 5,000 位香港女生選擇嘅亮白方案
⭐⭐⭐⭐⭐ 4.9/5.0（基於 1,234 條真實評價）
```

### 3️⃣ 權威背書 👩‍⚕️

**特點：** 強調專家推薦、科學驗證、專業認證

**適用場景：**
- 護膚品/保健品
- 高單價產品
- 專業服務
- 高端市場

**示例標題：**
```
🏥 香港皮膚科醫生推薦：15% 維 C 濃度係黃金比例
🔬 臨床測試證實：28 日亮度提升 37%
```

### 4️⃣ 痛點營銷 💔

**特點：** 強調問題帶來的困擾，產品如何解決

**適用場景：**
- 問題解決型產品
- 情感共鳴
- 新客獲取
- 轉化率低時

**示例標題：**
```
😩 每日照鏡見到自己塊面咁暗，心情都差咗？
❌ 試過好多美白產品，都係無效？
```

### 5️⃣ 優惠促銷 🎁

**特點：** 強調首次購買優惠、限時折扣、贈品

**適用場景：**
- 新客獲取
- 節日促銷
- 清倉大平賣
- 衝銷量

**示例標題：**
```
🎉 新客專享！首次購買立減$100 + 免費送價值$288 護膚套裝
🎊 3 週年慶典！全線 7 折 + 買一送一
```

### 6️⃣ 故事營銷 📖

**特點：** 用品牌故事或用戶轉變故事引起共鳴

**適用場景：**
- 品牌建設
- 長期價值
- 情感連結
- 忠誠度培養

**示例標題：**
```
💭 「35 歲先至明白，真正嘅亮白係由內而外嘅自信」
📖 從化學博士到護膚品創辦人：我嘅 3 年研發之路
```

---

## 📊 輸出內容

### 標準交付包包含：

1. **6 個廣告文案版本**
   - 標題、主要文案、CTA 按鈕、短描述、Hashtags
   - 每個版本 300-500 字
   - 粵語口語化創作

2. **A/B 測試建議**
   - 3 個測試組合（標題/文案風格/CTA）
   - 預算分配建議
   - 測試週期建議
   - 預期效果預測

3. **目標受眾分析**
   - 3 個細分群組
   - 每個群組的痛點和需求
   - 推薦文案風格
   - 最佳投放時間

4. **投放策略建議**
   - 預算分配（4 週漸進式）
   - 廣告版位建議
   - KPI 目標設定
   - 優化時間點

5. **預期效果報告**
   - CTR 預測
   - CPC 預測
   - 轉化率預測
   - ROAS 預測

---

## 🧪 A/B 測試組合

### 測試組合 1：標題測試

| 版本 | 標題風格 | 預算 | 測試週期 | 預期 CTR |
|------|----------|------|----------|----------|
| A | FOMO（最後 3 日） | $500 | 3 日 | 2.5-3.5% |
| B | 社交證明（5,000 位） | $500 | 3 日 | 2.0-3.0% |

**決策標準：** CTR > 2.5% 勝出

### 測試組合 2：文案風格測試

| 版本 | 風格 | 預算 | 測試週期 | 預期轉化率 |
|------|------|------|----------|------------|
| A | 權威背書（醫生推薦） | $1,000 | 5 日 | 3-5% |
| B | 痛點營銷（情感共鳴） | $1,000 | 5 日 | 2.5-4% |

**決策標準：** CPA < $150 勝出

### 測試組合 3：CTA 測試

| 版本 | CTA 按鈕 | 預算 | 測試週期 | 預期效果 |
|------|----------|------|----------|----------|
| A | 立即購買 | $500 | 7 日 | 直接轉化 |
| B | 了解更多 | $500 | 7 日 | 降低門檻 |

**決策標準：** 轉化率 > 3% 勝出

---

## 📈 投放預算分配建議

### 月預算 $8,000 HKD 分配

| 週期 | 預算 | 目標 | 重點 |
|------|------|------|------|
| 第 1 週 | $1,500 | 測試 | 標題 + 文案風格 |
| 第 2 週 | $2,000 | 優化 | 最佳組合 + 受眾細分 |
| 第 3 週 | $2,500 | 擴展 | 相似受眾 + 再營銷 |
| 第 4 週 | $2,000 | 穩定 | 最佳表現組合 |

### 廣告版位建議

| 版位 | 預算比例 | 說明 |
|------|----------|------|
| Facebook Feed | 50% | 主要轉化來源 |
| Instagram Feed | 30% | 年輕受眾 |
| Instagram Stories | 15% | 品牌曝光 |
| Audience Network | 5% | 額外覆蓋 |

---

## 🎯 KPI 目標設定

| 指標 | 目標值 | 行業基準 | 計算方式 |
|------|--------|----------|----------|
| **CTR** | > 2% | 1.5-2.0% | 點擊率 |
| **CPC** | < $5 HKD | $5-8 HKD | 單次點擊成本 |
| **CPA** | < $150 HKD | $150-200 HKD | 單次購買成本 |
| **ROAS** | > 3:1 | 2.5-3.0:1 | 廣告支出回報率 |
| **轉化率** | > 3% | 2-3% | 點擊到購買 |

---

## 💻 API 參考

### 生成廣告文案

```python
from copy_generator import generate_ads

# 基礎生成
result = generate_ads(
    product="維 C 亮白精華素",
    audience="25-45 歲女性",
    budget="5000-8000 HKD/月",
    styles=["fomo", "social_proof", "authority", "pain_point", "promotion", "story"]
)

# 獲取文案
for ad in result['ad_copies']:
    print(f"版本：{ad['version']}")
    print(f"標題：{ad['headline']}")
    print(f"文案：{ad['primary_text']}")
    print(f"CTA: {ad['cta']}")
    print(f"標籤：{ad['hashtags']}")
    print("---")
```

### 生成 A/B 測試建議

```python
from copy_generator import generate_ab_tests

tests = generate_ab_tests(
    ad_copies=result['ad_copies'],
    budget=8000,
    currency="HKD"
)

for test in tests:
    print(f"測試組合：{test['name']}")
    print(f"預算：{test['budget']}")
    print(f"週期：{test['duration']}日")
    print(f"決策標準：{test['success_criteria']}")
```

### 生成受眾分析

```python
from copy_generator import analyze_audience

audience = analyze_audience(
    product="維 C 亮白精華素",
    demographics="25-45 歲女性",
    location="香港",
    interests=["護膚", "美容", "健康"]
)

for segment in audience['segments']:
    print(f"受眾群組：{segment['name']}")
    print(f"年齡：{segment['age_range']}")
    print(f"痛點：{segment['pain_points']}")
    print(f"推薦文案：{segment['recommended_styles']}")
```

---

## 📁 文件結構

```
fb-ads-copywriter-pro/
├── SKILL.md                    # 技能描述（呢個文件）
├── _meta.json                  # 元數據
├── README.md                   # 使用說明
├── requirements.txt            # Python 依賴
├── scripts/
│   ├── copy-generator.py       # 核心生成腳本
│   ├── ab-test-generator.py    # A/B 測試生成
│   ├── audience-analyzer.py    # 受眾分析
│   ├── email-sender.py         # Email 發送
│   └── telegram-notifier.py    # Telegram 通知
├── references/
│   ├── api-docs.md             # API 文檔
│   ├── examples.md             # 示例文案
│   ├── best-practices.md       # 最佳實踐
│   └── facebook-ad-policy.md   # FB 廣告政策指南
└── assets/
    └── templates/
        ├── email-template.html # Email 交付模板
        └── report-template.md  # 交付包模板
```

---

## 🔧 配置選項

### 環境變量

| 變量 | 說明 | 必填 |
|------|------|------|
| `GLM_API_KEY` | GLM-4-Flash API Key | ✅ |
| `RESEND_API_KEY` | Resend Email API Key | ❌ |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | ❌ |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | ❌ |

### 生成選項

| 選項 | 說明 | 預設值 |
|------|------|--------|
| `--product` | 產品名稱 | - |
| `--audience` | 目標受眾 | - |
| `--budget` | 廣告預算 | - |
| `--styles` | 廣告風格（逗號分隔） | 全部 6 種 |
| `--language` | 語言 | `zh-HK` |
| `--tone` | 語氣風格 | `professional+friendly` |
| `--output` | 輸出格式 | `markdown` |
| `--variations` | 每個風格變體數量 | `1` |

---

## 📚 示例文案

### 示例 1：護膚品（FOMO 風格）

**產品：** 維 C 亮白精華素  
**受眾：** 25-45 歲女性  
**預算：** $5,000-8,000 HKD/月

**生成文案：**
```
⏰ 最後 3 日！香港女生瘋搶嘅亮白秘密

點解最近成個 FB 都係佢？🤔

過去 2 個星期，超過 2,000 位香港女生已經試過我哋嘅維 C 亮白精華素...

而家庫存告急！🚨

「用完第一支，色斑真係淡咗，同事仲問我係咪換咗粉底液！」- Karen, 32 歲

「28 日後，肌膚真係光咗一個度，唔係講笑！」- Michelle, 28 歲

🔬 15% 高濃度維 C，韓國進口原料
👩‍⚕️ 香港皮膚科醫生推薦
🌿 100% 天然，無添加防腐劑
✨ 28 日實證亮白效果

⚠️ 警告：由於需求激增，現貨只餘下最後 87 支

下次到貨要等 3-4 週... 你確定要錯過？

👉 立即搶購：https://beautyskin.com.hk/vitamin-c-serum

#香港品牌 #維 C 精華 #亮白護膚 #限時優惠
```

### 示例 2：電子產品（社交證明風格）

**產品：** 無線降噪耳機  
**受眾：** 18-35 歲，音樂愛好者  
**預算：** $3,000-5,000 HKD/月

**生成文案：**
```
🌟 超過 10,000 位音樂愛好者選擇嘅無線耳機

⭐⭐⭐⭐⭐ 4.8/5.0（基於 2,345 條真實評價）

「音質好到爆，降噪效果一流！坐地鐵都聽得清楚！」
- Alex C., 已購買 2 次

「40 小時續航，真係一星期都唔使充電！」
- Jason L., 已購買 1 次

「性價比超高，唔輸千元大牌！」
- Stephanie W., 已購買 3 次

📊 用戶實證數據：
✅ 96% 用戶滿意音質
✅ 93% 用戶滿意降噪效果
✅ 98% 用戶會推薦俾朋友

🏆 2025 年香港音響大獎 - 最佳無線耳機獎

你，係時候升級你嘅聽覺體驗！

👉 查看完整評價：https://audiotech.com.hk/reviews

#香港之選 #無線耳機 #降噪耳機 #真實評價
```

---

## 🎓 最佳實踐

### 1. 文案撰寫技巧

✅ **應該做：**
- 使用粵語口語化表達
- 適當使用 Emoji（3-5 個）
- 包含明確的 CTA
- 突出產品獨特賣點
- 使用數字和數據增強說服力
- 加入社會證明（評價、銷量）

❌ **不應該做：**
- 使用「免費」、「最平」等違規詞語
- 過度承諾效果（「100% 保證」）
- 文案過長（超過 500 字）
- 使用太多 Emoji（超過 10 個）
- 缺少明確的 CTA
- 忽略目標受眾痛點

### 2. A/B 測試技巧

- **每次只測試一個變量**（標題/文案/CTA/圖片）
- **預算分配均勻**（每個版本 50%）
- **測試週期足夠**（至少 3-7 日）
- **樣本數足夠**（每個版本至少 1,000 次展示）
- **記錄所有數據**（CTR、CPC、轉化率、ROAS）

### 3. 投放優化技巧

- **第 1 週：** 測試多個標題和文案風格
- **第 2 週：** 聚焦最佳表現組合
- **第 3 週：** 擴展相似受眾
- **第 4 週：** 穩定投放，持續優化
- **每週：** 檢視數據，調整策略

---

## 🐛 故障排除

### 問題 1：API 調用失敗

**錯誤信息：** `401 Unauthorized`

**解決方法：**
```bash
# 檢查 API Key 是否正確
echo $GLM_API_KEY

# 重新設置
export GLM_API_KEY="your-correct-api-key"
```

### 問題 2：文案生成質量低

**可能原因：** 提示詞不夠具體

**解決方法：**
```bash
# 提供更多產品細節
python scripts/copy-generator.py generate \
  --product "維 C 亮白精華素" \
  --description "15% 高濃度維 C，韓國進口，28 日實證效果" \
  --audience "25-45 歲女性，關注肌膚保養" \
  --usp "香港皮膚科醫生推薦，100% 天然成分"
```

### 問題 3：Email 發送失敗

**錯誤信息：** `403 Forbidden`

**解決方法：**
- 在 Resend Dashboard 驗證域名
- 使用已驗證的域名作為發件人
- 檢查 API Key 權限

---

## 📊 定價建議

| 版本 | 功能 | 價格 | 適用對象 |
|------|------|------|----------|
| **基礎版** | 6 個廣告版本，基礎 A/B 測試 | $29 | 小型企業/初創 |
| **專業版** | 無限生成，進階 A/B 測試，受眾分析 | $99 | 中型企業/營銷機構 |
| **企業版** | 定制語氣，批量生成，API 訪問，優先支持 | $299 | 大型企業/代理商 |

### 性價比分析

**假設月預算 $8,000 HKD：**

- **基礎版（$29）：** ROAS 提升 10% → 額外回報 $800 → **ROI 2,658%**
- **專業版（$99）：** ROAS 提升 20% → 額外回報 $1,600 → **ROI 1,516%**
- **企業版（$299）：** ROAS 提升 30% → 額外回報 $2,400 → **ROI 702%**

---

## 🔄 更新日誌

### v1.0.0 (2026-03-15)
- ✨ 初始版本發布
- ✅ 6 個廣告風格生成
- ✅ A/B 測試建議（3 個組合）
- ✅ 目標受眾分析（3 個細分）
- ✅ 投放策略建議
- ✅ Email 交付功能
- ✅ Telegram 通知功能
- ✅ 符合 Facebook 廣告政策

### 待開發功能
- [ ] 多語言支持（英文/普通話）
- [ ] 圖片生成集成
- [ ] 視頻腳本生成
- [ ] 競爭對手分析
- [ ] 轉化率追蹤
- [ ] A/B 測試結果分析
- [ ] 自動優化建議

---

## 📞 支持與反饋

### 聯絡方式

- 📧 Email: support@vic-ai.com
- 💬 Telegram: @vicaimonitor_bot
- 🌐 網站：https://platform-cyan-zeta.vercel.app
- 📚 文檔：https://docs.vic-ai.com

### 提交問題

如遇到任何問題或有改進建議，歡迎提交 Issue：
https://github.com/vic-ai/fb-ads-copywriter-pro/issues

### 社區討論

加入我們的 Telegram 群組，與其他用戶交流心得：
https://t.me/vicai_community

---

## 📜 許可證

MIT License - 詳見 LICENSE 文件

---

## 🙏 致謝

- **GLM-4-Flash** - 提供強大的 AI 文案生成能力
- **Resend** - 提供可靠的 Email 發送服務
- **Telegram** - 提供即時通知功能
- **OpenClaw** - 提供技能包框架
- **ClawHub** - 提供技能包分發平台

---

**開發者：** Vic AI Company  
**版本：** 1.0.0  
**最後更新：** 2026-03-15  
**狀態：** ✅ 已發布
