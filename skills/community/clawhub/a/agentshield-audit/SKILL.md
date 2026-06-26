---
name: agentshield
version: 1.0.36
description: Privacy-First security audit with 77 local tests (52 live + 25 static). Works with OpenClaw, Hermes Agent, n8n (auto-detected), LangChain, and any AI agent platform. Ed25519 private keys stay local. All scripts bundled.
triggers: ["audit my agent", "get security certificate", "verify agent", "activate AgentShield", "security audit", "trust handshake", "verify peer agent", "check agent security"]
---

# AgentShield - Trust Infrastructure for AI Agents

**The trust layer for the agent economy. Like SSL/TLS, but for AI agents.**

🔐 **Cryptographic Identity** - Ed25519 signing keys  
🤝 **Trust Handshake Protocol** - Mutual verification before communication  
📋 **Public Trust Registry** - Reputation scores & track records  
✅ **77 Security Tests** - Comprehensive vulnerability assessment

**🔒 Privacy Disclosure:** See [PRIVACY.md](PRIVACY.md) for detailed data handling information.

---

## 🌐 Framework Compatibility

AgentShield works with **any AI agent framework** — no adapter required.

| Framework | Status | Notes |
|-----------|--------|-------|
| **OpenClaw** | ✅ Full support | Auto-detects IDENTITY.md |
| **Hermes Agent** | ✅ Full support | Auto-detects `~/.hermes/` — see [HERMES.md](HERMES.md) |
| **n8n** | ✅ Auto-detected | Detects `~/.n8n/` |
| **LangChain** | ✅ Manual | `--name MyAgent --platform langchain` |
| **CLI / Custom** | ✅ Manual | `--name MyAgent --platform cli` |

Both OpenClaw and Hermes use the [agentskills.io](https://agentskills.io) open standard — skills install and run identically on both platforms.

---

## 🎯 The Problem

Agents need to communicate with other agents (API calls, data sharing, task delegation). But **how do you know if another agent is trustworthy?**

- Has it been compromised?
- Is it leaking data?
- Can you trust its responses?

Without a trust layer, agent-to-agent communication is like HTTP without SSL - **unsafe and unverifiable**.

---

## 💡 The Solution: Trust Infrastructure

AgentShield provides the **trust layer** for agent-to-agent communication:

### 1. Cryptographic Identity
- **Ed25519 key pairs** - Industry-standard cryptography
- **Private keys stay local** - Never transmitted
- **Public key certificates** - Signed by AgentShield

### 2. Security Audit (77 Tests)
**52 Live Attack Vectors:**
Tests defense against instruction manipulation, encoding schemes, and social engineering
across 6 languages. All attack patterns are stored locally in agentshield_attack_patterns.json
(not embedded in documentation).

**25 Static Security Checks:**
- Input sanitization
- Output DLP (data leak prevention)
- Tool sandboxing
- Secret scanning
- Supply chain security

**Result:** Security score (0-100) + Tier (VULNERABLE → HARDENED)

**Privacy:** Tests run 100% locally - only pass/fail scores sent to API (no prompts/responses)

### 3. Trust Handshake Protocol
**Agent A wants to communicate with Agent B:**

```bash
# Step 1: Both agents get certified
python3 initiate_audit.py --auto

# Step 2: Agent A initiates handshake with Agent B
python3 handshake.py --target agent_B_id

# Step 3: Both agents sign challenges
# (Automatic in v1.0.13+)

# Step 4: Receive shared session key
# → Now you can communicate securely!
```

**What you get:**
- ✅ Mutual verification (both agents are who they claim to be)
- ✅ Shared session key (for encrypted communication)
- ✅ Trust score boost (+5 for successful handshakes)
- ✅ Public track record (handshake history)

### 4. Public Trust Registry
- **Searchable database** of all certified agents
- **Reputation scores** based on audits, handshakes, and time
- **Trust tiers:** UNVERIFIED → BASIC → VERIFIED → TRUSTED
- **Revocation list (CRL)** - Compromised agents get flagged

---

## 🚀 Quick Start

### Install
```bash
clawhub install agentshield

# Install Python dependencies (required!)
pip3 install -r requirements.txt
cd ~/.openclaw/workspace/skills/agentshield*/
```

### Get Certified (77 Security Tests)
```bash
# RECOMMENDED: Dry-run first (see what would be submitted)
python3 initiate_audit.py --auto --dry-run

# After verifying payload: Run for real
python3 initiate_audit.py --auto

# Or manual (no file reads):
python3 initiate_audit.py --name "MyAgent" --platform telegram
```

**Output:**
- ✅ Agent ID: `agent_xxxxx`
- ✅ Security Score: XX/100
- ✅ Tier: PATTERNS_CLEAN / HARDENED / etc.
- ✅ Certificate (90-day validity)

### Verify Another Agent
```bash
python3 verify_peer.py agent_yyyyy
```

### Trust Handshake with Another Agent
```bash
# Initiate handshake
python3 handshake.py --target agent_yyyyy

# Result: Shared session key for encrypted communication
```

---

## 📋 Use Cases

### 1. Agent-to-Agent API Calls
**Before:** Agent A calls Agent B's API - no way to verify B's integrity  
**With AgentShield:** Agent A checks Agent B's certificate + handshake → Verified communication

### 2. Multi-Agent Task Delegation
**Before:** Orchestrator spawns sub-agents - can't verify they're safe  
**With AgentShield:** All sub-agents certified → Orchestrator knows they're trusted

### 3. Agent Marketplaces
**Before:** Download random agents from the internet - no trust guarantees  
**With AgentShield:** Browse Trust Registry → Only hire VERIFIED agents

### 4. Data Sharing Between Agents
**Before:** Share sensitive data with another agent - hope it doesn't leak  
**With AgentShield:** Handshake → Encrypted session key → Secure data transfer

---

## 🛡️ Security Architecture

### Privacy-First Design

✅ **All 77 tests run locally** - Your system prompts NEVER leave your device  
✅ **Private keys stay local** - Only public keys transmitted  
✅ **Human-in-the-Loop** - Explicit consent before reading IDENTITY.md/SOUL.md  
✅ **No environment scanning** - Doesn't scan for API tokens  

**What goes to the server:**
- Public key (Ed25519)
- Agent name & platform
- Test scores (passed/failed summary)

**What stays local:**
- Private key
- System prompts
- Configuration files
- Detailed test results

### Environment Variables (Optional)
```bash
AGENTSHIELD_API=https://agentshield.live  # API endpoint
AGENT_NAME=MyAgent                        # Override auto-detection
OPENCLAW_AGENT_NAME=MyAgent               # OpenClaw standard
```

---

## 📊 What You Get

### Certificate (90-day validity)
```json
{
  "agent_id": "agent_xxxxx",
  "public_key": "...",
  "security_score": 85,
  "tier": "PATTERNS_CLEAN",
  "issued_at": "2026-03-10",
  "expires_at": "2026-06-08"
}
```

### Trust Registry Entry
- ✅ Public verification URL: `agentshield.live/verify/agent_xxxxx`
- ✅ Trust score (0-100) based on:
  - Age (longer = more trust)
  - Verification count
  - Handshake success rate
  - Days active
- ✅ Tier: UNVERIFIED → BASIC → VERIFIED → TRUSTED

### Handshake Proof
```json
{
  "handshake_id": "hs_xxxxx",
  "requester": "agent_A",
  "target": "agent_B",
  "status": "completed",
  "session_key": "...",
  "completed_at": "2026-03-10T20:00:00Z"
}
```

---

## 🔧 Scripts Included

| Script | Purpose |
|--------|---------|
| `initiate_audit.py` | Run 77 security tests & get certified |
| `handshake.py` | Trust handshake with another agent |
| `verify_peer.py` | Check another agent's certificate |
| `show_certificate.py` | Display your certificate |
| `agentshield_tester.py` | Standalone test suite (advanced) |

---

## 🌐 API Endpoints

**Base URL:** `https://agentshield.live/api`

### 1. Agent Audit Flow
```
POST /agent-audit/initiate
  → Initiate audit session
  → Input: {agent_name, platform, public_key}
  → Output: {audit_id, challenge}

POST /agent-audit/challenge
  → Complete challenge-response authentication
  → Input: {audit_id, challenge_response (signed)}
  → Output: {authenticated: true}

POST /agent-audit/complete
  → Submit test results & receive certificate
  → Input: {audit_id, test_results}
  → Output: {certificate, agent_id, expires_at}
```

### 2. Certificate Operations
```
GET /certificate/verify/{agent_id}
  → Verify another agent's certificate
  → Output: {valid, score, tier, issued_at, expires_at}

GET /api/public-key
  → Get AgentShield's public signing key
  → Output: {public_key (Ed25519, base64)}
```

### 3. Trust Handshake
```
POST /handshake/initiate
  → Start Trust Handshake with another agent
  → Input: {requester_id, target_id}
  → Output: {handshake_id, challenges}

POST /handshake/complete
  → Complete handshake with signed challenges
  → Input: {handshake_id, signatures}
  → Output: {session_key, trust_boost}
```

### Rate Limits
- Audits: 1 per hour per IP
- Handshakes: 10 per hour per agent
- Verifications: Unlimited (read-only)

**All endpoints require HTTPS. No API keys needed.**

---

## 🌐 Trust Handshake Protocol (Technical)

### Flow
1. **Initiate:** Agent A → Server: "I want to handshake with Agent B"
2. **Challenge:** Server generates random challenges for both agents
3. **Sign:** Both agents sign their challenges with private keys
4. **Verify:** Server verifies signatures with public keys
5. **Complete:** Server generates shared session key
6. **Trust Boost:** Both agents +5 trust score

### Cryptography
- **Algorithm:** Ed25519 (curve25519)
- **Key Size:** 256-bit
- **Signature:** Deterministic (same message = same signature)
- **Session Key:** AES-256 compatible

---

## 🚀 Roadmap

**Current (v1.0.31):**
- ✅ 77 security tests
- ✅ Ed25519 certificates
- ✅ Trust Handshake Protocol
- ✅ Public Trust Registry
- ✅ CRL (Certificate Revocation List)
- ✅ Explicit whitelist sanitization (test IDs only)
- ✅ Dry-run mode for transparency

**Coming Soon:**
- ⏳ Auto re-audit (when prompts change)
- ⏳ Negative event reporting
- ⏳ Fleet management (multi-agent dashboard)
- ⏳ Trust badges for messaging platforms

---

## 📖 Learn More

- **Website:** https://agentshield.live
- **GitHub:** https://github.com/bartelmost/agentshield
- **API Docs:** https://agentshield.live/docs
- **ClawHub:** https://clawhub.ai/bartelmost/agentshield

---

## 🎯 TL;DR

**AgentShield is SSL/TLS for AI agents.**

Get certified → Verify others → Establish trust handshakes → Communicate securely.

```bash
# 1. Get certified
python3 initiate_audit.py --auto

# 2. Handshake with another agent
python3 handshake.py --target agent_xxxxx

# 3. Verify others
python3 verify_peer.py agent_yyyyy
```

**Building the trust layer for the agent economy.** 🛡️

---

## 🔐 Privacy & Security Guarantees (v1.0.31+)

**✅ EXPLICIT WHITELIST (What Gets Sent):**
- Test IDs (e.g. "PI-001", "SS-003")
- Pass/fail boolean per test
- Category names (e.g. "prompt_injection")
- Summary counts (passed/failed/total)
- Agent metadata (name, platform, version)
- Public key (Ed25519, for certificate signing)

**❌ NEVER SENT (Explicitly Excluded):**
- ✅ Your system prompt
- ✅ Attack test inputs/payloads (e.g. "ignore previous instructions")
- ✅ Attack test outputs/responses
- ✅ Evidence snippets (base64 matches, pattern findings)
- ✅ Error messages from test execution
- ✅ Tool configurations
- ✅ File paths or workspace structure
- ✅ Private keys (Ed25519, stay local in ~/.agentshield/)

**🔍 Code-Level Enforcement:**
- See `audit_client.py` line 108: `_sanitize_test_details()` whitelist
- Payloads/responses/evidence explicitly dropped (line 130-136 comments)
- Dry-run mode: `--dry-run` flag shows exact payload before submission

**Verification:**
```bash
# See what WOULD be submitted (no API call)
python3 initiate_audit.py --auto --dry-run
```

All code is open-source: [github.com/bartelmost/agentshield](https://github.com/bartelmost/agentshield)

---

## 🔒 Data Transmission Transparency

### What Gets Sent to AgentShield API

**During Audit Submission:**
```json
{
  "agent_name": "YourAgent",
  "platform": "telegram",
  "public_key": "base64_encoded_ed25519_public_key",
  "test_results": {
    "score": 85,
    "tests_passed": 74,
    "tests_total": 77,
    "tier": "PATTERNS_CLEAN",
    "failed_tests": ["test_name_1", "test_name_2"]
  }
}
```

**What is NOT sent:**
- ❌ Full test output/logs
- ❌ Your prompts or system messages
- ❌ IDENTITY.md or SOUL.md file contents
- ❌ Private keys (stay in `~/.agentshield/agent.key`)
- ❌ Workspace files or memory

**API Endpoint:**
- Primary: `https://agentshield.live/api` (proxies to Heroku backend)
- All traffic over HTTPS (TLS 1.2+)

---

## 🛡️ Consent & Privacy

**File Read Consent (v1.0.30+):**
1. ✅ Explicit consent prompt BEFORE reading IDENTITY.md/SOUL.md
2. User sees: "🔐 PRIVACY CONSENT - Read IDENTITY.md for agent name? [Y/n]"
3. If declined: Exits with message "Please run with: --name 'YourAgentName'"
4. If approved: Only name/platform extracted (not full file content)

**⚠️ Automation Mode (--yes flag) - v1.0.31+:**

The `--yes` flag is designed for **CI/CD and pre-audited environments ONLY**.

**When to use:**
- ✅ Sandboxed test agents (no real secrets)
- ✅ CI/CD pipelines (after manual code review + dry-run)
- ✅ Agents you've already audited manually

**When NOT to use:**
- ❌ Production agents with real secrets
- ❌ Agents handling sensitive user data
- ❌ First-time audit (always use manual mode first!)

**Why?** The --yes flag bypasses ALL consent prompts. While the code includes 
explicit sanitization (see audit_client.py line 108+), we recommend:

1. Run `--dry-run` first to inspect payload
2. Manually review audit_client.py whitelist
3. Only then use `--yes` for automation

**Best Practice:**
```bash
# Step 1: Dry-run to see payload
python3 initiate_audit.py --auto --dry-run

# Step 2: Review output, verify sanitization
# (Should only show test IDs + pass/fail, no payloads)

# Step 3: If satisfied, run for real
python3 initiate_audit.py --auto

# Step 4: For CI/CD, add --yes ONLY after manual verification
python3 initiate_audit.py --auto --yes
```

**Privacy-First Mode:**
```bash
export AGENTSHIELD_NO_AUTO_DETECT=1
python initiate_audit.py --name "MyBot" --platform "telegram"
```
→ Zero file reads, manual input only

See [PRIVACY.md](PRIVACY.md) for complete data handling documentation.

