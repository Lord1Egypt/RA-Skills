# CodeQL Debugging Guide

## Common Compilation Errors

### 1. "Type mismatch"
```
ERROR: Expected type X, but got Y
```
**Fix**: Check that you're not mixing `Expr` with `DataFlow::Node`. Convert with:
- `DataFlow::exprNode(expr)` → `DataFlow::Node`
- `node.asExpr()` → `Expr`

### 2. "No such predicate"
```
ERROR: No such predicate: Foo::bar/1
```
**Fix**: Check your import. For example, `RemoteFlowSource` requires:
- Java: `import semmle.code.java.dataflow.FlowSources`
- Python: `import semmle.python.dataflow.new.RemoteFlowSources`
- JS: automatically available with `import javascript`

### 3. "Ambiguous name"
```
ERROR: Ambiguous type name: Configuration
```
**Fix**: Qualify the name:
```ql
class MyConf extends TaintTracking::Configuration { ... }
// NOT: class MyConf extends Configuration { ... }
```

### 4. "Predicate body has no result"
```
WARNING: Predicate always returns empty result
```
**Fix**: Your `isSource` or `isSink` predicate is never satisfied. See "No Results" below.

---

## No Results

When a taint tracking query returns nothing:

### Step 1 — Check sources independently
```ql
// Temporarily: does this find ANY sources?
from DataFlow::Node source
where source instanceof RemoteFlowSource
select source, "Found source"
```
If this returns nothing → your source definition is wrong.

### Step 2 — Check sinks independently  
```ql
// Temporarily: does this find ANY sinks?
from DataFlow::Node sink
where /* your isSink condition */ ...
select sink, "Found sink"
```
If this returns nothing → your sink definition is wrong.

### Step 3 — Check if flow exists between simple pairs
Use `DataFlow::localFlow` first (easier than full taint tracking):
```ql
from DataFlow::Node a, DataFlow::Node b
where DataFlow::localFlow(a, b)
  and /* your source condition on a */
  and /* your sink condition on b */
select a, b
```

### Step 4 — Add partial flow debugging
```ql
// Find what nodes ARE reachable from your source
from MyConfig cfg, DataFlow::Node source, DataFlow::Node reached
where 
  cfg.isSource(source) and
  cfg.hasFlow(source, reached)
select reached, "Reachable from source"
```

---

## Too Many Results (False Positives)

### Add sanitizer conditions
```ql
override predicate isSanitizer(DataFlow::Node node) {
  // Data has been validated/escaped
  exists(MethodAccess ma |
    ma.getMethod().getName() in ["escapeHtml", "sanitize", "encode"] and
    node.asExpr() = ma
  )
}
```

### Restrict source scope
```ql
// Too broad:
override predicate isSource(DataFlow::Node source) {
  source instanceof RemoteFlowSource
}

// More specific (only certain endpoints):
override predicate isSource(DataFlow::Node source) {
  source instanceof RemoteFlowSource and
  exists(Method m | 
    source.getEnclosingCallable() = m and
    m.hasAnnotation("org.springframework.web.bind.annotation", "PostMapping")
  )
}
```

### Filter by location or class
```ql
// Exclude test files
where not source.getFile().getRelativePath().matches("%test%")
```

---

## Query Performance Issues

If a query is timing out or very slow:

1. **Avoid `any()`** in hot paths — it forces full enumeration
2. **Use `exists()` instead of joins** for existence checks
3. **Bind early**: put the most selective predicates first in `where`
4. **Use `pragma[inline]`** for predicates called many times:
   ```ql
   pragma[inline]
   predicate isInteresting(Expr e) { ... }
   ```
5. **Avoid `+` and `*` closure on large relations** (very expensive)

---

## Checking CodeQL Version Compatibility

Some APIs differ between CodeQL versions:

| Feature | Old API | New API (preferred) |
|---------|---------|---------------------|
| Python taint | `semmle.python.security.*` | `semmle.python.dataflow.new.*` |
| JS taint source | `HTTP::RequestInputAccess` | `RemoteFlowSource` |
| C++ dataflow | `DataFlow::Configuration` | `DataFlow::Configuration` (same) |

Always check: https://codeql.github.com/docs/codeql-language-guides/

---

## Useful Debug Predicates

```ql
// Print location of any node
select node, node.getLocation().toString()

// Count results per file
select count(DataFlow::Node n | /* your condition */ | n), "nodes found"

// Find what type something actually is
select e, e.getType().toString(), e.getType().getQualifiedName()
```
