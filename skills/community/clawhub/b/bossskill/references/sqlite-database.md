# SQLite 经营数据库

Use this when the user wants persistent local storage for the startup training system.

## Database Location

Default database path:

```text
startup_os.sqlite3
```

The caller can choose another path. Prefer one database per company/project.

## Tables

- `projects`: company/project profile.
- `team_members`: team member profile and scores.
- `customers`: customer relationship profile.
- `tasks`: owner/team/customer tasks and reminders.
- `training_records`: employee/founder/customer-service training records.
- `business_metrics`: daily/weekly/monthly operating metrics.
- `knowledge_cards`: user-confirmed knowledge for unknown industries/problems.
- `interaction_notes`: important decisions, corrections, and coaching notes.

## Usage

Initialize:

```powershell
python scripts/startup_os_db.py init --db startup_os.sqlite3
```

Add a project:

```powershell
python scripts/startup_os_db.py add-project --db startup_os.sqlite3 --name "项目名" --stage "验证期" --offer "产品/服务" --target-customer "目标客户"
```

List records:

```powershell
python scripts/startup_os_db.py list --db startup_os.sqlite3 --table customers
```

Add a team member with scores:

```powershell
python scripts/startup_os_db.py add-team-member --db startup_os.sqlite3 --project-id 1 --name "张三" --role "销售" --scores "execution=4,sales=3"
```

Export JSON:

```powershell
python scripts/startup_os_db.py export --db startup_os.sqlite3
```

Start local web admin:

```powershell
python scripts/startup_os_web.py --db startup_os.sqlite3 --port 8765
```

Then open:

```text
http://127.0.0.1:8765
```

## Agent Rules

- Store only user-provided facts, accepted conclusions, and completed training results.
- Keep sensitive customer data minimal.
- Do not store private customer details unless the user approves and business use is reasonable.
- Before giving advice, query related project/customer/team records when available.
- After the user corrects facts, update the corresponding record.

## Practical Workflow

1. Ask whether the user wants to create/use a local database.
2. Initialize database if needed.
3. Add project profile first.
4. Add team/customer records as user provides them.
5. Use tasks and training records to create follow-up loops.
6. Export JSON when syncing to Hermes/OpenClaw memory or another system.
