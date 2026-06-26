# CodeQL Reference: C / C++

## Import
```ql
import cpp
```

## Key Classes

| Class | Description | Example Usage |
|-------|-------------|---------------|
| `Function` | Any function/method | `f.getName() = "malloc"` |
| `FunctionCall` | A call expression | `call.getTarget()` |
| `Expr` | Any expression | `e.getType()` |
| `Variable` | Local/global variable | `v.getType() instanceof PointerType` |
| `ArrayExpr` | Array access `a[i]` | `a.getArrayOffset()` |
| `PointerDereferenceExpr` | `*ptr` | dereference checks |
| `AllocationExpr` | `malloc`, `new` | memory tracking |
| `DeallocationExpr` | `free`, `delete` | use-after-free |
| `BufferWriteExpr` | `strcpy`, `memcpy` | buffer overflow |

## Common Predicates

```ql
// Find calls to dangerous C functions
predicate isDangerousCall(FunctionCall call) {
  call.getTarget().getName() in [
    "gets", "strcpy", "strcat", "sprintf", "scanf"
  ]
}

// Find functions that take user-controlled size
predicate hasDynamicSize(AllocationExpr alloc) {
  not alloc.getSizeExpr() instanceof Literal
}
```

## Taint Tracking (C/C++)

```ql
import semmle.code.cpp.dataflow.TaintTracking
import semmle.code.cpp.security.Security

// Common sources: argv, environment variables, file reads
class UserControlledSource extends DataFlow::Node {
  UserControlledSource() {
    // argv parameters
    exists(Parameter p |
      p.getFunction().getName() = "main" and
      p.getIndex() = 1 and
      this.asExpr() = p.getAnAccess()
    )
    or
    // getenv() calls
    exists(FunctionCall c |
      c.getTarget().getName() = "getenv" and
      this.asExpr() = c
    )
  }
}
```

## Buffer Overflow Pattern

```ql
import cpp

from FunctionCall call, Expr dest, Expr src
where
  call.getTarget().getName() = "strcpy" and
  dest = call.getArgument(0) and
  src = call.getArgument(1) and
  // Source is not a string literal of known safe length
  not src instanceof StringLiteral
select call, "Potential buffer overflow: strcpy with non-literal source $@", src, src.toString()
```

## Use-After-Free Pattern

```ql
import cpp
import semmle.code.cpp.dataflow.DataFlow

// Track allocations through to deallocation and subsequent use
from AllocationExpr alloc, DeallocationExpr dealloc, VariableAccess use
where
  DataFlow::localFlow(DataFlow::exprNode(alloc), DataFlow::exprNode(dealloc.getFreedExpr())) and
  DataFlow::localFlow(DataFlow::exprNode(alloc), DataFlow::exprNode(use)) and
  use.getLocation().getStartLine() > dealloc.getLocation().getStartLine()
select use, "Use after free: memory allocated at $@ freed at $@",
  alloc, alloc.toString(), dealloc, dealloc.toString()
```

## Useful Tips

- Use `GlobalValueNumbering` for tracking values across assignments
- `dominates(b1, b2)` checks control flow dominance
- For pointer arithmetic: `PointerArithmeticExpr`
- For integer overflow: `semmle.code.cpp.security.Overflow`
- For format strings: `semmle.code.cpp.security.FormatString`
