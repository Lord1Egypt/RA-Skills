# Database Documentation Generator

A professional OpenClaw skill for generating database structure documentation from PostgreSQL databases.

## Features

- 📊 **Professional Excel Output**: Creates formatted Excel files with table schemas
- 🎨 **Automatic Formatting**: Merged headers, auto-adjusted column widths, professional styling
- 🔗 **PostgreSQL Support**: Extracts structure information from PostgreSQL databases
- 📝 **Complete Documentation**: Includes column names, data types, lengths, constraints, and comments
- ⚙️ **Easy Configuration**: Simple JSON configuration for database connection
- 🛡️ **Error Handling**: Robust error handling and detailed logging

## ⚠️ Security-First Installation

This skill uses **instruction-only installation** - no code is automatically downloaded or executed. This significantly reduces security risks.

### Installation Methods (Choose One)

#### Method A: Virtual Environment (RECOMMENDED)
```bash
# Create isolated environment
python -m venv venv-database-docs
source venv-database-docs/bin/activate  # On Windows: venv-database-docs\Scripts\activate

# Install with pinned versions for security
pip install psycopg2-binary==2.9.9 pandas==2.2.1 openpyxl==3.1.2
```

#### Method B: System Installation (Use with Caution)
```bash
# Install with user privileges only
pip install --user psycopg2-binary pandas openpyxl
```

#### Method C: Docker (Most Secure)
```dockerfile
# Dockerfile
FROM python:3.9-slim
RUN pip install psycopg2-binary pandas openpyxl
COPY . .
```

### Security Verification
```bash
# Run security check before use
python scripts/security_check.py

# Test with validation only
python scripts/generate_database_doc.py --validate-only
```

## Quick Start

1. **Set credentials securely** (NEVER in source code):
   ```bash
   # Environment variables (recommended)
   export DB_HOST=your-actual-host
   export DB_NAME=your-actual-database
   export DB_USER=your-actual-username
   export DB_PASSWORD=your-actual-EXAMPLE_PASSWORD
   
   # Enable SSL for security
   export DB_SSLMODE=require
   ```

2. **Run security validation**:
   ```bash
   python scripts/security_check.py
   ```

3. **Generate documentation**:
   ```bash
   python scripts/generate_database_doc.py
   ```

4. **Use in OpenClaw**:
   ```
   Generate database documentation for delivery_record table
   ```

## Security Guidelines

### Mandatory Practices
1. **Never store credentials** in source files or version control
2. **Always use virtual environments** or containers for isolation
3. **Verify package integrity** before installation
4. **Use SSL/TLS** for all database connections

### Network Security
- Configure firewall rules for database access
- Use VPN or SSH tunneling for remote connections
- Implement database-level IP whitelisting

### Output Security
- Store generated files in secure directories
- Set restrictive file permissions
- Consider encryption for sensitive schemas

## Usage Examples

### Example 1: Generate for specific tables
```
Generate database documentation for tables: users, orders, products
Host: EXAMPLE_HOST, Port: 5432, Database: mydb
Username: EXAMPLE_USER, Password: EXAMPLE_PASSWORD
```

### Example 2: Generate for all tables
```
Create database structure documentation for all tables
Connection: localhost:5432/mydb
Credentials: EXAMPLE_USER/EXAMPLE_PASSWORD
```

## Output Format

The generated Excel file includes:
- Each table on a separate worksheet
- Professional formatting with merged headers
- Column information: 代码, 数据类型, 长度, 强制, 注释
- Auto-adjusted column widths for readability

## Requirements

- Python 3.7+
- PostgreSQL database
- Required Python packages:
  - psycopg2-binary
  - pandas
  - openpyxl

## License

MIT License - see LICENSE file for details.

## Support

For issues or questions, please check the skill documentation or contact the maintainer.