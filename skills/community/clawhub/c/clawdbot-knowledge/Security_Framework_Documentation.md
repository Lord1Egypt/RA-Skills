# Security Framework Documentation - N8N MCP Server

## Overview

The Security Framework provides comprehensive security features for the N8N MCP Server, including Multi-Factor Authentication (MFA), Role-Based Access Control (RBAC), and Data Encryption & Privacy Protection. This enterprise-grade security system ensures data protection, access control, and compliance with privacy regulations.

## Features

### 🔐 Multi-Factor Authentication (MFA)
- **TOTP (Time-based One-Time Password)**: Google Authenticator, Authy compatible
- **SMS Authentication**: Twilio integration for SMS codes
- **Email Authentication**: SMTP-based email verification codes
- **Backup Codes**: Emergency access codes for account recovery
- **Challenge-Response System**: Secure challenge creation and verification

### 👥 Role-Based Access Control (RBAC)
- **Hierarchical Roles**: System and custom roles with inheritance
- **Granular Permissions**: Resource and action-based permission system
- **User Management**: Role assignment with expiration support
- **Permission Checking**: Real-time permission validation
- **Audit Trail**: Complete access control logging

### 🔒 Data Encryption & Privacy Protection
- **Symmetric Encryption**: AES-256-GCM for data at rest
- **Asymmetric Encryption**: RSA-2048 for key exchange
- **Data Classification**: Automatic PII and sensitive data detection
- **Data Anonymization**: GDPR-compliant data anonymization
- **Key Management**: Secure cryptographic key handling

## Configuration

### Environment Variables

```bash
# Multi-Factor Authentication
MFA_ENABLED=true
MFA_STORAGE_TYPE=memory  # memory, redis, database
MFA_ISSUER_NAME="N8N MCP Server"
MFA_CHALLENGE_EXPIRY_MINUTES=5
MFA_MAX_ATTEMPTS=3
MFA_CODE_LENGTH=6

# SMS Provider (Twilio)
SMS_PROVIDER=twilio  # twilio, mock
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1234567890

# Email Provider
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
FROM_EMAIL=noreply@n8n-mcp.local

# Role-Based Access Control
RBAC_ENABLED=true
RBAC_STORAGE_TYPE=memory  # memory, redis, database

# Encryption
ENCRYPTION_ENABLED=true
ENCRYPTION_KEY=your-base64-encoded-key-or-password
ANONYMIZATION_SALT=your-unique-salt

# Data Retention (GDPR/CCPA Compliance)
USER_DATA_RETENTION_DAYS=2555  # 7 years
LOG_RETENTION_DAYS=90
ANALYTICS_RETENTION_DAYS=365
CREDENTIAL_RETENTION_DAYS=1095  # 3 years

# Security Headers
SECURITY_HEADERS_ENABLED=true
CONTENT_SECURITY_POLICY="default-src 'self'"
HSTS_MAX_AGE=31536000

# Session Security
SESSION_TIMEOUT_MINUTES=60
SESSION_SECURE_COOKIES=true
SESSION_HTTPONLY_COOKIES=true

# Password Policy
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_NUMBERS=true
PASSWORD_REQUIRE_SPECIAL=true
PASSWORD_MAX_AGE_DAYS=90

# Audit Logging
AUDIT_LOGGING_ENABLED=true
AUDIT_LOG_LEVEL=INFO
AUDIT_LOG_FILE=logs/audit.log
```

## API Endpoints

### Multi-Factor Authentication

#### POST /api/mfa/setup/totp
Setup TOTP (Time-based One-Time Password) for authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
    "email": "user@example.com"
}
```

**Response:**
```json
{
    "success": true,
    "secret": "JBSWY3DPEHPK3PXP",
    "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "manual_entry_key": "JBSWY3DPEHPK3PXP"
}
```

#### POST /api/mfa/verify/totp
Verify TOTP setup and enable it.

**Request:**
```json
{
    "code": "123456"
}
```

**Response:**
```json
{
    "success": true,
    "backup_codes": [
        "A1B2-C3D4",
        "E5F6-G7H8",
        "..."
    ],
    "message": "TOTP enabled successfully"
}
```

#### POST /api/mfa/setup/sms
Setup SMS MFA for authenticated user.

**Request:**
```json
{
    "phone_number": "+1234567890"
}
```

**Response:**
```json
{
    "success": true,
    "message": "SMS MFA enabled"
}
```

#### POST /api/mfa/setup/email
Setup Email MFA for authenticated user.

**Request:**
```json
{
    "email_address": "user@example.com"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Email MFA enabled"
}
```

#### POST /api/mfa/challenge
Create MFA challenge for authentication.

**Request:**
```json
{
    "method": "totp"  // totp, sms, email, backup
}
```

**Response:**
```json
{
    "success": true,
    "challenge_id": "ch_1234567890abcdef",
    "method": "totp",
    "expires_at": "2025-07-08T12:05:00Z",
    "message": "Enter TOTP code"
}
```

#### POST /api/mfa/verify
Verify MFA challenge.

**Request:**
```json
{
    "challenge_id": "ch_1234567890abcdef",
    "code": "123456"
}
```

**Response:**
```json
{
    "success": true,
    "message": "MFA verification successful",
    "user_id": "user123",
    "method": "totp"
}
```

#### GET /api/mfa/status
Get user's MFA status.

**Response:**
```json
{
    "success": true,
    "mfa_enabled": true,
    "methods": ["totp", "sms", "backup"],
    "phone_number": "***7890",
    "email_address": "use***@example.com",
    "backup_codes_remaining": 8,
    "last_used": "2025-07-08T10:30:00Z"
}
```

### Role-Based Access Control

#### GET /api/rbac/roles
List all available roles (requires system:read permission).

**Response:**
```json
{
    "success": true,
    "roles": [
        {
            "name": "admin",
            "description": "Administrative access",
            "is_system_role": true,
            "permissions_count": 15,
            "inherits_from": [],
            "created_at": "2025-07-08T00:00:00Z",
            "updated_at": "2025-07-08T00:00:00Z"
        }
    ],
    "total_count": 6
}
```

#### POST /api/rbac/roles
Create new role (requires system:admin permission).

**Request:**
```json
{
    "name": "custom_role",
    "description": "Custom role for specific users",
    "permissions": [
        {
            "resource": "workflow",
            "action": "read"
        },
        {
            "resource": "workflow",
            "action": "create",
            "conditions": {
                "owner_only": true
            }
        }
    ]
}
```

**Response:**
```json
{
    "success": true,
    "message": "Role \"custom_role\" created successfully",
    "role": {
        "name": "custom_role",
        "description": "Custom role for specific users",
        "permissions": ["workflow:read", "workflow:create"]
    }
}
```

#### POST /api/rbac/users/{user_id}/roles
Assign role to user (requires user:manage permission).

**Request:**
```json
{
    "role_name": "developer",
    "expires_in_days": 365
}
```

**Response:**
```json
{
    "success": true,
    "message": "Role \"developer\" assigned to user \"user123\"",
    "expires_at": "2026-07-08T12:00:00Z"
}
```

#### GET /api/rbac/users/{user_id}/permissions
Get user's permissions.

**Response:**
```json
{
    "success": true,
    "user_id": "user123",
    "active_roles": [
        {
            "name": "developer",
            "description": "Workflow development access",
            "assigned_at": "2025-07-08T12:00:00Z",
            "expires_at": "2026-07-08T12:00:00Z"
        }
    ],
    "permissions": [
        "workflow:create",
        "workflow:read",
        "workflow:update",
        "workflow:delete",
        "node:read",
        "credential:read"
    ]
}
```

#### POST /api/rbac/check-permission
Check if user has specific permission.

**Request:**
```json
{
    "user_id": "user123",
    "resource": "workflow",
    "action": "create",
    "context": {
        "owner_id": "user123"
    }
}
```

**Response:**
```json
{
    "success": true,
    "user_id": "user123",
    "resource": "workflow",
    "action": "create",
    "has_permission": true
}
```

## Default Roles

The system comes with predefined roles:

### Super Admin
- **Permissions**: Full system access (`*:*`)
- **Use Case**: System administrators

### Admin
- **Permissions**: Administrative access to workflows, nodes, credentials, users, analytics, settings
- **Use Case**: Application administrators

### Developer
- **Permissions**: Full workflow and node access, read-only credentials, analytics access
- **Use Case**: Workflow developers

### User
- **Permissions**: Read workflows, create/update/delete own workflows, read own credentials
- **Use Case**: Regular users

### Viewer
- **Permissions**: Read-only access to workflows, nodes, analytics
- **Use Case**: Stakeholders, auditors

### API User
- **Permissions**: API access, workflow read and execute
- **Use Case**: External integrations

## Security Best Practices

### MFA Implementation
1. **Require MFA for Admin Roles**: Enforce MFA for users with administrative privileges
2. **Backup Codes**: Ensure users save backup codes securely
3. **Regular Code Rotation**: Encourage users to regenerate backup codes periodically
4. **SMS Security**: Consider SMS vulnerabilities and prefer TOTP when possible

### RBAC Implementation
1. **Principle of Least Privilege**: Assign minimal required permissions
2. **Regular Access Reviews**: Periodically review user permissions
3. **Role Expiration**: Use temporary role assignments when appropriate
4. **Audit Logging**: Monitor all permission changes and access attempts

### Data Protection
1. **Encryption at Rest**: Encrypt sensitive data in storage
2. **Encryption in Transit**: Use HTTPS for all communications
3. **Key Rotation**: Regularly rotate encryption keys
4. **Data Classification**: Properly classify and handle different data types

## Usage Examples

### Protecting Routes with RBAC

```python
from security import require_permission

@app.route('/api/admin/users', methods=['GET'])
@require_permission('user', 'read')
def list_users():
    # Only users with 'user:read' permission can access
    return jsonify({'users': []})

@app.route('/api/workflows', methods=['POST'])
@require_permission('workflow', 'create')
def create_workflow():
    # Only users with 'workflow:create' permission can access
    return jsonify({'workflow_id': 'new_workflow'})
```

### Manual Permission Checking

```python
from flask import g

def my_endpoint():
    rbac_system = g.rbac_system
    user_id = g.user_id
    
    if rbac_system.check_permission(user_id, 'workflow', 'delete'):
        # User can delete workflows
        pass
    else:
        return jsonify({'error': 'Insufficient permissions'}), 403
```

### Encrypting Sensitive Data

```python
from flask import g

def store_user_data(user_data):
    encryption_system = g.encryption_system
    
    # Automatically encrypt PII and sensitive fields
    encrypted_data = encryption_system.encrypt_sensitive_data(user_data)
    
    # Store encrypted_data in database
    return encrypted_data

def retrieve_user_data(encrypted_data):
    encryption_system = g.encryption_system
    
    # Automatically decrypt sensitive fields
    decrypted_data = encryption_system.decrypt_sensitive_data(encrypted_data)
    
    return decrypted_data
```

### MFA Integration

```python
def login_with_mfa(username, password):
    # 1. Verify username/password
    if not verify_credentials(username, password):
        return {'error': 'Invalid credentials'}
    
    # 2. Check if user has MFA enabled
    mfa_system = g.mfa_system
    status = mfa_system.get_user_mfa_status(username)
    
    if status['mfa_enabled']:
        # 3. Create MFA challenge
        challenge = mfa_system.create_challenge(username, 'totp')
        return {
            'mfa_required': True,
            'challenge_id': challenge['challenge_id'],
            'methods': status['methods']
        }
    else:
        # 4. Complete login without MFA
        return {'token': create_jwt_token(username)}
```

## Troubleshooting

### Common Issues

1. **MFA Setup Fails**
   - Check SMTP/SMS provider configuration
   - Verify network connectivity
   - Check provider credentials

2. **Permission Denied Errors**
   - Verify user has required role assigned
   - Check role permissions configuration
   - Ensure role assignment hasn't expired

3. **Encryption Errors**
   - Verify ENCRYPTION_KEY is set correctly
   - Check key format (Base64 or password)
   - Ensure consistent key across restarts

4. **TOTP Codes Not Working**
   - Check system time synchronization
   - Verify TOTP secret is correct
   - Consider time drift tolerance

### Debug Mode

Enable debug logging for detailed information:

```python
import logging
logging.getLogger('security').setLevel(logging.DEBUG)
```

### Health Checks

Monitor security system health:
- Check MFA challenge success rates
- Monitor permission check performance
- Verify encryption/decryption operations
- Track authentication failures

This Security Framework provides enterprise-grade security features while maintaining ease of use and integration with the existing N8N MCP Server infrastructure.
