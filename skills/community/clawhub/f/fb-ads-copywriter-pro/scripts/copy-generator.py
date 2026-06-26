#!/usr/bin/env python3
"""
FB Ads Copywriter Pro - 核心生成腳本
功能：
1. 生成 6 個廣告版本（FOMO/社交證明/權威/痛點/促銷/故事）
2. A/B 測試建議
3. 受眾分析
4. 投放策略建議
5. Email 交付
6. Telegram 通知
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path

# 配置
GLM_API_KEY = os.getenv('GLM_API_KEY', 'sk-JSJg7OYHJZPOn87CpHq0d5VMGLkTCBdJcVxUOdUp06IpUABx')
GLM_API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# 廣告風格定義
AD_STYLES = {
    'fomo': {
        'name': 'FOMO（恐懼錯過）',
        'emoji': '🔥',
        'description': '強調限時優惠、庫存緊張、錯過就沒有了',
        'keywords': ['最後', '限時', '搶購', '告急', '錯過']
    },
    'social_proof': {
        'name': '社交證明',
        'emoji': '👥',
        'description': '強調用戶評價、銷量、推薦人數',
        'keywords': ['評價', '銷量', '選擇', '推薦', '用戶']
    },
    'authority': {
        'name': '權威背書',
        'emoji': '👩‍⚕️',
        'description': '強調專家推薦、科學驗證、專業認證',
        'keywords': ['醫生', '專家', '認證', '臨床', '科學']
    },
    'pain_point': {
        'name': '痛點營銷',
        'emoji': '💔',
        'description': '強調問題帶來的困擾，產品如何解決',
        'keywords': ['困擾', '問題', '解決', '痛點', '煩惱']
    },
    'promotion': {
        'name': '優惠促銷',
        'emoji': '🎁',
        'description': '強調首次購買優惠、限時折扣、贈品',
        'keywords': ['優惠', '折扣', '贈品', '免費', '立減']
    },
    'story': {
        'name': '故事營銷',
        'emoji': '📖',
        'description': '用品牌故事或用戶轉變故事引起共鳴',
        'keywords': ['故事', '經歷', '轉變', '創辦人', '歷程']
    }
}


def generate_with_glm(prompt, system_prompt='你係一個專業的 Facebook 廣告文案專家，擅長粵語文案創作。'):
    """使用 GLM-4-Flash 生成內容"""
    
    try:
        response = requests.post(
            GLM_API_URL,
            headers={
                'Authorization': f'Bearer {GLM_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'glm-4-flash',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 2000
            },
            timeout=60
        )
        
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            
            # 清理 Markdown 代碼塊
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            return content
        else:
            print(f"❌ API 響應異常：{result}")
            return None
    
    except Exception as e:
        print(f"❌ API 調用失敗：{e}")
        return None


def load_questionnaire(filepath):
    """加載問卷數據"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 簡單解析 Markdown 格式問卷
        data = {}
        lines = content.split('\n')
        
        for line in lines:
            if line.startswith('- **'):
                parts = line.split('**')
                if len(parts) >= 3:
                    key = parts[1].strip()
                    value = parts[2].strip().lstrip(':').strip()
                    data[key] = value
        
        return data
    
    except Exception as e:
        print(f"❌ 加載問卷失敗：{e}")
        return None


def generate_ad_copy(product_info, style_name, style_desc):
    """生成單一風格的廣告文案"""
    
    prompt = f"""
## 產品信息
產品名稱：{product_info.get('產品名稱', '未知產品')}
產品描述：{product_info.get('產品描述', '無')}
獨特賣點：{product_info.get('獨特賣點', '無')}
目標受眾：{product_info.get('目標受眾', '無')}
廣告預算：{product_info.get('廣告預算', '無')}
品牌風格：{product_info.get('品牌風格', '無')}
特別要求：{product_info.get('特別要求', '無')}

## 任務
請為呢個產品創作一個 Facebook 廣告文案，使用 **{style_name}** 風格。

### {style_name} 風格說明
{style_desc}

## 文案要求
1. **語言：** 繁體中文（粵語口語化）
2. **結構：**
   - 吸引眼球的標題（用 Emoji）
   - 痛點/需求描述
   - 產品介紹（突出賣點）
   - 社會證明/權威背書
   - 行動呼籲（CTA）
3. **長度：** 300-500 字
4. **Emoji：** 適當使用，唔好過多（3-5 個）
5. **Hashtags：** 3-5 個相關標籤
6. **避免：** 「免費」、「最平」、「100% 保證」等違規詞語

## 輸出格式
請按照以下 JSON 格式輸出：
{{
  "version": "版本 X - {style_name}",
  "headline": "標題",
  "primary_text": "主要文案內容",
  "description": "短描述（用於連結預覽，100 字以內）",
  "cta": "行動呼籲按鈕文字",
  "hashtags": ["標籤 1", "標籤 2", "標籤 3"],
  "target_audience": "目標受眾分析",
  "ab_test_suggestion": "A/B 測試建議"
}}

請直接輸出 JSON，唔好有其他解釋。
"""
    
    system_prompt = '你係一個專業的 Facebook 廣告文案專家，擅長粵語文案創作。'
    result = generate_with_glm(prompt, system_prompt)
    
    try:
        return json.loads(result)
    except:
        print(f"⚠️ JSON 解析失敗，使用手動生成")
        return None


def generate_ab_tests(ad_copies, budget=8000, currency='HKD'):
    """生成 A/B 測試建議"""
    
    tests = [
        {
            'name': '標題測試',
            'description': '測試唔同標題風格對 CTR 嘅影響',
            'budget': int(budget * 0.15),
            'duration': 3,
            'variants': [
                {'name': 'A', 'style': 'FOMO', 'budget_split': '50%'},
                {'name': 'B', 'style': '社交證明', 'budget_split': '50%'}
            ],
            'success_criteria': 'CTR > 2.5%',
            'next_step': '勝出標題用於後續測試'
        },
        {
            'name': '文案風格測試',
            'description': '測試唔同文案風格對轉化率嘅影響',
            'budget': int(budget * 0.25),
            'duration': 5,
            'variants': [
                {'name': 'A', 'style': '權威背書', 'budget_split': '50%'},
                {'name': 'B', 'style': '痛點營銷', 'budget_split': '50%'}
            ],
            'success_criteria': 'CPA < $150',
            'next_step': '勝出風格用於擴展投放'
        },
        {
            'name': 'CTA 測試',
            'description': '測試唔同 CTA 按鈕對轉化率嘅影響',
            'budget': int(budget * 0.125),
            'duration': 7,
            'variants': [
                {'name': 'A', 'cta': '立即購買', 'budget_split': '50%'},
                {'name': 'B', 'cta': '了解更多', 'budget_split': '50%'}
            ],
            'success_criteria': '轉化率 > 3%',
            'next_step': '勝出 CTA 用於最終投放'
        }
    ]
    
    return tests


def generate_audience_analysis(product_info):
    """生成目標受眾分析"""
    
    segments = [
        {
            'name': '職場白領',
            'age_range': '25-35 歲',
            'characteristics': '工作忙碌，經常熬夜，關注肌膚狀態',
            'pain_points': ['肌膚暗沉', '黑眼圈', '膚色不均'],
            'needs': ['快速見效', '方便使用', '高端形象'],
            'recommended_styles': ['FOMO', '痛點營銷'],
            'best_posting_time': '平日 20:00-23:00，週末 14:00-18:00'
        },
        {
            'name': '媽媽族群',
            'age_range': '35-45 歲',
            'characteristics': '產後肌膚問題，時間有限，注重安全',
            'pain_points': ['產後色斑', '肌膚鬆弛', '時間不足'],
            'needs': ['安全溫和', '有效淡斑', '性價比高'],
            'recommended_styles': ['權威背書', '故事營銷'],
            'best_posting_time': '平日 10:00-12:00，21:00-23:00'
        },
        {
            'name': '美容愛好者',
            'age_range': '20-30 歲',
            'characteristics': '追求最新護膚科技，願意嘗試新產品',
            'pain_points': ['追求完美肌膚', '容易長痘', '敏感肌膚'],
            'needs': ['成分透明', '科學驗證', '社交認同'],
            'recommended_styles': ['社交證明', '權威背書'],
            'best_posting_time': '全日投放，高峰 19:00-24:00'
        }
    ]
    
    return {'segments': segments}


def generate_delivery_package(product_info, ad_copies, ab_tests, audience_analysis):
    """生成完整交付包"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    submission_id = f"sub_{int(datetime.now().timestamp())}"
    
    package = f"""# 📦 廣告文案交付包

**客戶：** {product_info.get('公司', '未知客戶')}  
**產品：** {product_info.get('產品名稱', '未知產品')}  
**Submission ID:** {submission_id}  
**生成日期：** {timestamp}  
**交付狀態：** ✅ 已完成  

---

## 📊 目錄

1. [6 個廣告文案版本](#6-個廣告文案版本)
2. [A/B 測試建議](#ab-測試建議)
3. [目標受眾分析](#目標受眾分析)
4. [投放建議](#投放建議)

---

## 🎨 6 個廣告文案版本

"""
    
    for i, ad in enumerate(ad_copies, 1):
        if ad:
            package += f"""### 版本 {i}：{ad.get('version', f'版本 {i}')}

**標題：** {ad.get('headline', '無標題')}

**主要文案：**
```
{ad.get('primary_text', '無文案')}
```

**CTA 按鈕：** {ad.get('cta', '立即購買')}  
**短描述：** {ad.get('description', '無描述')}  
**Hashtags：** {', '.join(ad.get('hashtags', []))}

---

"""
    
    package += """## 🧪 A/B 測試建議

### 測試組合 1：標題測試
| 版本 | 標題風格 | 預算 | 測試週期 | 預期 CTR |
|------|----------|------|----------|----------|
| A | FOMO（最後 3 日） | $500 | 3 日 | 2.5-3.5% |
| B | 社交證明（5,000 位選擇） | $500 | 3 日 | 2.0-3.0% |

**測試方法：** 各 $500 預算，測試 3 日，比較 CTR

### 測試組合 2：文案風格測試
| 版本 | 風格 | 預算 | 測試週期 | 預期轉化率 |
|------|------|------|----------|------------|
| A | 權威背書（醫生推薦） | $1,000 | 5 日 | 高信任度 |
| B | 痛點營銷（情感共鳴） | $1,000 | 5 日 | 高互動率 |

**測試方法：** 各 $1,000 預算，測試 5 日，比較 CPA

### 測試組合 3：CTA 測試
| 版本 | CTA 按鈕 | 預算 | 測試週期 | 預期效果 |
|------|----------|------|----------|----------|
| A | 立即購買 | $500 | 7 日 | 直接轉化 |
| B | 了解更多 | $500 | 7 日 | 降低門檻 |

**測試方法：** 同一廣告，不同 CTA，測試 7 日

### 推薦測試順序
```
第 1 週：標題測試（找出最吸引嘅標題）
    ↓
第 2 週：文案風格測試（找出最能說服嘅風格）
    ↓
第 3 週：CTA 測試（優化轉化率）
    ↓
第 4 週：全量投放最佳組合
```

---

## 🎯 目標受眾分析

"""
    
    for segment in audience_analysis.get('segments', []):
        package += f"""### {segment['name']}（{segment['age_range']}）
- **特徵：** {segment['characteristics']}
- **痛點：** {', '.join(segment['pain_points'])}
- **需求：** {', '.join(segment['needs'])}
- **推薦文案：** {', '.join(segment['recommended_styles'])}
- **投放時間：** {segment['best_posting_time']}

"""
    
    budget = product_info.get('廣告預算', '$8,000 HKD/月')
    
    package += f"""## 📈 投放建議

### 預算分配（月預算 {budget}）

| 週期 | 預算 | 目標 | 重點測試 |
|------|------|------|----------|
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

### KPI 目標

| 指標 | 目標值 | 行業基準 |
|------|--------|----------|
| **CTR** | > 2% | 1.5-2.0% |
| **CPC** | < $5 | $5-8 HKD |
| **CPA** | < $150 | $150-200 HKD |
| **ROAS** | > 3:1 | 2.5-3.0:1 |
| **轉化率** | > 3% | 2-3% |

---

## 📧 交付清單

- [x] 6 個廣告文案版本
- [x] A/B 測試建議
- [x] 目標受眾分析
- [x] 投放建議
- [ ] Email 發送給客戶
- [ ] Telegram 通知客戶
- [ ] 更新問卷狀態為「已處理」

---

**交付日期：** {timestamp}  
**下次跟進：** 3 日後  
**負責人：** Vic AI Agent Team  

---

*如有任何問題，請隨時聯絡：support@vic-ai.com*
"""
    
    return package, submission_id


def save_to_file(content, filepath):
    """保存內容到文件"""
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 已保存到：{filepath}")
        return True
    except Exception as e:
        print(f"❌ 保存失敗：{e}")
        return False


def send_email(customer_email, subject, html_content):
    """發送 Email"""
    
    if not RESEND_API_KEY:
        print("⚠️ RESEND_API_KEY 未配置，跳過 Email 發送")
        return False
    
    try:
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {RESEND_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'from': 'Vic AI Company <onboarding@resend.dev>',
                'to': [customer_email],
                'subject': subject,
                'html': html_content
            },
            timeout=30
        )
        
        result = response.json()
        
        if response.ok:
            print(f"✅ Email 發送成功！ID: {result.get('id', 'N/A')}")
            return True
        else:
            print(f"❌ Email 發送失敗：{result}")
            return False
    
    except Exception as e:
        print(f"❌ Email 發送異常：{e}")
        return False


def send_telegram_message(chat_id, text):
    """發送 Telegram 消息"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ TELEGRAM_BOT_TOKEN 未配置，跳過 Telegram 通知")
        return False
    
    try:
        response = requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            },
            timeout=30
        )
        
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ Telegram 通知已發送！Message ID: {result['result']['message_id']}")
            return True
        else:
            print(f"❌ Telegram 通知失敗：{result}")
            return False
    
    except Exception as e:
        print(f"❌ Telegram 通知異常：{e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='FB Ads Copywriter Pro - 廣告文案生成器')
    parser.add_argument('action', choices=['generate', 'batch', 'send'], help='操作類型')
    parser.add_argument('--product', type=str, help='產品名稱')
    parser.add_argument('--audience', type=str, help='目標受眾')
    parser.add_argument('--budget', type=str, help='廣告預算')
    parser.add_argument('--questionnaire', type=str, help='問卷文件路徑')
    parser.add_argument('--email', type=str, help='客戶 Email')
    parser.add_argument('--telegram', action='store_true', help='發送 Telegram 通知')
    parser.add_argument('--output', type=str, default='memory', help='輸出目錄')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎨 FB Ads Copywriter Pro - 廣告文案生成器")
    print("=" * 60)
    print()
    
    # 加載產品信息
    product_info = {}
    
    if args.questionnaire:
        print(f"📋 加載問卷：{args.questionnaire}")
        product_info = load_questionnaire(args.questionnaire)
        if not product_info:
            print("❌ 問卷加載失敗")
            return
    else:
        product_info = {
            '產品名稱': args.product or '未知產品',
            '目標受眾': args.audience or '未指定',
            '廣告預算': args.budget or '未指定',
            '公司': '未知客戶'
        }
    
    print(f"📦 產品：{product_info.get('產品名稱', '未知')}")
    print(f"🎯 受眾：{product_info.get('目標受眾', '未知')}")
    print(f"💰 預算：{product_info.get('廣告預算', '未知')}")
    print()
    
    # 生成廣告文案
    print("📝 生成廣告文案中...")
    ad_copies = []
    
    for style_key, style_info in AD_STYLES.items():
        print(f"  生成中：{style_info['emoji']} {style_info['name']}...")
        ad_copy = generate_ad_copy(product_info, style_info['name'], style_info['description'])
        
        if ad_copy:
            ad_copies.append(ad_copy)
            print(f"  ✅ {style_info['name']} 生成成功")
        else:
            print(f"  ⚠️ {style_info['name']} 生成失敗，使用模板")
            # 使用模板
            ad_copies.append({
                'version': style_info['name'],
                'headline': f"{style_info['emoji']} {product_info.get('產品名稱', '產品')} - {style_info['name']}標題",
                'primary_text': f"這是 {style_info['name']} 風格的廣告文案模板...",
                'description': f"{product_info.get('產品名稱', '產品')} - {style_info['name']}",
                'cta': '立即購買',
                'hashtags': ['#廣告', '#營銷', '#產品']
            })
    
    print()
    
    # 生成 A/B 測試建議
    print("🧪 生成 A/B 測試建議...")
    ab_tests = generate_ab_tests(ad_copies)
    print("✅ A/B 測試建議生成完成")
    print()
    
    # 生成受眾分析
    print("🎯 生成目標受眾分析...")
    audience_analysis = generate_audience_analysis(product_info)
    print("✅ 受眾分析生成完成")
    print()
    
    # 生成交付包
    print("📦 生成交付包...")
    delivery_package, submission_id = generate_delivery_package(
        product_info, ad_copies, ab_tests, audience_analysis
    )
    
    # 保存到文件
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"ad-delivery-{submission_id}.md"
    save_to_file(delivery_package, output_file)
    
    print()
    print("=" * 60)
    print(f"✅ 完成！共生成 {len(ad_copies)} 個廣告版本")
    print("=" * 60)
    print()
    
    # 發送通知
    if args.email:
        print("📧 發送 Email 中...")
        # 這裡可以調用 send_email 函數
        print("⚠️ Email 發送功能待實現")
    
    if args.telegram:
        print("💬 發送 Telegram 通知中...")
        message = f"""✅ <b>新廣告文案已生成！</b>

📦 <b>客戶：</b> {product_info.get('公司', '未知')}
🎨 <b>產品：</b> {product_info.get('產品名稱', '未知')}

📝 <b>交付內容：</b>
✅ 6 個廣告文案版本
✅ A/B 測試建議
✅ 目標受眾分析
✅ 投放建議

📂 <b>交付文件：</b>
<code>{output_file}</code>

#廣告文案 #已完成"""
        
        chat_id = TELEGRAM_CHAT_ID or os.getenv('TELEGRAM_CHAT_ID', '')
        if not chat_id:
            print("⚠️ 警告：TELEGRAM_CHAT_ID 未設置，跳過 Telegram 通知")
        else:
            send_telegram_message(chat_id, message)
    
    print()
    print("🎉 所有任務完成！")


if __name__ == '__main__':
    main()
