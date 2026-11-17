# Software Engineering Conventions

# Coding Standard

Every SWE project must define in STANDARDS.md:
- language;
- language version;
- compiler/toolchain;
- coding standard;
- formatter;
- linter;
- static analyzer;
- test framework;
- quality thresholds.

# Recommended standards

For high-integrity embedded C:
- consider MISRA C as applicable depending on context.

For high-integrity C++:
- consider MISRA C++ as applicable depending on context.

Any deviation from a mandatory rule of the selected standard must be:
- justified;
- documented;
- reviewed;
- traceable.

For Python:
- PEP 8 as the default convention;
- docstrings per project convention;
- typing when it adds value.

For Java/Kotlin/JavaScript/TypeScript:
- use the official conventions or those of the selected framework;
- maintain a single convention across the project.

# Naming

Adapt the convention to the language.

## C / C++ default project convention

files:
lower_snake_case.c
lower_snake_case.cpp
lower_snake_case.h

functions:
lower_snake_case()

local variables:
lower_snake_case

constants/macros:
UPPER_SNAKE_CASE

types/classes:
PascalCase

boolean variables:
is_ready
has_error
can_start
should_retry

## Python

modules/functions/variables:
lower_snake_case

classes:
PascalCase

constants:
UPPER_SNAKE_CASE

## Java / Kotlin / JS / TypeScript

functions/variables:
lowerCamelCase

classes/types:
PascalCase

constants:
UPPER_SNAKE_CASE

# Naming quality

A name must express the role.

Avoid:
data1
tmp2
value
foo
doStuff
processData

except for extremely limited and obvious local variables.

Include the unit in the name when it reduces ambiguity:

timeout_ms
speed_rpm
voltage_v
sample_rate_hz

Do not mix several units under the same name.

# Functions

A function must:
- have a clear responsibility;
- have a name describing its intent;
- limit side effects;
- validate its inputs when necessary;
- explicitly handle relevant errors;
- remain of reasonable complexity.

Complex functions must be decomposed or explicitly justified.

The project may define thresholds for:
- cyclomatic complexity;
- length;
- nesting;
- number of parameters.

Thresholds are indicators, not targets to be artificially gamed.

# Documentation

Document at minimum the public APIs.

For a public or complex function, specify when relevant:
- purpose;
- inputs;
- outputs;
- units;
- preconditions;
- postconditions;
- side effects;
- errors;
- concurrency assumptions;
- ISR/thread context;
- timing constraints.

Comments mainly explain WHY.

Avoid comments that literally repeat the code.

Any comment that becomes false must be corrected along with the code.

# Architecture and source tree

The organization must reflect the architecture.

Embedded example:

src/
  application/
  domain/
  drivers/
  middleware/
  platform/

include/
tests/
  unit/
  integration/
tools/
config/
docs/

Do not apply this structure when the framework used has a more suitable native structure.

In that case:
- follow the framework;
- document the correspondence between the architecture and the directories.

# Dependency rules

Define the allowed dependencies between layers/modules.

Avoid:
- circular dependencies;
- uncontrolled cross-cutting access;
- uncontrolled shared globals;
- avoidable direct coupling.

# Quality checks

Before merge/release, apply depending on the project:
- compilation;
- warnings;
- formatter;
- lint;
- static analysis;
- unit tests;
- integration tests;
- regression tests;
- code review;
- dependency/security checks.

Critical warnings must not be silently ignored.

# Tests

Every substantial test must have an ID when traceability requires it.

Examples:
SWE-UT-0042
SWE-IT-0018
SWE-VT-0031

A test must specify:
- objective;
- inputs;
- preconditions;
- procedure or automation;
- expected result;
- actual result;
- PASS/FAIL;
- configuration;
- requirement links.

# Generated Code

Explicitly identify generated code.

Do not mechanically apply the same style rules to generated code and manual code.

The generation chain must be:
- versioned;
- reproducible;
- identifiable.

# Secrets

Never commit:
- passwords;
- tokens;
- API keys;
- private keys.

Use the secrets mechanisms provided by the environment.
