# aws-ses — agent / harness notes

This repo is a portable **Agent Skill**: `SKILL.md` at the root plus scripts
and templates. It is not Hermes-only.

## What to load

1. Read `SKILL.md` first — the full sandbox → production playbook.
2. Use `templates/support-case-reply.md` when filing or answering an AWS
   production-access case. Fill every `{{placeholder}}`; never invent case IDs.
3. Run scripts with `python3 scripts/<name>.py`. Do not treat them as
   executables (no shebang).

## Hard rules

- Never echo, log, or paste IAM secrets or derived SMTP passwords. Use
  `gen_smtp_password.py --output PATH`; do not use `--show-password` in a
  logged or shared session.
- Credentials come from the boto3 chain (`AWS_PROFILE`, SSO, IAM role). There is
  no `--secret` flag; never put secrets in argv.
- `bounce_stats.py` masks recipient addresses. Only pass `--show-addresses` if
  the user asks, and do not paste the result into chat or logs.
- Ask before anything that sends mail, mutates AWS resources, or calls a
  third-party URL (Sendy, `curl` examples in `SKILL.md`).
- Do not read other skills' directories or create cron jobs, startup hooks, or
  state files.
- Preview mutating steps with `--dry-run` (`send_test_email.py`, `setup_domain.py`).
- Tests must stay mocked (`python3 -m unittest tests.test_aws_ses -v`). Do not
  hit a live AWS account unless the user explicitly asks.
- SMTP password ≠ IAM secret. Always derive with `scripts/gen_smtp_password.py --region <region>`.
- Marketing / newsletter / Sendy mail type is **MARKETING**, not TRANSACTIONAL.
- After a DENIED production-access case, reply on the existing case. Do not open a new one.

## Scripts

- `scripts/check_ses_status.py [domain]`
- `scripts/setup_domain.py <domain> [--dry-run] [--mail-from bounce.domain]`
- `scripts/verify_dns.py <domain>`
- `scripts/gen_smtp_password.py --region <region> --output <path> [--secret-stdin]`
- `scripts/send_test_email.py --from ... --to ... [--dry-run]`
- `scripts/bounce_stats.py [--json] [--show-addresses]`

Requires Python 3.11+, `boto3` (pinned in `requirements.txt`), and `dig` only
for `verify_dns.py`.
