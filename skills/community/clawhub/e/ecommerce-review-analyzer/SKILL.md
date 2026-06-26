---
name: ecommerce-review-analyzer
description: 淘宝京东拼多多评论分析工具。自动抓取商品评论，分析好评差评，生成专业分析报告。支持多店铺多商品对比，差评详情分析，改进建议。电商运营必备工具。
version: 1.0.7
license: MIT-0
metadata: {"openclaw": {"emoji": "📊", "requires": {"bins": ["python3"], "env": []}, "minVersion": "2026.3.22", "needsBrowser": true}}
dependencies: "pip install jieba python-docx fpdf2"
---

# 淘宝京东拼多多评论分析工具

自动抓取商品评论，分析好评差评，生成专业分析报告。

## 功能特点

- 🛒 **三平台支持**：淘宝、京东、拼多多
- 📊 **自动抓取**：浏览器自动化获取评论
- 🧠 **智能分析**：AI分析评论内容和情感
- 📈 **评分统计**：好评率、差评率、评分分布
- 💬 **差评详情**：完整差评内容和出处
- 💡 **改进建议**：AI生成改进建议
- 📄 **专业报告**：Word和PDF双格式输出
- 🎯 **多商品对比**：同一店铺多个商品对比
- 🏪 **多店铺对比**：不同店铺对比分析
- 💡 **改进建议**: AI生成改进建议
- 📄 **专业报告**: Word (.docx) + PDF 输出
- 🎯 **多商品**: 支持同一店铺多个商品
- 🏪 **多店铺**: 支持不同店铺对比分析
- 🛒 **多平台**: 支持淘宝/京东/拼多多对比

## 使用场景

- "分析淘宝店铺评论" / "Analyze Taobao reviews"
- "查看京东差评" / "Check JD negative reviews"
- "帮我分析这个产品的用户反馈"
- "ecommerce-review-analyzer"

## 支持平台

| 平台 | 方式 | 需要登录 |
|------|------|----------|
| 淘宝 | 浏览器自动化 | ✅ |
| 京东 | 浏览器自动化 | ✅ |
| 拼多多 | 浏览器自动化 | ✅ |

## 前置条件

- OpenClaw v2026.3.22+ (浏览器自动化)
- **必须使用OpenClaw内置浏览器自动化**（不支持第三方浏览器工具）
- 已登录目标电商平台
- 已配置OpenClaw browser工具

## ⚠️ 重要声明

> **本技能强制使用OpenClaw内置浏览器自动化功能。**
> 不支持Playwright、Selenium等第三方浏览器工具。
> 必须使用OpenClaw v2026.3.22+的browser工具。
> 浏览器会话继承用户已登录状态。

---

## 工作流程

```
用户请求
    ↓
1. 检测登录状态
    ↓
2. 协助扫码登录（如需要）
    ↓
3. 抓取商品评论
    ↓
4. AI分析评论内容
    ↓
5. 生成专业报告（Word+PDF）
```

---

## 输出格式

### Word报告 (.docx)

包含：
- 商品基本信息
- 评分分布表格
- 差评详情（含完整评论）
- 改进建议

### PDF报告

与Word内容完全一致，便于打印。

---

## 示例报告

```
┌─────────────────────────────────────────────┐
│  📊 商品评论分析报告                         │
└─────────────────────────────────────────────┘

商品：智能手表 Pro
平台：淘宝 / 京东
分析评论：1,234条

📊 评分分布
├─ ⭐⭐⭐⭐⭐ 好评：78% (970条)
├─ ⭐⭐⭐ 中评：15% (186条)
└─ ⭐⭐ 差评：7% (78条)

💬 差评详情

差评 1: ⭐⭐
"充电太慢了，充满要4个小时，退货！"
👤 用户B | 📅 2026-03-18 | 🏪 科技旗舰店

差评 2: ⭐
"App经常闪退，客服态度差，差评！"
👤 用户C | 📅 2026-03-15 | 🏪 科技旗舰店

💡 改进建议
• 优化充电速度
• 修复App稳定性
• 加强客服培训
```

---

## 浏览器自动化代码

### 抓取淘宝评论

```javascript
// 1. 打开商品页面
await browser.open({
  url: "https://item.taobao.com/item.htm?id=商品ID"
})

// 2. 等待页面加载
await browser.wait({ timeout: 5000 })

// 3. 检查是否需要登录
const needsLogin = await browser.evaluate(() => {
  return document.querySelector('.login-dialog') !== null
})

if (needsLogin) {
  // 协助用户扫码登录
  const qrImage = await browser.screenshot({ selector: '.qrcode-img' })
  await chat.send("⚠️ 请扫描二维码登录淘宝：", { image: qrImage })
  await browser.waitForNavigation({ timeout: 120000 })
}

// 4. 点击"评价"标签
await browser.click({ selector: 'a[href="#J_TabBar"]' })
await browser.wait({ timeout: 3000 })

// 5. 滚动加载更多评论
for (let i = 0; i < 3; i++) {
  await browser.evaluate(() => window.scrollBy(0, 500))
  await browser.wait({ timeout: 1000 })
}

// 6. 提取评论数据
const reviews = await browser.evaluate(() => {
  const items = []
  document.querySelectorAll('.J_KgRate_ReviewItem').forEach(el => {
    const rating = el.querySelector('.tb-rev-item-rating')?.children.length || 0
    const content = el.querySelector('.tb-rev-item__body-text')?.innerText || ''
    const user = el.querySelector('.tb-rev-item__user-name')?.innerText || ''
    const date = el.querySelector('.tb-rev-item__time')?.innerText || ''
    
    items.push({
      rating: rating,
      content: content.trim(),
      user: user.trim(),
      date: date.trim()
    })
  })
  return items
})

return reviews
```

### 抓取京东评论

```javascript
// 1. 打开商品页面
await browser.open({
  url: "https://item.jd.com/商品ID.html"
})

// 2. 等待加载
await browser.wait({ timeout: 5000 })

// 3. 滚动到评论区
await browser.evaluate(() => {
  const element = document.querySelector('#comment')
  if (element) element.scrollIntoView()
})
await browser.wait({ timeout: 2000 })

// 4. 提取评论
const reviews = await browser.evaluate(() => {
  const items = []
  document.querySelectorAll('.comment-item').forEach(el => {
    const rating = el.querySelector('.comment-star')?.className.match(/\d+/) || [0]
    const content = el.querySelector('.comment-con')?.innerText || ''
    const user = el.querySelector('.user-name')?.innerText || ''
    const date = el.querySelector('.comment-date')?.innerText || ''
    
    items.push({
      rating: parseInt(rating[0]) || 5,
      content: content.trim(),
      user: user.trim(),
      date: date.trim()
    })
  })
  return items
})

return reviews
```

### 抓取拼多多评论

```javascript
// 1. 打开商品页面
await browser.open({
  url: "https://mobile.yangkeduo.com/goods.html?goods_id=商品ID"
})

// 2. 等待加载
await browser.wait({ timeout: 5000 })

// 3. 点击评价标签
await browser.click({ selector: '[class*="comment"]' })
await browser.wait({ timeout: 2000 })

// 4. 提取评论
const reviews = await browser.evaluate(() => {
  const items = []
  document.querySelectorAll('[class*="comment-item"]').forEach(el => {
    const content = el.innerText || ''
    if (content.length > 10) {
      items.push({
        content: content.trim(),
        platform: '拼多多'
      })
    }
  })
  return items
})

return reviews
```

---

## Python代码示例

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from fpdf import FPDF
from datetime import datetime
import os

class ReviewAnalyzer:
    def __init__(self):
        self.reviews = []
    
    def add_review(self, product, platform, store, rating, content, date, user):
        """添加评论数据"""
        self.reviews.append({
            'product': product,
            'platform': platform,
            'store': store,
            'rating': rating,
            'content': content,
            'date': date,
            'user': user
        })
    
    def analyze(self):
        """分析评论数据"""
        total = len(self.reviews)
        if total == 0:
            return None
        
        positive = len([r for r in self.reviews if r['rating'] >= 4])
        negative = len([r for r in self.reviews if r['rating'] <= 2])
        neutral = total - positive - negative
        avg_rating = sum(r['rating'] for r in self.reviews) / total
        
        return {
            'total': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'avg_rating': avg_rating,
            'positive_rate': positive / total * 100,
            'negative_rate': negative / total * 100,
            'negative_reviews': [r for r in self.reviews if r['rating'] <= 2]
        }
    
    def generate_word_report(self, analysis, output_path):
        """生成Word报告"""
        doc = Document()
        section = doc.sections[0]
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)
        
        # 标题
        title = doc.add_heading('Product Review Analysis Report', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 基本信息
        info_table = doc.add_table(rows=4, cols=2)
        info_table.style = 'Table Grid'
        info_table.cell(0, 0).text = 'Product'
        info_table.cell(0, 1).text = self.reviews[0]['product'] if self.reviews else 'N/A'
        info_table.cell(1, 0).text = 'Platform'
        info_table.cell(1, 1).text = self.reviews[0]['platform'] if self.reviews else 'N/A'
        info_table.cell(2, 0).text = 'Reviews'
        info_table.cell(2, 1).text = str(analysis['total'])
        info_table.cell(3, 0).text = 'Date'
        info_table.cell(3, 1).text = datetime.now().strftime('%Y-%m-%d')
        
        doc.add_paragraph()
        
        # 评分分布
        h = doc.add_heading('Rating Distribution', level=1)
        
        rating_table = doc.add_table(rows=4, cols=3)
        rating_table.style = 'Table Grid'
        rating_table.cell(0, 0).text = 'Rating'
        rating_table.cell(0, 1).text = 'Count'
        rating_table.cell(0, 2).text = 'Percentage'
        rating_table.cell(1, 0).text = 'Positive (4-5)'
        rating_table.cell(1, 1).text = str(analysis['positive'])
        rating_table.cell(1, 2).text = f"{analysis['positive_rate']:.1f}%"
        rating_table.cell(2, 0).text = 'Neutral (3)'
        rating_table.cell(2, 1).text = str(analysis['neutral'])
        rating_table.cell(2, 2).text = f"{analysis['neutral'] / analysis['total'] * 100:.1f}%"
        rating_table.cell(3, 0).text = 'Negative (1-2)'
        rating_table.cell(3, 1).text = str(analysis['negative'])
        rating_table.cell(3, 2).text = f"{analysis['negative_rate']:.1f}%"
        
        doc.add_paragraph()
        
        # 差评详情
        h = doc.add_heading('Negative Reviews', level=1)
        
        for i, review in enumerate(analysis['negative_reviews'], 1):
            entry = doc.add_paragraph()
            run = entry.add_run(f'Review {i}: {"*" * review["rating"]}')
            run.font.bold = True
            
            quote = doc.add_paragraph()
            quote.add_run(f'"{review["content"]}"').font.italic = True
            
            detail = doc.add_paragraph()
            detail.add_run(f'User: {review["user"]} | Date: {review["date"]}').font.color.rgb = RGBColor(100, 100, 100)
            
            doc.add_paragraph()
        
        doc.save(output_path)
        return output_path
    
    def generate_pdf_report(self, analysis, output_path):
        """生成PDF报告"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # 标题
        pdf.set_font('Helvetica', 'B', 20)
        pdf.set_text_color(30, 60, 114)
        pdf.cell(0, 12, 'Product Review Analysis', new_x='LMARGIN', new_y='NEXT', align='C')
        pdf.ln(5)
        
        # 基本信息
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(51, 51, 51)
        pdf.cell(0, 6, f'Reviews: {analysis["total"]}', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)
        
        # 评分分布
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(30, 60, 114)
        pdf.cell(0, 8, 'Rating Distribution', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)
        
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(51, 51, 51)
        pdf.cell(0, 6, f'Positive: {analysis["positive"]} ({analysis["positive_rate"]:.1f}%)', new_x='LMARGIN', new_y='NEXT')
        pdf.cell(0, 6, f'Negative: {analysis["negative"]} ({analysis["negative_rate"]:.1f}%)', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)
        
        # 差评详情
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(30, 60, 114)
        pdf.cell(0, 8, 'Negative Reviews', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(51, 51, 51)
        for i, review in enumerate(analysis['negative_reviews'], 1):
            pdf.cell(0, 6, f'Review {i}: {"*" * review["rating"]}', new_x='LMARGIN', new_y='NEXT')
            pdf.multi_cell(0, 5, f'"{review["content"]}"')
            pdf.cell(0, 5, f'User: {review["user"]} | Date: {review["date"]}', new_x='LMARGIN', new_y='NEXT')
            pdf.ln(5)
        
        pdf.output(output_path)
        return output_path

# 使用示例
analyzer = ReviewAnalyzer()

# 添加评论
analyzer.add_review('Smart Watch Pro', 'Taobao', 'Tech Store', 5, 'Very good!', '2026-03-20', 'User A')
analyzer.add_review('Smart Watch Pro', 'Taobao', 'Tech Store', 2, 'Bad quality!', '2026-03-15', 'User B')

# 分析
analysis = analyzer.analyze()

# 生成报告
analyzer.generate_word_report(analysis, 'report.docx')
analyzer.generate_pdf_report(analysis, 'report.pdf')
```

---

## Notes

- 使用OpenClaw内置浏览器自动化
- 需要登录电商平台
- 支持中文评论分析
- 数据准确性优先
- 数据准确性优先
- 支持中文评论分析
