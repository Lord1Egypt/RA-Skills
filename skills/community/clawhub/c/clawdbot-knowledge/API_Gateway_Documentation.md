# API Gateway Documentation - N8N MCP Server

## Overview

The API Gateway provides comprehensive request/response management, rate limiting, authentication, monitoring, and security features for the N8N MCP Server. It implements enterprise-grade API management capabilities with intelligent throttling and adaptive performance optimization.

## Features

### 🚦 Rate Limiting & Throttling
- **Multi-tier Rate Limiting**: Different limits for free, premium, and enterprise users
- **Burst Token System**: Allows temporary bursts above normal limits
- **Adaptive Throttling**: Automatically reduces limits based on system load
- **Multiple Time Windows**: Per-second, per-minute, per-hour, and per-day limits
- **Storage Backends**: In-memory and Redis storage options

### 🔐 Authentication & Security
- **JWT Token Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Granular permissions system
- **Security Headers**: Automatic security header injection
- **Input Validation**: Comprehensive request validation and sanitization
- **Request Size Limits**: Configurable payload size restrictions

### 📊 Monitoring & Analytics
- **Real-time Metrics**: Request/response tracking and performance monitoring
- **Error Tracking**: Detailed error logging and analysis
- **Performance Alerts**: Automatic alerting for high error rates or response times
- **Endpoint Statistics**: Per-endpoint performance metrics
- **User Analytics**: User-specific usage tracking

### 🔄 Request/Response Transformation
- **Content Validation**: JSON schema validation
- **Response Compression**: Automatic response compression
- **Metadata Injection**: Request ID and processing time headers
- **Error Standardization**: Consistent error response format

## Configuration

### Environment Variables

```bash
# API Gateway
API_GATEWAY_ENABLED=true
RATE_LIMITING_ENABLED=true
RATE_LIMIT_STORAGE_URL=memory://  # or redis://localhost:6379

# Rate Limits
RATE_LIMIT_PER_SECOND=10
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_PER_DAY=10000

# Burst Handling
BURST_MULTIPLIER=2.0
BURST_WINDOW_SECONDS=60

# Adaptive Throttling
ADAPTIVE_THROTTLING_ENABLED=true
THROTTLING_THRESHOLD_CPU=80.0
THROTTLING_THRESHOLD_MEMORY=85.0
THROTTLING_REDUCTION_FACTOR=0.5

# Authentication
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_HOURS=24
JWT_REFRESH_TOKEN_DAYS=30

# Monitoring
MONITORING_ENABLED=true
METRICS_RETENTION_DAYS=30
ALERT_THRESHOLD_ERROR_RATE=5.0
ALERT_THRESHOLD_RESPONSE_TIME=2000.0

# Request/Response
MAX_REQUEST_SIZE=52428800  # 50MB
MAX_RESPONSE_SIZE=104857600  # 100MB
COMPRESSION_ENABLED=true
COMPRESSION_THRESHOLD=1024
```

### User Tier Configuration

The system supports three user tiers with different rate limits:

```python
USER_RATE_LIMITS = {
    'free': {
        'per_second': 2,
        'per_minute': 20,
        'per_hour': 200,
        'per_day': 1000
    },
    'premium': {
        'per_second': 10,
        'per_minute': 100,
        'per_hour': 1000,
        'per_day': 10000
    },
    'enterprise': {
        'per_second': 50,
        'per_minute': 500,
        'per_hour': 5000,
        'per_day': 50000
    }
}
```

## API Endpoints

### Authentication

#### POST /api/auth/login
Login with username and password to receive JWT token.

**Request:**
```json
{
    "username": "demo",
    "password": "demo"
}
```

**Response:**
```json
{
    "success": true,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": "demo",
        "tier": "free",
        "permissions": ["read"]
    },
    "expires_in": 86400
}
```

#### GET /api/auth/profile
Get current user profile information (requires authentication).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
    "success": true,
    "user": {
        "id": "demo",
        "tier": "free",
        "permissions": ["read"],
        "rate_limits": {
            "tier": "free",
            "remaining": {
                "per_second": 2,
                "per_minute": 19,
                "per_hour": 199,
                "per_day": 999
            },
            "burst_tokens": 20
        }
    }
}
```

#### POST /api/auth/refresh
Refresh JWT token (requires valid token).

### Gateway Management

#### GET /api/gateway/health
Check API Gateway health status.

**Response:**
```json
{
    "status": "healthy",
    "gateway_enabled": true,
    "components": {
        "rate_limiter": true,
        "monitor": true,
        "request_validator": true,
        "response_transformer": true
    },
    "timestamp": "2025-07-08T12:00:00Z"
}
```

#### GET /api/gateway/metrics
Get comprehensive gateway metrics.

**Response:**
```json
{
    "gateway_enabled": true,
    "timestamp": "2025-07-08T12:00:00Z",
    "rate_limiting": {
        "total_requests": 1000,
        "blocked_requests": 50,
        "throttled_requests": 25,
        "burst_requests": 10,
        "block_rate": 5.0,
        "throttle_rate": 2.5,
        "burst_rate": 1.0
    },
    "monitoring": {
        "total_requests": 1000,
        "successful_requests": 950,
        "failed_requests": 50,
        "error_rate_percent": 5.0,
        "average_response_time_ms": 150.5,
        "endpoint_stats": {
            "POST /api/create-enhanced-workflow": {
                "count": 100,
                "avg_response_time_ms": 250.0,
                "error_rate_percent": 2.0
            }
        },
        "top_errors": [
            ["Rate limit exceeded", 30],
            ["Invalid JSON payload", 15]
        ],
        "active_users": 25
    }
}
```

## Rate Limiting

### How It Works

1. **Client Identification**: Requests are identified by user ID (from JWT) or IP address hash
2. **Multi-Window Checking**: Each request is checked against per-second, per-minute, per-hour, and per-day limits
3. **Burst Tokens**: Users can exceed normal limits using burst tokens that replenish over time
4. **Adaptive Throttling**: System automatically reduces limits when CPU/memory usage is high

### Rate Limit Headers

All responses include rate limit information in headers:

```
X-RateLimit-Second: 9
X-RateLimit-Minute: 95
X-RateLimit-Hour: 950
X-RateLimit-Day: 9500
X-RateLimit-Burst-Tokens: 18
X-RateLimit-Throttled: 0.75  # Only present if throttled
```

### Rate Limit Exceeded Response

When rate limits are exceeded, the API returns:

```json
{
    "error": "Rate limit exceeded",
    "message": "Too many requests. Limit: 10 per minute",
    "retry_after": 45,
    "reset_time": "2025-07-08T12:01:00Z"
}
```

**Status Code:** 429 Too Many Requests

**Headers:**
```
Retry-After: 45
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 2025-07-08T12:01:00Z
```

## Security Features

### Request Validation

- **Size Limits**: Configurable maximum request size (default: 50MB)
- **Content Type Validation**: Ensures proper content types for different endpoints
- **JSON Schema Validation**: Validates JSON payloads against defined schemas
- **Input Sanitization**: Removes potentially dangerous characters from input

### Security Headers

All responses automatically include security headers:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

### JWT Token Security

- **HS256 Algorithm**: Secure HMAC-based signing
- **Configurable Expiration**: Default 24 hours for access tokens
- **Refresh Tokens**: 30-day refresh token support
- **Automatic Validation**: All protected endpoints automatically validate tokens

## Monitoring and Alerting

### Metrics Collection

The system automatically collects:

- **Request Metrics**: Total requests, success/failure rates, response times
- **Endpoint Statistics**: Per-endpoint performance and error rates
- **User Analytics**: User-specific usage patterns
- **Error Tracking**: Detailed error categorization and frequency

### Automatic Alerts

Alerts are triggered when:

- **Error Rate**: Exceeds 5% (configurable)
- **Response Time**: Exceeds 2000ms (configurable)
- **System Resources**: CPU > 80% or Memory > 85%

### Performance Optimization

- **Response Compression**: Automatic gzip compression for responses > 1KB
- **Connection Pooling**: Efficient database connection management
- **Caching**: In-memory caching for frequently accessed data
- **Adaptive Throttling**: Automatic load balancing based on system resources

## Usage Examples

### Using Rate Limiting Decorator

```python
from api_gateway import rate_limit_decorator

@app.route('/api/expensive-operation', methods=['POST'])
@rate_limit_decorator('premium')  # Use premium tier limits
def expensive_operation():
    # Your endpoint logic here
    return jsonify({'result': 'success'})
```

### Custom Authentication

```python
from api_gateway.gateway import APIGateway

@app.route('/api/admin-only', methods=['GET'])
@api_gateway.require_auth(['admin'])  # Require admin permission
def admin_only_endpoint():
    user_id = g.user_id
    return jsonify({'message': f'Hello admin {user_id}'})
```

### Manual Rate Limit Check

```python
from flask import g

def my_endpoint():
    rate_limiter = g.rate_limiter
    client_id = rate_limiter.get_client_identifier()
    allowed, info = rate_limiter.check_rate_limit(client_id, 'enterprise')
    
    if not allowed:
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    # Process request
    return jsonify({'result': 'success'})
```

## Troubleshooting

### Common Issues

1. **Rate Limits Too Restrictive**
   - Adjust `USER_RATE_LIMITS` in configuration
   - Consider implementing user tier upgrades

2. **High Memory Usage**
   - Switch from in-memory to Redis storage
   - Adjust `METRICS_RETENTION_DAYS`

3. **Authentication Failures**
   - Verify `JWT_SECRET_KEY` is set
   - Check token expiration settings

4. **Performance Issues**
   - Enable adaptive throttling
   - Adjust compression settings
   - Monitor system resources

### Debug Mode

Enable debug logging for detailed information:

```python
import logging
logging.getLogger('api_gateway').setLevel(logging.DEBUG)
```

### Health Checks

Monitor gateway health using:
- `/api/gateway/health` - Component status
- `/api/gateway/metrics` - Performance metrics
- `/api/health` - Overall system health
