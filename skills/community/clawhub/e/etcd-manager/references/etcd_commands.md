# etcd Commands Reference

## Basic Commands

### Version
```bash
etcdctl version
```

### Endpoint Health
```bash
etcdctl --endpoints="http://localhost:2379" endpoint health
```

### Member List
```bash
etcdctl --endpoints="http://localhost:2379" member list
```

## Key-Value Operations

### Put (Create/Update)
```bash
etcdctl --endpoints="http://localhost:2379" put /key value
```

### Get (Read)
```bash
# Get specific key
etcdctl --endpoints="http://localhost:2379" get /key

# Get with prefix
etcdctl --endpoints="http://localhost:2379" get /prefix --prefix

# Get keys only
etcdctl --endpoints="http://localhost:2379" get /prefix --prefix --keys-only

# Get with limit
etcdctl --endpoints="http://localhost:2379" get /prefix --prefix --limit=10
```

### Delete
```bash
# Delete specific key
etcdctl --endpoints="http://localhost:2379" del /key

# Delete with prefix
etcdctl --endpoints="http://localhost:2379" del /prefix --prefix
```

## Watch Operations

### Watch Key
```bash
etcdctl --endpoints="http://localhost:2379" watch /key
```

### Watch with Prefix
```bash
etcdctl --endpoints="http://localhost:2379" watch /prefix --prefix
```

## Lease Operations

### Grant Lease
```bash
# Grant 60 second lease
etcdctl --endpoints="http://localhost:2379" lease grant 60

# Put with lease
etcdctl --endpoints="http://localhost:2379" put /key value --lease=1234abcd
```

### Keep Alive
```bash
etcdctl --endpoints="http://localhost:2379" lease keep-alive 1234abcd
```

### Revoke Lease
```bash
etcdctl --endpoints="http://localhost:2379" lease revoke 1234abcd
```

## TLS Configuration

### With TLS
```bash
etcdctl \
  --endpoints="https://etcd.example.com:2379" \
  --cacert=/path/to/ca.crt \
  --cert=/path/to/client.crt \
  --key=/path/to/client.key \
  get /key
```

## Environment Variables

### API Version
```bash
# For etcdctl v3.6.1+, no need to set ETCDCTL_API
# For older versions:
export ETCDCTL_API=3
```

### Endpoints
```bash
export ETCDCTL_ENDPOINTS="http://localhost:2379"
```

## Common Patterns

### Backup Key Before Modification
```bash
# Always backup before put
OLD_VALUE=$(etcdctl --endpoints="$ENDPOINTS" get "$KEY" 2>/dev/null || echo "")
etcdctl --endpoints="$ENDPOINTS" put "$KEY" "$NEW_VALUE"
```

### Safe Delete
```bash
# Backup before delete
BACKUP=$(etcdctl --endpoints="$ENDPOINTS" get "$KEY" 2>/dev/null || echo "")
etcdctl --endpoints="$ENDPOINTS" del "$KEY"
```

### Batch Operations
```bash
# Using xargs for batch operations
etcdctl --endpoints="$ENDPOINTS" get /prefix --prefix --keys-only | \
  xargs -I {} etcdctl --endpoints="$ENDPOINTS" get {}
```

## Error Handling

### Check if Key Exists
```bash
if etcdctl --endpoints="$ENDPOINTS" get "$KEY" >/dev/null 2>&1; then
    echo "Key exists"
else
    echo "Key does not exist"
fi
```

### Handle Connection Errors
```bash
if ! etcdctl --endpoints="$ENDPOINTS" endpoint health >/dev/null 2>&1; then
    echo "Error: Cannot connect to etcd at $ENDPOINTS"
    exit 1
fi
```

## Performance Tips

1. **Use --prefix for batch operations**
2. **Set appropriate timeouts for production**
3. **Use TLS for secure connections**
4. **Monitor etcd metrics regularly**
5. **Keep etcd version up to date**