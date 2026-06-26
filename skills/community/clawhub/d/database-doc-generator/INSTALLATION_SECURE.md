# Secure Installation Guide

## ⚠️ Security-First Installation

This skill uses an **instruction-only installation** model. No code is automatically downloaded or executed during installation. This significantly reduces security risks.

## Installation Methods

### Method 1: Virtual Environment (RECOMMENDED)

```bash
# Create and activate virtual environment
python -m venv venv-database-docs

# On Windows
venv-database-docs\Scripts\activate

# On Unix/macOS
source venv-database-docs/bin/activate

# Install dependencies
pip install psycopg2-binary==2.9.9 pandas==2.2.1 openpyxl==3.1.2

# Verify installations
pip list | grep -E "psycopg2|pandas|openpyxl"
```

### Method 2: System-wide Installation (NOT RECOMMENDED)

```bash
# Install with user privileges (no sudo)
pip install --user psycopg2-binary pandas openpyxl
```

### Method 3: Docker Container (Most Isolated)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install psycopg2-binary pandas openpyxl

COPY . .

CMD ["python", "scripts/security_check.py"]
```

## Dependency Security

### Package Details

| Package | Version | Purpose | Security Notes |
|---------|---------|---------|----------------|
| psycopg2-binary | 2.9.9 | PostgreSQL adapter | Compiled binary, no build tools needed |
| pandas | 2.2.1 | Data manipulation | Well-maintained, large community |
| openpyxl | 3.1.2 | Excel file handling | Pure Python, no native extensions |

### Source Verification

```bash
# Check package signatures (if available)
pip install pip-tools
pip-compile requirements.in

# Verify package hashes
pip hash psycopg2-binary pandas openpyxl

# Check package maintainers
pip show psycopg2-binary
```

### Version Pinning

Create `requirements.txt`:
```txt
# requirements.txt - Pinned versions for security
psycopg2-binary==2.9.9
pandas==2.2.1
openpyxl==3.1.2
```

Install with pinned versions:
```bash
pip install -r requirements.txt
```

## Environment Isolation Strategies

### 1. Virtual Environment per Project
```bash
# Project-specific environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Conda Environment
```bash
# Create conda environment
conda create -n database-docs python=3.9
conda activate database-docs

# Install packages
conda install -c conda-forge psycopg2 pandas openpyxl
```

### 3. pipx for Tool Isolation
```bash
# Install as isolated application
pipx install psycopg2-binary pandas openpyxl
```

## Security Verification Steps

### Step 1: Verify Package Integrity
```bash
# Check package hashes
python -m pip hash psycopg2-binary pandas openpyxl

# Verify no unexpected dependencies
pip check
```

### Step 2: Run Security Audit
```bash
# Install security scanner
pip install safety

# Scan for vulnerabilities
safety check --full-report
```

### Step 3: Test in Sandbox
```bash
# Run security check first
python scripts/security_check.py --validate-only

# Test with dummy credentials
export DB_HOST=localhost DB_NAME=test DB_USER=test DB_PASSWORD=test
python scripts/generate_database_doc.py --validate-only
```

## Network Security for Dependencies

### Use Trusted Package Index
```bash
# Use official PyPI
pip install --index-url https://pypi.org/simple psycopg2-binary pandas openpyxl

# Or use organization's private index
pip install --index-url https://pypi.company.com/simple psycopg2-binary pandas openpyxl
```

### Verify SSL Certificates
```bash
# Ensure pip verifies SSL certificates
pip install --cert /path/to/cert.pem psycopg2-binary

# Or use system certificates
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org psycopg2-binary
```

## Post-Installation Security

### 1. Verify Installation
```bash
# Test imports
python -c "import psycopg2; import pandas; import openpyxl; print('All imports successful')"

# Check versions
python -c "import psycopg2; print(f'psycopg2: {psycopg2.__version__}')"
```

### 2. Set Environment Variables
```bash
# Create .env file (add to .gitignore)
cat > .env << EOF
DB_HOST=your_host
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_EXAMPLE_PASSWORD
DB_SSLMODE=require
EOF

# Load environment variables
export $(grep -v '^#' .env | xargs)
```

### 3. Configure Git Ignore
```.gitignore
# .gitignore
.env
*.env
venv*/
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.xlsx
*.xls
secure_config*.json
```

## Troubleshooting Secure Installation

### Common Issues and Solutions

1. **Permission Denied**
   ```bash
   # Use virtual environment instead of system install
   python -m venv venv
   source venv/bin/activate
   pip install psycopg2-binary
   ```

2. **SSL Certificate Errors**
   ```bash
   # Update certificates
   pip install --upgrade certifi
   
   # Or specify certificate bundle
   pip install --cert /etc/ssl/certs/ca-certificates.crt psycopg2-binary
   ```

3. **Network Restrictions**
   ```bash
   # Use proxy if behind firewall
   pip install --proxy http://proxy.company.com:8080 psycopg2-binary
   ```

4. **Version Conflicts**
   ```bash
   # Create fresh virtual environment
   python -m venv fresh_venv
   source fresh_venv/bin/activate
   
   # Install with exact versions
   pip install psycopg2-binary==2.9.9 pandas==2.2.1 openpyxl==3.1.2
   ```

## Compliance Considerations

### For Regulated Environments
1. **Air-gapped Networks**: Use approved package repositories
2. **Software Bills of Materials (SBOM)**: Document all dependencies
3. **Vulnerability Scanning**: Regular security scans
4. **Change Control**: Document all installation steps

### Audit Trail
```bash
# Document installation
echo "=== Installation Log $(date) ===" > install.log
echo "Python: $(python --version)" >> install.log
echo "pip: $(pip --version)" >> install.log
pip freeze >> install.log
```

## Uninstallation

### Safe Removal
```bash
# Deactivate virtual environment first
deactivate

# Remove virtual environment
rm -rf venv-database-docs

# Or uninstall packages
pip uninstall -y psycopg2-binary pandas openpyxl

# Clean pip cache
pip cache purge
```

## Support

For installation issues:
1. Check Python version (requires 3.7+)
2. Verify network connectivity to PyPI
3. Check system dependencies (libpq for PostgreSQL)
4. Review error messages for specific issues

---

**Remember**: Always install in isolated environments and verify package integrity before use.