---
name: crypto-alerts-kalkulasi
description: "Kelola alert trade-setup crypto top-50: tambah/lihat/hapus setup, jawab konfirmasi pasang/SL+, dan proses alert berkala. Gunakan saat user menulis perintah setup (alert BTC long entry ... tp ... cl ...), menjawab 'pasang', 'sudah <harga>', 'batal', 'ga jadi', atau meminta status alert crypto."
---

# crypto-alerts

Trade-setup alert engine untuk 50 crypto terbesar (CoinGecko free API, tanpa key).

## State machine per setup

- **Stage 1 — menunggu entry.** Harga menyentuh area entry (toleransi 0.30%) →
  bot bertanya *"PASANG POSISI?"* (reminder maks 3× per jam, 6 jam window).
  Entry miss (harga lolos melewati TP/CL tanpa sentuh) → setup auto-cancel.
- **Stage 2 — posisi jalan, belum SL+.** Gerak menguntungkan ≥0.2% dari entry →
  bot menyuruh pasang SL+ (sekali). TP/CL tersentuh lebih dulu → alert + auto-delete.
- **Stage 3 — SL+ terpasang.** TP kena → *"SAATNYA TP!"* + delete.
  CL kena → *"SAATNYA CL!"* + delete. SL+ kena → info keluar BE + delete (tanpa konfirmasi).

Threshold fixed: SL+ prompt di ±0.2%; tidak per-setup.

## Perintah CLI (jalankan dengan exec, python3)

Semua perintah: `python3 skills/crypto-alerts/scripts/alert_cli.py <cmd>`

- `add <SYMBOL> long|short entry <p> tp <p> cl <p>` — validasi urutan harga
  (long: cl<entry<tp; short: tp<entry<cl), simpan stage 1.
- `list` — semua setup aktif + stage.
- `remove <id>` — hapus manual.
- `resolve <id> pasang` — stage 1→2 saat user menjawab "pasang".
- `resolve <id> sudah <harga>` — stage 2→3, catat harga SL+ user.
- `resolve <id> batal` / `ga jadi` — hapus setup.
- `check` — headless: hitung alert, update state, cetak teks alert jika ada
  (silent = tidak ada yang perlu dikabari). Dijalankan otomatis tiap 60s oleh
  automations job `crypto-alerts-check`.

## Penanganan jawaban user

1. Identifikasi setup yang dimaksud (kalau ambigu, tampilkan `list` dan tanyakan).
2. Jalankan perintah `resolve` yang sesuai, lalu konfirmasi singkat ke user.
3. Jangan pernah eksekusi order exchange — bot hanya memberi alert dan mencatat state.

## Verifikasi

Setelah perubahan state: jalankan `list` dan tunjukkan hasilnya ke user.
