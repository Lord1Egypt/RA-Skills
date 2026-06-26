---
name: api-contract-tester
description: Validate API contracts between services using consumer-driven contract testing. Generate and verify Pact contracts, OpenAPI compliance tests, and schema compatibility checks for microservices.
---

# API Contract Tester

Validate that APIs honor their contracts. Generate consumer-driven contracts (Pact-style), verify OpenAPI spec compliance, test backward compatibility, and catch breaking changes before they reach production.

Use when: "test API contract", "check backward compatibility", "will this API change break consumers", "generate pact tests", "validate against OpenAPI spec", "contract testing", or before deploying API changes.

## Commands

### 1. `generate` — Create Contract Tests from OpenAPI Spec

#### Step 1: Find OpenAPI/Swagger Specs

```bash
# Look for OpenAPI specs
find . -maxdepth 4 -name "*.yaml" -o -name "*.yml" -o -name "*.json" | \
  xargs grep -l '"openapi"\|"swagger"\|openapi:' 2>/dev/null
```

#### Step 2: Parse and Generate Tests

Read each endpoint from the spec. For every path + method combination, generate:

1. **Happy path test** — valid request, verify response schema matches spec
2. **Required fields test** — omit each required field, expect 400/422
3. **Type validation test** — send wrong types, expect rejection
4. **Auth test** — if security scheme defined, test without credentials → 401

Output format (Python/pytest):

```python
import requests
import pytest

BASE_URL = "${BASE_URL}"

class TestContractUserEndpoint:
    """Contract tests for GET /api/users/{id}"""

    def test_happy_path(self):
        resp = requests.get(f"{BASE_URL}/api/users/1")
        assert resp.status_code == 200
        data = resp.json()
        # Verify response matches schema
        assert "id" in data
        assert isinstance(data["id"], int)
        assert "email" in data
        assert isinstance(data["email"], str)

    def test_not_found(self):
        resp = requests.get(f"{BASE_URL}/api/users/999999999")
        assert resp.status_code == 404

    def test_invalid_id_type(self):
        resp = requests.get(f"{BASE_URL}/api/users/not-a-number")
        assert resp.status_code in (400, 404, 422)
```

### 2. `verify` — Check API Against Existing Contracts

#### Step 1: Find Contract Files

```bash
# Look for Pact contracts, OpenAPI specs, or test fixtures
find . -maxdepth 4 \( -name "*.pact.json" -o -name "pacts" -type d -o -name "contract*.json" \) 2>/dev/null
```

#### Step 2: Verify Each Contract

For Pact contracts:
```bash
# If pact-verifier is installed
pact-verifier --provider-base-url=$PROVIDER_URL \
  --pact-url=./pacts/consumer-provider.json 2>&1
```

For OpenAPI specs, validate response schemas:
```bash
# Use openapi-spec-validator if available
pip install openapi-spec-validator 2>/dev/null
python3 -c "
from openapi_spec_validator import validate
validate({'openapi': '3.0.0', ...})  # parsed spec
print('Spec is valid')
"
```

If no tooling installed, manually validate by:
1. Reading the spec
2. Making requests to each endpoint
3. Comparing response structure to declared schema
4. Reporting mismatches

### 3. `breaking-changes` — Detect Breaking API Changes

Compare two versions of an OpenAPI spec and identify breaking vs. non-breaking changes.

#### Step 1: Get Both Versions

```bash
# Current version
cat api/openapi.yaml

# Previous version (from git)
git show HEAD~1:api/openapi.yaml > /tmp/old-spec.yaml 2>/dev/null || \
git show main:api/openapi.yaml > /tmp/old-spec.yaml
```

#### Step 2: Classify Changes

**Breaking changes (MUST flag):**
- Removed endpoint (path+method gone)
- Removed or renamed response field
- Changed field type (string → integer)
- New required request parameter
- Changed response status code for same operation
- Removed enum value
- Tightened validation (shorter maxLength, new pattern)

**Non-breaking changes (informational):**
- New optional field in response
- New optional query parameter
- New endpoint added
- Added enum value
- Loosened validation
- New response status code (additional error case)

#### Step 3: Report

```markdown
# API Breaking Change Report

## Breaking Changes (3 found)
1. `DELETE /api/users/{id}` — endpoint removed
   Impact: Any consumer calling this endpoint will get 404
   Migration: Use `PATCH /api/users/{id}` with `{active: false}` instead

2. `GET /api/orders` — response field `total_price` renamed to `amount`
   Impact: All consumers parsing `total_price` will break
   Migration: Add `total_price` as alias for one version cycle

3. `POST /api/orders` — new required field `currency`
   Impact: Existing requests without `currency` will fail validation
   Migration: Default to "USD" if not provided (temporary)

## Non-Breaking Changes (2 found)
- `GET /api/users` — new optional `?role=` filter parameter
- `GET /api/orders/{id}` — new `tracking_url` field in response

## Recommendation
3 breaking changes detected. Bump major version (v2 → v3) or add versioned endpoint prefix.
```

### 4. `compatibility-matrix` — Map Consumer Dependencies

Analyze which consumers depend on which API endpoints and fields:

```bash
# Search consumer codebases for API calls
rg -r '$1' 'fetch\(["\x27]([^"]+)["\x27]' --type js --type ts 2>/dev/null
rg -r '$1' 'requests\.(get|post|put|delete)\(["\x27]([^"]+)' --type py 2>/dev/null
rg -r '$1' 'axios\.(get|post|put|delete)\(["\x27]([^"]+)' --type js --type ts 2>/dev/null
```

Produce a matrix:
```
Endpoint          | consumer-web | consumer-mobile | consumer-worker
GET /api/users    |     ✓        |       ✓         |
POST /api/orders  |     ✓        |       ✓         |       ✓
DELETE /api/users  |              |                 |
```

Flag endpoints with zero consumers as deprecation candidates.
