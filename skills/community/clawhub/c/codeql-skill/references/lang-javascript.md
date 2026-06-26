# CodeQL Reference: JavaScript / TypeScript

## Import
```ql
import javascript
```

TypeScript is fully supported — the same `javascript` import handles both.

## Key Classes

| Class | Description |
|-------|-------------|
| `Function` | Any function (arrow, named, anonymous) |
| `CallExpr` | A function call |
| `MethodCallExpr` | `obj.method()` call |
| `DataFlow::Node` | A node in the data flow graph |
| `HTTP::RequestNode` | An incoming HTTP request |
| `HTTP::ResponseNode` | An HTTP response |
| `Expr` | Any expression |
| `PropAccess` | Property access `obj.prop` |
| `StringLiteral` | A string literal `"hello"` |
| `TemplateLiteral` | Template literal `` `${x}` `` |

## Taint Tracking (JavaScript)

```ql
import javascript
import DataFlow::PathGraph

class MyConfig extends TaintTracking::Configuration {
  MyConfig() { this = "MyConfig" }

  override predicate isSource(DataFlow::Node source) {
    // Express.js request parameters
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    // Define your sink here
    sink instanceof ... 
  }
}
```

## Remote Sources (Node.js / Express)

```ql
// RemoteFlowSource automatically covers:
// Express: req.body, req.query, req.params, req.headers
// Koa: ctx.query, ctx.request.body
// Next.js: req.query, getServerSideProps params
// Any HTTP framework request input
```

## SQL Injection (Node.js)

```ql
/**
 * @name SQL Injection (Node.js)
 * @description User-controlled data reaches a SQL query string
 * @kind path-problem
 * @problem.severity error
 * @id js/sql-injection-node
 */

import javascript
import DataFlow::PathGraph

class SqlInjectionConfig extends TaintTracking::Configuration {
  SqlInjectionConfig() { this = "SqlInjectionConfig" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    // mysql / mysql2 .query() first argument
    exists(MethodCallExpr call |
      call.getMethodName() = "query" and
      sink = call.getArgument(0).flow()
    )
    or
    // pg (node-postgres) .query() first argument  
    exists(MethodCallExpr call |
      call.getMethodName() = "query" and
      sink = call.getArgument(0).flow()
    )
  }
}

from SqlInjectionConfig cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "SQL injection: user input flows from $@ to SQL query.", source.getNode(), "this source"
```

## XSS (DOM-based)

```ql
/**
 * @name DOM-based XSS
 * @description User input flows to a dangerous DOM sink
 * @kind path-problem
 * @problem.severity error
 * @id js/dom-based-xss
 */

import javascript
import semmle.javascript.security.dataflow.DomBasedXssQuery
import DataFlow::PathGraph

// DomBasedXss::Configuration is pre-built — use it directly
from DomBasedXss::Configuration cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "DOM XSS: user input from $@ flows to $@.", source.getNode(), "this source", sink.getNode(), "this sink"
```

## Command Injection (Node.js)

```ql
import javascript
import semmle.javascript.security.dataflow.CommandInjectionQuery
import DataFlow::PathGraph

from CommandInjection::Configuration cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "Command injection: input from $@ reaches shell command.", source.getNode(), "here"
```

## Prototype Pollution Pattern

```ql
import javascript

// Find assignments to __proto__ or computed property from user input
from AssignExpr assign, PropAccess prop
where
  prop = assign.getLhs() and
  prop.getPropertyName() = "__proto__"
select assign, "Possible prototype pollution via __proto__ assignment"
```

## Pre-built Security Query Modules (use these!)

```ql
// Instead of writing from scratch, import these:
import semmle.javascript.security.dataflow.SqlInjectionQuery
import semmle.javascript.security.dataflow.XssQuery
import semmle.javascript.security.dataflow.CommandInjectionQuery
import semmle.javascript.security.dataflow.PathTraversalQuery
import semmle.javascript.security.dataflow.ServerSideRequestForgeryQuery
import semmle.javascript.security.dataflow.CodeInjectionQuery
```

## Tips

- JS CodeQL handles dynamic features: `eval`, `Function()`, computed properties
- For React: JSX is analyzed; `dangerouslySetInnerHTML` is a known XSS sink
- TypeScript type annotations don't affect query logic — treat as JS
- `flow()` converts an `Expr` to a `DataFlow::Node`
- Template literals (`` ` `` ) count as taint propagators — CodeQL tracks them
