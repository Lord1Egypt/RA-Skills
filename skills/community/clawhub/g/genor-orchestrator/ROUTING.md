# Model Routing Reference

> Quick-reference routing guidance. The authoritative inventory is `orchestrator-data/models.json`.
> For the full routing table with fallback chains, see the SKILL.md.

## Quick Routing

| Task Type | Primary | Fallback |
|-----------|---------|----------|
| Heavy coding | Best available | ACP agent |
| Quick edits | Fast cloud | Free tier |
| Research | Best reasoning | Free tier |
| Vision | Cloud vision | Local |
| Planning | Best reasoning | Free tier |
| Docs/summaries | Free tier | Fast cloud |

## Cost Cheat Sheet

- **Free tier first**: free models, local models
- **Subscription**: use within monthly limits
- **Pay-per-token**: use sparingly, prefer cheaper models
- **Last resort**: depleting funds — avoid

## Dashboard

Model inventory + editing: `http://localhost:8766` (when running)
See `{baseDir}/dashboard/serve.sh` to start.
