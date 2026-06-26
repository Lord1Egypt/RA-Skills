# Setup

## Goal

Install a generic Codex profile failover layer for OpenClaw without bundling any personal emails, account ids, or chat ids.

## Prerequisites

- OpenClaw state directory exists, usually `/home/node/.openclaw`
- `auth-profiles.json` contains multiple `openai-codex:*` profiles
- target session already exists in `sessions.json`
- Python 3 is available

## Docker içinde kullanım

OpenClaw bir container içinde çalışıyorsa komutları container içinde çalıştır.

Örnek shell erişimi:

```bash
docker exec -it <container-name> bash
```

Tek komut installer örneği:

```bash
docker exec -it <container-name> python3 /workspace/skills/codex-profile-failover/scripts/install_codex_profile_failover.py --workspace /workspace --session-key agent:main:main
```

Not: gerçek workspace yolu container içindeki kurulumuna göre değişebilir. Sık görülen yollar `/workspace`, `/app`, veya OpenClaw workspace mount noktasıdır.

## Codex login mantığı

Bu skill yeni bir Codex login akışı sağlamaz. Önce OpenClaw tarafında Codex hesaplarının normal giriş akışıyla eklenmiş olması gerekir.

Beklenen durum:

- `auth-profiles.json` içinde birden fazla `openai-codex:*` profil vardır
- skill bu mevcut profiller arasında geçiş yapar
- aktif session için `authProfileOverride` alanını yönetir

Yani sıralama şöyledir:

1. önce Codex hesaplarını OpenClaw içine bağla
2. sonra failover configlerini yaz
3. sonra watchdog veya manuel trigger ile profil taklasını çalıştır

## Recommended install path

Run the installer helper from the skill directory:

```bash
python3 scripts/install_codex_profile_failover.py --workspace /path/to/workspace --session-key agent:main:main
```

This writes two workspace-local config files:

- `config/codex-profile-watchdog.json`
- `config/codex-profile-rotation.json`

## Dry run first

```bash
python3 scripts/codex_profile_threshold_guard.py \
  --config /path/to/workspace/config/codex-profile-rotation.json \
  --state-dir /home/node/.openclaw \
  --json
```

Confirm that:

- the current profile is detected correctly
- a healthy alternative candidate appears when expected
- no personal identifiers were hardcoded into the config

## Apply one switch

```bash
python3 scripts/codex_profile_threshold_guard.py \
  --config /path/to/workspace/config/codex-profile-rotation.json \
  --state-dir /home/node/.openclaw \
  --apply --json
```

## Start background watchdog

```bash
nohup python3 scripts/codex_profile_watchdog.py \
  --config /path/to/workspace/config/codex-profile-watchdog.json \
  --state-dir /home/node/.openclaw \
  --apply >> /path/to/workspace/state/codex-profile-watchdog.log 2>&1 &
```

## Manual trigger

Use the manual trigger helper when the operator wants an explicit rotation attempt:

```bash
python3 scripts/trigger_profile_failover.py \
  --config /path/to/workspace/config/codex-profile-watchdog.json \
  --state-dir /home/node/.openclaw
```

## Session patch helper

Use this only when you already know the destination profile id:

```bash
python3 scripts/assign_codex_profile_to_session.py \
  agent:main:main \
  openai-codex:secondary \
  --config /path/to/workspace/config/codex-profile-watchdog.json \
  --state-dir /home/node/.openclaw
```

## Privacy rules before publishing

- remove local logs and backups from the publish folder
- keep only generic session ids in examples, such as `agent:main:main`
- do not include real emails, tokens, account ids, or workspace names in docs or scripts
- keep event log paths generic and workspace-local
