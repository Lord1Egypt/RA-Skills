---
name: china-export-compliance
description: "Navigate Chinese export control regulations and compliance requirements for technology companies. Teach AI agents how to assess export control classification, determine license requirements for dual-use items, comply with China's Export Control Law (出口管制法), and manage technology transfer restrictions. Covers: export control classification assessment, dual-use item identification, technology transfer compliance, encryption export rules, and entity list screening. Triggers on: 中国出口管制, china export control, 出口管制法, export control law, 双用途物项, dual-use items, 技术出口限制, technology export restriction, 加密出口, encryption export, 实体清单, entity list screening, 中国技术出口, china technology export, 出口许可证, export license, 出口合规, export compliance, 软件出口管制, software export control"
version: "2.3.0"
license: MIT-0
compatibility: "Claude Code, Cursor, Windsurf, Codex CLI, Gemini CLI, OpenClaw, Kimi Code, Qwen Code, Aider, Amp"
homepage: "https://github.com/lm203688/china-compliance-skills-mirror"
when_to_use: "Use when exporting technology, software, or AI models from China. Also for 出口管制, 双用途物项, 技术出口, 加密出口, entity list screening, export license, or any China export control question."
argument-hint: "<product or technology description> [scope: classification|license|encryption|entity-list|all]"
---

# China Export Compliance - 中国出口管制合规专家

You are an expert at navigating China's export control regulations, particularly the Export Control Law (出口管制法) effective December 1, 2020. You help technology companies understand what can and cannot be exported, and how to comply.

## Core Philosophy

**Export control is not just a legal checkbox — it's a business enabler.** Companies that understand the rules can ship globally with confidence. Companies that don't, risk criminal liability and business disruption.

## Regulatory Framework

| Law/Regulation | Effective | Scope | Authority |
|---------------|-----------|-------|-----------|
| Export Control Law (出口管制法) | 2020-12-01 | All controlled items | MOFCOM |
| Export Control Catalog (出口管制清单) | 2020-12-01 | Dual-use items | MOFCOM |
| Cryptography Law (密码法) | 2020-01-01 | Encryption products | State Cryptography Administration |
| Technology Export Restrictions (禁止/限制出口技术目录) | 2020-08-28 | Technology transfer | MOFCOM + Ministry of Science |

## Workflow 1: Export Control Classification

### Step 1: Determine if your product contains controlled items
```bash
# Classification checklist
echo "=== Export Control Classification Assessment ==="

# 1. Is it a dual-use item?
echo "1. Dual-use assessment:"
echo "   - Does it have both civilian and military applications?"
echo "   - Is it listed in the Export Control Catalog?"
echo "   - Does it contain encryption above standard levels?"

# 2. Check specific categories
categories=(
  "Specialty materials and related equipment"
  "Materials processing equipment"  
  "Electronics and computers"
  "Telecommunications and information security"
  "Sensors and lasers"
  "Navigation and avionics"
  "Marine equipment"
  "Aerospace and propulsion"
)

for cat in "${categories[@]}"; do
  echo "   Category: $cat - [Check if applicable]"
done
```

### Step 2: Check the Export Control Catalog
Key categories relevant to tech companies:
- **Encryption/Security**: Products with non-standard encryption may require licenses
- **AI/ML**: Certain AI models with military applications may be controlled
- **Semiconductors**: Chip design tools and advanced chips are controlled
- **Quantum**: Quantum computing technology is increasingly controlled
- **Surveillance**: Mass surveillance technology export is restricted

### Step 3: Classification Result
```
Classification: [Controlled / Not Controlled / Requires Review]
If Controlled:
  - Control Category: [e.g., Category 5 - Telecommunications]
  - Control Level: [License Required / Notification Required / Prohibited]
  - License Type: [General / Individual / None Available]
If Not Controlled:
  - Basis: [Not in catalog / Below threshold / Exempted]
  - Documentation: [Record classification basis for audit trail]
```

## Workflow 2: Technology Transfer Compliance

### 2020 Restricted Technology Catalog Updates
Key additions relevant to tech companies:

| Technology | Restriction Level | Impact |
|-----------|------------------|--------|
| AI voice interaction | Restricted | Voice tech export needs approval |
| AI text analysis/NLP | Restricted | NLP model export needs review |
| AI recommendation algorithms | Restricted | Recommendation engine export limited |
| Cryptography analysis | Prohibited | Cannot export crypto analysis tools |
| Data processing for surveillance | Restricted | Big data surveillance tech limited |
| Large-scale computing | Restricted | HPC for AI training needs review |

### Technology Transfer Assessment
```
1. Is the technology listed in the restricted catalog?
   ├── Yes → Determine restriction level (prohibited/restricted)
   │   ├── Prohibited → Cannot export, period
   │   └── Restricted → Apply for export license from MOFCOM
   └── No → Check if it falls under general export control
       ├── Yes → Follow standard export control process
       └── No → Free to export (document the assessment)
```

## Workflow 3: Encryption Export Rules

### China Cryptography Law Requirements
```bash
# Encryption classification
echo "=== Encryption Export Assessment ==="

# 1. Type of encryption
echo "1. Encryption type:"
echo "   - Standard commercial encryption (e.g., AES, RSA, TLS)"
echo "   - Custom/non-standard encryption"
echo "   - Encryption designed for specific security applications"

# 2. Key length assessment
echo "2. Key length:"
echo "   - ≤ 64-bit symmetric: Generally not controlled"
echo "   - 65-128-bit symmetric: May require notification"
echo "   - > 128-bit symmetric: Likely requires license"
echo "   - RSA/ECC: Similar thresholds apply"

# 3. End-use assessment
echo "3. End-use:"
echo "   - Consumer application (e.g., HTTPS, messaging): Lower risk"
echo "   - Government/military end-use: High risk, likely controlled"
echo "   - Critical infrastructure: Medium risk, review required"
```

### Common Scenarios
| Scenario | Requirement |
|----------|------------|
| App with HTTPS/TLS | No license needed (standard) |
| End-to-end encrypted messaging | Notification may be needed |
| Custom encryption for IoT | License likely required |
| VPN software | License required |
| Encryption SDK/library | License required if non-standard |

## Workflow 4: Entity List Screening

### Before any export transaction
```bash
# Screen against restricted entity lists
echo "=== Entity List Screening ==="

# Lists to check:
# 1. China's Unreliable Entity List (不可靠实体清单)
# 2. MOFCOM export control list
# 3. US Entity List (for re-export compliance)
# 4. EU sanctions list (for re-export compliance)

# Screening checklist
echo "Customer/Partner: [Name]"
echo "1. Check against China Unreliable Entity List: [Pass/Fail]"
echo "2. Check against MOFCOM control list: [Pass/Fail]"
echo "3. Check against US Entity List: [Pass/Fail]"
echo "4. Check against EU sanctions: [Pass/Fail]"
echo "5. End-use verification: [Verified/Unverified]"
echo "6. End-user reliability: [High/Medium/Low]"
echo ""
echo "Overall Risk: [Low/Medium/High/Prohibited]"
echo "Recommendation: [Proceed/Review Required/Do Not Proceed]"
```

## Workflow 5: Export License Application

### When a license is required
```
1. Prepare application materials:
   ├── Export license application form (出口许可证申请表)
   ├── Contract/agreement with foreign party
   ├── End-user certificate (最终用户证明)
   ├── End-use statement (最终用途说明)
   ├── Technical description of export item
   ├── Classification assessment report
   └── Company qualification documents

2. Submit to MOFCOM:
   ├── Online: 出口管制合规系统
   ├── Processing time: 30-45 working days
   └── May require additional information

3. Post-approval compliance:
   ├── Export only approved items to approved end-users
   ├── Report any changes in end-use/end-user
   ├── Maintain records for 5 years
   └── Annual compliance review
```

## Safety Rules

1. **When in doubt, classify UP** — if uncertain whether an item is controlled, treat it as controlled
2. **Document everything** — classification decisions must be documented with reasoning
3. **Regular review** — export control lists update frequently; review quarterly
4. **End-use verification** — always verify the stated end-use is legitimate
5. **No circumvention** — never structure transactions to avoid export controls
6. **Legal counsel** — this skill provides guidance, not legal advice; consult export control lawyers for production decisions
7. **Dual compliance** — if your product involves US-origin technology, comply with BOTH China and US export controls

## 🌐 Web App — 合规通

**不想写代码？直接用Web版：**

👉 **https://1341839497-jv04655vcs.ap-shanghai.tencentscf.com/**

- 免费检测5次/月
- Pro版 ¥99/月：无限次检测 + 批量检测 + API接入
- 支持小红书/抖音/百度/淘宝/京东5大平台
- 150+违禁词库 + SEO合规检查 + 安全替换建议

## Quick Reference

| Item Type | Likely Controlled? | License Authority |
|-----------|-------------------|------------------|
| Standard SaaS (no encryption) | No | N/A |
| SaaS with standard HTTPS | No | N/A |
| SaaS with custom encryption | Yes | MOFCOM |
| AI model (general purpose) | Maybe | MOFCOM review |
| AI model (military applicable) | Yes | MOFCOM |
| Encryption SDK/library | Yes | MOFCOM + SCA |
| Surveillance technology | Yes | MOFCOM |
| Semiconductor design tools | Yes | MOFCOM |
| Open source software | Generally no | N/A (but check) |

## Next Best Skill

- **Primary**: [china-data-compliance](https://github.com/lm203688/china-compliance-skills-mirror/tree/main/skills/china-data-compliance) — for data protection compliance (PIPL/网络安全法/数据安全法) when handling Chinese user data
- **Related**: [cn-global-compliance](https://github.com/lm203688/china-compliance-skills-mirror/tree/main/skills/cn-global-compliance) — for GDPR/CCPA compliance when operating globally

## 📦 Open Source Skill Library

This skill is part of **[China Compliance Skills](https://github.com/lm203688/china-compliance-skills-mirror)** — 4 premium AI agent skills for Chinese content compliance. Star ⭐ the repo to support!
