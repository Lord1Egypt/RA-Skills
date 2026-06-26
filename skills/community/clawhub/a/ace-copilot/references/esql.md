# IBM ACE ESQL Reference

## What is ESQL?

ESQL (Extended SQL) is ACE's proprietary scripting language used in Compute, Filter, and Database nodes. It operates on the logical message tree, enabling message transformation, routing logic, and database interaction.

---

## Message Tree Structure

Every message in ACE has a logical tree:

```
Root
├── Properties        — message metadata (domain, encoding, CCSID)
├── HTTPInputHeader   — HTTP headers (for HTTP flows)
├── MQMD              — MQ message descriptor (for MQ flows)
├── MQRFH2            — MQ RFH2 header
├── LocalEnvironment  — flow-local data (routing destinations, etc.)
├── Environment       — shared persistent data across nodes
└── Body              — the actual message content
    └── XMLNSC / JSON.Data / BLOB.Data / ...
```

Key references in ESQL:
- `InputRoot` — incoming message (read-only)
- `OutputRoot` — outgoing message (writable)
- `InputLocalEnvironment` — incoming local env
- `OutputLocalEnvironment` — outgoing local env
- `Environment` — shared across nodes in the same flow instance

---

## ESQL File Structure

```esql
BROKER SCHEMA com.example.myapp

CREATE COMPUTE MODULE MyFlow_Compute
  CREATE FUNCTION Main() RETURNS BOOLEAN
  BEGIN
    -- Copy all input to output (default passthrough)
    SET OutputRoot = InputRoot;

    -- Your transformation logic here

    RETURN TRUE;
  END;
END MODULE;
```

- `BROKER SCHEMA` — namespace for this ESQL file
- `CREATE COMPUTE MODULE` — module name must match the node's module property
- `Main()` — mandatory entry point; return TRUE to propagate to Out terminal

---

## Common ESQL Operations

### Copy Input to Output (Passthrough)
```esql
SET OutputRoot = InputRoot;
```

### Read XML Field
```esql
DECLARE myValue CHARACTER;
SET myValue = InputRoot.XMLNSC.RootElement.ChildElement;
```

### Set Output Field
```esql
SET OutputRoot.XMLNSC.Response.Status = 'OK';
SET OutputRoot.XMLNSC.Response.Code = 200;
```

### Read JSON Field
```esql
DECLARE amount DECIMAL;
SET amount = InputRoot.JSON.Data.payment.amount;
SET OutputRoot.JSON.Data.result = amount * 1.1;
```

### Build JSON Output from Scratch
```esql
SET OutputRoot.Properties.ContentType = 'application/json';
DELETE FIELD OutputRoot.JSON;
SET OutputRoot.JSON.Data.status = 'success';
SET OutputRoot.JSON.Data.transactionId = InputRoot.JSON.Data.id;
```

### String Concatenation
```esql
SET OutputRoot.XMLNSC.Message.Text = 'Hello, ' || InputRoot.XMLNSC.Request.Name;
```

### Conditional Logic
```esql
IF InputRoot.JSON.Data.amount > 1000 THEN
  SET OutputRoot.JSON.Data.category = 'HIGH_VALUE';
ELSEIF InputRoot.JSON.Data.amount > 100 THEN
  SET OutputRoot.JSON.Data.category = 'MEDIUM';
ELSE
  SET OutputRoot.JSON.Data.category = 'LOW';
END IF;
```

### Loops
```esql
DECLARE i INTEGER 1;
WHILE i <= CARDINALITY(InputRoot.XMLNSC.Items.Item[]) DO
  -- Process each item
  SET OutputRoot.XMLNSC.Results.Result[i].Value =
    InputRoot.XMLNSC.Items.Item[i].Value;
  SET i = i + 1;
END WHILE;
```

### FOR loop over repeated elements
```esql
FOR item AS InputRoot.XMLNSC.Items.Item[] DO
  -- item is a reference to each element
  SET OutputRoot.XMLNSC.Results.Result[LAST].Name = item.Name;
END FOR;
```

---

## ESQL Functions

### String Functions
| Function | Description |
|----------|-------------|
| `LENGTH(str)` | String length |
| `SUBSTRING(str FROM pos FOR len)` | Substring extraction |
| `UPPER(str)` / `LOWER(str)` | Case conversion |
| `TRIM(str)` | Remove whitespace |
| `REPLACE(str, find, replace)` | String replacement |
| `CONTAINS(str, substr)` | Check containment |
| `POSITION(substr IN str)` | Find position |

### Date/Time Functions
| Function | Description |
|----------|-------------|
| `CURRENT_DATE` | Today's date |
| `CURRENT_TIME` | Current time |
| `CURRENT_TIMESTAMP` | Current timestamp |
| `CAST(val AS DATE)` | Type conversion |

### Math Functions
| Function | Description |
|----------|-------------|
| `ABS(n)` | Absolute value |
| `ROUND(n, places)` | Rounding |
| `MOD(n, m)` | Modulo |
| `POWER(base, exp)` | Exponentiation |

### Type Casting
```esql
CAST(InputRoot.JSON.Data.amount AS DECIMAL)
CAST(InputRoot.XMLNSC.Date.Value AS DATE FORMAT 'yyyy-MM-dd')
CAST(myTimestamp AS CHARACTER FORMAT 'yyyy-MM-dd HH:mm:ss')
```

---

## Database Access in ESQL

### SELECT (lookup)
```esql
DECLARE refData ROW;
SELECT T.Description INTO refData
FROM Database.MYSCHEMA.LOOKUP_TABLE AS T
WHERE T.CODE = InputRoot.JSON.Data.code;

SET OutputRoot.JSON.Data.description = refData.Description;
```

### INSERT
```esql
INSERT INTO Database.MYSCHEMA.AUDIT_LOG (TXN_ID, STATUS, CREATED_AT)
VALUES (InputRoot.JSON.Data.txnId, 'PROCESSED', CURRENT_TIMESTAMP);
```

### UPDATE
```esql
UPDATE Database.MYSCHEMA.TRANSACTIONS AS T
SET T.STATUS = 'COMPLETE'
WHERE T.TXN_ID = InputRoot.JSON.Data.txnId;
```

---

## Filter Node ESQL

Filter nodes return TRUE (propagate via Out) or FALSE (propagate via Alternate):

```esql
CREATE FILTER MODULE MyFlow_Filter
  CREATE FUNCTION Main() RETURNS BOOLEAN
  BEGIN
    RETURN InputRoot.JSON.Data.amount > 1000;
  END;
END MODULE;
```

---

## Error Handling in ESQL

```esql
BEGIN
  -- risky operation
  SET OutputRoot.XMLNSC.Result = InputRoot.XMLNSC.Data.Value;
EXCEPTION
  WHEN OTHERS THEN
    SET OutputRoot.XMLNSC.Error.Message = 'Transformation failed';
    SET OutputRoot.XMLNSC.Error.Details = MESSAGE_TEXT();
    PROPAGATE TO TERMINAL 'failure';
    RETURN FALSE;
END;
```

---

## LocalEnvironment for Routing

Used by `RouteToLabel` and destination routing:

```esql
-- Set dynamic routing destination
SET OutputLocalEnvironment.Destination.RouterList.DestinationData[1].labelName = 'TargetA';
```

---

## ESQL Best Practices

1. Always `SET OutputRoot = InputRoot` first for transforms that modify (not replace) the message
2. Use `DELETE FIELD` to remove unwanted fields before building output
3. Use `CARDINALITY()` to get array length before iterating
4. Use `COALESCE(expr, default)` for null-safe field access
5. Declare variables near their usage, not all at the top
6. Use meaningful module and variable names that match the flow logic
7. For JSON output, always set `ContentType` in Properties
8. Wrap database operations in EXCEPTION handlers
