# CodeQL Reference: Python

## Import
```ql
import python
```

## Key Classes

| Class | Description |
|-------|-------------|
| `Function` | A Python function or method |
| `Call` | A function/method call |
| `Module` | A Python module |
| `Class` | A Python class |
| `Attribute` | An attribute access `obj.attr` |
| `ImportExpr` | An `import` statement |
| `StrConst` | String constant/literal |
| `Name` | A name reference (variable) |
| `Assign` | An assignment statement |

## Taint Tracking (Python)

```ql
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.dataflow.new.DataFlow
import semmle.python.Concepts
import DataFlow::PathGraph

class MyConfig extends TaintTracking::Configuration {
  MyConfig() { this = "MyConfig" }

  override predicate isSource(DataFlow::Node source) {
    // HTTP request data (Flask, Django, etc.)
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    // Define your dangerous sink
    exists(Call c |
      c.getFunc().(Attribute).getName() = "execute" and
      sink.asExpr() = c.getAnArg()
    )
  }
}
```

## Remote Sources (Python Web Frameworks)

```ql
import semmle.python.dataflow.new.RemoteFlowSources

// Automatically covers:
// Flask: request.args, request.form, request.json, request.data
// Django: request.GET, request.POST, request.body
// FastAPI: path/query/body parameters
```

## SQL Injection (Django ORM)

```ql
/**
 * @name SQL Injection via Django raw()
 * @description User input passed to Django's raw SQL interface
 * @kind path-problem
 * @problem.severity error
 * @id python/sql-injection-django
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.dataflow.new.RemoteFlowSources
import DataFlow::PathGraph

class DjangoSqlInjectionConfig extends TaintTracking::Configuration {
  DjangoSqlInjectionConfig() { this = "DjangoSqlInjectionConfig" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    exists(Call c, Attribute attr |
      attr = c.getFunc() and
      attr.getName() in ["raw", "extra", "RawSQL"] and
      sink.asExpr() = c.getArg(0)
    )
  }
}

from DjangoSqlInjectionConfig cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "SQL injection via Django raw query: input from $@.", source.getNode(), "this source"
```

## Command Injection (Python)

```ql
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.dataflow.new.RemoteFlowSources
import semmle.python.Concepts
import DataFlow::PathGraph

class CmdInjectionConfig extends TaintTracking::Configuration {
  CmdInjectionConfig() { this = "CmdInjectionConfig" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    // subprocess, os.system, os.popen
    sink instanceof SystemCommandExecution::Range
  }
}
```

## Common Patterns

```ql
// Find eval() calls with non-constant arguments
from Call call
where
  call.getFunc().(Name).getId() = "eval" and
  not call.getArg(0) instanceof StrConst
select call, "eval() called with non-constant argument"

// Find pickle.loads() (deserialization risk)
from Call call, Attribute attr
where
  attr = call.getFunc() and
  attr.getName() = "loads" and
  attr.getObject().(Name).getId() = "pickle"
select call, "Pickle deserialization — unsafe if input is untrusted"
```

## Tips

- Python CodeQL uses a newer API (`semmle.python.dataflow.new.*`) — prefer `new` over legacy
- For Flask specifically: `semmle.python.frameworks.Flask`
- For Django specifically: `semmle.python.frameworks.Django`
- AST nodes: use `AstNode.getLocation()` to get file/line info
- `ControlFlowNode` vs `AstNode`: taint tracking works on `DataFlow::Node`, not raw AST
