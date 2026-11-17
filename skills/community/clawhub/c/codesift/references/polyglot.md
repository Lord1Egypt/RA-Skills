# Go, JVM, shell, SQL migrations and infrastructure review

Use this guide for review units without a dedicated language guide. Read
patterns.md for reachability, redundancy, gates and cross-boundary contracts.
The helpers detect Go and JVM units but have no dependency reader for them;
collect_facts.sh lists such languages under dependency_languages_without_reader.

## Go

**Behavior.** Check every returned error: ignored errors, `err` shadowed by `:=`
in an inner scope, and `defer x.Close()` placed before the error check. An
interface holding a nil pointer is not nil. Trace goroutine lifetimes: a send
with no receiver, a missing `ctx.Done()` case or a channel nobody closes leaks
the goroutine. `defer` inside a loop holds resources until the function returns.
Since Go 1.22 each `for` iteration has its own loop variable, but only in modules
whose go.mod declares go 1.22 or later.

**Concurrency.** Concurrent map writes crash the process. Call `sync.WaitGroup.Add`
before starting the goroutine, not inside it. Run `go test -race` on packages with
shared state; it reports only races on paths the run executes.

**Unused code.** `deadcode` and staticcheck U1000 nominate candidates (see
patterns.md). Check build constraints (`//go:build`), GOOS/GOARCH variants,
exported identifiers with external importers, `go:linkname`, reflection, cgo and
plugin builds before calling code unused.

**Dependencies.** Read go.mod `replace` directives (local paths and forks),
`retract` and `toolchain` lines, vendoring (`vendor/modules.txt`) and the
GOPROXY, GOPRIVATE and GONOSUMDB settings in effect; `go list -m all` gives the
resolved module graph. Mirrors such as goproxy.cn are common in mainland China.

**Validation.** The helper's adapter runs `go test -count=1 -json ./...` with
GOPROXY=off: it never downloads modules, and -count=1 bypasses the test cache so
the counts come from a fresh run. Populate the module cache first through the
project's normal workflow; a missing module is reported as an environment failure.
Use --command for build tags, integration packages or `-race`.

## JVM: Java, Kotlin and Scala

**Behavior.** Look for swallowed exceptions (`catch (Exception e) {}`),
`Optional.get()` without a presence check, inconsistent `equals`/`hashCode`
pairs, mutable static state, executors that are never shut down and
`CompletableFuture` failures that nobody joins. In Kotlin, catching `Exception`
inside a coroutine also catches `CancellationException` and breaks cancellation;
`GlobalScope` escapes structured concurrency. With Spring's proxy-based AOP,
`@Transactional` and similar annotations do not apply to self-invocation or
private methods.

**Unused code.** Dependency injection (component scanning, `@Bean`), ServiceLoader
files under META-INF/services, annotation processors, JPA entities, serialization
frameworks, JNI and servlet descriptors create uses without a direct call. Treat
IDE and compiler unused warnings as candidates.

**Dependencies.** By default Maven resolves version conflicts by nearest
declaration and Gradle by highest version, so the declared version may not be
the resolved one; use `mvn dependency:tree` or `gradle dependencyInsight`. Check
repositories and mirrors in pom.xml, settings.xml and Gradle repository blocks.

**Validation.** There is no automatic adapter. Surefire and Gradle write one JUnit
XML file per test class, while the helper reads one fresh file at {report}: wrap
the run in a script that merges those files into {report}, or count them yourself
and record how. Treat each module of a multi-module build as its own unit and
check that its tests ran.

## Shell scripts

`set -e` does not apply inside conditions, `&&`/`||` lists or functions called
from them; `local x=$(cmd)` hides the failure of `cmd`; without `pipefail` a
pipeline reports only its last command. Quote expansions: `rm -rf "$dir/"` with
an empty `dir` targets `/`. Check `cd` failures, temporary files created with
`mktemp` and removed by a `trap`, and `#!/bin/sh` scripts that use bash features.
ShellCheck output is a candidate list. In CI scripts, also check exit-status
handling around `xargs`, `find -exec` and `tee`.

## SQL migrations

Compare migrations with ORM models and raw SQL, using the project's tooling where
it exists (patterns.md lists examples). Check:

- rolling-deploy compatibility: old and new code must both work against the
  schema at every step (expand, migrate, contract);
- a NOT NULL column added without a default fails or receives implicit values
  depending on the database, and some changes rewrite or lock a large table;
- PostgreSQL's `CREATE INDEX CONCURRENTLY` cannot run inside a transaction, which
  many migration runners open by default;
- branching histories (several Alembic heads, conflicting Django migrations),
  edits to already-applied migrations (Flyway validates checksums), irreversible
  down steps and data migrations that are not idempotent.

Read database-systems.md for storage-engine and durability questions.

## Infrastructure as code and CI

- **Terraform:** `lifecycle` settings such as `ignore_changes` that hide drift,
  `count`/`for_each` key changes that recreate resources, unpinned provider and
  module versions, state locking and sensitive outputs. Never run `apply`; `plan`
  reads live state with real credentials, so run it only when the user authorizes
  that access.
- **Kubernetes and Helm:** liveness probes that depend on downstream services
  (restart cascades), missing readiness checks, resource requests or limits,
  mutable image tags, RBAC wildcards, and ConfigMap or Secret keys referenced but
  not defined. A Helm value that is referenced but unset renders empty without
  failing unless the template uses `required`.
- **Containers:** unpinned base images, secrets in build arguments or layers,
  root users, and a missing .dockerignore that copies the repository into the image.
- **CI:** apply the gate procedure in patterns.md. Also check `pull_request_target`
  workflows that check out untrusted pull-request code with secrets available,
  third-party actions pinned to a branch instead of a commit SHA, and cache keys
  that let stale artifacts satisfy a check.
