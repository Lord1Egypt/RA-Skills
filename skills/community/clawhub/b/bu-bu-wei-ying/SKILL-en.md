---
name: bu-bu-wei-ying
description: Complex APP Development Unified Skill - Integrates best practices from Agile, CI/CD, and DevOps. Core principle: Test Every Step, Verify Every Layer, Link Every Stage, Protect Every Level.
category: devops
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - git
        - npm
    always: false
    emoji: "🏰"
version: 2.0.0
---

# Bu Bu Wei Ying - Complex APP Development Unified Skill

Use this skill when the user asks for complex application development, CI/CD pipeline setup, or DevOps tasks.

## Core Principles

### Fix Scope Principle (Highest Priority)
**Only fix the specified problem and related code - never modify other code**
- Only modify code that the user explicitly identified as problematic
- Only modify code directly related to the problem
- Never modify features that are already working correctly
- Confirm scope of changes before each modification
- Verify other functionality is not affected after changes

### Development Philosophy
**Test Every Step** → Run tests after every code change  
**Verify Every Layer** → Validate each module  
**Link Every Stage** → Ensure proper sequencing  
**Protect Every Level** → Implement safeguards at every layer

---

## Development Flow Checklist

### 1. Requirements Analysis
- [ ] Define functional and non-functional requirements
- [ ] Break down tasks into executable subtasks
- [ ] Estimate time and resources
- [ ] Define acceptance criteria

### 2. Code Development
- [ ] Create feature branch `git checkout -b feature/xxx`
- [ ] Write code following coding standards
- [ ] Write unit tests (> 80% coverage target)
- [ ] Run local lint/static analysis
- [ ] Code review

### 3. Build Phase
- [ ] Local build succeeds `npm run build` / `docker build`
- [ ] Run integration tests
- [ ] Security scan `npm audit` / `trivy image`
- [ ] Generate artifacts (Docker image/binary)

### 4. Testing Phase
- [ ] Deploy to staging environment
- [ ] Execute E2E tests
- [ ] Performance testing (latency, concurrency)
- [ ] Regression testing
- [ ] Obtain test report

### 5. Release Phase
- [ ] Create Release Tag
- [ ] Update CHANGELOG
- [ ] Execute canary release (5% → 25% → 100%)
- [ ] Monitor metrics
- [ ] Prepare rollback plan

### 6. Operations & Monitoring Phase
- [ ] Confirm monitoring alerts are active
- [ ] Check log aggregation
- [ ] Verify backup mechanisms
- [ ] Update documentation

---

## Common Commands Reference

### Package Management
```bash
npm install           # Install dependencies
npm run build        # Build project
npm test             # Run tests
npm run lint         # Lint code
npm run audit       # Security audit
```

### Docker
```bash
docker build -t app:v1 .              # Build image
docker run -d app:v1                  # Run container
docker-compose up -d                  # Start service stack
docker logs -f <container>            # View logs
```

### Git Workflow
```bash
git checkout -b feature/xxx            # Create feature branch
git add . && git commit -m "feat: xxx"
git push origin feature/xxx           # Push branch
git merge main                        # Merge main
git tag v1.0.0 && git push --tags     # Create tag
```

### CI/CD Checks
```bash
curl -I http://localhost:PORT/health   # Health check
netstat -tlnp | grep PORT             # Port check
tail -100 /var/log/app.log            # View logs
```

---

## Usage Examples

### Example 1: Develop New Feature
```
User: Help me develop a user registration feature
Agent:
1. Create branch feature/user-registration
2. Write API, database models, unit tests
3. Run tests to ensure passing
4. Build and push image to registry
5. Execute canary release
```

### Example 2: Troubleshoot Deployment Issue
```
User: Production deployment failed
Agent:
1. Check build logs
2. Verify environment variable configuration
3. Test database connectivity
4. Check network/ports
5. Execute rollback if needed
```

---

## Pitfall Risk Matrix

| Risk | Prevention |
|------|------------|
| Insufficient test coverage | Require coverage report |
| Security vulnerabilities | Must run security scan |
| Missing configuration | Use env var template checklist |
| Canary release failure | Prepare and verify rollback script |
| Missing logs | Confirm log aggregation is configured |
| Monitoring blind spots | Verify monitoring alerts before release |

---

## Verification Steps

After each task completion, execute:

1. **Self-Check Checklist** - Verify each item against the checklist
2. **Result Report** - Report key metrics (test coverage, build status, etc.)
3. **Next Steps** - Suggest optimizations or follow-up actions

---

## Automation Scripts

Available scripts in `scripts/checklist.sh`:

| Command | Description |
|---------|-------------|
| `verify-fix <file>` | Verify fix scope (core safety check) |
| `dev-check` | Full development check (lint + test + build) |
| `docker-build [name] [tag]` | Docker build with security scan |
| `health [host] [port] [path]` | Health check HTTP endpoint |
| `canary [image] [stages]` | Canary release (default: 5,25,100%) |
| `rollback [ns] [deploy]` | Rollback to previous stable version |
| `coverage [threshold]` | Check test coverage (default: 80%) |
| `all` | Execute all checks |

---

## Monitoring Templates

Import monitoring rules from `templates/` directory:

### Grafana (grafana-alerts.json)
- Application error rate
- Response latency
- Service availability
- CPU/Memory/Disk usage

### Datadog (datadog-alerts.json)
- Error rate alerts
- Latency alerts
- Health check failures
- Infrastructure metrics
- Log error surge detection
