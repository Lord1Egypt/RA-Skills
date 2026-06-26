# Output Examples

## Example 1: GBrain Documentation (11 topics)

**Source:** `github.com/garrytan/gbrain/tree/main/docs`

**Result:**
```
second-brain/gbrain/
├── 00-index.md              # Master index
├── 01-instalacao-e-setup.md # Installation paths, engines, providers
├── 02-arquitetura.md        # Topologies, brains/sources, retrieval
├── 03-configuracao-operacao.md # Commands, modes, cron
├── 04-ingestao-dados.md     # Capture, meetings, diligence
├── 05-embeddings-busca.md   # Providers, HNSW, reranking
├── 06-skills-automacao.md   # 43 skills, cron, minions
├── 07-mcp-integracoes.md    # MCP stdio/HTTP, clients
├── 08-avaliacao-qualidade.md # Eval framework, metrics
├── 09-seguranca-permissoes.md # RLS, OAuth, credentials
└── 10-guias-praticos.md     # Brain-first, compiled truth
```

**Key features:**
- Each file has source attribution
- Tables for comparisons
- Decision matrices
- Step-by-step commands
- Living document markers

---

## Example 2: OpenClaw Configuration (29 topics)

**Source:** `github.com/openclaw/openclaw/tree/main/docs/gateway`

**Result:**
```
second-brain/openclaw-config/
├── 00-indice.md
├── 01-gateway.md
├── 02-canais.md
├── 03-agentes.md
├── 04-ferramentas.md
├── 05-modelos.md
├── 06-mcp.md
├── 07-seguranca.md
├── 08-sandbox.md
├── 09-sessao.md
├── 10-contexto.md
├── 11-heartbeat.md
├── 12-skills.md
├── 13-embedding-providers.md
├── 14-model-gateway.md
├── 15-local-models.md
├── 16-pricing.md
├── 17-monitoring.md
├── 18-logging.md
├── 19-backup-restore.md
├── 20-upgrade.md
├── 21-troubleshooting.md
├── 22-cli-reference.md
├── 23-config-examples.md
├── 24-migration-guide.md
├── 25-api-reference.md
├── 26-webhooks.md
├── 27-remote-access.md
├── 28-local-model-services.md
└── 29-secrets-management.md
```

**Key features:**
- CLI commands extracted
- Config snippets
- Decision tables
- Source links to every section

---

## Example 3: Simple Library (5 topics)

**Source:** `docs.example.com`

**Result:**
```
second-brain/my-library/
├── 00-index.md
├── 01-quickstart.md
├── 02-api-reference.md
├── 03-configuration.md
└── 04-examples.md
```

---

## What Makes Good Output

✅ **Source attribution on every file**
```markdown
> **Source:** [github.com/...](URL)
> **Extracted:** 2026-05-22
```

✅ **Decision tables**
```markdown
| Option | Pros | Cons |
|--------|------|------|
| A | Fast | Expensive |
| B | Cheap | Slow |
```

✅ **Step-by-step checklists**
```markdown
- [ ] Step 1: Install
- [ ] Step 2: Configure
- [ ] Step 3: Verify
```

✅ **Living document markers**
```markdown
**Status:** 🟢 Living Document
**Last Sync:** 2026-05-22
```

✅ **Cross-references between files**
```markdown
See also: [02-architecture.md](02-architecture.md)
```

---

_Last updated: 2026-05-22
