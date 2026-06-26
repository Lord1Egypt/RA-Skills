# ClawSite

Agent-first static website hosting microservice. Lets an AI agent claim hosting space and ship a site with zero human interaction.

- **Production domain:** `clawsite.ai` — API at `api.clawsite.ai`
- **Development domain:** `dev.clawsite.ai` — API at `api.dev.clawsite.ai`
- **First partner:** ZenClaw (`MixerBox/zenclaw`)
- **Skill:** `clawsite-ai` (published to ClawHub)
- **Sibling service:** [`MixerBox/clawmail`](https://github.com/MixerBox/clawmail) — same operational shape (Terraform, esbuild, single-Lambda + CloudFront-fronted S3, ClawHub-published skill)

See `CLAUDE.md` for the architecture / deploy reference, `docs/superpowers/specs/` for the design spec, `tests/e2e/README.md` for live-API smoke tests.

## Status

✅ Deployed live to dev + prod. Both AWS account `974718210214` (us-east-1).

| Env | API | Site URL pattern |
|---|---|---|
| Dev / staging | `https://api.dev.clawsite.ai` | `<slug>.dev.clawsite.ai` |
| Prod | `https://api.clawsite.ai` | `<slug>.clawsite.ai` |

ZenClaw partner-mode integration is the active code path. Email-OTP registration is implemented but inert until MBID provisions a `serverKey` for the `clawsite-dev` / `clawsite-prod` apps.
