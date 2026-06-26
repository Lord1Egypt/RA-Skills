# Reusable Templates

Use these templates when preparing high-impact database changes.

## Migration Preflight Template

```markdown
# Migration Preflight

## Change Summary
- Migration id:
- Owner:
- Target environments:
- Planned window:

## Scope
- Tables and entities affected:
- Estimated row impact:
- Expected lock behavior:

## Rollback
- Rollback owner:
- Rollback trigger conditions:
- Rollback steps:

## Verification
- Pre-check queries:
- Post-check queries:
- Success criteria:
```

## Destructive Operation Checklist

```markdown
# Destructive Operation Checklist

- [ ] Environment confirmed
- [ ] Table and predicate confirmed
- [ ] Baseline row count captured
- [ ] Backup freshness confirmed
- [ ] Explicit user confirmation captured
- [ ] Rollback path documented
- [ ] Verification query ready
```

## Restore Drill Record

```markdown
# Restore Drill Record

- Date:
- System:
- Backup snapshot id:
- Start time:
- Finish time:
- Measured restore duration:
- RTO met (yes/no):
- RPO met (yes/no):
- Validation query results:
- Follow-up actions:
```
