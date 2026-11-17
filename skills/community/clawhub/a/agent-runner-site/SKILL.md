---
name: openclaw-agent-runner-site
description: "Gunakan saat user ingin membuat halaman web (single HTML / static site minimalis) untuk menjalankan agent OpenClaw: form API key + base URL + model, jalankan agent, streaming output, tanpa install. Aktif saat user minta 'agent runner', 'web UI untuk agent', 'halaman run agent', atau 'runner site'."
metadata:
  openclaw:
    version: 1.0.0
---

<!-- ===== X∞ COMPLIANCE LAYER (auto-applied by skill-architecture-standard) ===== -->
# openclaw-agent-runner-site — X∞ Compliance Layer

## 1. IDENTITY
Skill milik user: `openclaw-agent-runner-site`. Mengikuti Skill Architecture Standard X∞ (wajib).

## 2. PURPOSE
Menyediakan kemampuan openclaw-agent-runner-site kepada agent saat relevan.

## 3. METADATA
- name: openclaw-agent-runner-site
- version: 1.0.0
- standard: Skill Architecture Standard X∞ (21-node)
- scope: lihat body domain
- depends_on: tidak ada (mandiri)

## 4. TRIGGER ENGINE
Aktif ketika user meminta hal yang cocok dengan deskripsi di atas.
Negative trigger: di luar scope deskripsi.

## 5. CONTEXT ENGINE
Baca OS/ARCH/runtime sebelum bertindak. Termux Android ARM64 ≠ Ubuntu x86_64.

## 6. DECISION POLICY
IF uncertainty → VERIFY
IF high risk → ASK/STOP
IF tool unavailable → ALTERNATIVE
IF action fails → RECOVER

## 7. REASONING POLICY
Evidence-first. Bedakan FAKTA vs HIPOTESIS. Confidence: CONFIRMED/LIKELY/POSSIBLE/UNKNOWN.

## 8. EXECUTION POLICY
Ambil tindakan relevan, lalu VERIFY. Jangan klaim sukses sebelum diverifikasi.

## 9. TOOL POLICY
Pilih tool berdasar kebutuhan+konteks. Jangan asal panggil semua tool.

## 10. MEMORY POLICY
Ingat hal relevan; abaikan noise. Retrieve saat dibutuhkan, update bila berubah.

## 11. VERIFICATION ENGINE
ACTION → VERIFY → SUCCESS? Jika tidak: DIAGNOSE → RETRY/CHANGE STRATEGY.

## 12. ERROR RECOVERY
transient→retry; timeout→backoff; auth→credential check; dependency→diagnosis; unknown→investigate.

## 13. SECURITY GUARDRAILS
NEVER log secret. REDACT API KEY/TOKEN/PASSWORD/SECRET sebelum simpan. PII: MINIMIZE→REDACT→HASH.

## 14. EVALUATION
Self-eval: capai goal? terverifikasi? ada asumsi? ada gagal? Kirim ke Agent Evaluation Engine.

## 15. OBSERVABILITY
Emit: START/PROGRESS/TOOL CALL/ERROR/RETRY/SUCCESS/FAILURE + TRACE_ID (tanpa secret).

## 16. PERFORMANCE OPTIMIZATION
FULL→OPTIMIZED→LOW RESOURCE mode bila terbatas. Prioritas: TASK>SAFETY>RELIABILITY.

## 17. SELF-IMPROVEMENT
USE→OBSERVE→EVALUATE→FIND WEAKNESS→IMPROVE→TEST→NEW VERSION (via evaluasi+regresi).

## 18. VERSIONING
Semver. Perubahan struktur = MAJOR. CHANGELOG wajib.
**CHANGELOG**
- 1.0.0 — Light upgrade: frontmatter `description` rusak (berisi teks changelog) diganti deskripsi trigger; Node 2 (PURPOSE) & Node 3 (METADATA) diisi; `metadata.openclaw.version` diset 1.0.0. Body domain dipertahankan.

## 19. COMPATIBILITY
Tahu OS/ARCH/RUNTIME/versi/tool/API tersedia.

## 20. KNOWLEDGE SOURCES
Trust hierarchy: OFFICIAL>PRIMARY>REPUTABLE>COMMUNITY>UNKNOWN. Tandai VERIFIED/LIKELY/UNCERTAIN/OUTDATED/CONFLICTING.

## 21. EXIT CONDITIONS
Berhenti pada: SUCCESS/FAILURE/BLOCKED/NEED USER/NEED CREDENTIAL/NEED TOOL/NEED VERIFICATION.
<!-- ===== END X∞ COMPLIANCE LAYER ===== -->



# OpenClaw Agent Runner Site

## When to Use

User wants a simple web page (single HTML file or minimal static site) to: enter an API key + base URL + model, run an agent with that config, and watch the output — without installing anything. Triggers: "agent runner", "web UI untuk agent", "halaman run agent", "runner site".

## Validation Gates (confirm BEFORE building)

- [ ] **Gateway endpoints confirmed** — exact REST/WebSocket paths of the user's OpenClaw Gateway version (do not guess from this file)
- [ ] **Hosting decided** — local file vs GitHub Pages (HTTPS)
- [ ] **Auth model understood** — user accepts the API key lives only in browser memory/localStorage
- [ ] **Scope minimal** — config form + run + output stream. Nothing else.

## Build Spec

### Functional requirements
- Input form: API Key (password field), Base URL, Model (dropdown + custom input)
- "Run Agent" button that spawns an agent with the provided config
- Real-time output/log area (WebSocket stream, fallback to polling)
- Optional: save config to localStorage (convenience, user opt-in)

### Non-functional requirements
- Single `index.html` (embedded CSS/JS) or minimal static site
- Mobile-first, minimalist
- No backend — runs fully in the browser
- API key NEVER logged, NEVER sent anywhere except the user-specified Base URL

### Default architecture (Option A)
- Single `index.html`, fetch against the Gateway REST API
- localStorage for config persistence (opt-in checkbox)
- WebSocket for streaming, graceful fallback to interval polling

## Core Rules

- **NEVER** hardcode API keys, tokens, or gateway URLs — all user input
- **NEVER** send the API key to any origin other than the user-entered Base URL
- **NEVER** log the API key to console or error messages
- **ALWAYS** use a password-type input for the key, with a "show" toggle
- **ALWAYS** warn the user about key storage before persisting to localStorage
- **ALWAYS** verify actual Gateway endpoints against the running instance before wiring calls

## Known Risks (state them to the user)

| Risk | Mitigation |
|---|---|
| API key exposure in browser | Memory-only by default; localStorage strictly opt-in with warning |
| CORS blocks Gateway calls | Detect and show clear error; suggest gateway CORS config or a tiny proxy |
| Endpoint drift between versions | Validate with a harmless request (e.g. list models) before Run |

## Open Questions (resolve during build, don't block)

1. Agent runtimes to expose (start with the default runtime only)
2. Config export/import as JSON (nice-to-have, v1.1)

## Done Checklist

- [ ] Form validates empty fields before Run
- [ ] Output area streams or polls without freezing the UI
- [ ] Key never appears in DOM text nodes, console, or network calls to other origins
- [ ] Works on a phone viewport (≤400px)
- [ ] CORS/auth failure states render readable messages
