# ASF V4.0 OpenClaw Skill

**Version**: v0.9.0  
**OpenClaw Compatibility**: >=2026.3.24  
**Status**: ✅ Phase 1 Complete

---

## Overview

ASF V4.0 skill brings industrial-grade governance and optimization to OpenClaw:

- **Veto Enforcement**: Hard/soft veto rules for governance
- **Ownership Proof**: Verifiable single-writer proofs
- **Economics Scoring**: Cost-based role assignment optimization
- **Rework Risk**: Predictive risk analysis
- **Safe Optimizer**: Online optimization with rollback protection

---

## Installation

```bash
# The skill is in the workspace skills directory
# Enable in ~/.openclaw/openclaw.json:
{
  "skills": {
    "enabled": [
      "clawhub",
      "coding-agent",
      "asf-v4"  // Add this
    ]
  }
}
```

---

## Tools

### veto-check

Check if changes pass hard/soft veto rules.

```typescript
const result = await tools['veto-check']({
  changes: [
    { resourceType: 'contract', resourcePath: '/orders', action: 'update' }
  ],
  approvals: [
    { authority: 'architect', scope: 'contract:OpenAPI:*', status: 'approved' }
  ]
});

// Result:
// { passed: true/false, reason?: string, requiredRole?: string }
```

### ownership-proof

Generate verifiable ownership proofs.

```typescript
const result = await tools['ownership-proof']({
  resources: [
    { type: 'contract', path: '/orders#POST', format: 'openapi' }
  ],
  roles: [{ id: 'backend-team' }, { id: 'architect' }]
});

// Result:
// { proofs: [...], valid: true, invalidCount: 0 }
```

### economics-score

Compute role assignment economics score.

```typescript
const score = await tools['economics-score']({
  assignment: { taskToRole: { 'task-1': 'role-1', 'task-2': 'role-2' } },
  dag: { tasks: [...], edges: [...] },
  roles: [{ id: 'role-1', economics: { costPerTask: 1.0 } }]
});

// Result:
// { interfaceCost, bottleneck, skillMatch, parallelismGain, totalScore }
```

### interface-budget

Compute cross-role dependency cost.

```typescript
const budget = await tools['interface-budget']({
  roleId: 'backend-team',
  assignment: { taskToRole: {...} },
  dag: { tasks: [...], edges: [...] },
  roles: [...]
});

// Result:
// { baseCost, dependencyCost, totalCost, concurrentCap }
```

### rework-risk

Predict rework risk for tasks.

```typescript
const risk = await tools['rework-risk']({
  task: { id: 'task-1', featureId: 'feat-orders', risk: 'high' },
  contractChanges: [
    { contractId: 'api-orders', breaking: true, deprecated: false }
  ],
  historicalData: [...]
});

// Result:
// { score: 0.65, factors: ['Breaking change...'], mitigation: '...' }
```

### hot-contract

Analyze contract coupling and suggest role count.

```typescript
const analysis = await tools['hot-contract']({
  tasks: [
    { id: 'task-1', contractIds: ['api-orders', 'db-orders'] },
    { id: 'task-2', contractIds: ['api-orders'] }
  ],
  constraints: { kMin: 2, kMax: 8 }
});

// Result:
// { theoreticalMin, practicalMax, optimal, hotContracts, recommendation }
```

### conflict-resolve

Resolve ownership conflicts.

```typescript
const resolution = await tools['conflict-resolve']({
  resource: { id: 'api-orders', type: 'OpenAPI', path: '/orders' },
  conflictingRoles: [{ id: 'backend-team' }, { id: 'frontend-team' }],
  currentBudget: 80,
  budgetLimit: 100
});

// Result:
// { action: 'merge_roles' | 'introduce_contract', reason, contractCost }
```

### safe-optimize

Safe online optimization.

```typescript
const result = await tools['safe-optimize']({
  current: { roles: [...], assignment: {...} },
  metrics: {
    failureRate: 0.15,
    previewFailures: 1,
    queueLength: 10,
    utilization: 0.25,
    interfaceCost: 75,
    budget: 100
  },
  projectId: 'project-alpha'
});

// Result:
// { optimized, knobApplied, rolledBack, cooldownUntil }
```

---

## Commands

### asf:status

Check ASF V4.0 skill status.

```bash
asf:status
```

### asf:veto

Run veto check.

```bash
asf:veto --changes='[...]' --approvals='[...]'
```

### asf:proof

Generate ownership proof.

```bash
asf:proof --resources='[...]' --roles='[...]'
```

### asf:score

Calculate economics score.

```bash
asf:score --assignment='...' --dag='...' --roles='[...]'
```

### asf:risk

Predict rework risk.

```bash
asf:risk --task='...' --changes='[...]'
```

### asf:hot-contracts

Analyze hot contracts.

```bash
asf:hot-contracts --tasks='[...]'
```

---

## Configuration

Edit `config/asf-v4.config.yaml`:

```yaml
veto:
  mode: default  # default | strict | custom
  
economics:
  scoreWeights:
    interfaceCost: -0.30
    bottleneck: -0.20
    skillMatch: 0.20
    parallelismGain: 0.15
    reworkRisk: -0.15

optimizer:
  enabled: true
  cooldownMs: 1800000  # 30 minutes
  failureThreshold: 2
```

---

## Integration Phases

### Phase 1: Skill封装 (Current)

- [x] Skill index.ts
- [x] Tools definition
- [x] Commands definition
- [x] Configuration
- [ ] OpenClaw registration

### Phase 2: Agent OS Integration

- [ ] Memory Schema extension
- [ ] Agent Status extension
- [ ] Security Audit integration

### Phase 3: Production

- [ ] Performance testing
- [ ] Security audit
- [ ] Documentation

---

## API Reference

See [docs/ROLE-SYNTHESIZER-v0.9.0.md](../../docs/ROLE-SYNTHESIZER-v0.9.0.md) for detailed API.

---

## License

MIT License
