# Credential Hygiene Policy

## ⚠️ CRITICAL SECURITY POLICY

**NEVER include real credentials in any file, under any circumstances.**

## What Constitutes a Credential

### 🔴 NEVER INCLUDE (Examples):
- Database passwords (`Edan@edan`, `secure123`, etc.)
- API keys/tokens
- SSH private keys
- Encryption keys
- Personal access tokens
- Certificate private keys
- Authentication cookies/sessions

### 🟡 USE WITH CAUTION (Context matters):
- Database hostnames/IPs (use placeholders)
- Database names (use generic names)
- Usernames (use generic names)
- Port numbers (usually safe, but be cautious)
- File paths (use generic paths)

## Safe Placeholder Standards

### Database Connection Examples:

```python
# ✅ SAFE - Generic placeholders
db_config = {
    'host': 'EXAMPLE_HOST',           # Never use real IPs
    'port': 5432,                     # Standard port is OK
    'database': 'EXAMPLE_DATABASE',   # Never use real DB names
    'user': 'EXAMPLE_USER',           # Never use real usernames
    'password': 'EXAMPLE_PASSWORD'    # Never use real passwords
}

# ❌ UNSAFE - Real credentials (NEVER DO THIS)
db_config = {
    'host': '192.168.3.87',          # Real IP - UNSAFE
    'database': 'monitor_inform_test', # Real DB name - UNSAFE
    'user': 'postgres',              # Real username - UNSAFE
    'password': 'Edan@edan'          # Real password - CRITICAL
}
```

### Environment Variable Examples:

```bash
# ✅ SAFE - Documentation example
export DB_HOST=EXAMPLE_HOST
export DB_NAME=EXAMPLE_DATABASE
export DB_USER=EXAMPLE_USER
export DB_PASSWORD=EXAMPLE_PASSWORD

# ❌ UNSAFE - Real values in documentation
export DB_HOST=prod-db.company.com
export DB_PASSWORD=ProductionPassword123!
```

## Detection and Prevention

### Automated Checks
```bash
# Run credential scanner
python scripts/clean_credentials.py

# Run security validation
python scripts/security_check.py

# Use pre-commit hooks
pre-commit run --all-files
```

### Manual Review Checklist
Before committing any file:
- [ ] No passwords, tokens, or keys
- [ ] No real IP addresses or hostnames
- [ ] No real database/application names
- [ ] No real usernames or email addresses
- [ ] All paths are generic or relative
- [ ] Configuration examples use placeholders

## If You Accidentally Commit Credentials

### IMMEDIATE ACTION REQUIRED:

1. **Rotate Credentials Immediately**
   ```bash
   # Assume credentials are compromised
   # Change ALL affected passwords/keys
   ```

2. **Remove from Git History**
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch PATH_TO_FILE" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (warns collaborators)
   git push origin --force --all
   ```

3. **Audit Access Logs**
   - Check database access logs
   - Review API usage
   - Monitor for unauthorized access

4. **Document the Incident**
   - What was exposed
   - When it happened
   - What actions were taken
   - Lessons learned

## Secure Development Practices

### 1. Use Environment Variables
```python
import os

# Always get credentials from environment
db_config = {
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD']
}
```

### 2. Use Configuration Files (Securely)
```python
import json
import os

# Load from secure location
config_path = os.path.join(os.path.dirname(__file__), '..', 'secure_config.json')
with open(config_path, 'r') as f:
    config = json.load(f)
```

### 3. Use Secrets Management
```python
# Example with HashiCorp Vault
import hvac

client = hvac.Client(url=os.environ['VAULT_ADDR'])
secret = client.secrets.kv.read_secret_version(path='database/creds')
```

## Testing with Dummy Data

### Safe Test Configuration
```python
# test_config.py
TEST_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'test_database',
    'user': 'test_user',
    'password': 'test_password_123'  # OK for tests, not for examples
}

# But better: Use test containers
import testcontainers.postgres

with testcontainers.postgres.PostgresContainer() as postgres:
    db_config = {
        'host': postgres.get_container_host_ip(),
        'port': postgres.get_exposed_port(5432),
        'database': 'test',
        'user': 'test',
        'password': 'test'
    }
```

## Compliance Requirements

### For All Projects:
- No credentials in source code
- No credentials in documentation
- No credentials in commit history
- Regular credential scanning
- Immediate rotation if exposed

### For Regulated Environments (GDPR, HIPAA, PCI DSS):
- Additional encryption requirements
- Audit trail for credential access
- Regular security assessments
- Employee training on credential handling

## Tools and Resources

### Scanning Tools:
- `git-secrets` (AWS)
- `truffleHog`
- `gitleaks`
- `detect-secrets`

### Prevention Tools:
- Pre-commit hooks
- CI/CD pipeline checks
- IDE plugins (secret detection)

### Monitoring:
- GitGuardian
- Snyk Code
- GitHub Advanced Security

## Training and Awareness

### Regular Training Topics:
1. Recognizing sensitive information
2. Secure credential handling
3. Emergency response procedures
4. Tool usage and best practices

### Awareness Campaigns:
- "Credential Hygiene Month"
- Security champion program
- Regular security newsletters
- Incident response drills

## Contact and Reporting

### If You Find Credentials:
1. **DO NOT** share or discuss publicly
2. **DO** report to security team immediately
3. **DO** help coordinate credential rotation

### Emergency Contacts:
- Security Team: security@example.com
- Infrastructure Team: infra@example.com
- On-call Engineer: +1-XXX-XXX-XXXX

---

**Remember**: One exposed credential can compromise an entire system.  
**When in doubt, leave it out.**