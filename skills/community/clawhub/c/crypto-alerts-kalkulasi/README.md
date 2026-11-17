# crypto-alerts

Skill alert **trade-setup crypto top-50** untuk agent OpenClaw. Data harga dari
CoinGecko free API (tanpa API key). Agent memantau setup-mu dan memberi alert
bertahap di chat: saat entry, saat waktunya pasang SL+, dan saat TP/CL/SL+
tersentuh — lalu melupakan setup yang sudah selesai.

> Bukan nasihat keuangan. Skill ini hanya memberi alert & mencatat state —
> tidak pernah mengeksekusi order di exchange.

## Cara kerja (state machine per setup)

| Stage | Arti | Alert yang dikirim |
|---|---|---|
| 1 | Menunggu entry | 🔔 "PASANG POSISI?" saat harga menyentuh area entry (toleransi 0.30%, reminder maks 3×/jam). Harga lolos melewati TP/CL tanpa sentuh → setup auto-cancel. |
| 2 | Posisi jalan, belum SL+ | ✅ Gerak menguntungkan ≥0.2% (cocok untuk leverage tinggi seperti x25) → "PASANG SL+ sekarang!" (sekali). TP/CL tersentuh lebih dulu → alert + auto-delete. |
| 3 | SL+ terpasang | 🎯 TP kena / 🛑 CL kena → alert + hapus setup. ℹ️ SL+ kena → info keluar BE + hapus tanpa konfirmasi. |

Threshold fixed: SL+ prompt di ±0.2% dari entry.

## Instalasi

1. Salin folder skill ini ke workspace agent-mu: `~/.openclaw/workspace/skills/crypto-alerts/`
2. Siapkan file trigger `crypto-alerts-trigger.js` (ada di folder ini) — ganti `__WORKSPACE__` dengan path workspace agent-mu (mis. `/home/user/.openclaw/workspace`).
3. Pasang automasi pengecek (tiap 60 detik, hanya memanggil model saat ada alert):

```bash
openclaw automations add \
  --name crypto-alerts-check \
  --display-name "Crypto Alerts Check" \
  --every 60s \
  --session isolated \
  --announce \
  --message 'Balas persis dengan teks yang muncul SETELAH baris --- pada pesan ini. Jangan ubah format, jangan tambah komentar/analisis, jangan panggil tool. Jika tidak ada teks setelah baris ---, balas persis NO_REPLY.' \
  --trigger-script /path/ke/crypto-alerts-trigger.js
```

Syarat: Python 3 + akses internet ke `api.coingecko.com`. Gateway harus tetap
menyala agar pengecekan berjalan.

## Pemakaian (lewat chat ke agent-mu)

```
alert BTC long entry 76000 tp 78000 cl 74500   # buat setup
pasang                                          # konfirmasi posisi dibuka (stage 1→2)
sudah 76100                                     # konfirmasi SL+ terpasang + harganya (stage 2→3)
ga jadi / batal                                 # batalkan setup
list                                            # lihat semua setup aktif
remove <id>                                     # hapus manual
```

CLI langsung: `python3 skills/crypto-alerts/scripts/alert_cli.py <check|add|list|remove|resolve>`

Validasi urutan harga: long `cl < entry < tp`, short `tp < entry < cl`.

## Publikasi

```bash
npm i -g clawhub
clawhub login
clawhub skill publish ./crypto-alerts
```

## Catatan teknis

- Harga diambil 1 call API untuk semua koin top-50 (aman untuk rate limit gratis).
- Simbol→CoinGecko id di-cache 7 hari (`coins.json`).
- State disimpan di `setups.json` di folder skill — data lokal pribadi, tidak ikut ter-publish.
