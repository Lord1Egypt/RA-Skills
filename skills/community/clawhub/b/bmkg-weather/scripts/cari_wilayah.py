#!/usr/bin/env python3
"""
Cari kode wilayah adm4 BMKG berdasarkan nama kota/kelurahan.
Usage: python cari_wilayah.py "Padang"
       python cari_wilayah.py "Bogor Tengah"
"""

import sys
import urllib.request
import json

# Hardcoded kode wilayah kota besar yang sudah terverifikasi
KOTA_BESAR = {
    "jakarta pusat": "31.71.03.1001",
    "kemayoran": "31.71.03.1001",
    "jakarta selatan": "31.74.08.1001",
    "jakarta utara": "31.72.01.1001",
    "jakarta barat": "31.73.01.1001",
    "jakarta timur": "31.75.01.1001",
    "bandung": "32.73.01.1001",
    "bogor tengah": "32.71.03.1001",
    "bogor utara": "32.71.05.1001",
    "bogor timur": "32.71.02.1001",
    "bogor barat": "32.71.04.1001",
    "bogor": "32.71.03.1001",
    "depok": "32.76.01.1001",
    "bekasi": "32.75.04.1001",
    "tangerang": "36.71.01.1001",
    "surabaya": "35.78.01.1001",
    "malang": "35.73.01.1001",
    "semarang": "33.74.01.1001",
    "yogyakarta": "34.71.02.1001",
    "solo": "33.72.01.1001",
    "medan": "12.71.01.1001",
    "padang": "13.71.01.1001",
    "padang barat": "13.71.01.1001",
    "padang timur": "13.71.02.1001",
    "padang utara": "13.71.03.1001",
    "padang selatan": "13.71.04.1001",
    "pekanbaru": "14.71.01.1001",
    "batam": "21.71.01.1001",
    "palembang": "16.71.01.1001",
    "bandar lampung": "18.71.01.1001",
    "jambi": "15.71.01.1001",
    "bengkulu": "17.71.01.1001",
    "banda aceh": "11.71.01.1001",
    "makassar": "73.71.01.1001",
    "manado": "71.71.01.1001",
    "palu": "72.71.01.1001",
    "kendari": "74.71.01.1001",
    "gorontalo": "75.71.01.1001",
    "denpasar": "51.71.01.1001",
    "mataram": "52.71.01.1001",
    "kupang": "53.71.01.1001",
    "balikpapan": "64.72.01.1001",
    "samarinda": "64.71.01.1001",
    "pontianak": "61.71.01.1001",
    "banjarmasin": "63.71.01.1001",
    "palangkaraya": "62.71.01.1001",
    "jayapura": "91.71.01.1001",
    "sorong": "92.72.01.1001",
    "ambon": "81.71.01.1001",
    "ternate": "82.71.01.1001",
}

def cari_kode(nama_kota: str) -> str | None:
    """Cari kode adm4 berdasarkan nama kota."""
    key = nama_kota.lower().strip()
    
    # Exact match
    if key in KOTA_BESAR:
        return KOTA_BESAR[key]
    
    # Partial match
    for kota, kode in KOTA_BESAR.items():
        if key in kota or kota in key:
            return kode
    
    return None

def test_kode(kode: str) -> dict | None:
    """Test apakah kode valid dengan hit API BMKG."""
    url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            return data.get("lokasi")
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python cari_wilayah.py 'nama kota'")
        print("Contoh: python cari_wilayah.py 'Padang'")
        sys.exit(1)
    
    nama = " ".join(sys.argv[1:])
    print(f"🔍 Mencari kode wilayah untuk: {nama}")
    
    kode = cari_kode(nama)
    
    if kode:
        print(f"✅ Kode ditemukan: {kode}")
        print(f"🌐 Test API...")
        lokasi = test_kode(kode)
        if lokasi:
            print(f"✅ Valid! Lokasi: {lokasi.get('desa')}, {lokasi.get('kecamatan')}, {lokasi.get('kotkab')}, {lokasi.get('provinsi')}")
            print(f"\ncurl command:")
            print(f'curl "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode}"')
        else:
            print(f"❌ Kode {kode} tidak valid di API BMKG")
    else:
        print(f"❌ Kode tidak ditemukan untuk '{nama}'")
        print("💡 Tips: Coba nama yang lebih spesifik, contoh 'Padang Barat' atau 'Padang Timur'")
        print("💡 Atau buka https://cuaca.bmkg.go.id/ dan cari manual")

if __name__ == "__main__":
    main()
