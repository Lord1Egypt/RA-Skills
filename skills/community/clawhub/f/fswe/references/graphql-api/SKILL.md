# GraphQL API

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| language | string | en | en, id |
| depth | string | standard | quick, standard, deep |
| framework | string | apollo | apollo, mercurius, yoga |

## Checklist

### Schema Design
- [ ] Use descriptive type names (PascalCase)
- [ ] Use plural for collections (`users`, not `user`)
- [ ] Include `ID!` as primary key
- [ ] Use enums for fixed sets
- [ ] Add descriptions to all types and fields
- [ ] Design for client-driven queries, not DB shape
- [ ] Use input types for mutations
- [ ] Add `createdAt`, `updatedAt` to all types

### N+1 Prevention
- [ ] Use DataLoader for all relationship resolvers
- [ ] Batch database queries per request
- [ ] Never query inside a loop
- [ ] Use `include`/`select` for eager loading
- [ ] Monitor query count per request

```typescript
// DataLoader pattern
const userLoader = new DataLoader(async (ids: number[]) => {
  const users = await db.users.findByIds(ids);
  return ids.map(id => users.find(u => u.id === id));
});
```

### Resolvers
- [ ] Keep resolvers thin — delegate to services
- [ ] Validate input in mutations
- [ ] Return consistent error shapes
- [ ] Use `GraphQLError` with codes
- [ ] Never expose internal errors to clients

### Security
- [ ] Query depth limiting (max 10)
- [ ] Query complexity analysis
- [ ] Rate limit by query cost
- [ ] Introspection disabled in production
- [ ] Authentication on schema level, not resolver level
- [ ] Authorization per field

### Performance
- [ ] Cache at DataLoader level
- [ ] Use `@defer` / `@stream` for large responses
- [ ] Pagination with cursor-based approach
- [ ] Monitor resolver execution time

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Query in resolver loop | Use DataLoader batching |
| Exposing DB schema | Design schema for clients |
| No depth limit | Set max query depth |
| Introspection in prod | Disable it |
| Verbose error messages | Generic client errors, detailed logs |
