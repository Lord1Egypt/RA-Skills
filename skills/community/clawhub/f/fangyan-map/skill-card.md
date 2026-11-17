## Description:

Provides bidirectional lookup between Mandarin and eleven Chinese dialects for dialect-aware conversation, cross-dialect communication, cultural research, and localized writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esnowxu](https://clawhub.ai/user/esnowxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Mandarin-to-dialect mappings across supported Chinese dialects and to support dialect-aware agent responses. The included helpers can initialize a local dictionary, add new words, and optionally sync entries with Feishu bitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential discovery can fall back to /root/.openclaw/openclaw.json for API keys.

Mitigation: Remove the fallback and require explicit environment variables or a managed secret source before enabling AI enrichment.

Risk: Cloud synchronization can send local dictionary entries to Feishu bitable when enabled.

Mitigation: Default cloud_share.enabled to false, require explicit operator opt-in, and verify app_id, app_secret, app_token, and table_id permissions before use.

Risk: Executable incremental SQL and database rebuild behavior can alter local dictionary state.

Mitigation: Replace executable SQL imports with parameterized imports and back up dialect.db, incremental_words.sql, and sync_cursor.json before initialization or sync jobs.

Risk: The artifact includes a hardcoded task-queue helper and server evidence flags contaminated data.

Mitigation: Remove or isolate the task-queue helper and review the corpus to purge prompt-like or operational rows before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/esnowxu/skills/fangyan-map)
- [MiniMax Anthropic-compatible API endpoint](https://api.minimaxi.com/anthropic/v1)
- [Feishu Bitable records API endpoint](https://open.feishu.cn/open-apis/bitable/v1/apps/)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local dictionary, log, cursor, configuration, and cloud-sync state files when helper scripts are executed.]

## Skill Version(s):

1.0.32 (source: server release metadata, frontmatter, CHANGELOG released 2026-06-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
