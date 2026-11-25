---
name: code-agent-deploy
description: Deploys a local web project to the WEB DEPLOY platform with appcli and returns the address it opens at. Makes the project ready (Dockerfile, deploy.manifest.json, health check), has the platform build and run it (no Docker and no server access on this computer), and repairs and retries from what the server reports. Use when the user asks to deploy, publish, launch or put online a website, web application or backend API (部署、上线、发布、发到服务器), and for anything about a project deployed this way - its status or logs, a site that does not open or is asleep, runtime parameters, rolling back, restoring a backup, public access or the domain prefix, deleting it, plan limits, an appcli command or error code, or deploy.manifest.json.
---

# WEB DEPLOY: the deployment skill

## Goal

When the user says "deploy this project", take it from the local project to an address that opens, without making the user deal with Docker, servers or networking. The user only has to:

1. Set their deploy key once, in their own terminal (section 0).
2. Confirm once the diff that makes the project ready to deploy.
3. On the first deployment, confirm which local file the runtime parameters are read from (when there are any).
4. On the first deployment, decide whether to migrate local data (asked only when local data is found; the default is no).

**Language.** This skill is written in English; talk to the user in the language they use. The platform console is in Chinese, so its pages are named here by their path (`/keys`, `/plans`): name the page in the user's language and give the path. The questions and the report formats below are given in English; put them into the user's language as well.

## What to read, and when

This file is the workflow. The details are in the files below; read one when its moment comes, not before.

| File | Read it when |
|---|---|
| [appcli reference](references/appcli-reference.md) | Writing or checking deploy.manifest.json (its section 2); a command, an output field or a state is not clear (sections 3, 5, 6); an error code has to be looked up (section 7: search the file for the code) |
| [troubleshooting](references/troubleshooting.md) | A deployment or a command failed, before changing anything |
| [operations](references/operations.md) | The user asks about a project that is already deployed: status, logs, parameters, sleep, public access and the domain prefix, restoring data, deleting, rolling back |
| [personal project configuration](references/personal-configuration.md) | Deciding where a runtime parameter's live value comes from, or changing parameters later |
| [stack conventions](references/stacks.md) | The project is Java or Python, or uses MySQL / PostgreSQL |
| [base images](references/base-images.md) | Writing a Dockerfile's `FROM`, installing packages in it, setting up the npm / apt mirrors, or a build that cannot download something |
| [example project](references/example-nextjs-sqlite/) | Making a Node.js project ready: a complete Next.js + SQLite version that has passed acceptance on the platform |

## Rules that are never broken

1. Every deployment goes through the deployment platform, by running appcli. No SSH, no SCP, no direct connection to a server, no remote Docker.
2. Never read, print or ask for the deploy key. The user sets it themselves, in their own terminal (section 0).
3. Never put .env files, keys, tokens, database passwords, local databases or uploaded files into the image.
4. An upload that succeeded, or a task that is queued or running, is not a successful deployment. Wait for succeeded or failed.
5. Redact before showing logs: Authorization, Cookie, password, token, secret, private keys, passwords inside connection strings, and strings that start with `dpk_`.
6. Errors of category auth, server or platform are never worked around by another route. Never suggest opening SSH or the Docker API.
7. Do not change business code outside the checklist in section 2 unless it is explained separately and the user agrees.
8. Do not start containers locally as a rehearsal. Locally only static checks are done; deploy to the server and repair from what the server reports.
9. Do not create test data in the user's live project.

## Workflow

### 0. Before anything else

~~~bash
appcli version --json        # is appcli installed, what the platform supports, is anything out of date
appcli auth status --json    # are the key and the platform address configured
appcli plan --json           # what the user's plan gives, and which projects take its places (run it once the key is configured)
~~~

The image is built on the deployment platform's server. The developer's computer does not need Docker; do not ask the user to install or start it.

**appcli is not installed.** Tell the user it has to be installed from their platform (`npm install -g <platform address>/downloads/appcli`), and stop.

**Something is out of date** (`updates` in `appcli version --json`). Update first, then go on. Update each thing at most once in a conversation.

- `updates.appcli.outdated` is true: tell the user in one sentence that the deploy tool has a new version and is being updated, run `updates.appcli.command`, then run `appcli version --json` again.
- `updates.skill.outdated` is true: run `updates.skill.command`, then read the SKILL.md in the directory it prints again and start over from this section with the new instructions.
- A failed update does not block the deployment: tell the user why it failed and go on with what is installed.
- The output has no `updates`, or one of the two is absent: that check is not available; skip it.

**No key configured** (`DEPLOY_KEY_MISSING`).

- Ask the user to run `! appcli auth set-key` in their own terminal and paste their key; continue when they have.
- Do not add `--platform`: appcli is downloaded from the platform and carries that platform's address (`platformUrl` in `appcli auth status`).
- Only when `platformUrl` is null, or the user explicitly wants another platform, is an address needed. Use the one the user gives, as `! appcli auth set-key --platform <platform address>`. Never guess it.
- A user who has no key yet opens the platform address, signs in and creates one on the console's Deploy keys page (`/keys`). On a platform that is not open for registration an administrator issues it.

**The platform cannot be reached** (`PLATFORM_UNREACHABLE`). Ask the user to check the platform address and the network they are on, and stop.

**A feature is missing from the platform's capabilities.** Do not run the steps that need it, and say so in the result.

**The plan** (`appcli plan --json`) decides what the following steps can do. Look at it before choosing an approach. In `limits`, null means no limit.

- `limits.database`: `none`, the platform gives this user no MySQL / PostgreSQL database service and only SQLite can be used. `shared`: a shared instance can be used, a dedicated one (`mode: dedicated`) cannot. `dedicated`: both.
- `limits.memoryMb`, `limits.cpus`: the ceiling for each project. Asking for more in the manifest is not an error: the platform runs the project at the ceiling and writes a `[plan]` line into the deployment's events.
- `limits.sleepAfterDays`: a project nobody has visited for this many days in a row is put to sleep.
- `projects`: the user's projects that take the plan's places, each with its ID and state. When they are all taken (`usage.projects` has reached `limits.projects`) and this directory's manifest has no applicationId, a new project cannot be created: say which projects hold the places, and let the user choose between deactivating one and upgrading, before changing anything.
- `notices`: what is about to get in the way, each as a sentence that says what to do. Tell the user the ones that concern what they asked for **before** starting, so they are not met as a failure halfway. A notice that begins "tell the user" is passed on as it is.
- `plansUrl`: the page where the plan is changed.
- The command is not available (an older platform): skip it and assume no limits.

### 1. Identify the project

Read package.json / pom.xml / build.gradle / requirements.txt / pyproject.toml, the lock files, the framework configuration (next.config.*, vite.config.*, application.properties/yml, settings.py and so on), any existing Dockerfile / compose file / deploy.manifest.json, the **names** of the variables in .env* files (never output their values), and .gitignore.

Establish:

- The framework, how the application starts, and the port it really listens on.
- Whether it uses a database, which kind, and where it is: the SQLite file's place, or the major version of MySQL / PostgreSQL.
- Where attachments, uploads and generated files are written.
- The environment variables needed at run time, and which of them are build-time variables (such as `NEXT_PUBLIC_*`).
- Hard-coded localhost addresses and absolute local paths.
- Native dependencies (better-sqlite3, sharp, prisma and so on) and whether the build downloads anything.
- Where the local SQLite file and the attachment directories actually are (needed for the question in section 4.5).

MySQL / PostgreSQL are provided by the platform as a database service: a database of its own in a shared instance by default, a dedicated instance as an option (see stack conventions). When the project needs a database service the user's plan does not include (section 0), tell the user before changing anything. They either upgrade on the console's Plans page (`/plans`), or decide to move the project to SQLite. Changing the database is a business change; do not decide it yourself.

When a manifest with an applicationId already exists, run `appcli status --json` first to learn the project's state, and skip the changes that are already made.

### 2. Make the project ready to deploy

Produce the changes in the table below, **show the whole diff once, and ask the user to confirm once**.

- Node.js: follow the example project where it applies.
- Java, Python, MySQL / PostgreSQL: follow the stack conventions.
- After the changes, local `npm run dev` must behave as before: every environment variable that is introduced defaults to the value the project used locally.

| Change | Requirement |
|---|---|
| Dockerfile | Multi-stage. The runtime stage has `USER 10001` and copies only what is needed to run. For every variable in buildEnv the build stage has `ARG X` and `ENV X=$X`. With a migration tool, the start command runs the migration first (for example `prisma migrate deploy`) |
| Base image | Prefer the platform's own `node-base` (written as the name alone). Another public image may be used, with an explicit version; anything needed may be installed or upgraded on top of either (see base images) |
| .dockerignore | Excludes .env*, .appcli, node_modules, .next, .git, local databases (with their -wal / -shm files), upload directories and backups |
| .gitignore | Add `.appcli/` |
| .npmrc | Points at Alibaba's npmmirror, with binary mirrors for the dependencies that need them (see "npm registry" in base images). The Dockerfile copies it before `npm ci` |
| deploy.manifest.json | As in section 2 of the appcli reference; applicationId left empty; checked with `appcli validate --json` |
| Health check endpoint | `/api/health` by default, answering 200 with a small JSON body. It may do a read-only database check. It writes nothing and has no business logic. **It must be exempt from middleware such as login guards and i18n redirects** (in Next.js, exclude the path in the middleware's matcher) |
| Listening | Listen on `0.0.0.0`, on the port read from `PORT` |
| Next.js | `output: 'standalone'`; the standalone output also needs `public` and `.next/static` copied |
| Data paths | The database is read from `DATABASE_URL` (Java reads `JDBC_DATABASE_URL`, `DB_USER`, `DB_PASSWORD`), attachments from `UPLOAD_DIR`, generated files from `GENERATED_DIR` |
| Absolute addresses | Server-side code reads `PUBLIC_URL` (no trailing slash). Client-side code reads a `NEXT_PUBLIC_*` variable declared in the manifest's buildEnv as `from: "publicUrl"` |
| Cookies | An application with sign-in uses a cookie name that is unique to the project. Set the cookie's `Secure` attribute from the protocol of **the request** (the `X-Forwarded-Proto` header, for example Express `trust proxy`), or leave it unset when the framework cannot do that. Never hard-code it to true |

Storage and data:

- The root filesystem is read-only: the application can write only to the declared storage directories and to /tmp. When it writes anywhere else (for example `data/` or `public/uploads/` under the project directory), change it to read the matching environment variable and declare the directory in the manifest's storage.
- The database, the attachments and the files generated for good are each declared persistent; caches are ephemeral. A Next.js application that uses image optimisation or ISR declares `/app/.next/cache` as ephemeral storage.
- SQLite by default. With it the platform injects `DATABASE_URL=file:<database.path>`; when the driver the project uses wants another URL format, adapt how the project reads it.
- Private attachments must not live in a public static directory; they are downloaded through an endpoint that checks who is asking.

Address:

- The application runs at the root path `/`; do not add a basePath.
- HTTPS ends at the platform's gateway. The application listens on plain HTTP and configures no domain or certificate of its own.

Build:

- The project's own runtime version constraint comes first: choose `node-base` or a public image of the right version to suit it.
- Everything the build downloads goes through mirrors in mainland China: npm packages and binaries through Alibaba's npmmirror, apt through the Alibaba Cloud mirror (how, and how to check, is in base images). Do not switch to registry.npmjs.org or another registry abroad.
- With native modules such as better-sqlite3, configure the binary mirror in `.npmrc` and prefer a version that has prebuilt binaries. When there is none, install python3, make and g++ in the build stage and compile from source. A new project can also consider Node's built-in `node:sqlite`, which needs no native build.
- `next/font/google` makes the build fetch from Google, which usually cannot be reached from mainland China: change to `next/font/local` and put the font files into the project. This is outside the checklist, so explain it separately and get the user's agreement.
- Build-time variables such as `NEXT_PUBLIC_*` go only into buildEnv, never into env. buildEnv never contains a secret.

### 3. Static checks

Check before deploying and fix what is found (directly when it is within the checklist, otherwise explain it):

- Does the build context contain .env files, private keys, local databases or uploaded files?
- Does the Dockerfile COPY credentials or .env, or pass a secret in through `ARG`?
- Is a secret declared as `NEXT_PUBLIC_*` or placed in buildEnv?
- Is `.appcli/` in both .gitignore and .dockerignore?
- Does the manifest pass `appcli validate --json`?

### 4. Runtime parameters

On the first deployment, when the manifest declares env:

1. Classify each parameter as in "Two kinds of parameter whose value differs between local and live" in personal project configuration, and list its name, whether it is required, whether it is sensitive, and where its live value comes from (never its value):
   - A signing secret the application uses for itself (SESSION_SECRET, JWT_SECRET, NEXTAUTH_SECRET and the like): written as `generate` in the manifest by default, so the platform creates a new value.
   - A key that decrypts data already stored: when the user chooses to migrate local data it keeps the local value (`source`), otherwise `generate`.
   - Credentials of a third-party service: ask the user "Are these credentials for development and testing? Once the application is live, other people using it will spend this account's quota or cost money." To keep them use `source`; to use different ones use `manual` and ask the user to run `! appcli config set <NAME>` themselves.
   - Ordinary configuration: `source`.
2. Ask the user to confirm the local source file (for example `.env.local`). Only the declared parameters are submitted, never the whole file; registry credentials, deploy keys, private keys and variables that have nothing to do with this project are left out.
3. A value that is a localhost address or a path on this computer is pointed out; ask what the live value should be, do not guess.
4. When a deployment returns `CONFIG_MISSING_REQUIRED`: for the names in `details.manual` ask the user to run `! appcli config set <NAME>`; the names in `details.notInSource` are declared with a source file that does not contain them, so settle with the user where their value comes from. Deploy again when that is done.
5. Later deployments go by the platform's values; appcli only fills in what has been added and is missing (including creating a value for a newly added generate parameter).

### 4.5 Migrating local data (first deployment only, optional)

Only when the project has never been deployed successfully (the manifest has no applicationId, or `everSucceeded` in `appcli status --json` is false) and a local SQLite file or attachment directory is found, or the project uses a local MySQL / PostgreSQL. MySQL / PostgreSQL data is migrated through a SQL dump the user exports (how is in stack conventions); the AI never connects to the user's database itself.

1. List what would be migrated: the database file's path and size; for each attachment or generated-files directory its path, number of files and total size.
2. Point out that it may contain test data or personal information, and ask whether to migrate it. **The default is not to migrate**: when the user refuses, does not clearly agree, or does not answer, nothing is migrated.
3. When the user agrees: fill in `database.localPath` in the manifest (the local database file, as a path relative to the project) and `localPath` of the storage entries (the attachment and generated-files directories), and deploy with `--import-data`. appcli makes a consistent snapshot; do not copy .db files by hand.
4. appcli remembers the agreement (tied to the project ID): automatic retries before the first success bring the data along without asking the user again. When the project ID changes, the agreement is void.
5. A project that has been deployed successfully cannot import any more (`DATA_IMPORT_NOT_ALLOWED`); tell the user the live data will not be overwritten.

### 4.6 Backup before deploying (a project setting)

When the project has a database (`database.type` in the manifest is sqlite, mysql or postgres) and the manifest has no `backupBeforeDeploy` yet, ask the user once before the first deployment: "From now on, before every deployment and rollback, should the database be backed up on the server first? (Recommended: the five most recent are kept, and they can be restored if something goes wrong.)"

- The user agrees, does not clearly refuse, or does not answer: write `"backupBeforeDeploy": true`.
- The user clearly does not want it: write `"backupBeforeDeploy": false`, and tell them there will then be no pre-deployment backup to restore from if something goes wrong.
- From then on the setting is followed without asking again; when the user wants it changed, change the manifest.
- For a one-time exception use `appcli deploy --backup` or `--no-backup` and leave the manifest alone.
- A project without a database is not asked, and the field is not written.

### 5. Deploy

~~~bash
appcli deploy --wait --wait-timeout 540 --json                 # the default
appcli deploy --import-data --wait --wait-timeout 540 --json   # when the user agreed to migrate local data
appcli deploy --no-backup --wait --wait-timeout 540 --json     # when the user asked for no pre-deployment backup this once (--backup is the opposite)
~~~

appcli does it all: creates the project (the first time) → fills in parameters → packs the source → uploads it in parts → creates the task → waits for the platform to build the image and the server to run it. After the first deployment check that applicationId has been written into the manifest.

- `--wait-timeout 540` makes one call return within a tool call's time limit. When it returns `WAIT_TIMEOUT` the task is still running: keep waiting with `appcli deployment <deploymentId> --wait --wait-timeout 540 --json`. Do not deploy again.
- The deploymentId is written to `.appcli/state.json` as soon as the task is created; when a call is interrupted, take it from there.
- When the user asks to stop, `appcli cancel <deploymentId>` cancels a task that is waiting to be built, being built, or waiting for the server. Once the server is running it, it cannot be cancelled; wait for it to end.
- Output with `"pending": true` is a task still on its way (the command did not wait): neither a success nor an error. Wait for it with the command in `next`.

### 6. Results and automatic repair

Success: report the address (section 8).

Failure: read [troubleshooting](references/troubleshooting.md), then act on `error.category`:

| category | What to do |
|---|---|
| build, app | Read the evidence, find the cause, change the project and deploy again. Counts towards the automatic redeployments |
| transient | Do not change the project. `WAIT_TIMEOUT`: the task is still running, keep waiting (section 5) as many times as it takes. `DUPLICATE_DEPLOYMENT`: wait for the task in progress, never start a second one. The other codes: do what the code's entry says (appcli reference, section 7), and deploy again at most once |
| auth, local_env, user_input | Stop and say what the user needs to do |
| server, platform | Do not change the project and do not retry over and over. Report the error code and message and suggest contacting the administrator |

Errors about the plan (the plan's places are taken, the project is asleep, the builds of the day are used up and the like) come in several categories. Whatever the category, none of them is a problem of the project: do what troubleshooting says for that code.

Rules for automatic repair:

- At most 3 automatic redeployments for one request to deploy. When it still fails, stop, summarise each error and each change made, and let the user decide.
- Repairs stay within the checklist. When business code or data structures would have to change, explain first and get agreement.
- Before each repair say what the judgement rests on (quote the log lines).
- `restoredPrevious: true` means the address is still serving the previous version. Tell the user so; there is no need to retry in a hurry.
- When the first deployment fails, the address does not work yet.
- Never repair by turning the health check off, running as root, or turning the read-only filesystem off.
- Never try to fix a start that fails for lack of memory by raising memory in the manifest when the output has `notices`: the project already runs at the plan's ceiling (troubleshooting says what to tell the user).

### 7. After the deployment

For a project that is already deployed, read [operations](references/operations.md) first: it has the commands for status, logs, parameters, sleep, public access, backups, restoring, deleting and rolling back, and what to tell the user about each.

- When the user says the site "does not open" or "says it is starting", run `appcli status --json` first: the project may be asleep.
- Restoring data, deleting the project and rolling back are done only when the user explicitly asks, and after the user has confirmed which backup, which project ID or which version.
- A value the user has to type (`appcli config set NAME`) is typed by the user, in their own terminal.

### 8. What to hand over

Success:

~~~text
Address: https://<the domain the platform assigned>/ (public access: on)
Project ID: todo-app-k3f9
Deployment ID: dep_...
Changes made: (list of files)
Persistent directories: database /app/data, attachments /app/uploads (bound)
Runtime parameters: 3 submitted, 1 generated by the platform (SESSION_SECRET), 1 typed in by the user (OPENAI_API_KEY), 0 missing
Local data: not migrated / migrated (1 database, 230 attachment files)
Note: the entry was verified from the server itself; whether visitors' networks can reach it was not verified
Plan: Free; running at the plan's ceiling (256m memory, 0.25 CPU; the manifest asks for 512m / 1); after 7 days without a visit it goes to sleep and wakes when opened again (ten seconds or so)
~~~

- The address is the one appcli returned (`externalUrl`); it is the application's only address and does not change. Do not guess an address and do not hard-code an example one.
- The "Note" line is always there: a successful deployment means the server itself reached the application through the entry, nothing more.
- The "Plan" line says only what concerns this deployment: that it runs at the ceiling (the output has `notices`), that it will sleep when idle (`sleepAfterDays` is not null), and any of the plan's own `notices` the user should act on soon (it runs out in a few days, the builds are nearly used up). When none applies, leave the line out.

After the first successful deployment, also:

1. Say that anyone can open the address: public access is on by default (`externalAccess`).
2. When the application holds internal data or can be written to, remind the user to make sure sign-in protects it.
3. Ask whether to keep public access. Before turning it off, or changing the domain's prefix, read operations: the user has to be told what follows first.

Failure:

~~~text
Project ID / deployment ID:
Stage it failed in, and the error code:
What is live: still the previous version / nothing running
Key log lines (redacted):
Repairs tried (attempt n):
What the user has to decide, or the administrator has to handle:
~~~

## What may be changed

May be changed (after the user confirms the diff): the files and code points in the checklist of section 2, and the local appcli configuration.

Not changed: any server configuration, firewalls, Nginx, other projects, database structure, business logic (unless agreed separately). Problems on the server side are reported with their error code and evidence.
