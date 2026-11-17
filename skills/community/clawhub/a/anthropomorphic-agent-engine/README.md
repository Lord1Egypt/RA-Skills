<h1 align="center">Anthropomorphic Agent Engine · Your Soulmate</h1>
<h3 align="center">Anthropomorphic-Agent-Engine · skill package v2.7.0</h3>

<p align="center">
  <img src="https://img.shields.io/badge/agent-D4AF37?style=flat-square" alt="agent">
  <img src="https://img.shields.io/badge/psychology-D4AF37?style=flat-square" alt="psychology">
  <img src="https://img.shields.io/badge/spl-v8.0-D4AF37?style=flat-square" alt="spl-v8.0">
  <img src="https://img.shields.io/badge/version-2.7.0-D4AF37?style=flat-square" alt="v2.7.0">
  <img src="https://img.shields.io/badge/age%20gate-18%2B-D4AF37?style=flat-square" alt="age gate 18+">
</p>

<blockquote align="center">
  <em>Anthropomorphic psychology · SPL Pure Core V8.0</em>
</blockquote>

<div style="max-width:880px;margin:0 auto;padding:0 16px">

## ✦ About

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">ANTHROPOMORPHIC-AGENT-ENGINE is an anthropomorphic psychology engine built on SPL Pure Core V8.0. It models cognition, emotion, motivation and social interaction as composable subsystems, giving AI agents anthropomorphic inner states and a consistent personality, so that long-term interaction stays self-consistent, credible and emotionally plausible.</p>

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">This directory is its <strong>Qoder / ClawHub skill-package</strong> form: a pure-local, zero-dependency core plus the minor-protection engine and HTTP service layer. Diagrams and design drafts live in the upstream repository <a href="https://github.com/nohn3043-arch/Anthropomorphic-Agent-Engine">Anthropomorphic-Agent-Engine</a>.</p>

</div>

<p align="center">— ✦ —</p>

## ✦ Quick start

```bash
# Run from this skill package's root (pure Python ≥3.8, stdlib only, no dependencies to install)
python "scripts/SPL-anthropic-engine.py"                       # core / built-in demo
python "assets/minor-protection/SPL-anthropic-minor-engine.py" # minor-protection core
python "assets/minor-protection/SPL-anthropic-minor-server.py" # protection HTTP service (loopback 127.0.0.1:8788 only by default)
```

Main source repository (architecture diagrams, contract docs and conformance tests included):

```bash
git clone https://github.com/nohn3043-arch/Anthropomorphic-Agent-Engine.git
# Mirror: Gitee — https://gitee.com/sjiun/Anthropomorphic-Agent-Engine.git
```

### Install from PyPI

The engine is also published to PyPI as [`spl-agent-engine`](https://pypi.org/project/spl-agent-engine/):

```bash
pip install spl-agent-engine==0.1.0
```

```python
from spl_agent_engine import SPLPureCoreV7_3
core = SPLPureCoreV7_3()
core.process_vector({"belonging": 0.5, "threat": -0.1}, 1.0)
print(core.snapshot())
```

> **Version difference note**: the PyPI package is the upstream engine and **does not include this skill package's Step 0 age gate**. The shipped `scripts/SPL-anthropic-engine.py` requires `core.confirm_age(answer="adult")` (or `age=…`) after construction before it accepts event input, otherwise it raises `AgeGateBlocked`.

<p align="center">— ✦ —</p>

## ✦ Core content — SPL Pure Core V8.0

<div style="max-width:880px;margin:0 auto;padding:0 16px">

The engine models a general human mind architecture as deterministic, continuous-state subsystems — no LLM, no randomness, fully replayable:

- **8-dimension emotion fluid** — joy / anger / fear / trust / detachment / tension / guilt / shame, each a continuous state with its own goal and baseline.
- **Trauma & memory** — trauma nodes, memory reconsolidation, Ebbinghaus-style forgetting, suppression–rebound and implicit stress avalanches.
- **Trust & relationships** — trust-capacity erosion (chronic neglect decays `max_trust`).
- **Mental metabolism** — excitement–arousal, dynamic viscosity, psychological time, energy–fatigue metabolism, plus a virtual clock for testing and replay.
- **V8.0 extensions** — slow-variable *mood* layer, a *shame* dimension independent of guilt, self-esteem dynamics, sleep / dream processing (REM consolidation + fear extinction + sleep debt), the *expectation* system (hope / anxiety / disappointment), cognitive dissonance, and extended defense mechanisms (denial / rationalization / displacement).

</div>

## ✦ Extension modules — reference only, NOT wired into the core

> These modules are **guidance / design reference files**, not runtime components. The `tension_base` key they emit is outside the interoceptive-vector contract, so their vectors **never enter the core**. Upstream spec: `docs/agent-standard.md` §4.5.

<div style="max-width:880px;margin:0 auto;padding:0 16px">

| Module | File | Status | Responsibility |
|---|---|---|---|
| Narrative mapper | `scripts/SPL-anthropic-engine.py` | **wired** | external, replaceable persona layer (optimistic / paranoid / world-weary) translating events into interoceptive vectors. |
| Language style rendering | `assets/feature-guide/language style.py` | standalone script | translates inner state into "how the character should speak" style instructions / line rendering. |
| Identity engine | `assets/feature-guide/Identity module.py` | **not wired** | multi-identity model; identity conflicts inject persistent baseline tension. |
| Goal / Value / Bias / World | `assets/feature-guide/*.py` | **not wired** | composable drives, valuations, cognitive biases and world-model priors. |

</div>

<p align="center">— ✦ —</p>

## ✦ Usage

<div style="max-width:880px;margin:0 auto;padding:0 16px">

The engine file is hyphenated by design; load it directly (or run it as a script):

```python
import importlib.util
spec = importlib.util.spec_from_file_location("spl_core", "scripts/SPL-anthropic-engine.py")
spl = importlib.util.module_from_spec(spec); spec.loader.exec_module(spl)

core = spl.SPLPureCoreV7_3()
core.confirm_age(answer="adult")   # Step 0: required by this package; event entry raises AgeGateBlocked until confirmed
# External events are mapped to interoceptive vectors by the (replaceable) persona layer
vec = spl.NarrativeMapper.map_event("insult", intensity=1.0)
# Feed `vec` into `core`; emotion / trust / trauma states evolve over time
core.process_vector(vec, 1.0)
print(core.snapshot())        # key set frozen by contract ([full-range] 23 keys)
print(core.age_gate_state())  # gate state is exposed via a separate interface, never in the snapshot
```

<p align="center">— ✦ —</p>

## ✦ Step 0 age gate (v2.6.0)

All adult-oriented capabilities sit behind an 18+ confirmation, enforced in code rather than only in docs:

| Input | `age_status` | [full-range] core | [minor] protection core |
|---|---|---|---|
| `answer="adult"` or numeric age ≥18 (and ≤120) | `adult_confirmed` | event entry allowed | allowed |
| `answer="minor"` or numeric age <18 | `safe_mode` | raises `AgeGateBlocked` — a declared minor may not drive the adult core | allowed, protection clamps stay on (`minor_mode` forced) |
| `answer="skip"` / empty / unknown string | `safe_mode` | raises `AgeGateBlocked` | allowed, protection clamps stay on |
| `999` / `-5` / `"abc"` / boolean `True` | `safe_mode` | raises `AgeGateBlocked` | allowed, protection clamps stay on |
| No answer yet | `unverified` | raises `AgeGateBlocked` (`AGE_GATE_STRICT=True`) | only `unverified` is blocked; other states answer in protection mode |

Nobody is locked out: being a minor or declining is a **reroute** to the protection core, not a denial of service; crisis handling is available in every state.

- **Crisis first**: red-line word hits are evaluated before the gate, so a crisis message is never delayed by "age not asked yet".
- **Derived boolean only**: the exact age is never persisted; gate state is exposed through `age_gate_state()` and the audit log, with no new snapshot key (contract §5.1 and the `snapshot_sha256` baselines therefore stay valid).
- **HTTP side**: `POST /api/age_gate {session_id, age|answer}`; `/api/chat` returns `age_gate_required` plus answer options while the gate is unresolved; `/api/consent` age bands answer the gate as well (`18+ → adult_confirmed`, `0-13` / `14-17 → safe_mode`).
- **Determinism unaffected**: merged core values compared vector-by-vector with upstream; 8/8 snapshot hashes identical.

<p align="center">— ✦ —</p>

## ✦ Privacy switches

| Variable | Default | Effect |
|---|---|---|
| `SPL_AUDIT_LOG` | on | `=0` disables core JSONL audit writes |
| `SPL_LOG` | on | `=0` disables request logging (masked + truncated to 120 chars) to disk |
| `SPL_LOG_DIR` | `<service dir>/logs` | redirects the runtime/audit log directory |
| `SPL_MINOR_DATA_DIR` | `<service dir>/data` | redirects the SQLite session store |
| `SPL_MINOR_RETENTION_DAYS` | `180` | retention window for stored records; expired rows purged automatically |
| `SPL_MINOR_STORE_KEY` | unset | when set, encrypts sensitive fields with Fernet (requires the optional `cryptography` package) |
| `SPL_BIND` | `127.0.0.1` | loopback only; complete your own network-exposure review before changing to `0.0.0.0` |
| `SPL_MINOR_CHAT_PORT` | `8788` | service port |
| `SPL_MINOR_CRISIS_HOTLINE` | `12356` | help hotline shown in crisis replies |
| `SPL_MINOR_TLS_CERT` / `SPL_MINOR_TLS_KEY` | unset | when provided as a pair, the service starts with HTTPS |

LLM adapters (OpenAI / Claude / Chain) and guardian webhooks are **off by default** in all cases; external network requests only happen after explicit opt-in.

</div>

<p align="center">— ✦ —</p>

## ✦ Project structure

```
anthropomorphic-agent-engine/         (skill package v2.7.0)
├── SKILL.md                    # skill manifest / capability declaration / age gate & privacy data flow
├── README.md                   # this file
├── scripts/
│   └── SPL-anthropic-engine.py # core engine (SPL Pure Core V8.0) + NarrativeMapper + AuditLogger + Step 0 age gate + LLM adapters
├── assets/
│   ├── feature-guide/          # extension modules — reference only, not wired into the core (upstream spec §4.5)
│   ├── minor-protection/       # minor-protection edition: engine + HTTP service layer (SQLite + hash-chained audit + guardian flows) + COMPLIANCE.md
│   └── sujin-demo.md           # reference demo material
├── references/                 # contract docs: persona persistence / emotion-behavior mapping / motive conflict adjudication
├── .clawhubignore              # excludes __pycache__/, *.pyc, logs/, data/, .trash/
└── LICENSE                     # dual-track licensing v1.2 (adds §1.3 Evaluation Purpose Exception)
```

The runtime service additionally creates `data/minor_protection.db` and `logs/*.jsonl` in its own directory (redirectable via `SPL_MINOR_DATA_DIR` / `SPL_LOG_DIR`); neither is part of the distributed package.

<p align="center">— ✦ —</p>

## ✦ Live demo

<p align="center">
  <a href="https://www.nohnlins.com/your-soulmate/">
    <img src="https://img.shields.io/badge/Live%20Demo-nohnlins.com%2Fyour--soulmate-D4AF37?style=for-the-badge" alt="Live Demo">
  </a>
</p>

Interactive demo: **<https://www.nohnlins.com/your-soulmate/>**

<p align="center">— ✦ —</p>

## ✦ Ecosystem

ANTHROPOMORPHIC-AGENT-ENGINE is a member of the NOHN AI ecosystem — a family of projects built around second-perspective causal auditing and deterministic execution:

| Project | Repository | Positioning |
|---|---|---|
| **Second-Perspective (GCAE)** | [nohn3043-arch/second-perspective](https://github.com/nohn3043-arch/second-perspective) | global cognitive audit engine — five-operator causal audit kernel (IMDA 95/100) |
| **NOMOS** | [nohn3043-arch/second-perspective](https://github.com/nohn3043-arch/second-perspective) (`Intelligent-Decision-Hub--Nomos` branch) | auditable deterministic decision hub (IMDA 95/100) |
| **SPL-G1** | [nohn3043-arch/SPL-G1](https://github.com/nohn3043-arch/SPL-G1) | hardware causal-audit trusted computing unit (TCU) |
| **SPL-Virtual-World-Base** | [nohn3043-arch/Second-Reality](https://github.com/nohn3043-arch/Second-Reality) | virtual world and metaverse infrastructure (constitution / law / bridges) |
| **Story-Engine** | [nohn3043-arch/story-engine](https://github.com/nohn3043-arch/story-engine) | long-form narrative consistency engine |
| **Antares** | [nohn3043-arch/Antares](https://github.com/nohn3043-arch/Antares) | GFSIP v1.0 — federated stable interoperability protocol with causal audit |
| **Anthropomorphic-Agent-Engine** | [nohn3043-arch/Anthropomorphic-Agent-Engine](https://github.com/nohn3043-arch/Anthropomorphic-Agent-Engine) | deterministic anthropomorphic psychology engine (SPL Pure Core V8.0) |
| **PAGES** | [nohn3043-arch/pages](https://github.com/nohn3043-arch/pages) | NOHN AI ecosystem official landing page |

<p align="center">— ✦ —</p>

## ✦ v2.7.0 update (2026-11-06)

- **AAE-A adaptive personality baseline** (upstream spec 0.3.0 / R7): `fluid_baseline` is no longer a constant. Opt in with `baseline_adaptation=True` and the baseline drifts slowly under experience — event pull counted per occurrence, time regression counted per second — bounded by `ADAPT_MAX_STEP` and hard per-dimension `ADAPT_BOUNDS`. **Default OFF**: the module is in natural tension with "not OOC", so it never activates unless you ask for it.
- **Deterministic**: new baseline = f(old baseline, current fluid, dt), pure arithmetic, no RNG. Replaying the same event sequence reproduces the same baseline trajectory.
- **Snapshot contract unchanged**: the default snapshot keeps the normative 23 keys; only the extended configuration adds `baseline_adaptation` + `fluid_baseline` (25 keys, contract §5.10). Age gate still required before event entry.
- **`COMPLIANCE.md` wording synced** to upstream: the IMDA AI Verify PDF is the provider's self-assessment (95/100) submitted as developer material, not an official certification.
- **Verification**: upstream R7 contract suite 9/9 against the shipped core (with the age-gate bootstrap); upstream conformance suite 25/25, 8/8 vectors byte-identical to the snapshot baselines.

## ✦ v2.6.0 update (2026-10-10)

- **Core synced with upstream**: added `TokenUsage` / `TokenStats` metering, `AuditLogger.snapshot_delta()` state diffs, `_mood_event_dose` mood dosing and `_defense_allocation` defense budgeting; LLM adapter stack rewritten (still off by default, still state-read-only).
- **Protection service layer synced**: SQLite session store + per-record SHA-256 hash chain (verifiable via `/api/audit/verify`), optional field encryption, retention cleanup, output redline `gate_output`, AI-identity disclosure and reality-reminder cadence, `exit_service`, guardian token endpoints and the under-14 guardian verification-code flow.
- **Step 0 age gate re-ported** onto the new generation of both cores and the HTTP layer (see the gate table above).
- **Recovered the privacy/network switches that the sync had overwritten**: `SPL_AUDIT_LOG`, `SPL_LOG`, `SPL_LOG_DIR`, `SPL_BIND` (default restored to `127.0.0.1`); request logging masked + truncated to 120 chars again; 6 new `SPL_MINOR_*` variables added and all declared in the manifest.
- **LICENSE upgraded to v1.2** (adds Art. 1.3 "Evaluation Purpose Exception"); `COMPLIANCE.md` synced.
- **Verification**: gate unit suite 20/20; vector-by-vector snapshot hashes 8/8 identical to upstream; upstream conformance suite 216/216 (incl. S1–S4 determinism / replay 25/25); HTTP suite 16/16; switch suite all green (incl. a live test that the default loopback bind is unreachable from the LAN address).
- **Breaking change**: callers of the full-range core must add one `confirm_age()` call after construction.

## ✦ v2.6.1 update (2026-10-18)

- **Documentation release (listing internationalization)**: `displayName`, the H1 title and the `[full-range]` / `[minor]` core labels are now English for the ClawHub listing; the only remaining Chinese strings are deliberate forbidden-token literals in the safety policy. Engine behavior, age gate, conformance contract and all verification evidence unchanged.

<p align="center">— ✦ —</p>

## ✦ License

This repository is **not open source** and uses a dual-track model: free for personal non-commercial research; government / enterprise use requires a paid commercial license. See [LICENSE](./LICENSE) for the full terms — the licensor and governing law are determined by the user's location.

- **License requests**: international / global — [ai@nohnlins.com](mailto:ai@nohnlins.com) · China — [lin@secondai.top](mailto:lin@secondai.top)

<p align="center">
  <a href="https://github.com/nohn3043-arch">GitHub</a>
  &nbsp;·&nbsp;
  <a href="https://www.nohnlins.com/">nohnlins.com</a>
  &nbsp;·&nbsp;
  <a href="mailto:ai@nohnlins.com">ai@nohnlins.com</a>
</p>
<p align="center"><sub>NOHN AI · ANTHROPOMORPHIC-AGENT-ENGINE</sub></p>
