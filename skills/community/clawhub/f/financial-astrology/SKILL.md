---
name: financial-astrology
description: Phân tích chiêm tinh tài chính (Financial Astrology) — tính vị trí hành tinh, Nakshatra, Houses, aspects, combustion, và đánh giá tâm lý đám đông thị trường. Hỗ trợ phân tích Vàng (XAU/USD), Bitcoin (BTC/USD), và các thị trường tài chính. Focus: Day Trading M15/H1.
---

# 📊 Financial Astrology — Chiêm Tinh Tài Chính

Phân tích vị trí hành tinh + Nakshatra + Pada + Houses + Aspects + Combustion + **Tâm lý thị trường** theo quy tắc Financial Astrology.

## 🌙 QUY TẮC VÀNG: MOON LÀ "ACTIVATOR"

> **"Mỗi hành tinh có một xu hướng, nhưng Mặt Trăng quyết định xu hướng nào được kích hoạt HÔM NAY."**

Trong Vedic Astrology, Moon đại diện cho **Manas (Tâm trí)**. Vì thị trường tài chính là phản ánh của tâm lý đám đông (Fear & Greed), Moon di chuyển qua các Nakshatra sẽ xác định mood của trader mỗi ngày.

**Quy tắc:** "Hành tinh mà Moon tương tác hôm nay (qua Conjunction, Aspect, hoặc Nakshatra Lord) sẽ đặt trend cho cả phiên."

## ⚠️ Quy Tắc Tính Toán

### Julian Day (ĐÚNG CÁCH)
```python
# ✅ ĐÚNG: UTC trước, rồi mới tính JD
dt_utc = datetime.now(timezone.utc)
jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 
                dt_utc.hour + dt_utc.minute / 60.0, cal=swe.GREG_CAL)

# ❌ SAI: KHÔNG bao giờ cộng timezone offset vào giờ
jd = swe.julday(2026, 5, 1, 16+9)  # SAI!
```

### Input/Output
- **Input/Output**: JST (Asia/Tokyo, UTC+9) mặc định
- **Tính toán**: UTC
- **Ascendant sidereal** = Ascendant tropical − ayanamsa
- **House System**: Whole Sign (Vedic)

## 📋 Sử Dụng Script

### Phân tích Chiêm tinh Tài chính
```bash
# Phân tích hiện tại (JST)
python3 skills/financial-astrology/scripts/financial_astrology.py

# Thời gian cụ thể
python3 skills/financial-astrology/scripts/financial_astrology.py --date "2026-05-02 12:10:00" --tz Asia/Tokyo

# Chỉ định tọa độ
python3 skills/financial-astrology/scripts/financial_astrology.py --lat 34.93 --lon 136.97

# Phân tích asset cụ thể
python3 skills/financial-astrology/scripts/financial_astrology.py --asset gold
python3 skills/financial-astrology/scripts/financial_astrology.py --asset btc

# Xuất JSON
python3 skills/financial-astrology/scripts/financial_astrology.py --json

# Natal Chart với Dasha (Đại vận - Tiểu vận)
python3 skills/financial-astrology/scripts/financial_astrology.py --date "1995-04-25 18:30:00" --tz Asia/Ho_Chi_Minh --lat 21.1861 --lon 106.0763 --natal
```

### Tính Giờ Hora (Planetary Hours)
```python
# Sử dụng hora_service.py để tính giờ hora chính xác
from skills.financial_astrology.scripts.hora_service import get_current_hora

# Mặc định: Hekinan, Japan (Asia/Tokyo)
hora = get_current_hora()
print(f"Current hora lord: {hora['current_hora']['lord']}")
print(f"Trading bias: {hora['current_hora']['trading']}")

# Tùy chỉnh tọa độ và timezone
hora = get_current_hora(lat=34.9333, lon=136.9667, tz_name="Asia/Tokyo")
```

**Quy tắc tính Hora:**
- Hora chia 24h thành 24 giờ do 7 hành tinh cai quản
- Thứ tự Chaldean: Saturn → Jupiter → Mars → Sun → Venus → Mercury → Moon
- Giờ đầu tiên của ngày (sunrise) thuộc về hành tinh chủ quản ngày đó
- **VEDIC FIX:** Ngày bắt đầu từ sunrise, không phải midnight
- Nếu trước sunrise → dùng day lord của ngày hôm trước

## 🌙 MOON PHASES & MARKET BEHAVIOR

| Phase | Tâm lý thị trường | Chiến lược |
|-------|------------------|------------|
| 🌑 **New Moon** | Bắt đầu chu kỳ mới, ít biến động, sideways | Chờ breakout vài ngày sau |
| 🌒 **Waxing Crescent** | Lạc quan dần, Bullish | Buy dips, momentum |
| 🌓 **First Quarter** | Xung đột, decision point, biến động | Watch for reversal |
| 🌔 **Waxing Gibbous** | Lạc quan cao, Bullish | Trend following |
| 🌕 **Full Moon** | Đỉnh cảm xúc, biến động CAO, reversal | Tránh overtrading, watch reversal |
| 🌖 **Waning Gibbous** | Lạc quan giảm, thận trọng | Take profit, tighten SL |
| 🌗 **Last Quarter** | Đánh giá lại, biến động | Hedge, reduce position |
| 🌘 **Waning Crescent** | Bi quan, Bearish | Short, cash is king |

**Nghiên cứu:** Journal of Behavioral Finance — Returns giảm đáng kể quanh New Moon, tăng quanh Full Moon. Nhiều hedge fund theo dõi lunar cycles như sentiment indicator.

## 🌙 MOON SIGN & MARKET MOOD

| Nguyên tố | Cung | Mood | Xu hướng trade |
|-----------|------|------|----------------|
| 🔥 **Lửa** | ♈♌♐ | RISK-ON, tự tin, bullish | BUY dips, momentum plays |
| 🌍 **Đất** | ♉♍♑ | THỰC TẾ, safe haven | Vàng mạnh, focus fundamentals |
| 💨 **Khí** | ♊♎♒ | LÝ TRÍ, phân vân, sideways | Range trading, false breakouts |
| 💧 **Nước** | ♋♏♓ | CẢM XÚC, nhạy cảm | Watch sudden moves, tight SL |

## 🔗 MOON + PLANET COMBINATIONS (Quan trọng nhất cho Day Trading!)

### Moon ☌ Mars (Chandra-Mangal Yoga) = "Bull Run" 🐂
- **Trend:** Tăng nhanh, volume cao, aggressive bullish
- **Strategy:** Buy on dips, momentum trading
- **⚠️ Nếu Mars yếu (Cancer):** Có thể thành panic selling

### Moon ☌ Saturn (Vish Yoga) = "Slow Bleed" 🐻
- **Trend:** Range-bound đến negative, struggle tại resistance
- **Strategy:** Sell on rise, tránh fresh long

### Moon ☌ Rahu (Grahan Yoga) = "The Trap" 🕳️
- **Trend:** High volatility, fake breakout, sudden spikes
- **Strategy:** Option buying (gamma moves), KHÔNG hold qua đêm

### Moon ☌ Ketu = "Panic Button" 💥
- **Trend:** Drop đột ngột không có news, "bottom falls out"
- **Strategy:** Hedge, shorting opportunities

### Moon ☌ Jupiter = "Expansion" 📈
- **Trend:** Tăng trưởng ổn định, banking rally, optimism
- **Strategy:** Position trading, banking/finance stocks

### Moon ☌ Mercury = "Information Flow" 📡
- **Trend:** Volatility cao, whipsaws (lên xuống liên tục)
- **Strategy:** Scalping, quick in-out

### Moon ☌ Venus = "Risk Appetite" 💎
- **Trend:** Risk-on, consumer/luxury stocks mạnh
- **Strategy:** Growth stocks, consumer sector

### Moon ☌ Sun = "Stable Uptrend" ☀️
- **Trend:** Tăng ổn định, confidence cao, low volatility
- **Strategy:** Gold, government bonds, PSU

### Moon ☌ Rahu (Nakshatra) = "Disruption" 🌪️
- **Trend:** Biến động bất ngờ, fake moves
- **Strategy:** Tight SL, avoid overnight

### Moon ☌ Ketu (Nakshatra) = "Chaos" 🌀
- **Trend:** Panic fall, confusion, algorithm breaks
- **Strategy:** Cash, defensive positioning

## 🌟 NAKSHATRA & TRADING

### ✅ Nakshatra Tốt cho Trading
| Nakshatra | Lord | Loại trade | Đặc điểm |
|-----------|------|-----------|----------|
| 🐴 **Ashwini** | Ketu | Intraday, quick trades | Nhanh, action, mental agility |
| 🌸 **Pushya** | Saturn | Investment, positional | Auspicious nhất, wealth building |
| 🐂 **Rohini** | Moon | Profit-oriented | Growth, abundance, mid/large cap |
| 🛏️ **Uttara Phalguni** | Sun | Strategic planning | Discipline, portfolio diversification |
| ✋ **Hasta** | Moon | Swing trading | Precision, timing, chart analysis |

### ❌ Nakshatra Nên Tránh
| Nakshatra | Lord | Lý do |
|-----------|------|-------|
| 🌊 **Ardra** | Rahu | Emotional volatility |
| 🌿 **Moola** | Ketu | Destructive energy |
| 🐍 **Aslesha** | Mercury | Hidden motives, confusion |

### 🌊 Gandanta Points (Vùng nguy hiểm)
- **Nơi nước gặp lửa:** Last degree of Water signs (♋♏♓) ↔ First degree of Fire signs (♈♌♐)
- **Hiệu ứng:** Biến động cực đoan, reversal bất ngờ, "drowning point"
- **Chiến lược:** Tránh trade tại gandanta zones, hoặc dùng very tight SL

## 🔥 COMBUSTION (Hành tinh bị bốc cháy)

Khi hành tinh quá gần Mặt Trời, năng lượng bị "đốt cháy":

| Hành tinh | Orb Combust | Tác động thị trường |
|-----------|-------------|-------------------|
| ☿️ **Thủy** | ≤14° | Thông tin sai lệch, false signals, confusion |
| ♀️ **Kim** | ≤10° | Risk appetite sai, valuation distortion |
| ♂️ **Hoả** | ≤8° | Aggression giảm, nhưng bất ngờ tăng |
| ♃ **Mộc** | ≤10° | Over-optimism → thất vọng |
| ♄ **Thổ** | ≤14° | Fear amplification, panic |

### ⚡ Cazimi (Trong tim Mặt Trời)
- **Orb:** ≤0.5° từ Mặt Trời
- **Hiệu ứng:** Năng lượng hành tinh tập trung CỰC MẠNH
- **Market impact:** Trend rất mạnh nhưng một chiều

## 🔗 ASPECTS (Góc chiếu) — Ý nghĩa cho Trading

| Aspect | Orb | Symbol | Tác động |
|--------|-----|--------|----------|
| ☌ **Conjunction** | ≤8° | Năng lượng hợp nhất | Mạnh nhất, trend mới |
| ⚹ **Sextile** | ≤6° | Hài hòa | Cơ hội entry, flow tốt |
| □ **Square** | ≤7° | Căng thẳng | Biến động CAO, thử thách |
| △ **Trine** | ≤8° | Thuận lợi | Trend mạnh, tăng trưởng |
| ☍ **Opposition** | ≤8° | Đối cực | Turning point, biến động |
| ⚻ **Quincunx** | ≤3° | Điều chỉnh | Bất ổn, cần adapt |
| ∠ **Semi-Square** | ≤2.5° | Nhẹ căng thẳng | Watch for escalation |
| ⚼ **Sesquiquadrate** | ≤2.5° | Nhẹ căng thẳng | Friction building |

### 🌙 Moon Aspects — Quan trọng nhất cho M15/H1
- **Moon □ Hoả:** PANIC SELL / FOMO BUY, rất biến động ⚠️⚠️
- **Moon ☍ Hoả:** Bulls vs Bears, chiến trường, dễ đảo chiều
- **Moon □ Thủy:** False signals, thông tin trái ngược
- **Moon ☍ Thủy:** Market phân hóa, confusion
- **Moon □ Rahu:** BLACK SWAN potential ⚠️⚠️⚠️
- **Moon ☍ Rahu:** DISRUPTION lớn, biến động cực mạnh
- **Moon △ Mộc:** Bullish mạnh, expansion
- **Moon ☌ Mộc:** Optimism, steady growth
- **Moon □ Thổ:** Sợ hãi + tham lam, phân cực
- **Moon ☍ Thổ:** Fear vs Greed cực đoan, turning point

## 🪐 HÀNH TINH & ASSET CLASSES

| Asset | Hành tinh chủ quản | Sector liên quan |
|-------|-------------------|-----------------|
| 🥇 **Vàng (XAU/USD)** | ☀️ Mặt Trời, ♀️ Kim | Safe haven, inflation hedge |
| 🥈 **Bạc** | 🌙 Mặt Trăng | Industrial + precious metal |
| ₿ **Bitcoin** | 🐉 Rahu, ⛧ Thiên Vương | Crypto, decentralization |
| 💻 **Tech stocks** | ⛧ Thiên Vương | Innovation, disruption |
| ⛽ **Energy** | ♂️ Hoả | Oil, gas, defense |
| 🏦 **Finance/Banking** | ♃ Mộc, ♄ Thổ | Credit, lending, insurance |
| 📱 **IT/Telecom** | ☿️ Thủy | Software, communication |
| 🏗️ **Infrastructure** | ♄ Thổ | Real estate, cement, metals |
| 🎮 **Speculative** | 🐉 Rahu | Penny stocks, meme coins |

## ⏰ GIỜ HORA (PLANETARY HOURS) — CHaldean Order

### Quy tắc tính toán:
- **Thứ tự Chaldean:** Saturn → Jupiter → Mars → Sun → Venus → Mercury → Moon
- **Ngày bắt đầu từ sunrise** (VEDIC FIX), không phải midnight
- **Giờ đầu tiên** (sunrise) thuộc về hành tinh chủ quản ngày đó
- **Trước sunrise** → dùng day lord của ngày hôm trước

### Hành tinh chủ quản mỗi ngày:
| Ngày | Hành tinh |
|------|----------|
| Sunday | ☀️ Sun |
| Monday | 🌙 Moon |
| Tuesday | ♂️ Mars |
| Wednesday | ☿️ Mercury |
| Thursday | ♃ Jupiter |
| Friday | ♀️ Venus |
| Saturday | ♄ Saturn |

### Ý nghĩa Hora cho Trading:

| Hora | Trading Focus | Strategy | Element |
|------|--------------|----------|---------|
| ☀️ **Sun** | Authority, government, gold | Good for gold, government bonds, stable trades | 🔥 Fire |
| 🌙 **Moon** | Emotions, public sentiment, liquids | Watch sentiment shifts, silver, consumer goods | 💧 Water |
| ♂️ **Mars** | Energy, aggression, metals, real estate | Volatile moves, momentum trading, energy stocks | 🔥 Fire |
| ☿️ **Mercury** | Communication, tech, data, short-term | Scalping, IT stocks, quick in-out | 🌍 Earth |
| ♃ **Jupiter** | Expansion, banking, wisdom, growth | Banking stocks, position trading, bullish bias | ✨ Ether |
| ♀️ **Venus** | Luxury, arts, relationships, comfort | Consumer goods, luxury stocks, trend following | 🌍 Earth |
| ♄ **Saturn** | Discipline, restriction, delay, structure | Defensive positioning, infrastructure, cautious | 💨 Air |

## 📊 OUTER PLANETS & LONG-TERM CYCLES

| Hành tinh | Chu kỳ | Tác động thị trường |
|-----------|--------|-------------------|
| ♃ **Mộc** | 11.86 năm | Bull market cycles, expansion |
| ♄ **Thổ** | 29.46 năm | Bear market, correction, restructuring |
| ⛧ **Thiên Vương** | 84 năm | Disruption, innovation, bubbles |
| ♆ **Hải Vương** | 165 năm | Bong bóng, illusion, deception |
| ♇ **Diêm Vương** | 248 năm | System change, power shifts |
| **Júpiter-Saturn** | ~20 năm | Business cycle, regime change |

### ♇ Diêm Vương theo cung
| Cung | Giai đoạn | Tác động |
|------|-----------|----------|
| ♑ **Ma Kết** | 2008-2024 | Financial crisis, death of old banking |
| ♒ **Bảo Bình** | 2024-2044 | Crypto, AI, decentralization, tech revolution |

### ⛧ Thiên Vương theo cung
| Cung | Giai đoạn | Tác động |
|------|-----------|----------|
| ♈ **Bạch Dương** | 2010-2019 | Tech boom, cryptocurrency birth |
| ♉ **Kim Ngưu** | 2018-2026 | Finance disruption, currency, resources |

## 📈 SECTOR ROTATION THEO HÀNH TINH

| Hành tinh | Sector mạnh | Sector yếu |
|-----------|------------|-----------|
| ☀️ **Mặt Trời** | PSU, Gold, Government bonds | Crypto, speculative |
| 🌙 **Moon** | Silver, consumer, real estate | - |
| ☿️ **Thủy** | IT, media, telecom, brokerage | Heavy industry |
| ♀️ **Kim** | Luxury, consumer, art, beauty | Defense, mining |
| ♂️ **Hoả** | Defense, energy, metals, real estate | Utilities, bonds |
| ♃ **Mộc** | Banking, finance, education, FMCG | - |
| ♄ **Thổ** | Infrastructure, mining, cement | Tech, growth stocks |
| 🐉 **Rahu** | Crypto, penny stocks, tech, speculative | Traditional, conservative |
| 🔻 **Ketu** | Pharma (during crash), spiritual | - |

## 📅 LỊCH SỬ — Ví dụ điển hình

| Sự kiện | Cấu hình hành tinh |
|---------|-------------------|
| **1987 Black Monday** | Significant lunar cycle event |
| **2000 Dot-com crash** | Jupiter-Saturn conjunction |
| **2008 Financial crisis** | Saturn ☌ Ketu in Leo |
| **2020 COVID crash** | Mars ☌ Jupiter ☌ Saturn in Capricorn |
| **2021 Bull run** | Jupiter in Aquarius, Rahu in Taurus |
| **BTC ATH Oct 2025** | $126,198 — Cycle peak |

## ⚠️ Cảnh Báo

- **Correlation ≠ causation** — Hành tinh không "gây ra" biến động
- **Financial astrology là công cụ BỔ TRỢ**, KHÔNG thay thế phân tích kỹ thuật/cơ bản
- **Luôn dùng stop loss**, không risk quá 1-2% per trade
- **Đầu tư có rủi ro, tự chịu trách nhiệm**

## 🔧 Tham số Script

| Tham số | Mặc định | Mô tả |
|---------|----------|-------|
| `--tz` | Asia/Tokyo | Timezone IANA |
| `--date` | Hiện tại | YYYY-MM-DD HH:MM:SS |
| `--lat` | 34.9333 | Latitude |
| `--lon` | 136.9667 | Longitude |
| `--asset` | all | gold, btc, stocks, all |
| `--json` | False | Xuất JSON |
| `--natal` | False | Tính Dasha cho Natal Chart |
