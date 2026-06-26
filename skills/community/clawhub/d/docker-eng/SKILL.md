---
name: docker-eng
description: Deep Docker workflow—image design, multi-stage builds, security, runtime config, health checks, and operations. Use when containerizing apps, hardening images, or debugging container behavior in CI and production.
---

# Docker Eng — Deep Workflow

Containers package applications with their dependencies. Optimize for **small**, **reproducible** images and **clear** runtime contracts—not “SSH into a mini VM.”

## When to Offer This Workflow

**Trigger conditions:**

- Authoring Dockerfiles for apps or CI
- CVEs in base images; accidental secrets in layers
- Slow builds or oversized images pushing registry costs

**Initial offer:**

Use **six stages**: (1) base image & supply chain, (2) Dockerfile structure, (3) runtime config & secrets, (4) security hardening, (5) health & observability, (6) ops & debugging). Confirm registry and orchestrator (Kubernetes, ECS, etc.).

---

## Stage 1: Base Image & Supply Chain

**Goal:** Pin tags or digests; prefer minimal bases (distroless, slim) when compatible.

### Practices

- Scan images regularly (Trivy, Grype); track SBOM where required

---

## Stage 2: Dockerfile Structure

**Goal:** Multi-stage builds: compile in builder, copy only artifacts to runtime; order layers for cache hits (dependency manifests before source).

### Practices

- Maintain a robust `.dockerignore` (exclude secrets, build artifacts, VCS noise)

---

## Stage 3: Runtime Config & Secrets

**Goal:** Configuration via environment variables; secrets injected at runtime (K8s secrets, IAM, vault)—never `COPY` real secrets into the image.

---

## Stage 4: Security Hardening

**Goal:** Run as non-root; read-only filesystem where possible; minimal packages in final image; avoid leaking build tools in production.

---

## Stage 5: Health & Observability

**Goal:** `HEALTHCHECK` or orchestrator probes match real readiness (dependencies up); logs to stdout/stderr in structured form.

---

## Stage 6: Ops & Debugging

**Goal:** Tag images with git SHA; document how to exec/debug (or use debug sidecars for distroless).

---

## Final Review Checklist

- [ ] Base image pinned and scanned
- [ ] Multi-stage build; minimal runtime layer
- [ ] No secrets in layers
- [ ] Non-root and least privilege
- [ ] Health/readiness aligned with app
- [ ] .dockerignore and reproducible builds

## Tips for Effective Guidance

- Explain layer caching order—why `COPY package.json` before `COPY .` matters.
- Distroless images: no shell—use ephemeral debug containers or sidecars.

## Handling Deviations

- Windows containers: different paths and base images—validate separately.
