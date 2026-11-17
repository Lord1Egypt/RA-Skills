# Cybersecurity Engineering Conventions

# IDs

AST-### : asset
THR-### : threat
CYB-REQ-### : cybersecurity requirement
VULN-### : vulnerability
MIT-### : mitigation
CYB-TST-### : cybersecurity test

# Assets

Identify the elements requiring protection:
- data;
- credentials;
- firmware;
- communication;
- services;
- user accounts;
- cryptographic material.

# Threats

Each significant threat must contain:
- source;
- target asset;
- attack surface;
- preconditions;
- impact;
- likelihood when used;
- mitigation;
- residual risk.

# Secrets

Secrets must never be present:
- in Git;
- in public documents;
- in logs;
- in recorded prompts;
- in configuration examples.

# Interfaces

Every exposed interface must consider when relevant:
- authentication;
- authorization;
- confidentiality;
- integrity;
- replay;
- rate limiting;
- input validation;
- logging;
- updates;
- credential rotation.

# Vulnerabilities

A vulnerability must be traceable to:
- component;
- version;
- analysis;
- mitigation;
- verification;
- release containing the fix.

# Security release gate

Before a connected release, verify depending on context:
- secrets scan;
- dependency scan;
- known vulnerabilities;
- exposed services;
- authentication;
- update mechanism;
- logging;
- rollback/recovery.
