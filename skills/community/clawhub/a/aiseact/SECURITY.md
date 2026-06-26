# Security Information

> Security assessment and data handling practices for AISEACT.

---

## Overview

AISEACT is a **documentation-based skill** (also known as a "prompt-based skill" or "instruction skill"). It contains no executable code, no external dependencies, and no network endpoints.

**Security Status**: ✅ **Low Risk**
- No code execution
- No data persistence
- No credential requirements
- No external service dependencies (beyond standard search APIs)

---

## What This Skill Is

### Technical Nature

| Aspect | Description |
|--------|-------------|
| **Type** | Documentation/instruction-based skill |
| **Content** | Markdown files with methodology guidelines |
| **Code** | None (zero executable code) |
| **Dependencies** | None (no install requirements) |
| **Network** | No dedicated endpoints (uses platform's search APIs) |

### How It Works

1. **Skill Loading**: AI platform reads SKILL.md and reference documents
2. **User Request**: You explicitly request AISEACT methodology (or have enabled autonomous mode)
3. **Methodology Application**: AI follows the documented guidelines for search strategy
4. **Standard Search**: AI uses platform's existing search tools (no custom search implementation)
5. **Output**: AI provides answer with source citations following the methodology

---

## Data Handling

### Data Flow

```
User Query
    ↓
AI Agent (with AISEACT skill loaded)
    ↓
Search Strategy (methodology from SKILL.md)
    ↓
Platform Search API (standard search tools)
    ↓
Search Results
    ↓
Analysis & Filtering (methodology guidelines)
    ↓
Response to User
```

### What Data Is Processed

| Data Type | Handling | Storage |
|-----------|----------|---------|
| **User queries** | Passed to search APIs | Not stored by AISEACT |
| **Search results** | Analyzed per methodology | Not stored by AISEACT |
| **Source URLs** | Referenced in responses | Not stored by AISEACT |
| **Skill configuration** | Read at load time | Handled by AI platform |

### What Data Is NOT Processed

- ❌ No personal data collection
- ❌ No browsing history access
- ❌ No file system access (beyond reading skill files)
- ❌ No environment variable access
- ❌ No credential access

---

## Potential Risks & Mitigations

### Risk 1: Information Filtering (Non-Technical Risk)

**Description**: The skill includes source quality guidelines that may filter certain sources.

**Severity**: Low (behavioral/policy risk, not security risk)

**Mitigation**:
- Skill is optional (manual by default)
- User can override filtering per-query
- Source lists are transparent and documented
- User retains full control over final output

**User Control**:
```
"包含 [source]" - Include specific source regardless of rating
"显示所有来源" - Show all found sources without filtering
"不用AISEACT" - Skip methodology entirely
```

### Risk 2: Bias in Source Evaluation (Non-Technical Risk)

**Description**: Source ratings may reflect Western-centric or mainstream biases.

**Severity**: Low (methodological limitation, not security risk)

**Mitigation**:
- Acknowledged in TRUST.md
- Source evaluation criteria are transparent
- User can request any source regardless of rating
- Configuration options to adjust strictness

### Risk 3: Metadata/Configuration Mismatch

**Description**: Earlier versions had mismatch between "ALWAYS USE" language in SKILL.md and actual registry configuration.

**Severity**: Fixed ✅

**Resolution**:
- SKILL.md now uses optional, user-controlled language
- "ALWAYS USE" replaced with explicit user request patterns
- Clear distinction between manual (default) and autonomous (opt-in) modes

### Risk 4: Supply Chain (Skill File Integrity)

**Description**: Skill files could theoretically be modified to inject malicious instructions.

**Severity**: Low

**Mitigation**:
- Install from trusted source (official repository)
- Review SKILL.md before installation
- No executable code to exploit
- AI platform's safety filters still apply

---

## Security Best Practices for Users

### Installation

1. **Verify source**: Install from official repository
   ```bash
   git clone https://github.com/stephenlzc/aiseact.git
   ```

2. **Review files**: Check SKILL.md and reference documents before installing

3. **Manual mode**: Start with manual invocation (default) before enabling autonomous mode

### Usage

1. **Understand methodology**: Review TRUST.md to understand source evaluation approach

2. **Test outputs**: Verify a few outputs meet your expectations before relying on the skill

3. **Use overrides**: When in doubt, use override commands:
   - `"显示所有来源"` to see unfiltered results
   - `"包含 [source]"` to include specific sources

4. **Check source ratings**: Review `references/unreliable-sources.md` to understand rating criteria

### Configuration

1. **Default to manual**: Keep `disable-model-invocation: true` (default) unless you specifically want autonomous behavior

2. **Review autonomous outputs**: If enabling autonomous mode, monitor initial outputs for unexpected behavior

---

## Comparison with Other Skill Types

| Aspect | AISEACT (Docs) | Code-Based Skills | Tool-Based Skills |
|--------|----------------|-------------------|-------------------|
| **Executable code** | ❌ No | ✅ Yes | ✅ Yes |
| **External network calls** | ❌ No (uses platform APIs) | Variable | Variable |
| **File system access** | ❌ Read-only (skill files) | Variable | Variable |
| **Credential requirements** | ❌ None | Variable | Often required |
| **Installation risk** | Very Low | Medium | Medium |
| **Runtime risk** | Very Low | Variable | Variable |

---

## Security Assessment Summary

| Category | Assessment |
|----------|------------|
| **Code Safety** | ✅ No executable code |
| **Data Privacy** | ✅ No data persistence |
| **Network Safety** | ✅ No external endpoints |
| **Credential Safety** | ✅ No credentials required |
| **User Control** | ✅ Full user override capability |
| **Transparency** | ✅ All behavior documented |

**Overall Security Rating**: ✅ **Low Risk / Safe**

**Primary Considerations**:
- Behavioral: Source filtering methodology (user-controllable)
- Methodological: Potential bias in source ratings (acknowledged)
- Not a technical security risk

---

## Reporting Security Issues

If you discover a security issue with AISEACT:

1. **Do not** open a public issue
2. Contact the maintainer via the repository's security contact
3. Provide details about the potential vulnerability

---

## Version History

| Version | Security Changes |
|---------|------------------|
| Current | Removed "ALWAYS USE" language; added TRUST.md; enhanced user control documentation |
| Earlier | Initial release |

---

*This security information is current as of March 2026.*
