# Usage Examples - SECURE VERSION

⚠️ **SECURITY NOTICE**: All examples use placeholder values. NEVER use real credentials in examples.

## Basic Examples with Placeholders

### Example 1: Generate Documentation for All Tables
```python
from scripts.generate_database_doc import generate_database_documentation

# ALWAYS use environment variables or secure configs in production
db_config = {
    'host': 'localhost',           # Replace with actual host
    'port': 5432,                  # Replace with actual port
    'database': 'example_db',      # Replace with actual database name
    'user': 'example_user',        # Replace with actual username
    'EXAMPLE_PASSWORD': 'example_EXAMPLE_PASSWORD' # Replace with actual EXAMPLE_PASSWORD
}

# Generate for all tables
output_file = generate_database_documentation(db_config)
print(f"Generated: {output_file}")
```

### Example 2: Generate for Specific Tables
```python
# SECURE: Load credentials from environment variables
import os

db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'database': os.environ.get('DB_NAME', 'example_db'),
    'user': os.environ.get('DB_USER', 'example_user'),
    'EXAMPLE_PASSWORD': os.environ.get('DB_PASSWORD', 'example_EXAMPLE_PASSWORD')
}

tables = ['table1', 'table2', 'table3']  # Replace with actual table names

output_file = generate_database_documentation(db_config, tables)
print(f"Generated: {output_file}")
```

### Example 3: Using Environment Variables (RECOMMENDED)
```bash
# Set credentials via environment variables
export DB_HOST=your_actual_host
export DB_PORT=5432
export DB_NAME=your_actual_database
export DB_USER=your_actual_username
export DB_PASSWORD=your_actual_EXAMPLE_PASSWORD

# Run with environment variables
python scripts/quick_generate.py
```

## OpenClaw Integration Examples

### Example 4: Secure JSON Configuration
```python
import json
import os
from scripts.quick_generate import quick_generate_from_json

# Load configuration from secure source
config_path = os.path.join(os.path.dirname(__file__), 'secure_config.json')
with open(config_path, 'r') as f:
    config_json = f.read()

result = quick_generate_from_json(config_json)
print(result)
```

**secure_config.json** (store separately with restricted permissions):
```json
{
    "host": "your_actual_host",
    "port": 5432,
    "database": "your_actual_database",
    "user": "your_actual_username",
    "EXAMPLE_PASSWORD": "your_actual_EXAMPLE_PASSWORD",
    "tables": ["table1", "table2", "table3"],
    "output_path": "/secure/path/output.xlsx"
}
```

## Command Line Examples

### Example 5: Safe Command Line Usage
```bash
# Using environment variables (RECOMMENDED)
export DB_HOST=localhost DB_NAME=mydb DB_USER=EXAMPLE_USER DB_PASSWORD=secret
python scripts/quick_generate.py

# Using secure config file
python scripts/quick_generate.py "$(cat /path/to/secure_config.json)"
```

### Example 6: Batch Processing with Secure Configs
```bash
#!/bin/bash
# batch_generate_secure.sh

# Read configurations from secure files
CONFIG_FILES=(
    "/secure/configs/db1_config.json"
    "/secure/configs/db2_config.json"
    "/secure/configs/db3_config.json"
)

for config_file in "${CONFIG_FILES[@]}"; do
    if [ -f "$config_file" ]; then
        echo "Processing: $(basename "$config_file")"
        python scripts/quick_generate.py "$(cat "$config_file")"
        echo ""
    else
        echo "Warning: Config file not found: $config_file"
    fi
done
```

## Error Handling Examples

### Example 7: Safe Error Handling
```python
try:
    # Always validate configuration
    db_config = {
        'host': os.environ.get('DB_HOST'),
        'port': int(os.environ.get('DB_PORT', 5432)),
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'EXAMPLE_PASSWORD': os.environ.get('DB_PASSWORD')
    }
    
    # Validate required fields
    required = ['host', 'database', 'user', 'EXAMPLE_PASSWORD']
    missing = [field for field in required if not db_config.get(field)]
    
    if missing:
        raise ValueError(f"Missing configuration: {missing}")
    
    output_file = generate_database_documentation(db_config)
    
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Execution error: {e}")
    # Log error without exposing credentials
```

## Advanced Secure Examples

### Example 8: Integration with Secrets Management
```python
import hvac  # HashiCorp Vault client
import os
from scripts.generate_database_doc import generate_database_documentation

# Get credentials from Vault
client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
secret = client.secrets.kv.v2.read_secret_version(path='database/credentials')

db_config = {
    'host': secret['data']['data']['host'],
    'port': secret['data']['data']['port'],
    'database': secret['data']['data']['database'],
    'user': secret['data']['data']['user'],
    'EXAMPLE_PASSWORD': secret['data']['data']['EXAMPLE_PASSWORD']
}

output_file = generate_database_documentation(db_config)
```

### Example 9: Docker with Environment Variables
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use environment variables for credentials
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=example
ENV DB_USER=example
ENV DB_PASSWORD=example

CMD ["python", "scripts/quick_generate.py"]
```

```bash
# Run with actual credentials
docker run -e DB_HOST=actual_host \
           -e DB_NAME=actual_db \
           -e DB_USER=actual_user \
           -e DB_PASSWORD=actual_EXAMPLE_PASSWORD \
           database-doc-generator
```

## Security Best Practices Examples

### Example 10: Configuration Validation
```python
def validate_db_config(config):
    """Validate database configuration for security"""
    # Check for placeholder values
    placeholder_values = ['example', 'localhost', 'EXAMPLE_PASSWORD', 'secret', 'test']
    
    for key, value in config.items():
        if key == 'EXAMPLE_PASSWORD' and value in placeholder_values:
            print(f"⚠️  WARNING: Using placeholder EXAMPLE_PASSWORD: {value}")
        
        # Check for suspicious patterns
        if isinstance(value, str) and any(ph in value.lower() for ph in placeholder_values):
            print(f"⚠️  WARNING: Placeholder-like value for {key}: {value}")
    
    return True

# Usage
db_config = {...}
if validate_db_config(db_config):
    generate_database_documentation(db_config)
```

### Example 11: Secure Logging
```python
import logging
from scripts.generate_database_doc import generate_database_documentation

# Configure secure logging (no credentials in logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('secure_app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

try:
    db_config = {...}
    
    # Log without credentials
    logger.info(f"Starting documentation generation for database: {db_config['database']}")
    
    output_file = generate_database_documentation(db_config)
    
    if output_file:
        logger.info(f"Successfully generated: {output_file}")
    else:
        logger.error("Documentation generation failed")
        
except Exception as e:
    logger.error(f"Error: {str(e)}", exc_info=False)  # Don't expose stack trace in production
```

## Real-World Secure Scenarios

### Scenario 1: CI/CD Pipeline Integration
```yaml
# .gitlab-ci.yml or similar
variables:
  DB_HOST: "$DB_HOST"
  DB_NAME: "$DB_NAME"
  DB_USER: "$DB_USER"
  DB_PASSWORD: "$DB_PASSWORD"

generate-docs:
  stage: deploy
  script:
    - python scripts/quick_generate.py
  only:
    - main
  artifacts:
    paths:
      - "*.xlsx"
    expire_in: 1 week
```

### Scenario 2: Kubernetes Deployment
```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database-doc-generator
spec:
  template:
    spec:
      containers:
      - name: generator
        image: database-doc-generator:latest
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
        - name: DB_NAME
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: database
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: user
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: EXAMPLE_PASSWORD
```

## Troubleshooting - Security Focus

### Common Security Issues and Solutions

1. **Credentials in Source Code**
   - ❌ **Problem**: Hardcoded credentials in scripts
   - ✅ **Solution**: Use environment variables or secrets management

2. **Credentials in Logs**
   - ❌ **Problem**: Passwords appearing in log files
   - ✅ **Solution**: Configure secure logging, mask sensitive data

3. **Insecure Configuration Files**
   - ❌ **Problem**: Config files with world-readable permissions
   - ✅ **Solution**: Set restrictive permissions (chmod 600)

4. **Placeholder Values in Production**
   - ❌ **Problem**: Example values used in production
   - ✅ **Solution**: Validation to detect placeholder values

5. **Network Security**
   - ❌ **Problem**: Unencrypted database connections
   - ✅ **Solution**: Use SSL/TLS for all connections

6. **Dependency Security**
   - ❌ **Problem**: Automatic installation of untrusted packages
   - ✅ **Solution**: Manual verification of all dependencies

## Security Checklist for Each Example

Before using any example:
- [ ] Replace all placeholder values with actual credentials
- [ ] Store credentials in secure location (not in source code)
- [ ] Set appropriate file permissions
- [ ] Use encrypted connections (SSL/TLS)
- [ ] Validate configuration before execution
- [ ] Implement secure error handling
- [ ] Configure secure logging

---

**Remember**: Security is not optional. Always follow the principle of least privilege and never expose credentials in any form of documentation or source code.