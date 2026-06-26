# Member Sync Troubleshooting

Read this file only when the request is blocked by member lookup, sync coverage, or alias maintenance.

## When To Load

- `feishu_members.py sync` does not produce the expected people
- `resolve --query ...` returns `not_found`
- `validate-aliases` reports broken mappings
- The app's authorized contact scope does not cover the expected users

## How v1 Sync Works

1. Read the authorized scope from `GET /contact/v3/scopes`
2. Collect authorized `department_ids` and `user_ids`
3. Fetch direct department users from `GET /contact/v3/users/find_by_department`
4. Merge all results into `feishu_members.json`
5. Apply manual aliases from `member_aliases.json`

## Known v1 Limitation

`contact/v3/scopes` returns identifiers only. If the scope contains direct users that are not also returned by department-user queries, v1 stores them as identifier-only stub records. Natural-language resolution for those users depends on manual aliases until a user-detail API is added.

## Maintenance Actions

- Re-run:
  `python3 feishu-task-management/toolkit/scripts/feishu_members.py sync`
- Check current stats:
  `python3 feishu-task-management/toolkit/scripts/feishu_members.py stats`
- Test a lookup:
  `python3 feishu-task-management/toolkit/scripts/feishu_members.py resolve --query "张三"`
- Validate aliases:
  `python3 feishu-task-management/toolkit/scripts/feishu_members.py validate-aliases`
