---
name: fastapi-backend-deployment-troubleshooting
description: Systematic troubleshooting guide for deploying FastAPI + SQLAlchemy backends
tags: python, fastapi, sqlalchemy, deployment, troubleshooting
version: "1.0"
---

# FastAPI Backend Deployment Troubleshooting

Systematic approach to deploying and fixing FastAPI + SQLAlchemy backends.

## Overview

This skill documents the process of deploying a FastAPI backend with SQLAlchemy ORM, including common pitfalls and troubleshooting patterns encountered during a real-world quantitative trading system deployment.

## Common Issues & Solutions

### 1. Dependency Version Conflicts

**Problem**: FastAPI pins specific versions of starlette, causing conflicts when requirements.txt specifies both.

```
ERROR: Cannot install -r requirements.txt (line 7) and starlette==0.41.0 because these package versions have conflicting dependencies
```

**Solution**: Remove the explicit starlette version from requirements.txt and let FastAPI pull in its compatible version.

```bash
# Check FastAPI's required starlette version
pip show fastapi | grep Requires
```

### 2. Module Import Errors

**Pattern**: Core modules don't export expected symbols

#### Config Module Fix
`core/config.py` may need a global settings instance:

```python
@lru_cache()
def get_settings() -> Settings:
    """Get global config singleton"""
    return Settings()

# Add this for direct import compatibility
settings = get_settings()
```

#### Exceptions Module Fix
`core/exceptions.py` needs a base exception class:

```python
class JuyidaException(Exception):
    """System base exception"""
    code: int = 500
    message: str = "System internal error"
    
    def __init__(self, message: str = None, code: int = None):
        self.message = message or self.message
        self.code = code or self.code
        super().__init__(self.message)

class BusinessException(JuyidaException):
    """Business exception base class"""
    # ... existing code
```

#### Auth Module Fix
`core/auth.py` needs decode_token alias:

```python
# Alias for backward compatibility
decode_token = verify_token
```

#### Dependencies Module Fix
`core/dependencies.py` needs pagination dependency:

```python
class PaginationDep:
    """Pagination dependency"""
    def __init__(self, page: int = 1, page_size: int = 20):
        self.page = max(1, page)
        self.page_size = min(100, max(1, page_size))
        self.offset = (self.page - 1) * self.page_size
        self.limit = self.page_size

async def get_current_user_id():
    """Get current user ID"""
    return None
```

### 3. Database Index Name Conflicts (CRITICAL!)

**Problem**: SQLite does not allow duplicate index names across tables. When multiple tables define indexes with same generic names like `idx_symbol_time`, table creation fails.

**Error**:
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) index idx_symbol_time already exists
```

**Solution**: Prefix all indexes with table-specific names.

#### Step-by-Step Fix Process:

1. **Identify all duplicate indexes**:
```bash
cd backend
grep -hr "Index(" apps/ | sort | uniq -d
```

2. **Rename patterns systematically**:
| Generic Name | Table-Specific Names |
|--------------|---------------------|
| `idx_symbol_time` | `idx_orders_symbol_time`, `idx_trades_symbol_time`, `idx_quotes_symbol_time` |
| `idx_user_time` | `idx_orders_user_time`, `idx_trades_user_time`, `idx_flows_user_time`, `idx_signals_user_time`, `idx_alerts_user_time` |
| `idx_user_status` | `idx_rules_user_status`, `idx_alerts_user_status`, `idx_strat_user_status` |

3. **Fix each model file**:

**apps/market/models.py**:
```python
# Before
Index('idx_symbol_time', 'symbol', 'quote_time')
Index('idx_symbol_date', 'symbol', 'trade_date', unique=True)

# After
Index('idx_quotes_symbol_time', 'symbol', 'quote_time')
Index('idx_daily_symbol_date', 'symbol', 'trade_date', unique=True)
```

**apps/trading/models.py**:
```python
# Orders table
Index('idx_orders_user_time', 'user_id', 'order_time')
Index('idx_orders_symbol_time', 'symbol', 'order_time')

# Trades table
Index('idx_trades_user_time', 'user_id', 'trade_time')
Index('idx_trades_symbol_time', 'symbol', 'trade_time')

# Capital flows table
Index('idx_flows_user_time', 'user_id', 'flow_time')
```

**apps/risk/models.py**:
```python
# Risk rules table
Index('idx_rules_user_type', 'user_id', 'rule_type')
Index('idx_rules_user_status', 'user_id', 'status')

# Risk alerts table
Index('idx_alerts_user_status', 'user_id', 'status')
Index('idx_alerts_user_time', 'user_id', 'alert_time')
```

**apps/strategy/models.py**:
```python
Index('idx_strat_user_status', 'user_id', 'status')
Index('idx_signals_user_time', 'user_id', 'signal_time')
```

4. **Verify fixes**:
```bash
grep -hr "Index('idx_" apps/ | sort | uniq -d
# Should return nothing if all conflicts fixed
```

### 4. Missing Optional Dependencies

**Problem**: Some packages are listed as optional but required in code:

```
ModuleNotFoundError: No module named 'psutil'
```

**Solution**: Install them separately:
```bash
pip install psutil
```

## Deployment Verification Checklist

- [ ] All dependencies install without version conflicts
- [ ] All Python modules import without errors
- [ ] Database initialization completes successfully
- [ ] All tables created (verify count matches expected)
- [ ] Health check endpoint returns 200
- [ ] API docs accessible at `/docs`
- [ ] Test user login works

## Quick Start After Fixes

```bash
cd backend
source venv/bin/activate

# Initialize database
python init_db.py

# Start server
python main.py

# Verify
curl http://localhost:8000/health
open http://localhost:8000/docs
```

## Key Lessons Learned

1. **SQLite is strict about index names** - Always prefix indexes with table names in multi-table schemas
2. **Module imports need consistent exports** - Aliases help with backward compatibility during refactoring
3. **Verify after each major fix** - Don't wait until the end to test database initialization
4. **Use grep to find duplicates** - Systematically identify and fix naming conflicts

## Typical Time Estimates

| Task | Estimated Time |
|------|---------------|
| Dependency installation | 2-5 min |
| Module import fixes | 10-15 min |
| Index name conflict resolution | 15-30 min |
| Database initialization | 1-2 min |
| Service verification | 2-3 min |
| **Total** | **30-60 min** |
