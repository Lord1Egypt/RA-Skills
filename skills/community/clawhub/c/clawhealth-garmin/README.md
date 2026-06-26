# clawhealth-garmin

Sync Garmin Connect health data into a local SQLite database and expose it as JSON for OpenClaw / AI agents.

---

## TL;DR

- Pull health data from Garmin → store it in local SQLite
- Expose JSON commands → usable by OpenClaw / AI agents
- Install via ClawHub
- The main thing users need to do is complete Garmin login setup

---

## What is this?

`clawhealth-garmin` is an OpenClaw skill that turns your Garmin health data into:

- queryable data (SQLite)
- callable JSON interfaces
- context that AI agents can use

For example, your agent can answer questions like:

- “How did I sleep yesterday?”
- “What is my HRV trend this week?”
- “Am I overtraining?”

---

## Key Features

- Garmin login with MFA support
- Daily health data sync into SQLite
- HRV / sleep / training metrics / body composition
- Activity data (list + details)
- JSON output for agent / automation workflows
- Raw data persistence for later analysis

---

## Installation (ClawHub)

Install this skill inside your OpenClaw environment:

```bash
clawhub install clawhealth-garmin
````

After installation, the skill is copied into your workspace and will be loaded automatically in a new OpenClaw session.

---

## How this skill works

This is a **thin wrapper skill**:

* it does not include the full `clawhealth` source code
* it fetches the required `src/clawhealth` from GitHub at runtime
* it may install Python dependencies when needed

Why this design:

* keep the skill package small
* keep the main source code in the main repository
* separate skill publishing from source iteration

---

## Before first use: Garmin login setup

After ClawHub installation, the main thing the user still needs to do is:

1. configure Garmin username
2. configure Garmin password or password file
3. complete one MFA login flow

---

## Recommended setup: password file

It is recommended to use a password file instead of storing the password directly in an environment variable.

Create `.env` in the skill directory:

```text
CLAWHEALTH_GARMIN_USERNAME=you@example.com
CLAWHEALTH_GARMIN_PASSWORD_FILE=./garmin_pass.txt
```

Then create the password file:

```bash
echo "YOUR_PASSWORD" > garmin_pass.txt
chmod 600 garmin_pass.txt
```

Notes:

* `CLAWHEALTH_GARMIN_PASSWORD_FILE` is the recommended option
* plaintext password env vars are supported, but not recommended
* relative paths are resolved relative to the skill directory

If you really want to use plaintext env vars, you can also use:

```text
CLAWHEALTH_GARMIN_USERNAME=you@example.com
CLAWHEALTH_GARMIN_PASSWORD=YOUR_PASSWORD
```

but this is not the preferred setup.

---

## How should Docker users configure it?

If your OpenClaw is running inside Docker, you can create `.env` and the password file inside the container.

Example:

```bash
docker exec -it openclaw bash -c '
cd ~/.openclaw/workspace/skills/clawhealth-garmin &&
printf "CLAWHEALTH_GARMIN_USERNAME=you@example.com\nCLAWHEALTH_GARMIN_PASSWORD_FILE=./garmin_pass.txt\n" > .env &&
printf "YOUR_PASSWORD" > garmin_pass.txt &&
chmod 600 .env garmin_pass.txt &&
echo "Configuration complete. Return to the chat UI and trigger login."
'
```

If your container name is not `openclaw`, replace it with your own container name.

---

## Garmin login flow (MFA)

### Step 1: trigger login

```bash
python {baseDir}/run_clawhealth.py garmin login --username you@example.com --json
```

If it returns `NEED_MFA`, that is expected. Continue to step 2.

### Step 2: submit MFA code

```bash
python {baseDir}/run_clawhealth.py garmin login --mfa-code 123456 --json
```

After that, the Garmin login session will be stored locally in the skill config directory.

---

## Start syncing data

After login succeeds, you can sync a date range:

```bash
python {baseDir}/run_clawhealth.py garmin sync --since 2026-03-01 --until 2026-03-03 --json
```

Query a daily summary for one date:

```bash
python {baseDir}/run_clawhealth.py daily-summary --date 2026-03-03 --json
```

---

## Common commands

### Daily summary

```bash
python {baseDir}/run_clawhealth.py daily-summary --date 2026-03-03 --json
```

### HRV

```bash
python {baseDir}/run_clawhealth.py garmin hrv-dump --date 2026-03-03 --json
```

### Sleep stages and sleep score

```bash
python {baseDir}/run_clawhealth.py garmin sleep-dump --date 2026-03-03 --json
```

### Training metrics

```bash
python {baseDir}/run_clawhealth.py garmin training-metrics --json
```

### Body composition

```bash
python {baseDir}/run_clawhealth.py garmin body-composition --date 2026-03-03 --json
```

### Activities list and details

```bash
python {baseDir}/run_clawhealth.py garmin activities --since 2026-03-01 --until 2026-03-03 --json
python {baseDir}/run_clawhealth.py garmin activity-details --activity-id 123456789 --json
```

---

## Where is data stored?

* config / tokens: `{baseDir}/config`
* SQLite database: `{baseDir}/data/health.db`

---

## Security Notes

* Garmin credentials and session data stay in your local environment
* your health data is not sent to the skill author
* password files are recommended over plaintext passwords
* do not commit `.env`, password files, or local databases to Git

---

## FAQ

### 1. I installed the skill. Why can I not use it yet?

Because ClawHub installs the skill into your workspace, but Garmin account login still requires you to configure username, password, and complete MFA yourself.

### 2. Is `NEED_MFA` an error?

No. It means step 1 succeeded and you now need to submit the MFA code.

### 3. Why is a password file recommended?

Because it is safer than storing the password directly in a plaintext environment variable, and it is more suitable for long-running environments.

### 4. Why does it download code from GitHub on first run?

Because this is a thin wrapper skill. The skill package is published separately, while the required `clawhealth` source is fetched at runtime.

### 5. Why does it sometimes install dependencies automatically?

Because the skill needs Python dependencies at runtime. If they are missing in the environment, it may bootstrap them automatically.

---

## Documentation

* Chinese documentation: `README_zh.md`
* Skill spec: `SKILL.md`

---

## Source Repository

[https://github.com/ernestyu/clawhealth](https://github.com/ernestyu/clawhealth)
