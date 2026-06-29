# 📖 Tài liệu Skill Financial Astrology — Chiêm Tinh Tài Chính

> **Ngày tạo:** 02/05/2026  
> **Cập nhật:** 11/05/2026  
> **Tác giả:** Trading Bot (AI Assistant) cho anh Minh Swati  
> **Mục đích:** Tài liệu tham khảo khi reset session, rebuild skill, hoặc bàn giao

---

## 🆕 Cập nhật 11/05/2026: Hora Service Chính xác

**Thay đổi:**
- Thêm `hora_service.py` — module tính Giờ Hora (Planetary Hours) chính xác theo Swiss Ephemeris
- Tích hợp `hora_service.py` vào `financial_astrology.py` thay thế hàm `calculate_planetary_hours` cũ
- **VEDIC FIX:** Ngày bắt đầu từ sunrise, không phải midnight
- **Trước sunrise** → dùng day lord của ngày hôm trước
- Thứ tự Chaldean: Saturn → Jupiter → Mars → Sun → Venus → Mercury → Moon

**Cách sử dụng:**
```python
from skills.financial_astrology.scripts.hora_service import get_current_hora
hora = get_current_hora(lat=34.9333, lon=136.9667, tz_name="Asia/Tokyo")
print(f"Current hora lord: {hora['current_hora']['lord']}")
```

---

## 1. Skill này dùng để làm gì?

Phân tích vị trí hành tinh (sidereal/Vedic) và áp dụng vào **giao dịch ngắn hạn (Day Trading M15/H1)** cho Vàng (XAU/USD) và Bitcoin (BTC/USD).

### Output chính
- Vị trí 8 hành tinh + 3 ngoại hành tinh (sidereal)
- Moon phase → sentiment thị trường ngắn hạn
- Moon Nakshatra + Pada → mood trader
- House placement (Whole Sign) → khu vực tác động
- Moon-Planet combinations (Vedic Yoga) → xu hướng chính hôm nay
- Moon Aspects → tín hiệu biến động cho M15/H1
- Combustion detection → cảnh báo false signal
- All major aspects giữa các hành tinh
- Sector analysis: Vàng, Bitcoin, stocks
- Day Trading Signal Summary

### KHÔNG dùng để
- Thay thế phân tích kỹ thuật/cơ bản
- Cam kết lợi nhuận
- Tự động thực hiện lệnh

---

## 2. Nguyên lý cốt lõi

### 2.1 Financial Astrology là gì?
Ngành chiêm tinh ứng dụng vào thị trường tài chính, dựa trên giả thuyết: **vị trí hành tinh ảnh hưởng đến tâm lý đám đông (fear & greed) → tác động đến biến động giá.**

> ⚠️ Correlation ≠ causation. Đây là công cụ **BỔ TRỢ**, không phải công cụ dự báo chính xác.

### 2.2 Quy tắc vàng: MOON là "ACTIVATOR"

> *"Mỗi hành tinh có một xu hướng, nhưng Mặt Trăng quyết định xu hướng nào được kích hoạt HÔM NAY."*

- Moon = Manas (Tâm trí) trong Vedic Astrology
- Thị trường = tâm lý đám đông → Moon di chuyển qua các Nakshatra → xác định mood trader mỗi ngày
- Hành tinh mà Moon tương tác hôm nay (qua Conjunction, Aspect, hoặc Nakshatra Lord) → đặt trend cho cả phiên

### 2.3 Hệ thống chiêm tinh sử dụng

| Thành phần | Hệ thống | Lý do |
|-----------|----------|-------|
| Zodiac | **Sidereal** (Nirayana) | Vedic Astrology, chính xác hơn Tropical cho hành tinh cố định |
| Ayanamsa | **Lahiri** | Chuẩn mực Vedic, được dùng rộng rãi nhất |
| House System | **Whole Sign** | Mỗi house = 1 cung hoàng đạo, đơn giản và chính xác cho Vedic |
| Planets | 8 bodies + 3 outer | Mặt Trăng, Mặt Trời, Thủy, Kim, Hoả, Mộc, Thổ, Rahu + Thiên Vương, Hải Vương, Diêm Vương |
| Nodes | **True Node** (Rahu/Ketu) | Rahu = North Node, Ketu = South Node (đối diện 180°) |

---

## 3. Thư viện & Công nghệ

### 3.1 Swiss Ephemeris (pyswisseph)

**Thư viện cốt lõi** — tính toán vị trí hành tinh chính xác.

- **Package:** `pyswisseph` (Python wrapper)
- **Version:** 2.10.3.2
- **Nguồn gốc:** Austrian Astrological Institute (Astrodienst)
- **Cài đặt:** `pip3 install pyswisseph`

#### Các hàm quan trọng đã dùng:

```python
import swisseph as swe

# 1. Cài đặt chế độ sidereal + ayanamsa Lahiri
swe.set_sid_mode(swe.SIDM_LAHIRI)

# 2. Tính Julian Day (phẢI dùng UTC)
jd_ut = swe.julday(year, month, day, hour + minute/60.0 + second/3600.0, cal=swe.GREG_CAL)

# 3. Lấy ayanamsa
ayanamsa = swe.get_ayanamsa_ut(jd_ut)

# 4. Tính vị trí hành tinh (sidereal)
r, _ = swe.calc_ut(jd_ut, body_id, swe.FLG_SIDEREAL)
# r[0] = longitude, r[1] = latitude, r[2] = distance, r[3] = speed

# 5. Tính House (tropical trước, trừ ayanamsa sau)
tropical_cusps, asmc = swe.houses(jd_ut, lat, lon, b'P')
asc_sidereal = (tropical_cusps[0] - ayanamsa) % 360

# 6. Body IDs
swe.MOON, swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS
swe.JUPITER, swe.SATURN, swe.TRUE_NODE  # Rahu
```

### 3.2 Python Standard Library

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # timezone handling
import json  # xuất JSON
import argparse  # CLI arguments
```

### 3.3 Không dùng API bên ngoài

- ❌ Không gọi API thiên văn nào
- ❌ Không gọi API tài chính nào (giá được lấy từ script khác `get_price.js`)
- ✅ Hoàn toàn offline, chỉ cần Swiss Ephemeris

---

## 4. Quy tắc tính toán quan trọng

### 4.1 Julian Day — ĐÚNG CÁCH

```python
# ✅ ĐÚNG: Tính JD từ UTC, KHÔNG cộng timezone offset
dt_utc = datetime.now(timezone.utc)
jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 
                dt_utc.hour + dt_utc.minute / 60.0, cal=swe.GREG_CAL)

# ❌ SAI: KHÔNG bao giờ cộng timezone offset vào giờ JD
jd = swe.julday(2026, 5, 1, 16+9)  # SAI! Sai số lớn!
```

### 4.2 Ascendant Sidereal

```python
# Swiss Ephemeris chỉ tính tropical houses → phải trừ ayanamsa
tropical_cusps, asmc = swe.houses(jd_ut, lat, lon, b'P')
asc_sidereal = (tropical_cusps[0] - ayanamsa) % 360
```

### 4.3 House Calculation (Whole Sign)

```python
def get_house(planet_lon, asc_lon):
    asc_sign = int(asc_lon / 30) % 12
    p_sign = int(planet_lon / 30) % 12
    return (p_sign - asc_sign + 12) % 12 + 1
```

### 4.4 Nakshatra Calculation

```python
def get_nakshatra(longitude):
    span = 360.0 / 27.0  # 13°20' mỗi nakshatra
    pada_span = span / 4.0  # 4 pada mỗi nakshatra
    idx = int(longitude / span) % 27
    pos = longitude % span
    pada = int(pos / pada_span) + 1
    return idx, NAKSHATRA_27[idx], pada, NAKSHATRA_LORDS[idx], NAKSHATRA_SYMBOLS[idx]
```

### 4.5 Aspect Calculation

```python
def angle_diff(a, b):
    diff = abs(a - b) % 360
    return min(diff, 360 - diff)  # khoảng cách ngắn nhất trên vòng tròn

# Check aspect
for aname, ainfo in ASPECTS.items():
    angle = ainfo['angle']
    orb = ainfo['orb']
    target = abs(diff - angle)
    if target <= orb:
        # có aspect này
```

### 4.6 Combustion Detection

```python
sun_lon = bodies_data['Mặt Trời']['lon']
for name, limit in COMBUST_ORBS.items():
    diff = angle_diff(sun_lon, bodies_data[name]['lon'])
    if diff <= 0.5:
        # Cazimi — năng lượng cực mạnh
    elif diff <= limit:
        # Combust — năng lượng bị đốt cháy
```

---

## 5. Cấu trúc thư mục skill

```
skills/financial-astrology/
├── SKILL.md                          # Hướng dẫn sử dụng (OpenClaw đọc cái này)
├── DOCUMENTATION.md                  # Tài liệu chi tiết (file này)
├── scripts/
│   └── financial_astrology.py        # Script chính (~400 dòng)
```

### Cách OpenClaw gọi skill

1. OpenClaw đọc `SKILL.md` → biết skill làm gì
2. Khi user yêu cầu phân tích chiêm tinh → exec script:
   ```bash
   python3 skills/financial-astrology/scripts/financial_astrology.py
   ```
3. Script xuất kết quả → OpenClaw đọc → tổng hợp vào báo cáo trading

---

## 6. Các tham số CLI

| Tham số | Mặc định | Mô tả |
|---------|----------|-------|
| `--tz` | Asia/Tokyo | Timezone IANA |
| `--date` | Hiện tại | YYYY-MM-DD HH:MM:SS |
| `--lat` | 34.9333 | Latitude (Hekinan, Nhật Bản) |
| `--lon` | 136.9667 | Longitude |
| `--asset` | all | gold, btc, stocks, all |
| `--json` | False | Xuất JSON thay vì text |

### Ví dụ

```bash
# Hiện tại (JST)
python3 scripts/financial_astrology.py

# Thời gian cụ thể
python3 scripts/financial_astrology.py --date "2026-05-02 12:10:00" --tz Asia/Tokyo

# Chỉ xuất JSON
python3 scripts/financial_astrology.py --json

# Phân tích riêng Vàng
python3 scripts/financial_astrology.py --asset gold
```

---

## 7. Quy tắc diễn giải (Interpretation Rules)

### 7.1 Moon Phase → Market Behavior

| Phase | Tâm lý | Chiến lược |
|-------|--------|------------|
| 🌑 New Moon | Ít biến động, sideways | Chờ breakout |
| 🌒 Waxing Crescent | Lạc quan dần | Buy dips |
| 🌓 First Quarter | Xung đột, decision | Watch reversal |
| 🌔 Waxing Gibbous | Lạc quan cao | Trend following |
| 🌕 Full Moon | Đỉnh cảm xúc, biến động CAO | Tránh overtrading |
| 🌖 Waning Gibbous | Lạc quan giảm | Take profit |
| 🌗 Last Quarter | Đánh giá lại | Hedge |
| 🌘 Waning Crescent | Bi quan | Short, cash |

### 7.2 Moon-Planet Combinations (Quan trọng nhất)

| Combination | Trend | Strategy |
|-------------|-------|----------|
| 🌙☌♂ Chandra-Mangal | Bull Run 🐂 | Buy dips, momentum |
| 🌙☌♄ Vish Yoga | Slow Bleed 🐻 | Sell on rise |
| 🌙☌🐉 Grahan Yoga | The Trap 🕳️ | Option buying, tight SL |
| 🌙☌🔻 Ketu | Panic Button 💥 | Hedge, short |
| 🌙☌♃ Jupiter | Expansion 📈 | Position trading |
| 🌙☌☿ Mercury | Info Flow 📡 | Scalping |
| 🌙☌♀ Venus | Risk Appetite 💎 | Growth stocks |
| 🌙☌☀ Sun | Stable Uptrend ☀️ | Gold, bonds |

### 7.3 Moon Aspects — Tín hiệu M15/H1

| Aspect | Planet | Ý nghĩa |
|--------|--------|---------|
| Moon □ Hoả | Mars | PANIC SELL / FOMO BUY ⚠️⚠️ |
| Moon ☍ Hoả | Mars | Bulls vs Bears, đảo chiều ⚠️ |
| Moon □ Rahu | Rahu | BLACK SWAN ⚠️⚠️⚠️ |
| Moon ☍ Rahu | Rahu | DISRUPTION cực mạnh ⚠️⚠️⚠️ |
| Moon △ Mộc | Jupiter | Bullish mạnh ✅ |
| Moon □ Thổ | Saturn | Fear + Greed phân cực ⚠️ |

### 7.4 Combustion → False Signals

| Hành tinh | Orb | Tác động |
|-----------|-----|----------|
| Thủy ☿ | ≤14° | Thông tin sai lệch, false signals |
| Kim ♀ | ≤10° | Risk appetite sai |
| Hoả ♂ | ≤8° | Aggression giảm |
| Mộc ♃ | ≤10° | Over-optimism |
| Thổ ♄ | ≤14° | Fear amplification |

### 7.5 Nakshatra Trading Quality

| Loại | Nakshatra | Lord | Dùng cho |
|------|-----------|------|----------|
| ✅ Tốt | Ashwini | Ketu | Intraday, quick trades |
| ✅✅ Rất tốt | Pushya | Saturn | Investment, wealth building |
| ✅ Tốt | Rohini | Moon | Profit-oriented, growth |
| ❌ Tránh | Ardra | Rahu | Emotional volatility |
| ❌ Tránh | Mula | Ketu | Destructive energy |
| ❌ Tránh | Ashlesha | Mercury | Hidden motives, confusion |

---

## 8. Hành tinh & Asset Classes

| Asset | Hành tinh chủ quản | Sector |
|-------|-------------------|--------|
| 🥇 Vàng (XAU/USD) | ☀️ Mặt Trời, ♀️ Kim | Safe haven, inflation hedge |
| 🥈 Bạc | 🌙 Mặt Trăng | Industrial + precious metal |
| ₿ Bitcoin | 🐉 Rahu, ⛧ Thiên Vương | Crypto, decentralization |
| 💻 Tech stocks | ⛧ Thiên Vương | Innovation, disruption |
| ⛽ Energy | ♂️ Hoả | Oil, gas, defense |
| 🏦 Finance/Banking | ♃ Mộc, ♄ Thổ | Credit, lending |

---

## 9. Quy trình tạo skill (Step by Step)

### Bước 1: Xác định yêu cầu
- Anh Minh muốn phân tích thiên văn bổ trợ cho trading Vàng & Bitcoin
- Focus: Day Trading M15/H1
- Language: Tiếng Việt

### Bước 2: Nghiên cứu nguyên lý
- Financial Astrology (J.N. Bhasin, Raymond Merrman)
- Vedic Astrology (sidereal, Lahiri ayanamsa, Whole Sign houses)
- Moon phases & market behavior research (Journal of Behavioral Finance)
- Nakshatra trading quality

### Bước 3: Chọn công cụ
- **Swiss Ephemeris** (pyswisseph) — thư viện thiên văn chính xác nhất
- Python 3 — dễ đọc, dễ maintain
- Không dùng API bên ngoài — chạy offline, không phụ thuộc network

### Bước 4: Viết script
1. Cài đặt Swiss Ephemeris: `pip3 install pyswisseph`
2. Định nghĩa dữ liệu: 27 nakshatras, lords, symbols, zodiac signs, aspects, combustion orbs
3. Viết hàm tính: Julian Day, planet positions, houses, nakshatras, aspects, combustion, moon phase
4. Viết hàm diễn giải: moon combinations, moon aspects, nakshatra quality, sector analysis
5. Format output: text đẹp, dễ đọc, có emoji

### Bước 5: Tạo SKILL.md
- Mô tả skill để OpenClaw nhận diện
- Ghi rõ cách dùng script
- Liệt kê quy tắc diễn giải

### Bước 6: Test & Debug
- Test với nhiều thời gian khác nhau
- So sánh vị trí hành tinh với các nguồn khác
- Fix bug: Julian Day tính sai timezone, Ascendant sidereal

---

## 10. Lưu ý khi rebuild / reset session

### Nếu reset session, cần:
1. ✅ Giữ nguyên folder `skills/financial-astrology/`
2. ✅ Kiểm tra pyswisseph còn cài: `pip3 show pyswisseph`
3. ✅ Kiểm tra script chạy được: `python3 scripts/financial_astrology.py`
4. ✅ Kiểm tra SKILL.md còn trong folder

### Nếu mất pyswisseph:
```bash
pip3 install pyswisseph
```

### Nếu cần cập nhật:
- Sửa `financial_astrology.py` → thêm hành tinh, thêm aspect, sửa orb
- Sửa `SKILL.md` → thay đổi mô tả, thêm ví dụ
- Luôn test: `python3 scripts/financial_astrology.py --json`

---

## 11. Tích hợp với hệ thống trading

### Flow hoạt động:
```
User yêu cầu phân tích
    ↓
OpenClaw gọi script financial_astrology.py
    ↓
Script xuất kết quả chiêm tinh
    ↓
OpenClaw gọi get_price.js → lấy giá hiện tại
    ↓
OpenClaw gọi analyze_btc.js / phân tích kỹ thuật
    ↓
OpenClaw tổng hợp: cơ bản + kỹ thuật + chiêm tinh
    ↓
Xuất đề xuất BUY/SELL với giá vào lệnh, SL, TP
```

### Script liên quan:
- `get_price.js` — lấy giá Vàng & Bitcoin từ TradingView
- `analyze_btc.js` — phân tích kỹ thuật Bitcoin
- `package.json` — dependencies (Node.js: @mathieuc/tradingview)

---

## 12. Cảnh báo & Red Lines

⚠️ **Luôn nhắc user:**
- Financial astrology là công cụ BỔ TRỢ
- Correlation ≠ causation
- Luôn dùng stop loss
- Không risk quá 1-2% per trade
- Đầu tư có rủi ro, tự chịu trách nhiệm

❌ **Không bao giờ:**
- Cam kết lợi nhuận
- Tự động thực hiện lệnh
- Đưa ra lời khuyên tài chính cá nhân
- Thay thế phân tích kỹ thuật/cơ bản

---

## 13. Nguồn tham khảo

### Sách
- *Financial Astrology* — J.N. Bhasin
- *The World According to the Stars* — Raymond Merrman
- *Lal Kitab* — Five volumes of Vedic astrology rules

### Nghiên cứu
- Journal of Behavioral Finance — Moon phases & stock returns
- Cambridge Judge Business School — Lunar cycles & investor sentiment

### Công cụ
- Swiss Ephemeris: https://www.astro.com/swisseph
- pyswisseph: https://github.com/aloistr/pyswisseph
- Ayanamsa Lahiri: chuẩn mực Vedic Astrology

---

## 15. Dasha (Vimshottari)

### Giới thiệu

**Dasha** là chu kỳ hành tinh chủ quản trong Vedic Astrology, dùng để dự đoán sự kiện cuộc đời.

**Vimshottari Dasha** là hệ thống phổ biến nhất:
- Tổng chu kỳ: **120 năm**
- Dựa trên **Moon Nakshatra** lúc sinh
- Mỗi hành tinh có số năm khác nhau

### Số năm mỗi hành tinh

| Hành tinh | Số năm |
|-----------|--------|
| Ketu | 7 |
| Venus | 20 |
| Sun | 6 |
| Moon | 10 |
| Mars | 7 |
| Rahu | 18 |
| Jupiter | 16 |
| Saturn | 19 |
| Mercury | 17 |
| **Tổng** | **120** |

### Cách tính

1. Tìm Moon Nakshatra lúc sinh
2. Nakshatra Lord là hành tinh bắt đầu Dasha
3. Tính phần remaining trong Nakshatra
4. Dasha đầu tiên = remaining × years của Lord
5. Các Dasha tiếp theo theo thứ tự: Ketu → Venus → Sun → Moon → Mars → Rahu → Jupiter → Saturn → Mercury

### Antardasha (Tiểu vận)

Mỗi Dasha được chia thành 9 Antardasha:
- Antardasha = (Dasha years × Sub-lord years) / 120
- Thứ tự Antardasha giống thứ tự Dasha, bắt đầu từ Main Lord

### Sử dụng trong script

```bash
# Natal Chart với Dasha
python3 scripts/financial_astrology.py --date "1995-04-25 18:30:00" --tz Asia/Ho_Chi_Minh --lat 21.1861 --lon 106.0763 --natal

# Transit analysis (không Dasha)
python3 scripts/financial_astrology.py
```

### Lưu ý

- Dasha chỉ tính cho **Natal Chart** (thêm `--natal`)
- Transit analysis **không dùng Dasha** (tâm lý đám đông)
- Dasha dùng để phân tích **cuộc đời cá nhân**

---

## 14. Changelog

| Ngày | Phiên bản | Thay đổi |
|------|-----------|----------|
| 2026-05-02 | v3 | Bản hiện tại — Full features: Moon phase, nakshatra, aspects, combustion, houses, sector analysis |
| 2026-05-02 | v4 | Thêm Dasha (Vimshottari) cho Natal Chart, --natal flag |

---

**📝 Ghi chú cho anh Minh:**  
File này chứa toàn bộ kiến thức về skill Financial Astrology. Nếu reset session, chỉ cần:
1. Giữ folder `skills/financial-astrology/`
2. Đảm bảo `pyswisseph` còn cài
3. Session mới sẽ tự đọc `SKILL.md` và dùng được ngay

Nếu cần thêm tính năng mới (thêm hành tinh, thêm indicator, xuất PDF...), cứ bảo em! 📊
