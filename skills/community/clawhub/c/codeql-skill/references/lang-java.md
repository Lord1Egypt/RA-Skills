# CodeQL Reference: Java / Kotlin

## Import
```ql
import java
```

## Key Classes

| Class | Description |
|-------|-------------|
| `Method` | A Java/Kotlin method |
| `MethodAccess` | A call to a method |
| `Class` | A Java class or interface |
| `Field` | A class field |
| `Parameter` | A method parameter |
| `ReturnStmt` | A return statement |
| `StringLiteral` | String literal value |
| `Annotation` | `@Override`, etc. |
| `Constructor` | Class constructor |

## Taint Tracking (Java)

```ql
import java
import semmle.code.java.dataflow.TaintTracking
import semmle.code.java.security.QueryInjection   // for SQL
import DataFlow::PathGraph

class SqlInjectionConfig extends TaintTracking::Configuration {
  SqlInjectionConfig() { this = "SqlInjectionConfig" }

  override predicate isSource(DataFlow::Node source) {
    // HTTP request parameters are sources
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    // JDBC execute calls are sinks
    exists(MethodAccess ma |
      ma.getMethod().getName() in ["execute", "executeQuery", "executeUpdate"] and
      ma.getMethod().getDeclaringType().hasQualifiedName("java.sql", "Statement") and
      sink.asExpr() = ma.getArgument(0)
    )
  }
}
```

## Common Remote Sources (Java)

```ql
import semmle.code.java.dataflow.FlowSources

// RemoteFlowSource covers:
// - HttpServletRequest.getParameter()
// - HttpServletRequest.getHeader()
// - Spring @RequestParam, @RequestBody, @PathVariable
// - JAX-RS @QueryParam, @PathParam
```

## SQL Injection (Full Example)

```ql
/**
 * @name SQL Injection
 * @description Unsanitized user input reaches a SQL query
 * @kind path-problem
 * @problem.severity error
 * @id java/sql-injection-custom
 */

import java
import semmle.code.java.dataflow.TaintTracking
import semmle.code.java.dataflow.FlowSources
import DataFlow::PathGraph

class SqlInjectionConfig extends TaintTracking::Configuration {
  SqlInjectionConfig() { this = "SqlInjectionConfig" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    exists(MethodAccess ma |
      ma.getMethod().getName().matches("execute%") and
      ma.getMethod().getDeclaringType()
        .hasQualifiedName("java.sql", ["Statement", "PreparedStatement"]) and
      sink.asExpr() = ma.getAnArgument()
    )
  }

  override predicate isSanitizer(DataFlow::Node node) {
    // PreparedStatement with parameterized queries is safe
    node.getType() instanceof TypeString and
    exists(MethodAccess ma |
      ma.getMethod().getName() = "prepareStatement" and
      node.asExpr() = ma.getArgument(0)
    )
  }
}

from SqlInjectionConfig cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "SQL injection: user input flows from $@ to SQL query.", source.getNode(), "here"
```

## XSS Pattern (Spring MVC)

```ql
import java
import semmle.code.java.dataflow.TaintTracking
import semmle.code.java.dataflow.FlowSources
import semmle.code.java.frameworks.spring.SpringWeb

class XssConfig extends TaintTracking::Configuration {
  XssConfig() { this = "XssConfig" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    exists(MethodAccess ma |
      ma.getMethod().getName() = "addAttribute" and
      sink.asExpr() = ma.getArgument(1)
    )
  }
}
```

## Useful Predicates

```ql
// Check if a method overrides one from a supertype
predicate overridesMethod(Method m, string className, string methodName) {
  m.overrides*(any(Method base |
    base.getDeclaringType().hasQualifiedName(_, className) and
    base.getName() = methodName
  ))
}

// Find serializable classes (deserialization risk)
predicate isSerializable(Class c) {
  c.getAnAncestor().hasQualifiedName("java.io", "Serializable")
}
```

## Tips

- Use `semmle.code.java.security.*` for pre-built security query modules
- `@SuppressWarnings` annotations can indicate developer awareness — check anyway
- For Android: import `semmle.code.java.frameworks.android.*`
- Kotlin code compiles to JVM bytecode — Java queries mostly work for Kotlin too
