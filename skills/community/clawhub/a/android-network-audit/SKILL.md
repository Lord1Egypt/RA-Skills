---
name: android-network-audit
description: "Use when auditing Android/Termux network exposure, connectivity, proxies, listeners, and unsafe ports from the device."
metadata:
  openclaw:
    version: 1.2.0
---



# ANDROID NETWORK AUDIT — SPESIFIKASI INTI

Skill ini mengaudit eksposur jaringan Android/Termux **dari dalam perangkat**, bersifat **read-only**. Gunakan untuk memeriksa konektivitas, interface/IP, DNS, proxy, port yang mendengarkan, serta mengklasifikasikan risiko eksposur — terutama sebelum men-deploy service atau membagikan jaringan (tethering/hotspot).

**Gunakan saat:**
- setup environment baru di Termux;
- sebelum menjalankan service/server di Termux;
- debugging koneksi bermasalah (gagal konek, lambat, DNS error);
- memastikan tidak ada listener tidak aman terekspos ke LAN;
- memverifikasi routing / proxy / DNS.

**Jangan gunakan untuk:**
- penetration testing / eksploitasi tanpa izin tertulis;
- operasi destruktif pada jaringan;
- pengganti tools keamanan khusus (IDS/IPS/nmap scan eksternal);
- akses jaringan perangkat/orang lain tanpa otorisasi.

---

## QUICK REFERENCE / CHECKLIST (READ-ONLY)

Ikuti urutan di bawah. Hentikan & laporkan jika langkah gagal diverifikasi.

- [ ] **Platform** — Deteksi Termux (`$PREFIX`/`$HOME` mengandung `com.termux`) vs Android restricted vs unknown.
- [ ] **Connectivity** — `ping -c1 -W3` host publik; jika gagal → NO_INTERNET, stop lanjut.
- [ ] **Interface/IP** — `ip addr` (fallback `ifconfig` / `/proc/net/fib_trie`); catat interface UP, IP, VPN/tunnel.
- [ ] **DNS** — `/etc/resolv.conf`, `getprop net.dns1/2`.
- [ ] **Proxy** — `env | grep -i proxy`, `getprop http_proxy/https_proxy` (**mask** credential).
- [ ] **Listening ports** — `ss -tulpen` (fallback `netstat` / `/proc/net/tcp`+`tcp6`); waspadai `0.0.0.0`/`::`.
- [ ] **Risk** — Klasifikasi LOW/MEDIUM/HIGH (lihat §Exposure Risk Classification).
- [ ] **Report** — Format laporan di §OUTPUT FORMAT. Read-only: jangan ubah config tanpa izin.

---

## RUNBOOK AUDIT (urutan eksekusi)

1. **Platform detection** → tentukan TERMUX / ANDROID_RESTRICTED / UNKNOWN.
2. **Connectivity check** → `ping -c1 -W3 8.8.8.8 || ping -c1 -W3 1.1.1.1`. Gagal → NO_INTERNET, beri recovery, stop.
3. **Interface & IP** → `ip -o addr show`; fallback `/proc/net/fib_trie` / `route`. Catat UP + IP + VPN.
4. **DNS** → `/etc/resolv.conf` + `getprop net.dns1 net.dns2`.
5. **Proxy** → `env | grep -iE 'proxy'` + `getprop http_proxy https_proxy`; mask `user:pass@`.
6. **Listening ports** → `ss -tulpen`; fallback `netstat -tulpen` / `/proc/net/tcp*`; flag `0.0.0.0`/`::`.
7. **Classify risk** → LOW/MEDIUM/HIGH (§Exposure Risk Classification).
8. **Report** → format §OUTPUT FORMAT, read-only.

---

## EXPOSURE RISK CLASSIFICATION

**LOW**
- Hanya listener di `127.0.0.1` / `::1` (localhost).
- Tidak ada port tak biasa terbuka.

**MEDIUM**
- Listener di `0.0.0.0` atau `::` (ekspos ke semua interface).
- Service tanpa autentikasi.
- Proxy terbuka tanpa pembatasan.

**HIGH**
- Port sensitif (SSH/ADB/database) terbuka ke semua interface.
- Kombinasi proxy + listener + tanpa firewall lokal.
- Informasi/port yang bisa diakses perangkat lain di jaringan yang sama (mis. hotspot).

---

## PLATFORM DETECTION

```
IF $PREFIX atau $HOME mengandung "com.termux":
    PLATFORM = TERMUX
    FALLBACK_CHAIN = iproute2 > net-tools > termux-tools > /proc
ELSE IF Android non-Termux:
    PLATFORM = ANDROID_RESTRICTED
    FALLBACK_CHAIN = dumpsys > /proc (termux-tools tak tersedia)
ELSE:
    PLATFORM = UNKNOWN
```

## REQUIREMENTS

Di Termux, paket umum: `net-tools`, `iproute2`, `termux-tools`, `procps`. Jika absen → gunakan fallback yang ada, laporkan & sarankan `pkg install <paket>`. Di Android non-Termux, akses terminal terbatas → andalkan `getprop` / `/proc`.

---

## CONCRETE EXAMPLES (input → output)

**Contoh 1**
- User: "Cek apakah ada port terbuka di Termux."
- Aksi: `ss -tulpen | grep LISTEN` → temukan `0.0.0.0:8080`.
- Output: WARNING MEDIUM — listener di `0.0.0.0:8080` terekspos ke LAN; identifikasi proses (jika ada PID), sarankan bind ke `127.0.0.1` atau firewall.

**Contoh 2**
- User: "Kenapa koneksi gagal?"
- Aksi: mulai dari Connectivity Check → `ping` timeout, tapi `curl -sI https://example.com` OK.
- Output: NO_ICMP (bukan NO_INTERNET) — operator blokir ICMP; konektivitas aplikasi normal. Recovery: cek airplane mode / wifi / data hanya bila aplikasi juga gagal.

**Contoh 3**
- User: "Aman nggak jaringannya?"
- Aksi: jalankan seluruh checklist.
- Output: laporan penuh + Exposure Risk + Recommendation.

---

## EDGE CASES

- **ICMP diblokir operator** → `ping` gagal padahal HTTP jalan; jangan klaim NO_INTERNET. Uji via `curl`/`getprop`.
- **IPv6 listener (`:::`)** → sering luput; perlakukan sama berisiko dengan `0.0.0.0`.
- **Tanpa root** → PID pemilik listener di `/proc/net/tcp` kosong; laporkan "proses tak teridentifikasi (butuh root)" bukan mengira tak ada.
- **PAC / proxy otomatis** → `env` kosong tapi `getprop` ada; cek keduanya.
- **Dual-stack (IPv4+IPv6)** → interface bisa punya keduanya; catat keduanya.
- **Hotspot/tether aktif** → device jadi gateway; listener makin berisiko terekspos ke klien.

---

## FAILURE MODES

| Mode gagal | Penyebab | Respons |
|------------|----------|---------|
| `ss`/`ip` not found | paket tak terinstall | turun ke net-tools / `/proc` |
| `ping` selalu timeout | ICMP diblokir | uji via `curl`/`getprop`, jangan klaim NO_INTERNET |
| `/proc/net/tcp` tanpa nama proses | tanpa root | laporkan UNKNOWN owner |
| resolv.conf kosong | resolver diatur via prop | pakai `getprop net.dns1/2` |
| Output ambigu | parsing gagal | validasi ulang, jangan asumsi |

---

## COMMON MISTAKES / ANTI-PATTERNS

| Mistake | Fix |
|---------|-----|
| Auditing tanpa konteks izin | Cek dulu apa ini device sendiri & scope read-only |
| Mengabaikan perbedaan localhost vs LAN | Laporkan keduanya — ekspos LAN adalah risiko nyata |
| Lupa memeriksa proxy | Cek env vars (`http_proxy`, `HTTPS_PROXY`, `ALL_PROXY`) + `getprop` |
| Hanya cek nomor port, bukan proses | Identifikasi pemilik (PID) setiap listener |
| Mengasumsikan root tersedia | Sebagian besar cek jalan tanpa root; catat yang butuh root |
| Menyimpulkan "aman" tanpa cek bind address | Verifikasi `0.0.0.0`/`::` vs `127.0.0.1`/`::1` |

## RED FLAGS (jangan biarkan lewat)

- Melaporkan port terbuka tanpa mengidentifikasi proses pemilik.
- Mengklaim "aman" tanpa mengecek interface listener.
- Mengabaikan listener IPv6 (`:::`).
- Melewatkan konfigurasi proxy / PAC.

## RATIONALIZATION PREVENTION

| Excuse | Reality |
|--------|---------|
| "Port-nya localhost saja" | Verifikasi bind address — `0.0.0.0` vs `127.0.0.1` |
| "Port utama sudah saya cek" | Audit SEMUA listener + proses, bukan sampel |
| "Cuma dev tool" | Dev tool tetap ekspos jaringan |

---

## HOW TO USE

1. **Kumpulkan konteks**: deteksi platform Termux, izin, batas background.
2. **Audit interface**: enumerate listener + proses pemilik (IPv4 + IPv6).
3. **Cek konektivitas**: DNS, env proxy, reachability test.
4. **Laporkan**: kategorikan temuan per severity + saran perbaikan.
Lihat RUNBOOK AUDIT untuk prosedur lengkap.

---

## OUTPUT FORMAT

```
NETWORK AUDIT
Platform: TERMUX / ANDROID_RESTRICTED / UNKNOWN
Connectivity: OK / FAILED / NO_ICMP
DNS: <ringkasan>
Proxy: <aktif/tidak, host:port (masked)>
Interfaces: <ringkasan, sertakan VPN>
Listening Ports: <daftar port + bind address + risiko>
Exposure Risk: LOW / MEDIUM / HIGH
Recommendation: <tindakan yang disarankan>
```

---

## ERROR HANDLING (detail)

- **DEPENDENCY ERROR** → laporkan paket hilang, cara `pkg install`, fallback `/proc`.
- **TOOL ERROR** → laporkan pesan; jangan lanjut jika output tak bisa dipercaya.
- **PERMISSION ERROR** → laporkan path ditolak; minta izin / sumber lain.
- **NETWORK ERROR** → laporkan koneksi gagal; fallback offline parsial.
- **ENVIRONMENT ERROR** → laporkan platform mismatch; pendekatan konservatif.
- **OUTPUT ERROR** → laporkan output tak wajar; validasi ulang.
- **UNKNOWN ERROR** → laporkan ERROR; jangan lanjut dengan asumsi.

---

## SECURITY

- Jangan kirim laporan lengkap ke channel publik.
- Jangan menampilkan credential jika muncul di env/config (mask `user:pass@`).
- Jangan memodifikasi konfigurasi jaringan tanpa izin.
- Audit hanya baca, kecuali user minta aksi perbaikan.

---

## VERIFICATION CHECKLIST (pasca-aksi nyata)

- [ ] Tiap perintah terverifikasi jalan (bukan sekadar exit 0).
- [ ] Connectivity terverifikasi (ping atau curl).
- [ ] Interface/IP terdeteksi & konsisten.
- [ ] DNS terperiksa (resolv.conf + getprop).
- [ ] Proxy terperiksa & nilai di-mask.
- [ ] Semua listener (IPv4+IPv6) terdaftar + bind address.
- [ ] Pemilik proses dicatat atau dilaporkan UNKNOWN (tanpa root).
- [ ] Risk classification diberikan dengan alasan.
- [ ] Tidak ada modifikasi jaringan tanpa izin.

---

## SELF-CHECK

Sebelum menyatakan audit selesai: semua poin VERIFICATION CHECKLIST terpenuhi, tidak ada asumsi tak terverifikasi, laporan read-only.

## QUALITY GATE

Target ≥ 90 untuk production-ready. Evaluasi: audit lengkap tanpa bagian terlewat? fallback jalan saat tool hilang? output mudah dipahami? risiko eksposur jelas? tidak ada asumsi Linux desktop? Jika < 90: perbaiki skill sebelum siap.

## GOLDEN RULE

Audit harus aman, read-only, dan tidak mengubah sistem. Jika ragu, laporkan sebagai WARNING, bukan menyelesaikan dengan asumsi.

---

## TOOLKIT / FILES

- `scripts/audit_net.sh` — audit eksposur jaringan read-only (konektivitas, interface/IP, DNS, proxy masked, listening ports, risk classification). Tidak pernah mengubah sistem. Contoh:
  `bash scripts/audit_net.sh` atau `bash scripts/audit_net.sh --json`
