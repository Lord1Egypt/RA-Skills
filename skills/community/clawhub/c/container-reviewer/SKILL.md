# dockerfile-reviewer

## Description
Review Dockerfiles and docker-compose files for security vulnerabilities, oversized images, build inefficiencies, and missing best practices. Returns a structured report with severity ratings and corrected examples.

## Use when
- "review my Dockerfile"
- "is this container secure"
- "optimize my docker build"
- "why is my image so large"
- "check my docker-compose"
- Any Dockerfile, docker-compose.yml, or .dockerignore

## Input
Paste the Dockerfile and/or docker-compose.yml. Optionally specify:
- Target environment (production, CI, local dev)
- Base image constraints (must use specific distro, etc.)
- Whether the app runs as a service or a one-shot job

## Output format

```
## Dockerfile Review

### Critical (fix before production)
- [Finding] — [security or correctness risk]
  ✗ Before: [problematic line(s)]
  ✓ After:  [corrected line(s)]

### Warnings (should fix)
- [Finding] — [size or reliability impact]

### Suggestions (nice to have)
- [Finding] — [explanation]

### What's correct
- [Specific patterns done right]

### Summary
[2–3 sentences: biggest risk, estimated image size savings if any, top fix]
```

## Review checklist

### Security
- Running as `root` (no `USER` directive) — container escape risk
- Secret or credential in `ENV`, `ARG`, or `RUN` layer — visible in image history
- Base image not pinned (`FROM ubuntu:latest` instead of `ubuntu:22.04`) — supply chain risk
- Using `curl | bash` to install software — arbitrary code execution
- Unnecessary packages installed (attack surface)
- No `HEALTHCHECK` — orchestrator can't detect unhealthy containers
- Writable filesystem where read-only would suffice

### Image size
- Large base image when `alpine` or `distroless` would work
- Installing dev tools in production image (compilers, debuggers, test frameworks)
- Multiple `RUN` commands that should be chained with `&&` (each RUN = a layer)
- `COPY . .` before dependency install (cache busting on every code change)
- Not using `.dockerignore` — copying node_modules, .git, build artifacts
- Leftover apt/apk cache not cleaned in same RUN layer

### Build correctness
- Wrong `WORKDIR` — files land in unexpected paths
- `EXPOSE` port doesn't match what the app actually listens on
- `CMD` vs `ENTRYPOINT` confusion — CMD should be overridable args, ENTRYPOINT the executable
- Using `ADD` when `COPY` is sufficient (`ADD` has implicit tar extraction and URL fetch)
- Build args used as secrets (visible in `docker history`)

### docker-compose specific
- No `restart` policy — containers don't recover from crashes
- Hardcoded secrets in `environment:` block — use `.env` or secrets
- Named volumes not defined in `volumes:` section
- Port binding to `0.0.0.0` when `127.0.0.1` would suffice
- No resource limits (`mem_limit`, `cpus`) — one container can starve others
- Depends_on without `condition: service_healthy` — race conditions on startup

### Multi-stage build
- Single-stage build for compiled language — ships compiler in production image
- Build artifacts not properly copied from builder stage
- Redundant stages that could be merged

## Severity definitions
- **Critical:** Security vulnerability or correctness bug that affects production
- **Warning:** Image bloat, reliability issue, or hard-to-debug behavior
- **Suggestion:** Style, caching efficiency, or future-proofing improvement

## Self-improvement instructions
After each review, note the most impactful finding. After 20 reviews, surface "Top 3 Dockerfile mistakes" at the start of the response.
