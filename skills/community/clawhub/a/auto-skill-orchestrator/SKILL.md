---
name: skill-workflow-planner
slug: skill-workflow-planner
version: 1.1.5
description: "Gunakan saat user secara eksplisit meminta bantuan menyusun rencana urutan pengerjaan beberapa skill OpenClaw (mis. 'bantu susun alur skill A lalu B')."
metadata:
  openclaw:
    version: 1.1.5
---

# skill-workflow-planner — X∞ Compliance Layer

## 1. IDENTITY
`skill-workflow-planner` adalah skill pembantu penyusun rencana. Perannya: membantu user merangkai **rencana tertulis** (daftar langkah berurutan) ketika user ingin menyusun beberapa skill OpenClaw secara berurutan. Skill ini hanya menghasilkan teks rencana; eksekusi setiap langkah tetap di tangan user/agent dengan persetujuan eksplisit. Tidak ada instruksi terselubung untuk menjalankan skill secara otomatis.

## 2. PURPOSE
Memberikan user kerangka untuk:
- menjabarkan tujuan menjadi daftar langkah berurutan;
- mencatat dependensi antar-langkah;
- menandai langkah berisiko tinggi yang butuh persetujuan;
- menyusun catatan verifikasi sederhana.

## 3. METADATA
Lihat frontmatter (name, slug, version, description). Version mengikuti SemVer; setiap perubahan struktur/kebijakan wajib dicatat di CHANGELOG.

## 4. TRIGGER ENGINE
Aktif HANYA ketika user secara eksplisit meminta bantuan menyusun rencana/urutan beberapa skill (mis. "tolong susun alur skill A dan B", "bantu rancang urutan eksekusi skill ini"). Tidak aktif untuk: permintaan umum, task yang cukup satu skill, atau sekadar minta hasil tanpa minta susunan rencana.

**Frasa pemicu spesifik:**
- "susun alur skill", "bantu rancang urutan", "buatkan rencana workflow dari skill berikut";
- task dengan >1 skill yang sudah disebut user tapi butuh penyusunan urutan.

**Bukan trigger sendirian:** frasa umum seperti "buat aplikasi", "kerjakan saja", "urus semua" TIDAK cukup — butuh permintaan penyusunan rencana eksplisit.

**Contoh kalimat user:**
- "Tolong bantu susun rencana: research lalu coding lalu testing untuk dashboard XAU/USD."
- "OpenClaw error pas jalanin gateway di Termux, bantu rancang urutan penanganannya."

**Negative trigger (JANGAN aktifkan):**
- coding/debugging langsung satu skill tanpa perlu rencana lintas skill;
- user sudah menunjuk skill tertentu dan tidak butuh susunan rencana.

## 5. CONTEXT ENGINE
Sebelum menyusun rencana, catat: OS, ARCH, runtime, versi tool/API, batasan resource. **Termux Android ARM64 ≠ Ubuntu x86_64** (path, package manager, binary, permission berbeda). Verifikasi environment bila rencana menyangkut skill bergantung platform.

## 6. DECISION POLICY

| KONDISI | MAKA | ALASAN |
|---|---|---|
| Intent ambigu / kurang konteks | VERIFY (tanya klarifikasi minimal) | Salah arah lebih mahal dari satu pertanyaan |
| Langkah berisiko tinggi | TANDAI BUTUH PERSETUJUAN | Keamanan & oversight wajib |
| Langkah bergantung langkah lain | URUTKAN berdasar dependensi | Hindari langkah prematur |
| Alternatif langkah tidak tersedia | CATAT sebagai langkah butuh persiapan | Rencana tetap lengkap |

## 7. REASONING POLICY
Evidence-first. Bedakan **FAKTA** (terverifikasi) vs **HIPOTESIS** (dugaan). Confidence: CONFIRMED / LIKELY / POSSIBLE / UNKNOWN. Jangan klaim rencana sempurna tanpa konfirmasi user.

## 8. PLANNING STEPS (bukan eksekusi)
Urutan penyusunan rencana:
1. **PARSE** tujuan → goal, input, output, risiko, success condition.
2. **LIST** langkah yang diperlukan.
3. **URUTKAN** berdasar dependensi (A→B→C bila ada ketergantungan).
4. **TANDAI** langkah berisiko (destruktif / kredensial / perubahan sistem) sebagai BUTUH PERSETUJUAN.
5. **TULIS** rencana tertulis (checklist langkah).
6. **AJUKAN** ke user; eksekusi dilakukan user/agent atas persetujuan eksplisit.

Preferensi tool: gunakan `read`/`exec` untuk file/shell, `web_fetch`/`browser` untuk web. Jangan memanggil semua tool sekaligus.

## 9. TOOL POLICY
Pilih tool berdasar kebutuhan + konteks, bukan kebiasaan. Redact secret sebelum log/store.

## 10. NOTES (bukan routing memory)
Catat preferensi dan tujuan yang **user nyatakan secara eksplisit**, bukan keputusan pemilihan skill. Simpan ke memory hanya bila user memintanya.

## 11. VERIFICATION CHECKLIST (bila user minta bantuan cek hasil)
- [ ] File/dir yang dijanjikan benar-benar ada (`read`/`ls`/`stat`).
- [ ] Isi sesuai harapan (bukan kosong/template).
- [ ] Aksi berdampak nyata (proses jalan, build lulus).
- [ ] Tidak ada regression pada konfigurasi/dependensi lain.

## 12. ERROR HANDLING
Bila rencana gagal di lapangan: catat langkah bermasalah, usulkan revisi ke user, jangan infinite loop.

## 13. SECURITY GUARDRAILS
NEVER log secret. REDACT API KEY / TOKEN / PASSWORD / SECRET sebelum simpan atau tampilkan. Untuk task sensitif (kredensial, perubahan sistem, destruktif), wajibkan approval user. Jangan bypass safeguard apa pun.

## 14. EVALUATION
Self-eval: rencana jelas? langkah logis dan berurutan? risiko ditandai?

## 15. OBSERVABILITY
Catat rencana yang dibuat (tanpa secret) untuk audit user.

## 16. PERFORMANCE OPTIMIZATION
Gunakan langkah minimal yang cukup menyelesaikan tujuan.

## 17. SELF-IMPROVEMENT
Belajar dari feedback user tentang format rencana (bukan tentang pemilihan skill).

## 18. VERSIONING
SemVer. Perubahan struktur = MAJOR; penambahan panduan = MINOR; perbaikan redaksi = PATCH. CHANGELOG wajib tiap rilis.

---

**CHANGELOG**
- 1.1.4 — Rewrite total jadi planning-only helper murni: hanya menghasilkan rencana tertulis; eksekusi di tangan user. Kepatuhan SkillSpector LLM.
- 1.1.3 — Persempit trigger, approval gate di pipeline, ganti judul jadi Workflow Planner.
- 1.1.1 — Kepatuhan SkillSpector: perbaikan frontmatter dan redaksi.

## 19. COMPATIBILITY
Ketahui OS / ARCH / RUNTIME / versi tool & API yang tersedia sebelum menyusun rencana. Skill yang incompatible dengan environment = tandai butuh persiapan, cari alternatif.

## 20. KNOWLEDGE SOURCES
Trust hierarchy: OFFICIAL > PRIMARY > REPUTABLE > COMMUNITY > UNKNOWN. Jangan pasang skill eksternal otomatis bila source/code tak terpercaya.

## 21. EXIT CONDITIONS
Berhenti (dan laporkan) pada: SUCCESS / FAILURE / BLOCKED / NEED USER / NEED CREDENTIAL / NEED TOOL / NEED VERIFICATION.

# OpenClaw Skill Workflow Planner X∞

## Overview
Skill pembantu (advisor) yang membantu user menyusun **rencana** urutan pengerjaan beberapa skill OpenClaw ketika diminta. Skill ini hanya menghasilkan rencana tertulis; eksekusi dilakukan oleh agent/user. Menyelesaikan dependensi dan konflik instruksi agar agent bekerja dengan context tetap ramping.

---

## When to Use
Gunakan ketika:
- user secara eksplisit meminta bantuan menyusun rencana/urutan beberapa skill, dan task butuh >1 kemampuan;
- perlu menyusun alur beberapa skill yang saling mendukung;
- perlu merencanakan urutan model, plugin, dan tool—bukan hanya skill.

Jangan gunakan untuk:
- coding/debugging langsung yang cukup satu skill tanpa koordinasi;
- menggantikan approval user untuk high-risk change;
- membuat loop tanpa progress check.

---

## Core Operating Model

### 1. PLANNING PIPELINE
```
USER REQUEST (eksplisit: bantu susun rencana)
  ↓ PARSE TUJUAN
  ↓ LIST LANGKAH
  ↓ URUTKAN BERDASAR DEPENDENSI
  ↓ TANDAI LANGKAH BUTUH PERSETUJUAN
  ↓ TULIS RENCANA TERTULIS
  ↓ AJUKAN KE USER
  (EKSEKUSI dilakukan oleh user/agent, bukan oleh skill ini)
```
Skill ini hanya menghasilkan rencana tertulis. Eksekusi tiap langkah tetap di tangan user/agent dengan persetujuan eksplisit.

### 2. UNIVERSAL RULE
Jika user setuju dengan rencana → user/agent yang menjalankan langkah sesuai urutan. Skill ini mengusulkan alur & meminta konfirmasi sebelum aksi berdampak (terutama high-risk). Jangan mengeksekusi destruktif tanpa approval.

### 3. MINIMAL STEPS
Gunakan **langkah minimal yang cukup menyelesaikan tujuan**. Lebih banyak langkah ≠ lebih baik.

### 4. TASK BREAKDOWN (template)
Tentukan sebelum susun rencana: GOAL, INPUT, OUTPUT, DOMAIN, COMPLEXITY, TOOLS REQUIRED, CONSTRAINTS, RISK, SUCCESS CONDITION.

### 5. DEPENDENCY ORDER
Berurutan bila ada ketergantungan (A→B→C). Jangan jalankan langkah yang butuh hasil dari langkah lain sebelum langkah itu selesai.

### 6. RISK TAGGING
Tandai langkah destruktif / kredensial / perubahan sistem sebagai BUTUH PERSETUJUAN.

### 7. RESULT VERIFICATION
EXPECTED vs ACTUAL. Tidak cocok → sarankan revisi ke user.

### 8. ADAPTATION
Task berubah → REASSESS rencana. Jangan pakai rencana usang.

### 9. HEALTH CHECK
Sebelum rencana menyangkut skill kritis: AVAILABLE? COMPATIBLE? DEPENDENCIES OK? KNOWN BROKEN? Bila tidak sehat → sarankan alternatif.

### 10. NON-NEGOTIABLE RULES
- NEVER klaim rencana sempurna tanpa konfirmasi user.
- NEVER langkah tanpa urutan dependensi yang jelas.
- NEVER infinite loop.
- UNTUK aksi berdampak (destruktif, kredensial, perubahan sistem): selalu minta approval user.

---

## Concrete Examples (Input → Output)

**Contoh 1 — Web app trading**
- Input: "Tolong bantu susun rencana: research lalu coding lalu testing untuk dashboard analisis XAU/USD."
- Workflow usulan: RESEARCH → CODING → TESTING.
- Output ke user: rencana tertulis + verifikasi (build lulus, endpoint merespons) setelah user/agent menjalankan.

**Contoh 2 — Debug**
- Input: "OpenClaw error saat menjalankan gateway."
- Workflow usulan: READ LOG → CHECK ENV TERMUX ARM64 → FIX → VERIFY.
- Eksekusi: dilakukan user/agent atas persetujuan.

---

## Edge Cases
- **User sudah sebut skill**: hormati, tapi tetap bantu susun urutan bila diminta.
- **Skill dependen platform (Termux)**: verifikasi binary/path sebelum masukkan ke rencana; fallback ke tool CLI bila skill gagal.
- **Dua intent bertentangan**: clarifikasi minimal atau pilih intent primer + flag sisanya.

## Common Mistakes / Anti-Patterns
| Anti-Pattern | Fix |
|---|---|
| Langkah tanpa urutan | Tentukan dependency order dulu |
| Tak ada verifikasi | Sediakan checklist hasil |
| Infinite loop | Depth/attempt limit + state change check |

## Failure Modes
- **Wrong order**: intent ambigu → verifikasi klarifikasi.
- **Silent gap**: rencana kosong → checklist EXISTENCE/CONTENT wajib.

## Red Flags
- Rencana tanpa analisis dependensi.
- Tak ada langkah verifikasi.

## How to Use
1. **Parse intent** → tentukan langkah yang dibutuhkan.
2. **Analyze dependencies** → selesaikan prioritas.
3. **Tulis rencana** → ajukan ke user.
4. **Verify** hasil akhir (bila user minta bantuan cek).

## Quick Reference
| Situasi | Aksi |
|---|---|
| Banyak skill relevan | Rancang urutan optimal |
| Langkah konflik | Resolve prioritas |
| Task kompleks | Dekomposisi ke sub-task |
| Rencana gagal | Sarankan revisi ke user |

## Golden Principle
Bantu user menyusun rencana skill secara cerdas, tapi eksekusi tetap di tangan user: aksi berdampak selalu butuh persetujuan.
