---
name: bmkg-weather
description: >
  Get real-time Indonesian weather forecasts and earthquake data from BMKG (Badan Meteorologi,
  Klimatologi, dan Geofisika) — Indonesia's official meteorological agency. Use this skill
  whenever the user asks about weather in Indonesia, Indonesian cities, rainfall, temperature,
  wind, humidity, earthquake alerts, or early warning in any Indonesian location.
  Trigger on phrases like "cuaca", "prakiraan cuaca", "hujan", "gempa", "BMKG", "cuaca Jakarta",
  "cuaca hari ini", "weather Indonesia", or any Indonesian city/region weather query.
  No API key required — completely free official government data.
---

# BMKG Weather Skill

Fetch real-time Indonesian weather forecasts and earthquake data from BMKG's open API.
No API key needed. Rate limit: 60 requests/minute per IP.

**Attribution required:** Always mention "Sumber: BMKG" in responses.

---

## API Endpoints

### 1. Prakiraan Cuaca (Weather Forecast)
```
GET https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_wilayah}
```
- Forecast: 3 hari ke depan, per 3 jam (8 data/hari)
- Update: 2x sehari
- Format: JSON

### 2. Peringatan Dini / Nowcast
```
GET https://data.bmkg.go.id/peringatan-dini-cuaca/
```
- Early warning hingga level kecamatan
- Format: XML (CAP)

### 3. Data Gempa Bumi
```
GET https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json
GET https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json
```

---

## Cara Penggunaan

### Step 1: Tentukan kode wilayah (adm4)

Format kode: `PP.KK.CC.DDDD`
- PP = Kode provinsi (2 digit)
- KK = Kode kota/kabupaten (2 digit)  
- CC = Kode kecamatan (2 digit)
- DDDD = Kode kelurahan/desa (4 digit)

**Cara lookup kode wilayah (gunakan script):**
```bash
python scripts/cari_wilayah.py "Padang"
python scripts/cari_wilayah.py "Bogor"
```
Script otomatis cari kode dan test validitasnya ke API BMKG.

Jika tidak ditemukan, cari manual di https://cuaca.bmkg.go.id
Atau lihat: `references/kode-wilayah.md`

### Step 2: Fetch data cuaca

```bash
# Contoh: Jakarta Pusat - Kemayoran
curl "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=31.71.03.1001"

# Contoh: Surabaya - Wonokromo
curl "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=35.78.31.1007"
```

### Step 3: Parse response JSON

Response structure:
```json
{
  "lokasi": {
    "provinsi": "DKI Jakarta",
    "kotkab": "Kota Adm. Jakarta Pusat",
    "kecamatan": "Kemayoran",
    "desa": "Kemayoran",
    "lon": 106.845,
    "lat": -6.164,
    "timezone": "Asia/Jakarta"
  },
  "data": [{
    "cuaca": [
      [ /* hari 1, array per 3 jam */ ],
      [ /* hari 2 */ ],
      [ /* hari 3 */ ]
    ]
  }]
}
```

### Step 4: Format response ke user

Untuk setiap entry cuaca, field yang tersedia:

| Field | Deskripsi | Satuan |
|-------|-----------|--------|
| `local_datetime` | Waktu lokal | YYYY-MM-DD HH:mm:ss |
| `t` | Suhu udara | °C |
| `hu` | Kelembapan | % |
| `weather_desc` | Kondisi cuaca (ID) | - |
| `weather_desc_en` | Kondisi cuaca (EN) | - |
| `ws` | Kecepatan angin | km/jam |
| `wd` | Arah angin dari | - |
| `tcc` | Tutupan awan | % |
| `vs_text` | Jarak pandang | km |
| `tp` | Curah hujan | mm |
| `image` | URL ikon cuaca | SVG |

---

## Data Gempa Bumi

```bash
# Gempa terbaru (1 gempa)
curl "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"

# 15 gempa terkini
curl "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"

# 15 gempa dirasakan
curl "https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json"
```

Response fields gempa:
- `Tanggal`, `Jam` — waktu kejadian
- `Magnitude` — kekuatan gempa
- `Kedalaman` — kedalaman dalam km
- `Wilayah` — lokasi episenter
- `Potensi` — potensi tsunami atau tidak
- `Koordinat` — lat,lon

---

## Contoh Output ke User

```
🌤️ Prakiraan Cuaca Jakarta Pusat - Kemayoran
📅 Senin, 26 April 2026 | 14:00 WIB

🌡️ Suhu: 31°C
💧 Kelembapan: 69%
🌬️ Angin: 9.6 km/jam dari Timur
☁️ Tutupan awan: 7%
👁️ Jarak pandang: >10 km
🌦️ Kondisi: Cerah

---
Sumber: BMKG (data.bmkg.go.id)
```

---

## Kode Wilayah Kota Besar

| Kota | Kode adm4 Contoh |
|------|-----------------|
| Jakarta Pusat (Kemayoran) | `31.71.03.1001` |
| Jakarta Selatan (Kebayoran) | `31.74.08.1001` |
| Surabaya | `35.78.01.1001` |
| Bandung | `32.73.01.1001` |
| Medan | `12.71.01.1001` |
| Makassar | `73.71.01.1001` |
| Semarang | `33.74.01.1001` |
| Yogyakarta | `34.71.01.1001` |
| Denpasar | `51.71.01.1001` |
| Palembang | `16.71.01.1001` |
| Pekanbaru | `14.71.01.1001` |
| Balikpapan | `64.72.01.1001` |
| Manado | `71.71.01.1001` |
| Jayapura | `91.71.01.1001` |

Untuk kode wilayah lengkap, lihat: `references/kode-wilayah.md`

---

## Catatan Penting

1. **Wajib cantumkan BMKG** sebagai sumber data di setiap response
2. Kode wilayah menggunakan **Kepmendagri No. 100.1.1-6117 Tahun 2022**
3. Jika kode wilayah tidak diketahui, gunakan kode kota terdekat atau minta user clarifikasi
4. Data diupdate **2x sehari** — pagi dan sore
5. Jika API tidak merespons, informasikan ke user dan sarankan cek langsung di https://cuaca.bmkg.go.id
