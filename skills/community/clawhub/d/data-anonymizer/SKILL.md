---
name: data-anonymizer
description: Anonymize sensitive data in databases, files, and APIs for testing and compliance. Detect PII (names, emails, SSNs, addresses, phone numbers), apply anonymization strategies (masking, hashing, synthetic replacement), and generate realistic fake data.
---

# Data Anonymizer

Anonymize production data for safe use in testing, development, and analytics. Detect PII automatically, apply appropriate anonymization strategies (masking, hashing, synthetic replacement, generalization), and generate realistic fake data that preserves data relationships and statistical properties.

Use when: "anonymize data", "mask PII", "create test data from production", "GDPR compliance", "data masking", "remove personal data", "sanitize database", "fake data generation", or when preparing production data for non-production use.

## Commands

### 1. `detect` — Find PII in Data Sources

#### Step 1: Scan for PII Patterns

```bash
# Scan files for common PII patterns
rg -n "(\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b)" --type-not binary 2>/dev/null | head -20
echo "--- Emails found above ---"

rg -n "\\b\\d{3}[-.]?\\d{2}[-.]?\\d{4}\\b" --type-not binary 2>/dev/null | head -20
echo "--- SSN-like patterns above ---"

rg -n "\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b" --type-not binary 2>/dev/null | head -20
echo "--- Phone numbers above ---"

rg -n "\\b\\d{4}[- ]?\\d{4}[- ]?\\d{4}[- ]?\\d{4}\\b" --type-not binary 2>/dev/null | head -20
echo "--- Credit card-like patterns above ---"
```

#### Step 2: Scan Database Schema

```bash
# Find columns likely containing PII (by name pattern)
python3 -c "
pii_column_patterns = [
    'email', 'phone', 'address', 'street', 'city', 'zip', 'postal',
    'ssn', 'social_security', 'tax_id', 'national_id',
    'first_name', 'last_name', 'full_name', 'name',
    'birth', 'dob', 'date_of_birth', 'age',
    'credit_card', 'card_number', 'cvv', 'expiry',
    'ip_address', 'ip', 'user_agent',
    'password', 'secret', 'token', 'api_key',
    'latitude', 'longitude', 'lat', 'lng', 'geo',
    'photo', 'avatar', 'image_url',
    'salary', 'income', 'bank_account', 'iban', 'routing',
]

# Parse schema from SQL dump or migration files
import sys
for pattern in pii_column_patterns:
    print(f'  - {pattern}*')
print('\\nUse these patterns to grep your database schema:')
print('rg -i \"(\" + \"|\".join(pii_column_patterns[:5]) + \")\" migrations/ schema.sql')
"
```

#### Step 3: Classify Sensitivity

| Level | Data Types | Strategy |
|-------|-----------|----------|
| **Critical** | SSN, credit card, passwords, API keys | Delete or hash (irreversible) |
| **High** | Email, phone, full name, address | Synthetic replacement |
| **Medium** | Date of birth, IP address, location | Generalization (year only, /24 subnet) |
| **Low** | Age range, city, job title | Keep or slight perturbation |

### 2. `anonymize` — Apply Anonymization

#### Strategy 1: Synthetic Replacement (recommended for test data)

```python
# Generate realistic fake data preserving format and relationships
import hashlib

def anonymize_email(email):
    """Consistent fake email — same input always produces same output"""
    h = hashlib.sha256(email.encode()).hexdigest()[:8]
    domain = email.split('@')[1] if '@' in email else 'example.com'
    return f"user_{h}@test-{domain}"

def anonymize_name(name):
    """Replace with consistent fake name"""
    from faker import Faker
    fake = Faker()
    fake.seed_instance(hash(name) % (2**32))
    return fake.name()

def anonymize_phone(phone):
    """Keep format, replace digits"""
    import re
    h = hashlib.sha256(phone.encode()).hexdigest()
    digits = [c for c in h if c.isdigit()]
    result = ''
    d = 0
    for c in phone:
        if c.isdigit():
            result += digits[d % len(digits)]
            d += 1
        else:
            result += c
    return result

def anonymize_address(address):
    """Replace with fake address in same region"""
    from faker import Faker
    fake = Faker()
    fake.seed_instance(hash(address) % (2**32))
    return fake.address()
```

#### Strategy 2: Masking (quick, for logs/exports)

```python
def mask_email(email):
    parts = email.split('@')
    return f"{parts[0][:2]}***@{parts[1]}" if '@' in email else '***'

def mask_phone(phone):
    return phone[:3] + '***' + phone[-2:]

def mask_ssn(ssn):
    return '***-**-' + ssn[-4:]

def mask_card(card):
    return '****-****-****-' + card[-4:]
```

#### Strategy 3: SQL-Level Anonymization

```sql
-- PostgreSQL anonymization script
UPDATE users SET
    email = 'user_' || md5(email) || '@example.com',
    first_name = 'User',
    last_name = 'Test_' || substring(md5(last_name) from 1 for 6),
    phone = '+1' || lpad(abs(hashtext(phone))::text, 10, '0'),
    address_line1 = floor(random() * 9999)::text || ' Test Street',
    city = 'Testville',
    zip_code = lpad(abs(hashtext(zip_code))::text, 5, '0'),
    date_of_birth = date_of_birth - (random() * 365)::int * interval '1 day',
    ssn = NULL
WHERE true;

-- Verify no real data remains
SELECT email FROM users WHERE email NOT LIKE '%@example.com' LIMIT 5;
```

### 3. `verify` — Validate Anonymization

After anonymization, verify:
- No real email addresses remain (check against known patterns)
- No real phone numbers (validate format but not real numbers)
- Statistical properties preserved (age distribution, geographic spread)
- Referential integrity maintained (FK relationships intact)
- Uniqueness constraints respected (no duplicate generated values)

### 4. `report` — Generate Compliance Report

```markdown
# Data Anonymization Report

## Scope
- Database: production_backup_20260429
- Tables processed: 15
- Records processed: 2.3M

## PII Found and Anonymized
| Column | Table | Records | Strategy | Verified |
|--------|-------|---------|----------|----------|
| email | users | 150,000 | Synthetic | ✅ |
| phone | users | 148,322 | Synthetic | ✅ |
| ssn | employees | 1,200 | Deleted | ✅ |
| address | orders | 890,000 | Synthetic | ✅ |
| ip_address | logs | 5.2M | Generalized (/24) | ✅ |

## Verification
- ✅ No real emails in anonymized data
- ✅ Foreign key integrity preserved
- ✅ Unique constraints satisfied
- ✅ Statistical distributions preserved (±5%)
```
