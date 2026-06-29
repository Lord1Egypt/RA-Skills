# 🔮 Financial Astrology — Chiêm Tinh Tài Chính

**Phân tích chiêm tinh Vedic (Sidereal) ứng dụng vào thị trường tài chính** — Vàng (XAU/USD) & Bitcoin (BTC/USD).

<p align="center">
  <a href="https://clawhub.ai/skills/financial-astrology"><img src="https://img.shields.io/badge/clawhub-skill-blue" alt="ClawHub"></a>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/swisseph-v2.10.3.2-orange" alt="Swiss Ephemeris">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

**[🇺🇸 English](README.md)**

---

## 📖 Giới thiệu

**Financial Astrology** phân tích vị trí hành tinh (Vedic/Sidereal) và áp dụng vào **giao dịch ngắn hạn (Day Trading M15/H1)**. Sử dụng [Swiss Ephemeris](https://www.astro.com/swisseph) — thư viện thiên văn chính xác nhất thế giới — chạy hoàn toàn **offline**, không cần API bên ngoài.

> ⚠️ **Disclaimer:** Correlation ≠ causation. Đây là công cụ **bổ trợ**, không phải dự báo chính xác. Đầu tư có rủi ro.

## ✨ Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| 🌙 **Moon Phase** | Tâm lý thị trường theo pha Mặt Trăng |
| 🌟 **Nakshatra** | 27 Nakshatra + Pada + Trading quality |
| 🪐 **Hành tinh** | 8 hành tinh + 3 ngoại hành tinh (sidereal) |
| 🏠 **Houses** | Whole Sign Houses + Ascendant |
| 🔗 **Aspects** | Conjunction, Trine, Square, Opposition... |
| 🔥 **Combustion** | Hành tinh bị Mặt Trời đốt cháy |
| ⚡ **Cazimi** | Hành tinh trong tim Mặt Trời |
| 🌙☌ **Moon Combinations** | Chandra-Mangal, Vish Yoga, Grahan Yoga... |
| ⏰ **Hora** | Giờ hành tinh (Planetary Hours) |
| 📊 **Sector Analysis** | Vàng→Sun/Venus, Bitcoin→Rahu/Uranus |
| 🌀 **Dasha** | Vimshottari Dasha cho Natal Chart |
| 🎯 **Day Trading Signal** | Tín hiệu M15/H1 |

## 🚀 Cài đặt

```bash
pip install pyswisseph
git clone https://github.com/kimminhpro/financial-astrology-skill.git
cd financial-astrology-skill
python3 scripts/financial_astrology.py
```

## 🔧 Sử dụng

```bash
# Hiện tại (JST)
python3 scripts/financial_astrology.py

# Thời gian cụ thể
python3 scripts/financial_astrology.py --date "2026-05-02 12:10:00" --tz Asia/Tokyo

# Phân tích Vàng
python3 scripts/financial_astrology.py --asset gold

# Phân tích Bitcoin
python3 scripts/financial_astrology.py --asset btc

# Xuất JSON
python3 scripts/financial_astrology.py --json

# Natal Chart + Dasha
python3 scripts/financial_astrology.py --date "1995-04-25 18:30:00" --tz Asia/Ho_Chi_Minh --lat 21.1861 --lon 106.0763 --natal
```

Chi tiết xem tại [README.md](README.md) tiếng Anh.

## ⚠️ Cảnh báo

- ❌ Không cam kết lợi nhuận
- ❌ Không thay thế phân tích kỹ thuật/cơ bản
- ✅ Luôn dùng stop loss
- ✅ Tự chịu trách nhiệm
