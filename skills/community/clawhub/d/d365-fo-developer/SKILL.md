---
name: d365-fo-developer
description: "Comprehensive D365 Finance & Operations development assistant covering X++, customizations, integrations, data entities, DMF, security, and deployment. Use when the user needs help with: (1) Writing X++ code and customizations, (2) D365 F&O integrations (OData, Custom Services, DMF), (3) Data entities and export/import jobs, (4) Security (XDS, Record Level Security), (5) Build/CI/CD in Azure DevOps and LCS, (6) Migration from AX 2009/2012 to D365 F&O."
---

# D365 F&O Developer

## Quick Reference

### X++ Development

**Key patterns:**
- Use `select` vs `while select` appropriately — `select` for single record, `while select` for batch
- Always use `ttsBegin` / `ttsCommit` for transactional writes
- Prefer `SysDictTable` / `SysDictField` over raw schema queries
- Use `buf2Buf()` for record copying, `DictField::extendedFieldType()` for EDT lookups

**Common snippets:**

```x++
// Select with field list (avoid SELECT *)
select Field1, Field2 from myTable where myTable.RecId == _recId;

// While select with joins
while select myTable
    join myTable2 where myTable2.RefRecId == myTable.RecId
{
    // process
}

// Insert with initFrom
myTable2.initFrom(myTable);
myTable2.FieldX = value;
myTable2.insert();
```

### Data Entities

- **OData endpoint**: `/data/<EntityName>` — supports CRUD via GET/POST/PATCH/DELETE
- **DMF (Data Management Framework)**:
  - Export: Create data project → Add entity → Export to CSV/Excel/Package
  - Import: Upload file → Map fields → Import
  - Programmatic: Use `DMFDataManagementService` or OData `/data/DataManagementDefinitionGroups`
- **Key entity patterns**: `DataEntity`, `SysDataEntity`, custom entities via `DataEntityAttribute`

### Integrations

See [references/integrations.md](references/integrations.md) for detailed OData, Custom Services, and DMF patterns.

- **OData**: Standard REST endpoint. Auth via AAD. Service endpoint: `https://<env>.operations.dynamics.com/api/services/UserSessionService/AifUserSessionService`
- **Custom Services**: X++ service classes exposed as SOAP/WCF endpoints. Use `SysServiceController` for data operations
- **DMF**: Best for bulk data. REST endpoint `/data/DataManagementDefinitionGroups/Microsoft.Dynamics.DataEntities.ImportFromPackage`

### Security

See [references/security.md](references/security.md) for XDS and Record Level Security details.

- **XDS (Extensible Data Security)**: Role-based row-level filtering. Constraint-based policies applied via AOT
- **Record Level Security**: Similar to XDS but applies at the record level per user/role
- **Duties & Privileges**: Granular permission items. Map to menu items and service operations

### Build & Deploy

**Hotfix/ISV deployment:**
1. Export model from Dev environment
2. Deploy model package to Build environment
3. Run full build pipeline
4. Generate deployable package via LCS

**CI/CD with Azure DevOps:**
- Use D365 F&O Build Automation tasks
- X++ compilation via `xppc.exe`
- Unit tests via SysTest framework

## Error Handling Patterns

```x++
try
{
    ttsBegin;
    // transactional logic
    ttsCommit;
}
catch (Exception::Error)
{
    ttsAbort;
    throw error("Descriptive error message");
}
```

## Performance Tips

- Avoid `SELECT *` — always specify field lists
- Use `setTimeout(DB_TIMEOUT)` for long-running queries
- Prefer `insert_recordset` / `update_recordset` over row-by-row operations
- Index hint via `index` keyword when table is large

## References

For detailed guides, read these files as needed:
- [Integrations](references/integrations.md) — OData, Custom Services, DMF deep dive
- [Security](references/security.md) — XDS, RLS, Duties & Privileges
