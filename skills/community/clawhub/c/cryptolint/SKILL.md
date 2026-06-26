---
name: CryptoLint
version: 1.0.0
description: "Cryptography misuse & weak algorithm detector -- detects deprecated algorithms, hardcoded keys/IVs, ECB mode, weak random number generation, timing-vulnerable comparisons, and insecure TLS configuration"
homepage: https://cryptolint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udd10",
      "primaryEnv": "CRYPTOLINT_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash", "python3", "jq"]
      },
      "configPaths": ["~/.openclaw/openclaw.json"],
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# CryptoLint -- Cryptography Misuse & Weak Algorithm Detector

CryptoLint scans codebases for cryptographic anti-patterns, deprecated algorithms (MD5, SHA-1, DES, RC4), hardcoded keys and IVs, insecure encryption modes (ECB), weak random number generation, timing-vulnerable comparisons, and insecure TLS/SSL configuration. It uses regex-based pattern matching against 90 cryptography-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `cryptolint scan [file|directory]`
One-shot cryptography quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 cryptography patterns against each file (free tier limit)
4. Calculates a crypto quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if crypto quality is poor
8. Free tier limited to first 30 patterns (WA + KM categories)

**Example usage scenarios:**
- "Scan my code for crypto issues" -> runs `cryptolint scan .`
- "Check this file for weak algorithms" -> runs `cryptolint scan src/crypto.ts`
- "Find hardcoded encryption keys" -> runs `cryptolint scan src/`
- "Audit cryptography usage in my project" -> runs `cryptolint scan .`
- "Check for MD5 or SHA1 usage" -> runs `cryptolint scan .`

### Pro Tier ($19/user/month -- requires CRYPTOLINT_LICENSE_KEY)

#### `cryptolint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering weak algorithms, key management, encryption modes, and random number generation.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 cryptography patterns (WA, KM, EM, RN categories)
3. Detects insecure encryption modes (ECB, CBC without auth)
4. Identifies weak random number generation for crypto
5. Full category breakdown reporting

#### `cryptolint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `cryptolint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `cryptolint scan --category WA [directory]`
Filter scan to a specific check category (WA, KM, EM, RN, TC, CP).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category WA
```

### Team Tier ($39/user/month -- requires CRYPTOLINT_LICENSE_KEY with team tier)

#### `cryptolint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including timing attacks and certificate/protocol checks.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes timing & comparison checks (timing side-channels, non-constant-time comparison)
4. Includes certificate & protocol checks (TLS verification disabled, insecure protocols)
5. Full category breakdown with per-file results

#### `cryptolint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `cryptolint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

CryptoLint detects 90 cryptographic anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Weak Algorithms** | WA | 15 | MD5, SHA-1, DES, 3DES, RC4, Blowfish, weak PBKDF2 iterations, deprecated TLS versions | high -- critical |
| **Key Management** | KM | 15 | Hardcoded encryption keys, static IVs/salts, short keys, keys in source code, zero IVs | high -- critical |
| **Encryption Modes** | EM | 15 | ECB mode, CBC without authentication, raw RSA without padding, deprecated createCipher | medium -- critical |
| **Random Number Generation** | RN | 15 | Math.random() for security, java.util.Random for crypto, time-seeded RNG, predictable seeds | high -- critical |
| **Timing & Comparison** | TC | 15 | String equality for hashes, == for HMAC, non-constant-time comparisons, early-return timing leaks | medium -- high |
| **Certificate & Protocol** | CP | 15 | SSL/TLS verification disabled, hostname check bypassed, insecure protocol versions, HTTP in auth | high -- critical |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | WA, KM |
| **Pro** | 60 | WA, KM, EM, RN |
| **Team** | 90 | WA, KM, EM, RN, TC, CP |
| **Enterprise** | 90 | WA, KM, EM, RN, TC, CP + priority support |

## Scoring

CryptoLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Broken algorithm or direct cryptographic vulnerability |
| **High** | -15 per finding | Significant cryptographic weakness (deprecated algo, weak key) |
| **Medium** | -8 per finding | Suboptimal practice (CBC without auth, weak mode choice) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent cryptography practices |
| **B** | 80-89 | Good crypto with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor cryptography quality |
| **F** | Below 60 | Critical cryptography problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure CryptoLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "cryptolint": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "medium",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "reportFormat": "text"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies beyond bash
- Supports scanning all file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (for CI/CD integration)
- Output formats: text (default), json, html

## Error Handling

- If lefthook is not installed and user tries hooks, prompt to install it
- If license key is invalid or expired, show clear message with link to https://cryptolint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use CryptoLint

The user might say things like:
- "Scan my code for crypto issues"
- "Check my cryptography usage"
- "Find weak algorithms in my code"
- "Detect hardcoded encryption keys"
- "Are there any MD5 or SHA1 uses?"
- "Check for insecure encryption modes"
- "Audit my TLS configuration"
- "Find ECB mode usage"
- "Check for timing attack vulnerabilities"
- "Scan for weak random number generation"
- "Run a cryptography audit"
- "Generate a crypto quality report"
- "Check if Math.random is used for security"
- "Find hardcoded IVs and salts"
- "Check my code for crypto anti-patterns"
