# 模块管理

## Intent → Action

| User says | Script command |
|-----------|----------------|
| "日报新增 XX" / "add XX module" | `manage_modules.py add --name "XX" --keywords "..." --prompt "..."` |
| "日报删除 XX" / "remove XX" | `manage_modules.py remove --name "XX"` |
| "日报关闭/禁用 XX" | `manage_modules.py disable --name "XX"` |
| "日报开启/启用 XX" | `manage_modules.py enable --name "XX"` |
| "日报有哪些模块" | `manage_modules.py list` |
| "把 XX 放到第N个" | `manage_modules.py reorder --name "XX" --priority N` |

Script path: `{baseDir}/scripts/manage_modules.py`

## Add Module Flow

1. Extract module name from user message
2. Generate 3-5 search keywords (Chinese + English, include `{date}`)
3. Generate collector prompt (domain-specific, require source URLs)
4. Run: `python3 {baseDir}/scripts/manage_modules.py add --name "{name}" --keywords "{kw1},{kw2}" --prompt "{prompt}"`
5. Reply: "✅ 已新增「XX」板块，下次生成日报时将自动包含。"

## Config Location

- User override: `finance-report-config.yaml` (workspace root)
- Default: `{baseDir}/assets/default-config.yaml`
- Schema: `{baseDir}/references/module-schema.md`
