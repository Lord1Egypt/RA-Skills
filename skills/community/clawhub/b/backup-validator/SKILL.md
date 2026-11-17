---
name: "openclaw-backup-validator"
slug: openclaw-backup-validator
version: 1.1.0
homepage: https://github.com/pmuhammadagus-byte/openclaw-settings
description: "Use when validating OpenClaw backup artifacts before push: skill structure, secret leaks, Termux compatibility, and repo readiness."
changelog: ClawHub professional standard: Overview, When to Use, How to Use, Common Mistakes, Red Flags, Rationalizations, Quick Reference
emoji: "🛡️"
  openclaw:
    requires:
      bins:
        - bash
        - git
        - python3
    os:
      - linux
      - darwin
      - win32
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - git
        - python3
    os:
      - linux
      - darwin
      - win32
---

# OPENCLAW BACKUP VALIDATOR

## When to Use

Gunakan skill ini ketika:
- akan menjalankan backup sebelum push ke GitHub;
- baru menambahkan/mengubah skill di workspace;
- ingin memastikan tidak ada secret bocor;
- ingin memastikan struktur skill/workspace valid;
- ingin memastikan kompatibilitas Termux/Android sebelum deploy.

---

## PURPOSE

Memvalidasi seluruh artefak backup OpenClaw sebelum di-push ke repo remote.
Mencegah:
- secret leakage
- skill tidak valid
- struktur rusak
- asumsi Linux desktop palsu di Termux/Android

---

## TRIGGER

Gunakan skill ini saat:
- `backup.sh` akan dijalankan
- ada perubahan di `workspace/`, `skills/`, atau `skill-workshop/`
- sebelum commit/push repo `openclaw-settings`
- setelah menambah skill baru

Jangan gunakan untuk:
- validasi Git log (gunakan Git tools)
- recovery data yang sudah terhapus permanen
- pengganti backup script yang ada

---

## PRECONDITIONS

- Script backup `~/openclaw-backup/backup.sh` ada dan dapat dieksekusi
- Repo Git `~/openclaw-backup` terinisialisasi
- `python3` tersedia untuk redaction
- `grep`, `find`, `git` tersedia di PATH

Jika salah satu tidak ada, laporkan dan berikan fallback.

---

## INPUT

- `BACKUP_DIR` default: `~/openclaw-backup`
- `WORKSPACE_DIR` default: `~/.openclaw/workspace`
- Optional: `EXTRA_PATHS` tambahan path untuk divalidasi

---

## WORKFLOW

PHASE 1 — REQUIREMENT ANALYSIS
↓
Tentukan tujuan validasi.

PHASE 2 — ENVIRONMENT ANALYSIS
↓
Deteksi platform: Linux desktop / Termux / Android.

PHASE 3 — ARCHITECTURE
↓
Siapkan daftar cek: structure, secret, skill, compatibility.

PHASE 4 — IMPLEMENTATION
↓
Jalankan setiap validator.

PHASE 5 — VALIDATION
↓
Kumpulkan hasil dan klasifikasi.

PHASE 6 — HARDENING
↓
Tambahkan fallback jika tool/command gagal.

PHASE 7 — SELF-TEST
↓
Simulasikan kasus normal, failure, dan edge case.

PHASE 8 — FINALIZATION
↓
Laporkan status: PASS / FAIL / WARNING.

---

## EXECUTION

Jalankan validator dalam urutan ini:

### 1. Platform Detection

Deteksi environment sebelum memilih strategi validasi.

IF `$PREFIX` contains `com.termux` OR `$HOME` contains `com.termux`:
  PLATFORM = TERMUX
ELSE IF `uname -s` = `Linux` AND `uname -m` = `x86_64`:
  PLATFORM = LINUX_DESKTOP
ELSE:
  PLATFORM = UNKNOWN

Catat platform di laporan.

### 2. Structure Validation

Validasi struktur direktori backup.

Cek:
- `workspace/` ada
- `skills/` ada
- `workspace-attestations/` ada
- `skill-workshop/` ada
- `agents/` ada
- `tui/` ada
- `config/` ada
- `metadata/` ada

Jika ada direktori wajib yang hilang:
- laporkan ERROR
- berikan nama direktori yang hilang
- berikan recovery action: jalankan `backup.sh`

### 3. Skill File Validation

Untuk setiap `SKILL.md` di `workspace/skills/`:

Cek:
- file ada dan bukan direktori
- ada frontmatter `name`
- ada `description`
- minimal satu bagian konten

Jika `SKILL.md` rusak:
- laporkan ERROR
- sebutkan path dan masalahnya
- berikan fallback: perbaiki manual atau restore dari Git

### 4. Secret Leak Detection

Gunakan dua lapisan validasi:

#### 4a. Pattern Scan

Cari pola sensitif:
- Telegram bot token: `[0-9]{8,10}:[A-Za-z0-9_-]{35,}`
- OpenAI key: `sk-[A-Za-z0-9]{20,}`
- GitHub token: `ghp_[A-Za-z0-9]{30,}` atau `github_pat_[A-Za-z0-9_]{20,}`
- NVIDIA key: `nvapi-[A-Za-z0-9_-]{16,}`
- AWS key: `AKIA[0-9A-Z]{16}`
- Private key header: `-----BEGIN [A-Z ]*PRIVATE KEY-----`

Jika ditemukan:
- laporkan ERROR
- sebutkan file dan pola yang terdeteksi
- berikan recovery: redact menggunakan script backup atau hapus/ubah file

#### 4b. Redaction Verification

Jika backup sudah di-redact oleh `backup.sh`:
- pastikan file redacted tidak mengandung pola sensitif asli
- pastikan `agents/*/models.json` tidak berisi `api_key`, `token`, `secret`, `password`

Jika redaction kurang:
- laporkan WARNING
- sarankan jalankan ulang `backup.sh`

### 5. Git Status Validation

Cek repo backup:

- `git status --porcelain` harus kosong setelah commit
- Jika ada modified tetapi belum di-commit:
  - laporkan WARNING
  - minta commit atau `git reset --hard` jika aman
- Jika ada untracked file penting:
  - laporkan WARNING
  - minta `git add` atau sesuaikan `.gitignore`

### 6. Remote Sync Validation

Cek apakah branch `main` di remote up-to-date:

- `git rev-parse HEAD`
- `git rev-parse origin/main`

Jika berbeda:
- laporkan INFO bahwa push diperlukan
- Jika berbeda jauh, laporkan WARNING untuk potential conflict

### 7. Skill Compatibility Check

Untuk setiap skill baru/diubah:

Cek:
- tidak ada tool/command fiktif
- tidak ada dependency yang tidak terdokumentasi
- path yang digunakan sesuai platform

IF PLATFORM = TERMUX:
  - pastikan tidak mengasumsikan systemd
  - pastikan tidak mengasumsikan path `/usr/local/...`
  - pastikan tidak memanggil service desktop-only
  - pastikan binary yang dibutuhkan tersedia atau punya fallback

Jika ketidakcocokan ditemukan:
- laporkan WARNING atau ERROR
- berikan alternatif Termux-realistik

### 8. Metadata Consistency

Cek:
- `metadata/system.txt` berisi backup date valid
- `metadata/skills-list.txt` konsisten dengan `workspace/skills/`
- `metadata/workspace-skill-files.txt` konsisten dengan file yang ada

Jika inkonsistensi:
- laporkan WARNING
- berikan recovery: jalankan ulang backup atau perbaiki metadata manual

---

## OUTPUT FORMAT

Berikan laporan dalam bentuk:

VALIDASI BACKUP — PASS / FAIL / WARNING

Platform: TERMUX / LINUX_DESKTOP / UNKNOWN

### Summary
- Total skills checked: X
- Total files checked: Y
- Secret leaks: Z
- Structural issues: W
- Compatibility issues: V

### Details

#### Structural
- [OK] `workspace/`
- [FAIL] `agents/` missing

#### Skills
- [OK] `aurum-brain/SKILL.md`
- [WARN] `new-skill/SKILL.md` missing description

#### Secrets
- [OK] No Telegram token leak
- [FAIL] `path/to/file` contains possible API key pattern

#### Git
- [OK] Clean working tree
- [WARN] Uncommitted changes detected

#### Compatibility
- [OK] No Linux desktop-only assumptions in Termux
- [FAIL] `skill-x` references `/usr/local/bin/run.sh` on Termux

### Recovery Actions
1. Jalankan ulang `backup.sh`
2. Redact file yang bocor
3. Perbaiki `SKILL.md` yang rusak
4. ...

---

## ERROR HANDLING

INPUT ERROR
→ Jelaskan path/format yang salah
→ Berikan contoh input yang benar
→ Jangan lanjut validasi parsial tanpa konfirmasi

DEPENDENCY ERROR
→ `python3` tidak ada: gunakan `grep` + sed sebagai fallback parsial
→ `git` tidak ada: laporkan ERROR dan minta install

TOOL ERROR
→ `grep`/`find` gagal: laporkan ERROR dengan pesan dari tool
→ Jangan lanjut validator berikutnya jika struktur tidak bisa dibaca

NETWORK ERROR
→ Tidak mempengaruhi validasi offline
→ Skip remote sync check, laporkan INFO

AUTH ERROR
→ Tidak relevan untuk validator lokal
→ Skip

TIMEOUT
→ Batasi durasi scan direktori
→ Jika timeout, laporki sebagian hasil dan minta retry

PERMISSION ERROR
→ Laporkan file/directory yang tidak bisa dibaca
→ Berikan recovery: `chmod` atau jalankan dengan permission yang sesuai

ENVIRONMENT ERROR
→ Jika platform tidak terdeteksi, set UNKNOWN dan lanjut dengan asumsi konservatif

OUTPUT ERROR
→ Jika laporan tidak bisa ditulis, gunakan stdout sebagai fallback

UNKNOWN ERROR
→ Tangkap exception
→ Laporkan ERROR
→ Jangan redact otomatis tanpa tahu konteks

---

## RETRY & FALLBACK

PRIMARY VALIDATOR
 ↓
FAILED?
 ↓
SAFE RETRY max 2x
 ↓
FAILED?
 ↓
FALLBACK validator subset
 ↓
FAILED?
 ↓
STOP
REPORT ERROR

Aturan:
- Jangan retry tanpa batas
- Jangan retry setelah operasi destruktif
- Jangan lanjut push jika validator gagal dengan ERROR kritis

---

## SECURITY

- Jangan cetak isi file sensitif
- Jangan simpan hasil scan secret ke file yang tidak dilindungi
- Jangan kirim laporan lengkap ke channel publik
- Jangan jalankan command berbahaya untuk validasi
- Jangan hapus file selama validasi; hanya laporkan

---

## SELF-CHECK

Sebelum menyatakan validator selesai, pastikan:

[ ] Tujuan validator jelas
[ ] Setiap cek memiliki kriteria pass/fail/warning
[ ] Error handling tersedia untuk setiap kategori
[ ] Fallback untuk tool yang tidak tersedia
[ ] Platform detection berjalan
[ ] Tidak ada command fiktif
[ ] Tidak ada asumsi Linux desktop
[ ] Output mudah dibaca agent
[ ] Recovery action jelas untuk setiap masalah
[ ] Tidak ada side effect destruktif

---

## QUALITY GATE

Nilai validator:

Architecture: apakah alur validasi logis dan tidak terputus?
Reliability: apakah tetap berjalan jika sebagian tool gagal?
Clarity: apakah laporan mudah dipahami agent/user?
Tool Usage: apakah hanya pakai tool yang tersedia?
Error Handling: apakah semua error tercover?
Security: apakah aman dari secret exposure?
Compatibility: apakah aman di Termux/Android/desktop?
Maintainability: apakah mudah diperbarui jika pola secret berubah?
Extensibility: apakah mudah menambah cek baru?
Verification: apakah agent bisa mempercayai hasil laporan?

Target: minimal 90 untuk production-ready.

Jika di bawah 90: perbaiki validator sebelum menganggap siap.

---

## FINAL RESPONSE FORMAT

Setelah menjalankan validasi, berikan:

STATUS: PASS / FAIL / NEEDS IMPROVEMENT
PLATFORM: TERMUX / LINUX_DESKTOP / UNKNOWN
SCORE: 0-100

SUMMARY:
- Ringkasan hasil utama

DETAILS:
- Daftar cek dengan status

RECOVERY:
- Langkah perbaikan yang perlu dilakukan

Jika PASS:
- aman untuk lanjut backup/push

Jika FAIL:
- jangan push sampai diperbaiki

Jika NEEDS IMPROVEMENT:
- perbaiki sesuai rekomendasi, lalu validasi ulang

---

## GOLDEN RULE

Jangan pernah memaksa laporan PASS jika ada ERROR kritis.
Lebih baik validator menolak push daripada secret bocor atau skill rusak.

Target akhirnya:

RELIABLE
+
SECURE
+
PLATFORM-AWARE
+
ACTIONABLE
+
PRODUCTION-READY

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Validating presence only | Check integrity, not just existence |
| No hash verification | Compare hashes for consistency |
| Ignoring permissions | Validate file permissions |
| Missing restore test | Verify backup can be restored |

## Red Flags

- Claiming valid without integrity check
- No restore verification
- Missing permission checks
- Ignoring corruption signs

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The files are there" | Existence ≠ integrity. |
| "It worked before" | Verify current backup. |
| "Hashes take too long" | Integrity matters. |

## Quick Reference

| Situasi | Aksi |
|---------|------|
| Validasi backup | Jalankan checker |
| Backup rusak | Diagnosa & repair |
| Cek integritas | Hash + struktur |
| Restore | Verifikasi hasil |
| Rutin | Jadwalkan validasi |
