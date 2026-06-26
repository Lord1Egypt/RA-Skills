# D365 F&O Integrations

## OData

**Endpoint format:** `https://<env>.operations.dynamics.com/data/<EntityName>`

### Common operations:
```http
# GET records
GET /data/Customers?$top=10&$filter=contains(Name, 'Test')

# GET by key
GET /data/Customers(AccountNumber='DE-001')

# POST new record
POST /data/Customers
{ "AccountNumber": "NEW-001", "Name": "New Customer", ... }

# PATCH update
PATCH /data/Customers(AccountNumber='DE-001')
{ "Name": "Updated Name" }

# DELETE
DELETE /data/Customers(AccountNumber='DE-001')
```

### Authentication:
- Azure AD OAuth2 (client_credentials or auth code flow)
- Scope: `https://<env>.operations.dynamics.com/.default`
- Header: `Authorization: Bearer <token>`

### Batch operations:
```http
POST /$batch
Content-Type: multipart/mixed; boundary=batch_01

--batch_01
Content-Type: application/http
Content-Transfer-Encoding: binary

POST Customers HTTP/1.1
{ "AccountNumber": "BATCH-001" }

--batch_01--
```

## Custom Services

**Pattern:**
1. Create service class in X++ extending `SysServiceController`
2. Add methods with `[SysEntryPointAttribute]` and `[DataContractAttribute]`
3. Deploy as endpoint, accessible via SOAP/WCF
4. Call via `SYSaction()` on the service reference

```x++
[DataContract]
class MyIntegrationService
{
    [DataMember, SysEntryPointAttribute]
    public str ProcessOrder(str orderData)
    {
        // parse JSON/XML orderData
        // create SalesOrder
        return "Success";
    }
}
```

## DMF (Data Management Framework)

### REST API:
```http
POST /data/DataManagementDefinitionGroups/Microsoft.Dynamics.DataEntities.ImportFromPackage
Body: { "packageUrl": "<SAS URL>", "definitionGroupId": "DEF-GROUP-ID" }
```

### Programmatic (X++):
Use `DMFDataManagementService` to create import/export jobs, execute, and retrieve status.

### Key entities for common integrations:
- **Customers**: `Customers` entity
- **Sales orders**: `SalesOrderHeader` / `SalesOrderLine`
- **Vendors**: `Vendors`
- **Products**: `ReleasedProducts`
- **Inventory**: `InventOnHand`, `InventTransferOrder`
