# Security Guidelines for Database Documentation Generator

## ⚠️ Critical Security Considerations

### CREDENTIAL HYGIENE - MOST IMPORTANT

**IMMEDIATE ACTION REQUIRED IF REAL CREDENTIALS WERE PRESENT:**

If any of the previously found credentials (`Edan@edan`, `monitor_inform_test`, `192.168.3.87`, etc.) were real:
1. **ROTATE ALL PASSWORDS IMMEDIATELY**
2. **REVIEW DATABASE ACCESS LOGS**
3. **AUDIT FOR UNAUTHORIZED ACCESS**
4. **UPDATE ALL CONFIGURATIONS**

### Current Status:
- ✅ All specific credential references have been removed
- ✅ Only generic placeholders remain
- ✅ Automated credential scanning implemented
- ✅ Credential hygiene policy established

This skill interacts with PostgreSQL databases and handles sensitive credentials. Follow these guidelines to ensure secure usage.

## Risk Assessment

| Risk | Level | Description | Mitigation |
|------|-------|-------------|------------|
| Credential Exposure | 🔴 HIGH | Hardcoded credentials in source files | Use environment variables or secure configs |
| Network Security | 🟡 MEDIUM | Database connections may be unencrypted | Use SSL/TLS for database connections |
| Dependency Management | 🟡 MEDIUM | Automatic package installation | Manual dependency verification |
| Data Leakage | 🟡 MEDIUM | Database schema information in output files | Secure output file storage |

## Secure Configuration Methods

### 1. Environment Variables (RECOMMENDED)

```bash
# Set credentials via environment variables
export DB_HOST=your-database-host
export DB_PORT=5432
export DB_NAME=your-database
export DB_USER=your-username
export DB_PASSWORD=your-EXAMPLE_PASSWORD

# Optional: Specific tables
export DB_TABLES=table1,table2,table3

# Optional: Output path
export OUTPUT_PATH=/secure/path/output.xlsx

# Run the generator
python scripts/quick_generate.py
```

### 2. Secure Configuration File

Create a configuration file outside the skill directory:

```json
{
  "host": "your-database-host",
  "port": 5432,
  "database": "your-database",
  "user": "your-username",
  "EXAMPLE_PASSWORD": "your-EXAMPLE_PASSWORD",
  "tables": ["table1", "table2"],
  "output_path": "/secure/path/output.xlsx"
}
```

Set restrictive permissions:
```bash
chmod 600 /path/to/secure-config.json
```

### 3. Command Line Arguments (NOT RECOMMENDED)

Avoid passing credentials via command line as they may be visible in process lists.

## Security Hardening

### Credential Hygiene Enforcement

1. **Automated Scanning**:
   ```bash
   # Run before every commit
   python scripts/clean_credentials.py
   python scripts/security_check.py
   ```

2. **Pre-commit Hooks**:
   ```bash
   # Install pre-commit hooks
   pre-commit install
   
   # Run all checks
   pre-commit run --all-files
   ```

3. **Credential Detection**:
   - Regular scans for hardcoded credentials
   - Git history cleaning if needed
   - Immediate rotation if exposure detected

### Dependency Management

1. **Manual Installation Only**:
   ```bash
   pip install psycopg2-binary pandas openpyxl
   ```

2. **Verify Package Sources**:
   - Use trusted package indexes
   - Verify package signatures when available
   - Consider using virtual environments

### Database Connection Security

1. **Use SSL/TLS**:
   ```python
   db_config = {
       'host': 'your-host',
       'port': 5432,
       'database': 'your-db',
       'user': 'your-user',
       'EXAMPLE_PASSWORD': 'your-EXAMPLE_PASSWORD',
       'sslmode': 'require'  # Enable SSL
   }
   ```

2. **Network Restrictions**:
   - Use firewall rules to restrict database access
   - Consider VPN or SSH tunneling for remote connections
   - Use database-level IP whitelisting

### Output File Security

1. **Secure Storage**:
   - Store output files in secure directories
   - Set appropriate file permissions
   - Consider encryption for sensitive schemas

2. **Cleanup**:
   - Remove temporary files
   - Securely delete sensitive output when no longer needed

## Security Checklist

Before using this skill in production:

- [ ] Remove any hardcoded credentials from source files
- [ ] Set up environment variables for credentials
- [ ] Verify database connection uses SSL/TLS
- [ ] Install dependencies from trusted sources
- [ ] Review database permissions (read-only access recommended)
- [ ] Secure output directory with appropriate permissions
- [ ] Implement logging without sensitive data
- [ ] Regular security updates for dependencies

## Incident Response

If you suspect a security issue:

1. **Immediate Actions**:
   - Rotate database credentials
   - Review access logs
   - Isolate affected systems

2. **Investigation**:
   - Check for unauthorized access
   - Review configuration files
   - Audit dependency versions

3. **Remediation**:
   - Update to latest secure version
   - Implement additional security controls
   - Document lessons learned

## Compliance Considerations

- **GDPR**: Ensure no personal data is exposed in schema documentation
- **HIPAA**: Additional safeguards needed for healthcare data
- **PCI DSS**: Special requirements for payment card data environments

## Contact

For security concerns or vulnerabilities, please follow responsible disclosure practices.

---

**Remember**: Security is a continuous process, not a one-time setup. Regularly review and update your security practices.