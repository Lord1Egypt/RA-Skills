# ClawGator Superpowers

<img src="logo.jpg" alt="ClawGator Superpowers Logo" width="100%">

Framework pengembangan perangkat lunak lengkap untuk pengguna ClawGator.

**Based on:** [obra/superpowers](https://github.com/obra/superpowers)  
**License:** MIT (same as obra/superpowers)

---

## Deskripsi / Description

Skill ini menyediakan **workflow pengembangan perangkat lunak lengkap** yang memastikan tim ClawGator selalu:
- 💡 Think before they code
- 📋 Plan before they build
- ✅ Verify before they ship
- 🧪 Test before production

Complete software development framework for ClawGator team. Ensures the team always thinks before coding, plans before building, verifies before shipping, and tests before production.

---

## Credit & License

**This skill is based on:** [obra/superpowers](https://github.com/obra/superpowers) by [Obra](https://github.com/obra)

- **Original:** https://github.com/obra/superpowers
- **License:** MIT
- **This fork:** Adapted specifically for ClawGator team and OpenClaw ecosystem
- **Changes:** Bilingual support (Indonesian + English), ClawGator branding, customized workflows

---

## 🌏 Bilingual Support / Dukungan Bahasa Ganda

Skill ini mendukung dua bahasa / This skill supports two languages:

**Bahasa Indonesia / Indonesian:**
- Keywords: "buat", "tambah", "kembangkan", "rancang", "plan", "desain", "fix", "debug"
- Output: Bahasa Indonesia

**English:**
- Keywords: "build", "create", "add", "develop", "design", "plan", "fix", "debug"
- Output: English

---

<img src="github-credits.jpg" alt="GitHub Credits" width="35%">

## Fitur Utama / Key Features

### 💡 Brainstorming & Design
- Memahami requirement dan konteks proyek
- Menjelaskan ide-ide sebelum implementasi
- Validasi desain melalui dialog interaktif
- Menghasilkan dokumen desain yang terstruktur

### 📋 Planning
- Memecah pekerjaan menjadi tasks kecil (2-5 menit)
- Mendefinisikan acceptance criteria
- Membuat rencana implementasi terperinci

### 🌳 Git Worktrees
- Setup workspace terisolasi di branch baru
- Protect branch utama (main/master)
- Enable development paralel tanpa conflict

### 🚀 Eksekusi Sistematis
- Mengerjakan tasks sesuai rencana
- Tracking progress
- Verifikasi hasil antar batch

### 🧪 Test-Driven Development (TDD)
- RED: Tulis test → Lihat fail
- GREEN: Implement minimal code → Lihat pass
- REFACTOR: Clean up → Stay green
- **Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

### 🔍 Systematic Debugging
- Phase 1: Investigasi Root Cause
- Phase 2: Analisis Pola
- Phase 3: Hipotesis & Testing
- Phase 4: Fix & Verify
- **Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

### 📊 Code Review
- Request code review antar tasks
- Apply feedback dari review
- Ensure code quality dan consistency

### ✅ Verification & Completion
- Verify tests sebelum mark selesai
- Wrap up development branch dengan options:
  * Merge ke main
  * Create Pull Request
  * Keep branch untuk continued work
  * Discard branch

---

## 14 Sub-Skills Lengkap / Complete Sub-Skills

| Skill | Kategori | Category | Fungsi / Function |
|-------|---------|----------|-------------------|
| **using-superpowers** | Process | Process | Skill dasar - memandu semua langkah |
| **brainstorming** | Process | Process | Memahami requirement & desain |
| **writing-plans** | Process | Process | Buat rencana implementasi |
| **executing-plans** | Execution | Execution | Eksekusi plan dengan checkpoints |
| **finishing-a-development-branch** | Process | Process | Wrap up development branch |
| **test-driven-development** | Quality | Quality | RED-GREEN-REFACTOR cycle |
| **systematic-debugging** | Quality | Quality | 4-phase root cause analysis |
| **verification-before-completion** | Quality | Quality | Verify fix selesai |
| **using-git-worktrees** | Git | Git | Isolated workspace di new branch |
| **subagent-driven-development** | Execution | Execution | Fresh subagent per task |
| **dispatching-parallel-agents** | Execution | Execution | Paralel agents |
| **requesting-code-review** | Review | Review | Review code terhadap plan |
| **receiving-code-review** | Review | Review | Apply feedback dari review |
| **writing-skills** | Meta | Meta | Buat skill OpenClaw baru |

---

## 📦 Installation / Cara Install

### Prerequisites / Prasyarat

```bash
# Pastikan OpenClaw sudah terinstall / Ensure OpenClaw is installed
openclaw --version
```

### Method 1: Local Installation (Recommended / Direkomendasikan)

```bash
# Clone atau download skill ini
# Clone or download this skill

# Copy ke extensions OpenClaw / Copy to OpenClaw extensions
cp -r /home/clawgator-superpowers ~/.openclaw/extensions/

# Pastikan struktur folder benar / Verify folder structure
ls -la ~/.openclaw/extensions/clawgator-superpowers/
# Expected output:
# - SKILL.md
# - openclaw.plugin.json
# - package.json
# - README.md
# - references/
# - skills/ (14 sub-skills)

# Update openclaw.json config
nano ~/.openclaw/openclaw.json

# Tambahkan ke plugins.allow / Add to plugins.allow:
{
  "plugins": {
    "allow": [
      "whatsapp",
      "clawgator-superpowers"    <-- Tambahkan ini / Add this
    ],
    "entries": {
      "clawgator-superpowers": {
        "enabled": true,
        "config": {
          "brainstormingMode": "standard",
          "maxTasksPerPlan": 5,
          "enableVerification": true,
          "saveDesignDocs": true,
          "tddEnforced": true,
          "debuggingStrictMode": true,
          "useGitWorktrees": true
        }
      }
    }
  }
}

# Restart OpenClaw gateway untuk reload skill / Restart gateway to reload skill
kill -USR1 $(pgrep openclaw-gateway)

# Atau restart service / Or restart service
systemctl restart openclaw-gateway

# Verify skill sudah terinstall / Verify skill is installed
openclaw skills list | grep clawgator
```

### Method 2: Install via ClawHub (Future / Mendatang)

```bash
# Install via ClawHub (kalau sudah dipublish)
npx clawhub install clawgator-superpowers
```

---

## 📚 Usage / Cara Menggunakan

### Starting New Projects / Memulai Proyek Baru

**Bahasa Indonesia:**
```
Buat fitur login
Tambah autentikasi
Kembangkan dashboard baru
Rancang API endpoint
Plan user management
```

**English:**
```
Build login feature
Create authentication system
Develop new dashboard
Design API endpoint
Plan user management implementation
```

Skill akan otomatis / Skill will automatically:
1. Mengaktifkan `using-superpowers` / Activate using-superpowers
2. Brainstorming untuk pahami requirement / Brainstorming to understand requirements
3. Buat git worktree baru / Create new git worktree
4. Tulis implementasi plan / Write implementation plan
5. Eksekusi dengan TDD / Execute with TDD
6. Test dan verify / Test and verify

### Fixing Bugs / Fix Bug

**Bahasa Indonesia:**
```
Fix bug: database connection error
Perbaiki: login tidak berfungsi
Debug: performance issue
```

**English:**
```
Fix bug: database connection error
Debug: performance issue
Troubleshoot: login not working
```

Skill akan otomatis / Skill will automatically:
1. Mengaktifkan `systematic-debugging` / Activate systematic-debugging
2. Investigasi root cause (4 phases) / Investigate root cause (4 phases)
3. Implement fix dengan TDD / Implement fix with TDD
4. Verify fix / Verify fix
5. Run semua tests / Run all tests

---

## 🔧 Available Tools / Tools Tersedia

| Tool | Deskripsi / Description | Input / Input Required |
|------|-------------------------|------------------------|
| **brainstorm** | Mulai sesi brainstorming | `topic` (string, wajib/required), `context` (object, optional) |
| **create_git_worktree** | Buat git worktree baru | `branchName` (wajib/required), `basedOn` (optional) |
| **write_implementation_plan** | Buat rencana implementasi | `planPath` (wajib/required), `design` (wajib/required) |
| **execute_plan** | Eksekusi plan dengan TDD | `planPath` (wajib/required), `batchSize` (optional) |
| **systematic_debug** | Debugging sistematis | `issue` (wajib/required), `evidence` (optional) |
| **request_code_review** | Request code review | `taskNumber` (wajib/required), `planPath` (wajib/required) |
| **apply_code_review_feedback** | Terapkan feedback | `taskNumber` (wajib/required), `feedback` (wajib/required) |
| **finish_development_branch** | Selesaikan branch | `action` (wajib/required), `branchName` (wajib/required) |
| **get_status** | Cek status proyek aktif | Tidak ada input / No input |

---

## 🔧 Configuration / Konfigurasi

| Parameter | Type / Tipe | Default | Deskripsi / Description |
|-----------|-------------|---------|-------------------------|
| `brainstormingMode` | enum | standard | Mode brainstorming |
| `maxTasksPerPlan` | number | 5 | Maksimal tasks per rencana / Max tasks per plan |
| `enableVerification` | boolean | true | Aktifkan verifikasi otomatis / Enable auto verification |
| `saveDesignDocs` | boolean | true | Simpan dokumen desain / Save design documents |
| `tddEnforced` | boolean | true | Paksa TDD / Enforce TDD (no code without test first) |
| `debuggingStrictMode` | boolean | true | Paksa debugging sistematis / Enforce systematic debugging |
| `useGitWorktrees` | boolean | true | Gunakan git worktrees / Use git worktrees |

---

## 🔄 Workflow / Alur Kerja

```
Permintaan / Request → Using Superpowers → Brainstorming → Git Worktree
                              ↓
                    Writing Plans → Executing Plans → TDD → Code Review
                              ↓
                    Verification → Finish Branch → Merge/PR/Keep/Discard
```

---

## ⚠️ Iron Laws

1. **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST** (TDD)
2. **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST** (Debugging)
3. **If you think there is even a 1% chance a skill might apply, you ABSOLUTELY MUST invoke it**

---

## 📋 TDD Cycle

```
RED → Write failing test → Verify fails
GREEN → Implement minimal code → Verify passes
REFACTOR → Clean up → Stay green
REPEAT → Next test
```

---

## 🔍 Debugging Cycle

```
Phase 1: Root Cause Investigation
  - Read errors carefully
  - Reproduce consistently
  - Check recent changes
  - Trace data flow

Phase 2: Pattern Analysis
  - Find working examples
  - Compare against references
  - Identify differences

Phase 3: Hypothesis & Testing
  - Form single hypothesis
  - Test it
  - Learn & iterate

Phase 4: Fix & Verify
  - Implement fix at root cause
  - Verify with original issue
  - Run all tests
```

---

## 📂 Folder Structure / Struktur Folder

```
/home/clawgator-superpowers/
├── SKILL.md                    (11KB - Main skill documentation)
├── openclaw.plugin.json        (Plugin configuration)
├── package.json                 (Metadata)
├── README.md                    (This file - Usage guide)
├── references/                   (Reference documentation)
└── skills/                      (14 sub-skills from obra/superpowers)
    ├── using-superpowers/
    ├── brainstorming/
    ├── writing-plans/
    ├── executing-plans/
    ├── test-driven-development/
    ├── systematic-debugging/
    ├── using-git-worktrees/
    ├── subagent-driven-development/
    ├── dispatching-parallel-agents/
    ├── requesting-code-review/
    ├── receiving-code-review/
    ├── verification-before-completion/
    ├── finishing-a-development-branch/
    └── writing-skills/
```

---

## 📌 Notes for ClawGator Users / Catatan untuk Pengguna ClawGator

- Skill ini **WAJIB digunakan** sebelum memulai pengembangan fitur baru / **MUST use** this skill before starting new feature development
- Setiap brainstorming session akan menghasilkan desain yang divalidasi / Each brainstorming session produces validated designs
- Setiap development menggunakan TDD (RED-GREEN-REFACTOR) / All development uses TDD
- Setiap bug fix menggunakan systematic debugging (4 phases) / All bug fixes use systematic debugging
- Setiap task di-review terhadap plan sebelum melanjutkan / Each task is reviewed against the plan
- Semua work diisolasi di git worktrees (jangan edit main langsung) / All work is isolated in git worktrees (don't edit main directly)
- Gunakan untuk fitur-fitur OpenClaw, tool internal, atau proyek ClawGator / Use for OpenClaw features, internal tools, or ClawGator projects

---

## 🔗 Links & References

- **Original Repository:** https://github.com/obra/superpowers
- **This Fork:** Adapted for ClawGator Users
- **OpenClaw Documentation:** https://docs.openclaw.ai
- **OpenClaw GitHub:** https://github.com/openclaw/openclaw
- **ClawHub:** https://clawhub.com (Skill marketplace)

---

## 📋 Version & Info / Versi & Info

| Item | Value / Nilai |
|------|---------------|
| **Version / Versi** | 1.0.0 |
| **Based on / Berdasarkan** | obra/superpowers (100% workflow, 14 sub-skills) |
| **License / Lisensi** | MIT (same as obra/superpowers) |
| **Team / Tim** | ClawGator Team |
| **Language Support / Dukungan Bahasa** | 🌏 Bahasa Indonesia & English |
| **OpenClaw Engine** | >= 2026.2.0 |

---

## 👥 Contributing / Berkontribusi

Skill ini adalah fork dari obra/superpowers yang disesuaikan untuk ekosistem ClawGator. Untuk kontribusi ke workflow asli, silakan kunjungi repository obra/superpowers.

This skill is a fork of obra/superpowers adapted for the ClawGator ecosystem. For contributing to the original workflow, please visit the obra/superpowers repository.

---

## 📜 License

```
MIT License

Copyright (c) 2026 ClawGator Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**Made with ❤️ for ClawGator Users**

**Original by:** [Obra](https://github.com/obra) - obra/superpowers

**Adapted by:** ClawGator Team - 2026
