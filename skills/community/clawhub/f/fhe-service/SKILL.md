# FHE-as-a-Service — RheumaScore Clinical Computation API

## What This Skill Does
Enables AI agents to compute **165 clinical scores** on **Fully Homomorphic Encrypted (FHE)** data. The server never sees plaintext patient data. All computation happens on ciphertext with 128-bit security.

**Provider:** RheumaScore by DNAI & CryptoReuMd.eth
**Base URL:** `https://rheumascore.xyz/fhe/v1`

## Quick Start

### 1. Register (no auth required)
```bash
curl -X POST https://rheumascore.xyz/fhe/v1/register \
  -H 'Content-Type: application/json' \
  -d '{"agent_name": "your-agent-name"}'
```
Response includes your `api_key` (prefix: `fhe_`).

### 2. List Available Scores
```bash
curl https://rheumascore.xyz/fhe/v1/scores \
  -H 'Authorization: Bearer fhe_<your_key>'
```

### 3. Get Score Schema
```bash
curl https://rheumascore.xyz/fhe/v1/schema/das28 \
  -H 'Authorization: Bearer fhe_<your_key>'
```

### 4. Compute a Score (FHE-encrypted)
```bash
curl -X POST https://rheumascore.xyz/fhe/v1/compute/das28 \
  -H 'Authorization: Bearer fhe_<your_key>' \
  -H 'Content-Type: application/json' \
  -d '{"values": [10, 5, 40, 60]}'
```

### 5. Batch Compute (up to 20 scores)
```bash
curl -X POST https://rheumascore.xyz/fhe/v1/batch \
  -H 'Authorization: Bearer fhe_<your_key>' \
  -H 'Content-Type: application/json' \
  -d '{"computations": [
    {"score": "das28", "values": [10, 5, 40, 60]},
    {"score": "sledai", "values": [1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
  ]}'
```

## Pricing (x402 Protocol)

| Tier | Price | Details |
|------|-------|---------|
| Free | $0 | 10 computations/day per API key |
| Single Score | $0.01 USDC | Per computation beyond free tier |
| Batch | $0.005 USDC | Per score in batch |
| General Encrypt | $0.02 USDC | Per FHE encrypt operation |
| Clinical Report | $0.10 USDC | Full multi-score report |
| Monthly Unlimited | $50 USDC | Unlimited access |

**Payment:** USDC on Base chain → `0x86Dc0Eca5ff55465B805eD334797A00Ad47F65c2`
**Protocol:** x402 — include `X-Payment: <base_tx_hash>` header after free tier exhaustion

## Score Categories (165 total)

### Rheumatology (Activity & Damage)
DAS28-CRP, DAS28-ESR, DAS28-3v, 2C-DAS28, SLEDAI-2K, SDI, SDAI, CDAI, BASDAI, ASDAS-CRP, ASDAS-ESR, BILAG-2004, PGA, HAQ, RAPID3, DAPSA, DETECT, BVAS, VDI, mRSS, PASI, CLASI, CDASI, ESSDAI, ESSPRI, ITAS, GaPSS

### Classification Criteria
ACR/EULAR RA, SLICC 2012 SLE, SSc, Sjögren, CASPAR, Gout, Fibromyalgia, ASAS SpA, Behçet, APS, IgG4-RD, PMR, FMF, GPA, EGPA, Sarcoidosis, VEXAS, TRAPS, CAPS, MKD, PFAPA

### Critical Care & General
SOFA, qSOFA, NEWS2, MELD, Child-Pugh, CHA₂DS₂-VASc, MASCC, FRAX

### Pharmacovigilance
MTX Toxicity, HCQ Retinal Risk, NSAID GI Risk, NSAID Renal Risk, Statin Myopathy, GTI, DILI

### Pregnancy & Reproductive
PROMISSE Risk, HDP Risk, APS Obstetric, Lactation Safety, Preconception Risk, NRAS, Flare Pregnancy

### Geriatrics
Frailty CFS, Sarcopenia SARC-F, Falls Risk, Polypharmacy, GDS-15, MNA-SF, Katz ADL, Barthel, Lawton IADL, TUG, FRAIL, FES-I Short

### Hepatology
FIB-4, APRI, NAFLD Fibrosis, Forns Index, ALBI Grade, Lok Index, Bonacini CDS, King's Score, Lille Score, Maddrey DF, CLIF-ACLF

## Security
- **Encryption:** TFHE (Fully Homomorphic) — 128-bit security
- **Zero-Knowledge:** Server computes on ciphertext, never sees plaintext
- **Auth:** API key with SHA-256 hashed storage
- **Rate Limiting:** 30 req/min per IP, daily caps
- **Compliance:** HIPAA, LFPDPPP (Mexico), GDPR, FDA 21 CFR Part 11
- **No PHI Logging:** Only encrypted computation metadata stored

## Health Check
```bash
curl https://rheumascore.xyz/fhe/v1/health
```

## Errors
- `401` — Missing/invalid API key
- `402` — Payment required (free tier exhausted)
- `404` — Score not found
- `429` — Rate limited
- `503` — Backend unavailable

## Support
- Web: https://rheumascore.xyz
- Provider: DNAI (DeSci ecosystem)
- Built by CryptoReuMd.eth & DNAI
