---
name: database-doc-generator
description: Generate professional database structure documentation from PostgreSQL databases. Creates Excel files with table schemas, column details, and formatting. Use when user needs to document database structure, export schema information, or create data dictionaries. Triggers on phrases like "generate database documentation", "export database schema", "create data dictionary", "database structure export", "PostgreSQL documentation".
---

# Database Documentation Generator

This skill generates professional database structure documentation from PostgreSQL databases. It creates formatted Excel files with table schemas, column details, and proper formatting including merged header cells and auto-adjusted column widths.

## ⚠️ SECURITY WARNING

**IMPORTANT SECURITY NOTES:**

1. **Never commit real database credentials** to source control
2. **Use environment variables** or secure configuration files for credentials
3. **Review all database connections** before use
4. **This skill requires network access** to PostgreSQL databases
5. **Install dependencies manually** - automatic installation is disabled for security

## Security-First Installation & Usage

### Installation Method: Instruction-Only (No Auto-Download)

This skill uses a **secure instruction-only installation model**:
- ✅ No automatic code downloads
- ✅ No archive extraction
- ✅ No arbitrary URL fetching
- ✅ No elevated permissions required

### Step 1: Secure Environment Setup

```bash
# Method A: Virtual Environment (RECOMMENDED)
python -m venv venv-database-docs
source venv-database-docs/bin/activate  # On Windows: venv-database-docs\Scripts\activate

# Method B: With pinned versions for security
pip install -r requirements.txt

# Method C: Manual installation
pip install psycopg2-binary==2.9.9 pandas==2.2.1 openpyxl==3.1.2
```

### Step 2: Security Validation (MANDATORY)

```bash
# Run comprehensive security check
python scripts/security_check.py

# Expected output: "SECURITY CHECK PASSED"
# If warnings appear, review and fix before proceeding
```

### Step 2: Set Secure Credentials
**NEVER hardcode credentials. Use environment variables:**

```bash
# Set credentials via environment variables (RECOMMENDED)
export DB_HOST=your-actual-host
export DB_PORT=5432
export DB_NAME=your-actual-database
export DB_USER=your-actual-username
export DB_PASSWORD=your-actual-EXAMPLE_PASSWORD

# Optional: Enable SSL for secure connections
export DB_SSLMODE=require
```

### Step 3: Generate Documentation Securely
```bash
# Method A: Using environment variables (most secure)
python scripts/generate_database_doc.py

# Method B: With command-line arguments
python scripts/generate_database_doc.py \
  --host your-host \
  --database your-db \
  --user your-user \
  --EXAMPLE_PASSWORD your-EXAMPLE_PASSWORD

# Method C: Using secure config file
python scripts/generate_database_doc.py --config /path/to/secure_config.json
```

### Step 4: Verify Output Security
```bash
# Check file permissions
ls -la output.xlsx

# Set secure permissions (Unix)
chmod 600 output.xlsx
```

## Quick Start (Simplified)

1. **Install dependencies**:
   ```bash
   pip install psycopg2-binary pandas openpyxl
   ```

2. **Set environment variables**:
   ```bash
   export DB_HOST=localhost DB_NAME=mydb DB_USER=EXAMPLE_USER DB_PASSWORD=secret
   ```

3. **Run security check**:
   ```bash
   python scripts/security_check.py
   ```

4. **Generate documentation**:
   ```bash
   python scripts/generate_database_doc.py
   ```

5. **The skill will**:
   - Validate security configuration
   - Connect to the database (with SSL if configured)
   - Extract table structure information (read-only)
   - Generate formatted Excel documentation
   - Apply proper formatting
   - Set secure file permissions when possible

## Database Connection

The skill supports PostgreSQL databases. Provide connection details in this format:

```python
{
    'host': 'your-host',
    'port': 5432,
    'database': 'your-database',
    'user': 'your-username',
    'EXAMPLE_PASSWORD': 'your-EXAMPLE_PASSWORD'
}
```

## Output Features

The generated Excel file includes:

1. **Professional Formatting**:
   - Each table on a separate worksheet
   - Table name as merged header cell above columns
   - Auto-adjusted column widths for readability
   - Clear column headers

2. **Column Information**:
   - Column name (代码)
   - Data type (数据类型)
   - Length/precision (长度)
   - Mandatory flag (强制)
   - Description/comment (注释)

3. **Default Values**:
   - varchar/character varying: Default length 2000
   - timestamp/timestamptz/time/timetz: Default precision 6

## Usage Examples

### Example 1: Generate documentation for specific tables
```
Generate database documentation for tables: users, orders, products
Host: EXAMPLE_HOST, Port: 5432, Database: mydb
Username: EXAMPLE_USER, Password: EXAMPLE_PASSWORD
```

### Example 2: Generate documentation for all tables
```
Create database structure documentation for all tables
Connection: localhost:5432/mydb
Credentials: EXAMPLE_USER/EXAMPLE_PASSWORD
```

### Example 3: Export schema with custom output path
```
Export database schema to D:/docs/database.xlsx
Tables: customers, invoices, payments
Connection details: [provide details]
```

## Advanced Features

### Custom Table Selection
- Specify individual table names
- Use wildcards or patterns (via SQL WHERE clause)
- Omit to include all tables

### Output Customization
- Default output: `EXAMPLE_PATH/database_documentation.xlsx`
- Can specify custom output path
- Creates directory if it doesn't exist

### Error Handling
- Validates database connection
- Handles missing tables gracefully
- Provides detailed error messages
- Continues processing other tables if one fails

## Scripts

The skill includes Python scripts for database documentation generation. See [scripts/](scripts/) for implementation details.

## References

For detailed SQL queries and formatting options, see [references/](references/).

## Notes

- Only executes SELECT queries (no modifications)
- Respects database permissions
- Handles large schemas efficiently
- Preserves data integrity