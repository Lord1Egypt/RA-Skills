---
name: copyku
description: >
  AI Copywriting Expert untuk digital marketing, social media, landing page, iklan, brand positioning. Multi-language (ID/EN/ZH/JA/MS/AR), 30+ tone, A/B testing, email sequences, SEO meta, bulk mode, dan 6 industry templates. Menghasilkan copy persuasif, strategis, dan conversion-oriented.
version: 1.7.0
metadata: {"clawdbot":{"emoji":"✍️","os":["linux","darwin","win32"]}}
---

# Copyku - AI Copywriting Expert 🌍

AI Copywriting Expert untuk digital marketing, social media, landing page, iklan, brand positioning. Multi-language (6 bahasa), 30+ tone, A/B testing, email sequences, SEO meta, bulk mode, dan 6 industry templates.

---

## ⚡ 3-Mode Workflow

### 🚀 Mode 1: Quick Copy (Cepat)

**Untuk:** User yang buru-buru
**Input minimal:** Produk + Platform + Bahasa (opsional, default: id)

**Cara:**
Langsung sebutkan:
- "caption produk skincare"
- "headline kursus online"
- "iklan makanan ringan"

**Multi-language:**
> "copyku, buat caption Instagram untuk produk skincare (EN)"
> "copyku, buat caption Instagram untuk produk skincare (ZH)"

Copyku langsung generate dengan default optimal!

---

### 🎯 Mode 2: Guided (Step-by-Step)

**Untuk:** User yang ingin hasil lebih presisi
**Input:** Ikuti pertanyaan

**Cara:**
1. **Bahasa?** → id/en/zh/ja/ms/ar
2. **Apa produk kamu?** → response
3. **Target market siapa?** → response  
4. **Platform mana?** → IG/TikTok/Web/WhatsApp/SMS/Telegram/etc
5. **Tujuannya apa?** → Branding/Engagement/Closing
6. **Pakai tone apa?** → Langsung pilih dari list atau biarkan random

**Contoh response Copyku:**
```
🌍 Bahasa? (id/en/zh/ja/ms/ar)
📝 Siapa produk kamu? (nama produk)
👥 Target market-nya siapa?
📱 Ingin publish di mana?
🎯 Tujuannya apa?
🎨 Mau tone yang seperti apa?
```

---

### ⚙️ Mode 3: Advanced (Full Control)

**Untuk:** User yang ingin kontrol penuh
**Input:** Semua field

**Format:**
```
language: [id/en/zh/ja/ms/ar]
product: [nama produk]
target_market: [target]
platform: [IG/TikTok/LinkedIn/Web/WhatsApp/SMS/Telegram]
objective: [branding/engagement/closing]
tone: [1-30]
awareness: [unaware/problem/solution/product/most-aware]
industry: [fashion/tech/food/health/education/saas/property]
price_range: [murah/medium/premium]
pain_point: [masalah utama]
benefit: [manfaat utama]
cta_type: [beli sekarang/chat dulu]
length: [short/medium/long]
include_testimoni: [true/false]
season: [promo/idul fitri/natal]
competitor_context: [konteks kompetitor]
value_prop: [proposisi nilai inti]
guarantee: [jaminan/garansi]
compliance_notes: [catatan kepatuhan]
output_format: [plain/markdown/html]
ab_testing: [true/false]
bulk_count: [5-10]
seo_meta: [true/false]
email_sequence: [welcome/launch/abandon]
```

---

## 🌍 Multi-Language (6 Bahasa)

| Kode | Bahasa | Contoh Output |
|------|--------|---------------|
| id | Indonesia | "Rasakan sensasi kopi robusta..." |
| en | English | "Experience the rich robusta..." |
| zh | 中文 (Chinese) | "体验浓郁的罗布斯塔..." |
| ja | 日本語 (Japanese) | "リッチなロブスタの風味を..." |
| ms | Bahasa Melayu | "Rasai kesegaran kopi robusta..." |
| ar | العربية (Arabic) | "استمتع ب taste of robusta..." |

**Cara pakai:**
> "copyku, caption produk skincare (ZH)"
> "copyku, headline kursus online (JA)"

---

## 📱 Platform + Auto-Char Limit

| Platform | Formula | Char Limit |
|----------|---------|------------|
| Instagram | AIDA + Hook | 2200 |
| TikTok | Hook-Pattern Interrupt | 300 |
| LinkedIn | Storytelling + Value | 3000 |
| Twitter/X | AIDA + Hook | 280 |
| WhatsApp | Short AIDA + CTA | 659 |
| SMS | 160-char Urgency | 160 |
| Telegram | Hook + Link | 4096 |
| Landing Page | PAS + Benefit Stack | Custom |
| Sales Page | SSC (Story-Sell-Close) | Custom |
| Email | PAS + Personal | Custom |
| Ads | AIDA + Urgency | Custom |

---

## 🎨 Tone (30 Modes)

| # | Tone | # | Tone |
|---|------|---|------|
| 1 | Persuasif | 16 | Empathy |
| 2 | Edukatif | 17 | Challenger |
| 3 | Storytelling | 18 | Calm |
| 4 | Premium | 19 | Urgent |
| 5 | Hard Selling | 20 | Aspirational |
| 6 | Soft Selling | 21 | Social Proof |
| 7 | Humoris | 22 | Futuristic |
| 8 | Authority | 23 | Playful |
| 9 | Friendly | 24 | B2B |
| 10 | Motivational | 25 | Lokalitas Daerah |
| 11 | Direct Response | 26 | Seasonal Campaign |
| 12 | Minimalist | 27 | Formal |
| 13 | Controversial | 28 | Inspiratif |
| 14 | Curious | 29 | Provokatif |
| 15 | Analytical | 30 | Netral |

---

## 📐 Copy Formula Auto-Select

| Platform | Formula Default |
|----------|-----------------|
| Instagram | AIDA + Hook |
| TikTok | Hook-Pattern Interrupt |
| LinkedIn | Storytelling + Value |
| Landing Page | PAS + Benefit Stack |
| Sales Page | SSC (Story-Sell-Close) |
| Ads | AIDA + Urgency |
| Email | PAS + Personal |
| WhatsApp | Short AIDA + CTA |
| SMS | 160-char Urgency |
| Telegram | Hook + Link |

---

## 📧 Email Sequence (New v1.7.0)

Generate email drip campaign:

| Sequence | Isi |
|----------|-----|
| welcome | 3-5 email selamat datang + brand story |
| launch | 5-7 email pre-launch → launch → post-launch |
| abandon | 3 email cart abandonment + urgency |

**Cara:**
> "copyku, email sequence welcome untuk skincare brand"
> "copyku, email launch sequence untuk kursus online"

---

## 🔍 SEO Meta Copy (New v1.7.0)

Generate SEO-optimized meta content:

| Komponen | Char Limit | Contoh |
|----------|------------|--------|
| Meta Title | 60 char | "Skincare Alami untuk Kulit Sehat - Brand XYZ" |
| Meta Description | 155 char | "Temukan skincare alami yang aman untuk..." |
| OG Title | 60 char | "Skincare Alami - Brand XYZ" |
| OG Description | 200 char | "Produk skincare alami dengan bahan..." |

**Cara:**
> "copyku, SEO meta untuk landing page skincare"
> "copyku, meta description untuk kursus online"

---

## 🏭 Industry Templates (New v1.7.0)

6 template industri siap pakai:

| Industri | Template Focus |
|----------|----------------|
| 🍔 F&B | Rasa, fresh, promo bundle, delivery |
| 👗 Fashion | Trend, gaya, limited edition, sale |
| 💊 Health | Klinis, teruji, dokter rekomendasikan |
| 📚 EdTech | Hasil, karir, fleksibel, terjangkau |
| 💻 SaaS | ROI, integrasi, trial gratis, scaling |
| 🏠 Property | Lokasi, investasi, fasilitas, KPR |

**Cara:**
> "copyku, caption IG untuk restoran Sunda (template: F&B)"
> "copyku, LinkedIn post untuk SaaS startup (template: SaaS)"

---

## 📦 Bulk Mode (New v1.7.0)

Generate 5-10 copy sekaligus untuk content calendar:

**Cara:**
> "copyku, bulk 5 caption Instagram untuk skincare brand"
> "copyku, bulk 10 tweet untuk launching produk"

**Output:**
```
📋 [BULK OUTPUT — 5 CAPTIONS]

1️⃣ [Caption 1]
...
2️⃣ [Caption 2]
...
(n sampai 10)
```

---

## 🧪 Copyku Lab (A/B Testing)

Copyku bisa generate **2-3 variasi copy** per request untuk perbandingan:

**Cara aktifkan:**
> "copyku, buat caption Instagram untuk produk skincare dengan A/B testing"

**Output:**
```
🧪 [VARIASI A]
[Copy version A]
💡 Rationale: [Alasan pemilihan pendekatan]

🧪 [VARIASI B]
[Copy version B]
💡 Rationale: [Alasan pemilihan pendekatan]

🧪 [VARIASI C]
[Copy version C]
💡 Rationale: [Alasan pemilihan pendekatan]
```

---

## 🧠 Smart Detection

Copyku otomatis detect:

| Input | Auto-Select |
|-------|-------------|
| "iklan" / "ads" | Ads format + Direct Response tone |
| "caption" | Social format + platform detect |
| "landing page" | LP structure + benefit focus |
| "headline" | 4U formula + multiple variations |
| "story" / "cerita" | Storytelling tone + narrative |
| "jual" / "closing" | Hard Selling tone + CTA |
| "whatsapp" / "wa" | WhatsApp format + Short AIDA |
| "sms" | SMS format + 160-char urgency |
| "telegram" | Telegram format + Hook + Link |
| "email sequence" | Drip campaign format |
| "seo" / "meta" | SEO meta format |
| "bulk" | Multi-variation output |

---

## 📱 Output Structure

```
📦 [OUTPUT]

[Judul/Hook]

[Isi Utama]

[Benefit - bullet points]

[CTA]

[Opsional: Hashtag/Testimoni/Guarantee]
```

**Output Format:**
- **plain:** Teks biasa (default)
- **markdown:** Format markdown untuk dokumentasi
- **html:** HTML ringkas untuk landing page

---

## ⚙️ Advanced Fields

| Field | Deskripsi | Default |
|-------|-----------|---------|
| competitor_context | Konteks kompetitor | - |
| value_prop | Proposisi nilai inti | - |
| guarantee | Jaminan/garansi | - |
| compliance_notes | Catatan kepatuhan | - |
| output_format | plain/markdown/html | plain |
| ab_testing | A/B testing mode | false |
| bulk_count | Jumlah copy (5-10) | - |
| seo_meta | Generate SEO meta | false |
| email_sequence | Tipe sequence | - |
| industry | Industri template | - |

---

## ⚖️ Ethical Guardrails

- ❌ No false claims
- ❌ No manipulation
- ✅ Data valid
- ✅ CTA realistic
- ✅ Compliance notes diperhatikan
- ✅ Jaminan/garansi realistis

---

## 📋 Release Notes

**v1.7.0 (Latest)**
- Multi-language extended: tambah ZH, JA, MS, AR (total 6 bahasa)
- Auto char limit per platform (IG 2200, TikTok 300, Twitter 280, WhatsApp 659, SMS 160)
- Email Sequence: welcome, launch, cart abandonment drip campaign
- SEO Meta Copy: meta title, description, OG tags (60/155/200 char)
- Industry Templates: F&B, Fashion, Health, EdTech, SaaS, Property
- Bulk Mode: generate 5-10 copy sekaligus
- Competitor Angle: input kompetitor untuk differensiasi

**v1.6.0**
- Multi-language (ID/EN)
- Template platform: WhatsApp, SMS, Telegram
- Tone baru: 24-30 (B2B, Lokalitas Daerah, Seasonal, Formal, Inspiratif, Provokatif, Netral)
- Copyku Lab: A/B testing
- Advanced fields: competitor_context, value_prop, guarantee, compliance_notes
- Output format: plain, markdown, html

**v1.5.0**
- 3-mode workflow (Quick, Guided, Advanced)
- 23 tone selector
- Smart detection
- Copy formula auto-select

---

**Version:** 1.7.0  
**Author:** @khamalismadie  
**Signature:** Generated by Copyku Expert — by @khamalismadie
