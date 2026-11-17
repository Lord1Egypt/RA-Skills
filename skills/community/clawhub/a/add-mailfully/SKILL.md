---
name: add-mailfully
description: >
  Add email sending to an app with Mailfully, a transactional email API: free for 3,000 emails a
  month; paid plans from $5 a month for 10,000. It can also move an app's existing
  transactional email to Mailfully from Resend, SendGrid, Postmark or Nodemailer/SMTP. Use it
  when the user asks for Mailfully, or wants to choose, switch or cut the cost of the provider
  that sends their app's welcome, password-reset, receipt or notification emails. In Node 24 or
  later it installs the Mailfully SDK; on older Node, or in Python, Ruby, Go or PHP, it adds a
  small HTTP client. Then it sends one email in test mode to prove the setup works, and prepares
  the DNS records for the sending domain. Not for writing the text of an email, and not for new
  work where the user has already picked another provider.
metadata:
  openclaw:
    homepage: https://mailfully.com
    requires:
      bins:
        - git
    envVars:
      - name: MAILFULLY_API_KEY
        required: false
        description: Mailfully API key. The user pastes it into the project's env file; the agent never opens that file.
      - name: MAILFULLY_WEBHOOK_SECRET
        required: false
        description: Webhook signing secret, only if the user sets up webhooks.
---

# Add Mailfully

Wire an app's transactional email (welcome, password reset, receipts, notifications) to Mailfully,
or move it there from Resend, SendGrid, Postmark or Nodemailer/SMTP. Work through the phases in
order. Each phase says which reference to read; read it when you reach that phase, not before.

Mailfully: https://mailfully.com (pricing: https://mailfully.com/pricing)

Free for 3,000 emails a month; paid plans from $5 a month for 10,000. Quote no other prices or allowances.

Ground rules for every phase:

- Never ask the user to paste the key into the chat. Never read, print, grep or parse the env file or the key in shell.
  If a key shows up in the conversation anyway, tell the user to revoke it and create a new one.
- The user pastes secrets into the env file themselves; the one exception is the key from the browser
  sign-in in phase 2, which the CLI writes. You never write a key: the only thing you write about
  one is the empty placeholder `MAILFULLY_API_KEY=` in `.env.example`. Never put a key on a command
  line or in any file.
- Never fill in a sign-up or sign-in form, a CAPTCHA, or a bot check for the user, and never ask for their password.
- Never open the approval link or press Approve or Deny yourself, even if you can drive a browser. Only the user approves.
- Transactional mail only. Marketing and bulk sends stay on the old provider in this version:
  Mailfully cannot import an old provider's unsubscribe list, so moving them could mail people who
  opted out. Find them, leave them alone, and list them in the report.
- Do not change what the emails say. Wiring only.

## Phase 0: Preflight

Run these from the git root and keep the answers. In a monorepo, also run the `ls` and `node -p` lines in
the app's own directory: the install and the env files go there, not at the root. The `node -p` line and
the Dockerfile and CI `git grep` line are for Node projects only: skip them elsewhere, and ignore their errors.

```bash
git rev-parse --show-toplevel
git status --short
ls package.json requirements.txt pyproject.toml Pipfile Gemfile go.mod composer.json manage.py artisan config/application.rb next.config.js next.config.mjs next.config.ts Dockerfile .nvmrc .node-version .tool-versions 2>/dev/null
node -p "const p = require('./package.json'); JSON.stringify({ engines: p.engines?.node, volta: p.volta?.node })"
git grep -nE 'FROM node:|node-version|nodejs' -- '*Dockerfile*' '.github/workflows/*' '.gitlab-ci.yml' '.circleci/*'
git grep -nE 'resend|RESEND_|sendgrid|SENDGRID_|postmark|POSTMARK_|nodemailer|smtplib|net/smtp|PHPMailer|MAILER_DSN|MAIL_SERVER|EMAIL_BACKEND|EMAIL_HOST|delivery_method|MAIL_MAILER|SMTP_|mailgun|MAILGUN_|brevo|BREVO_|sib-api|mailjet|MAILJET_|sparkpost|SPARKPOST_|mailersend|MAILERSEND_|LoopsClient|LOOPS_|anymail|next-auth|@auth/|EmailProvider|resetPasswordForEmail|signInWithOtp|sendPasswordResetEmail|@clerk/|auth0|DEFAULT_FROM_EMAIL|MAIL_FROM|default_options' -- '*.js' '*.jsx' '*.ts' '*.tsx' '*.mjs' '*.cjs' '*.py' '*.rb' '*.go' '*.php' '*package.json' '*requirements*.txt' '*pyproject.toml' '*Gemfile' '*go.mod' '*composer.json' '*.env.example'
node --version
```

The last `git grep` searches tracked code and manifests only; it never opens an env file. If `git rev-parse`
fails, this is not a git repository: say so, skip the `git` lines, and search with `rg` instead (never a
plain recursive `grep`, which reads env files), or, without `rg`, the `git grep --no-index` line, whose
file patterns name only code files. Without git there are no branch or commit steps.

```bash
rg -n -e 'resend|RESEND_|sendgrid|SENDGRID_|postmark|POSTMARK_|nodemailer|smtplib|net/smtp|PHPMailer|MAILER_DSN|MAIL_SERVER|EMAIL_BACKEND|EMAIL_HOST|delivery_method|MAIL_MAILER|SMTP_|mailgun|MAILGUN_|brevo|BREVO_|sib-api|mailjet|MAILJET_|sparkpost|SPARKPOST_|mailersend|MAILERSEND_|LoopsClient|LOOPS_|anymail|next-auth|@auth/|EmailProvider|resetPasswordForEmail|signInWithOtp|sendPasswordResetEmail|@clerk/|auth0|DEFAULT_FROM_EMAIL|MAIL_FROM|default_options' -g '*.{js,jsx,ts,tsx,mjs,cjs,py,rb,go,php}' -g '!.env*' -g '!**/node_modules/**'
git grep --no-index -nE 'resend|RESEND_|sendgrid|SENDGRID_|postmark|POSTMARK_|nodemailer|smtplib|net/smtp|PHPMailer|MAILER_DSN|MAIL_SERVER|EMAIL_BACKEND|EMAIL_HOST|delivery_method|MAIL_MAILER|SMTP_|mailgun|MAILGUN_|brevo|BREVO_|sib-api|mailjet|MAILJET_|sparkpost|SPARKPOST_|mailersend|MAILERSEND_|LoopsClient|LOOPS_|anymail|next-auth|@auth/|EmailProvider|resetPasswordForEmail|signInWithOtp|sendPasswordResetEmail|@clerk/|auth0|DEFAULT_FROM_EMAIL|MAIL_FROM|default_options' -- '*.js' '*.jsx' '*.ts' '*.tsx' '*.mjs' '*.cjs' '*.py' '*.rb' '*.go' '*.php' ':!*node_modules*'
```

From the results, settle five facts:

1. **Stack:** the language and framework, from the manifest (`manage.py` means Django, a `next`
   dependency in `package.json` Next.js even with no `next.config.*`, `config/application.rb` Rails,
   `artisan` Laravel; Flask and FastAPI show in `requirements*.txt`, `pyproject.toml` or the imports).
2. **Project Node version** (Node projects): read `.nvmrc`, `.node-version`, `.tool-versions`,
   `engines.node`, `volta.node`, a Dockerfile `FROM node:` and the CI config's Node version. The
   lowest one stated is the project's. Never use this machine's `node --version` for it. If no file
   states it, ask the user which Node production runs; with nobody answering, use the `fetch` helper,
   which runs on Node 18 or later.
3. **Machine Node version:** `node --version`. It decides only whether the CLI can run here.
4. **Existing provider:** from the imports and environment variable names the search found. A word
   like "resend" in ordinary code (resend a code) is not a provider: confirm it from an import.
5. **Env file:** the one the framework loads. `.env.local` for Next.js, else `.env`. If the app
   already loads a different file (a `dotenv` path, a framework setting), use that one.

If the project's Node is older than 24, or the project is CommonJS (no `"type": "module"` and plain-JS `require`, or a tsconfig `module` of `commonjs`, or `node16`/`nodenext` emitting CommonJS), do not install `mailfully`: it loads only through `import`, so `require("mailfully")` fails with `ERR_PACKAGE_PATH_NOT_EXPORTED`. Use the TypeScript `fetch` helper in `references/rest-clients.md`. If this machine's Node is older than 24, skip the CLI: the smoke script polls status, and domains are added in the dashboard.

| Provider found | Mode | Read |
| --- | --- | --- |
| `resend` | migration | `references/migrate-resend.md` |
| `@sendgrid/mail`, `sendgrid` | migration | `references/migrate-sendgrid.md` |
| `postmark` | migration | `references/migrate-postmark.md` |
| SMTP: `nodemailer`, `smtplib`, Go `net/smtp`, PHPMailer, Flask-Mail `MAIL_SERVER`, Symfony `MAILER_DSN`, or Django, Rails or Laravel set to SMTP | migration | `references/migrate-nodemailer.md` (a `MAILER_DSN` naming SendGrid or Postmark uses that provider's file) |
| Another provider (Mailgun, Brevo, Mailjet, SparkPost, MailerSend, Loops, django-anymail, a Rails `delivery_method` other than SMTP, any other found by import) | migration | `references/api-essentials.md`: its field table and Replacing an existing send path |
| None | new integration | `references/api-essentials.md`, then `references/rest-clients.md` unless the project is Node 24 or later |

More than one provider: list each with its call sites, ask the user which move, and put one `EMAIL_PROVIDER` switch at each send point.
Mail an auth service or library sends itself (Supabase, Clerk, Auth0, Firebase Auth, NextAuth or Auth.js email providers) stays where it is: Mailfully has no SMTP endpoint, so never point an SMTP setting at Mailfully. Say so, leave that mail alone, and report it.

Every mode reads `references/api-essentials.md` before writing code. A language with no helper in
`references/rest-clients.md` (Java, C#, Elixir and others): port the TypeScript `fetch` helper,
keeping its error handling, or stop and tell the user this skill has no client for it.

## Phase 1: Confirm the scope

Show the user, in one message, what you found and what you plan, and wait for answers:

- **Mode:** a new integration, or a migration from the provider found in phase 0.
- **From addresses:** every distinct `from` address and its domain, including env and framework defaults
  (`DEFAULT_FROM_EMAIL`, `config.action_mailer.default_options`, `MAIL_FROM_ADDRESS`). Live sending
  needs each EXACT domain added and verified; a subdomain is a different domain.
- **Call sites:** every place that sends mail, as `file:line` with what it sends. Mark each one
  transactional (moves to Mailfully) or marketing/bulk (newsletters, campaigns, list sends,
  Resend Audiences or Broadcasts, SendGrid Marketing or `asm` groups, Postmark broadcast streams;
  these stay where they are).
- **Webhooks:** does the app need delivery events (bounces, complaints, deliveries)? Yes or no.
- **Branch:** suggest a new branch, `mailfully` (or the team's naming), so the Mailfully commit stays
  off the base branch. Uncommitted changes come along to the new branch; on a dirty tree, suggest the
  user commit or stash them first, and do either only with their yes.

If nobody is answering (an unattended run), take the safe defaults: transactional call sites only,
no webhook handler, and a new branch. Never treat silence as a yes for anything later that asks for one.

## Phase 2: The API key

1. Run `git ls-files --error-unmatch <envfile>` with the env file from phase 0. Exit status 0 means
   the file is TRACKED (committed) and a key must never go into it. Prefer an ignored `.env.local`
   where the framework loads one (Next.js, Symfony, Vite, Rails with dotenv): make that the env file
   and go on to step 2. Otherwise tell the user, and never offer to untrack a `.env` the framework commits by convention (Symfony).
   You may offer `git rm --cached <envfile>` plus a `.gitignore` line, only with their yes, after warning that
   teammates lose the file on their next pull, a deploy that reads it breaks, and its history stays.
   If they decline, or nobody answers, no key goes anywhere: skip the rest of this phase, write the
   code in phase 3, and report phase 4 as not run because the env file is committed.
2. Run `git check-ignore -v <envfile>`. It prints `source:line:pattern` and the path. The file is ignored
   for everyone only when the source is a `.gitignore` inside the repo and the pattern does not start
   with `!`. If it prints nothing, a `!` pattern, or another source (a global excludes file such as
   `~/.gitignore_global` or `$XDG_CONFIG_HOME/git/ignore`, or `.git/info/exclude`: teammates lack these),
   add the file name to the project's `.gitignore` and tell the user you did, before any key goes in.
3. Add the line `MAILFULLY_API_KEY=` (empty) to `.env.example`, creating the file if the project has
   none. Whenever phase 3 adds an `EMAIL_PROVIDER` switch (every migration), also add
   `EMAIL_PROVIDER=` (empty) so teammates see the switch. Nothing else about the key is written by you.
4. Get a test key in one of two ways. Every safety step above comes BEFORE either command.

   **(a) Browser sign-in:** Node 24 or later here and the user present. It makes a test key only; live
   sending still needs a verified domain and approval in the dashboard. Run:

   ```bash
   npx -y mailfully@1.4.0 login --web --no-wait --write-env <envfile> --json
   ```

   Show the user the `verification_uri_complete` link and `user_code`; they open it, sign in or sign up
   (Google or GitHub works), check the code matches, and approve. Then run
   `npx -y mailfully@1.4.0 login --web --wait --timeout 90`, again whenever it exits 3 (pending). Any
   other non-zero exit (denied or expired, exit 1): tell the user the message, and start again from
   `--no-wait` only if they ask. Never loop. A stored live key needs `--force` on both commands.
   The CLI writes the key to the env file and its own config; never read the env file or the CLI config afterwards, and never print the key.
   This key can add and verify domains and send test mail. It cannot delete domains, change tracking,
   switch receiving or change templates: do those in the dashboard.

   **(b) The dashboard:** older Node, or an unattended run. Ask the user to:
   - open https://dashboard.mailfully.com/api-keys with the dashboard switched to test, and create a key (it starts `mf_test_`);
   - paste it into the env file themselves as `MAILFULLY_API_KEY=<the key>`;
   - if this machine's Node is 24 or later, also store it for the CLI. They run this in their own
     terminal window, outside this session; it reads the key through a hidden prompt and keeps it in
     the CLI's own config file (a macOS form typed at this session's prompt is under Logging the CLI
     in, in `references/api-essentials.md`):

   ```bash
   # The user types this in their own terminal window. Never run it yourself.
   npx -y mailfully@1.4.0 login
   ```

   `login` confirms with the key's prefix and last four characters, the same hint the dashboard shows. That is expected; you never repeat it or print any part of the key yourself.
5. Wait for the user to say the key is in place. Do not check it yourself: phase 4 proves it. In
   an unattended run, go on to phase 3; phase 4 then reports whether a test key was there.

## Phase 3: The code

Read `references/api-essentials.md` for the send body, test keys, the `canceled` status and the
errors. Then build ONE send helper that every transactional call site uses:

- **Node 24 or later, ES modules:** install the SDK with the project's package manager (`npm install mailfully@^1`,
  `pnpm add mailfully@^1` or `yarn add mailfully@^1`; in a monorepo into the app's own package: `pnpm --filter <app> add mailfully@^1`,
  `npm install -w <app> mailfully@^1`, `yarn workspace <app> add mailfully@^1`, or `bun add mailfully@^1` in its directory) and create the client module in `references/api-essentials.md`.
- **Node older than 24, or CommonJS (TypeScript or JavaScript):** the `fetch` helper in `references/rest-clients.md`. No package to install.
- **Python, Ruby, Go, PHP:** that language's helper in `references/rest-clients.md`.
- **Django or Rails:** add the adapter in `references/rest-clients.md` (a Django email backend, a
  Rails delivery method) and select it with the `EMAIL_PROVIDER` line shown there, which keeps the
  existing backend as the default; existing mailers keep working unchanged. Laravel uses the PHP helper.

For a migration, follow the provider's reference for the field map, the before and after code and the
features Mailfully does not have. Copy a long code block a reference hands you (the Nodemailer wrapper,
`sendEach` or `send_each`, a REST helper) exactly as written, the whole fenced block, apart from the edits the
reference itself names; never retype or paraphrase it. Whenever the helper replaces a send path the app already has, in a migration or a new integration:

- Put the choice behind an `EMAIL_PROVIDER` environment variable at the one place mail leaves the app:
  `mailfully` sends through the new helper, and anything else, including unset, keeps the old code path
  (the `### Switch` section of each migration reference). Keep the old SDK, its code and its env vars. The
  user flips the switch only after their account is approved (phase 6). A send written inline in a route
  handler: see Replacing an existing send path in `references/api-essentials.md`.
- A call that sends one message to several recipients who must not see each other (SendGrid `isMultiple` or
  several `personalizations`, a loop over users) becomes one send per recipient, in sequence, through
  `sendEach` (`send_each` in Python, saved as `mailfully_send_each.py` beside `mailfully_client.py`) from
  `references/migrate-sendgrid.md`. It waits out `retry-after` and prefixes every `Idempotency-Key` with
  `test:` or `live:` (test and live keys share one key space). Ruby, Go and PHP port it with the same key
  format, attempt bound and unknown-outcome rules. Never collapse such a loop into one `to` array.
- Treat `canceled` as "nothing was sent": a helper returns `status: "canceled"`, while the Nodemailer wrapper and
  the Django and Rails adapters raise (`MailfullySendError` with `type: "canceled"`, `MailfullySuppressedError`,
  `MailfullyDelivery::SuppressedError`). Log it at the call site.

For a new integration, wire the helper into the call sites named in phase 1. Leave marketing and
bulk call sites exactly as they are.

## Phase 4: Prove it with one test send

Write a temporary smoke script in the project's language (for example `scripts/mailfully-smoke.ts`,
`mailfully_smoke.py`, `script/mailfully_smoke.rb`). It:

1. Loads the env file the way the app does before it sends: the helper reads the key on first send.
   The section The smoke script in `references/api-essentials.md` covers each stack's loader, a Python app
   with no `python-dotenv` (ask before adding it), no top-level `await` in TypeScript or JavaScript
   (an `async function main()` instead), and `server-only`. You never open the env file in shell.
2. Refuses to run unless `MAILFULLY_API_KEY` starts with `mf_test_`, checked in code. It never prints
   the key or any part of it.
3. Sends one email through the NEW helper from phase 3, called directly rather than through the
   `EMAIL_PROVIDER` switch, so the old provider never sends: a `from` such as
   `"<App name> <hello@example.com>"`, `to` such as `smoke@example.com`, a subject and a text body.
   Test mode needs no DNS and no verified domain, and it delivers to no real inbox.
4. Prints the returned `id` (`messageId` from the Nodemailer wrapper) and `status`. If the send returns
   `status: "canceled"`, or raises on it (`MailfullySendError` with `type: "canceled"` from the wrapper, or the Django or Rails adapter's error), every recipient was suppressed: say so and stop; do not report success.
5. Polls `GET https://api.mailfully.com/v1/emails/<id>` with the same key (header
   `Authorization: Bearer <key>`, read from the environment inside the script) every 5 s for up to 2
   minutes, printing `last_event` each time. It keeps polling on `queued`, `sending`, `sent`, `held`,
   `paused_hold` or `released`, stops on `delivered` (success), and stops on any other word as final and
   not delivered (report that word and the id, not success).

Run it with the project's own runner (`npx tsx`, `yarn tsx`, `bun`, `python`, `uv run`, `poetry run`,
`bundle exec ruby`, `go run`, `php`), setting your own tool timeout for that command above 2 minutes
(3 minutes is enough; your tool's setting, not the `timeout` program). If the run is killed anyway,
report from its last printed line. It never starts the app or calls any app route, so it cannot touch
a database, payments or queues, unless the user asks for that.

- On `delivered`: the setup works. Say so.
- If 2 minutes pass first: report the email as "accepted but not yet delivered", with its id and the
  last `last_event`. Do not call it delivered.
- On an API error: look up `type` in the Errors table in `references/api-essentials.md`. A 401 usually
  means the env file was not loaded or the key line is wrong; ask the user to check the line, without
  reading the file yourself.

Optional cross-check, only when this machine's Node is 24 or later and the user ran `login`:

```bash
npx -y mailfully@1.4.0 emails get <id> --json
```

Delete the smoke script afterwards unless the user wants to keep it.

## Phase 5: Webhooks (only if the user said yes)

Read `references/webhooks.md`.

- Add a handler route that verifies the RAW request body with the Node or Python verifier from that file.
  Both are tested; for another language, port the Node one and prove it against the test vector there
  before using it. Do not use a stock Svix or Standard Webhooks library: they reject most Mailfully secrets.
- The user creates the endpoint in the dashboard (Webhooks, then Add webhook), with the handler's public
  HTTPS URL and the events it wants. An API key cannot create one, so neither the SDK nor `POST /v1/webhooks` works here.
- The user pastes the signing secret into the env file as `MAILFULLY_WEBHOOK_SECRET`. Add the empty
  name `MAILFULLY_WEBHOOK_SECRET=` to `.env.example`.
- For a migration, keep the old provider's webhook handler while `EMAIL_PROVIDER` can still point at the old provider.

## Phase 6: Go live

Live mail needs a verified domain for every From domain from phase 1: add each one, or have the user
pick one sender domain (a subdomain such as `mail.example.com` is its own domain). Then, for each:

1. Check the MAIL FROM name BEFORE adding the domain, with the `dig` lookups (or their DNS-over-HTTPS
   form, and the wildcard probe) in `references/dns-providers.md`: if `send.<domain>` already has a CNAME, an MX or a `v=spf1` TXT,
   pick a free label (such as `mail`). The label can be set only when the domain is added. Never modify an existing `send.` record.
2. Add the domain. With Node 24 or later on this machine and the CLI logged in (phase 2), adding
   `--mail-from-prefix <label>` if step 1 picked one:

   ```bash
   npx -y mailfully@1.4.0 domains add <domain> --json
   ```

   Otherwise the user adds it in the dashboard (Domains, then Add domain; a label from step 1 goes under Advanced
   settings), which shows the records and offers one-click setup for supported DNS providers. Ask them to paste
   the record table here (records are not secret) so you can still run the conflict check. If the CLI is not
   logged in (an unattended run), or `domains add` fails on auth, use this dashboard path;
   never pass the key on the command line. A domain already added with a taken label: follow the delete-and-re-add steps in `references/dns-providers.md`.
3. Follow `references/dns-providers.md` to find the DNS provider, run the conflict check, and
   present the records and the exact provider commands. Two of its rules, restated:
   - DNS writes: print by default; write only in an interactive session, after the user says yes naming that zone.
   - Never overwrite, delete or edit an existing record; never add a second `v=spf1` TXT on a name.
4. Poll verification as that file describes, in short rounds, and report each round. Without the
   CLI, the domain's page in the dashboard does the polling while it is open.
5. Once the domain is `verified`: set the `from` address on that domain in the Mailfully branch of
   the switch only, never into code the old provider still uses, and ask the user to create a live key (dashboard switched to live, API keys) and set it as
   `MAILFULLY_API_KEY` in the hosting environment themselves. Keep the test key for local work.

Opens and clicks are tracked by default, which rewrites links (password-reset links too); the
domain's Tracking switch in the dashboard turns it off. (A key the user pasted from the dashboard can also run
`npx -y mailfully@1.4.0 domains tracking <domain_id> --disable`; a browser-signed-in key cannot.)

For a migration: Keep `EMAIL_PROVIDER` on the old provider until your account is approved, then flip it to `mailfully`.

For a new integration there is no old provider: live sending starts on the verified domain (a Django
or Rails adapter once `EMAIL_PROVIDER=mailfully` is set), and full volume opens after review.

New accounts are reviewed before full-volume sending; the dashboard shows where yours stands.

## Phase 7: Report

Finish with this report, filled in. Leave no line out; write "none" where nothing applies.

```text
Mailfully setup

Mode: <new integration | migration from PROVIDER>
Branch: <branch>
Files changed:
  - <path>: <what changed>
Smoke test: <delivered | canceled (every recipient suppressed) | accepted but not yet delivered | error TYPE | not run (no test key) | not run (env file is committed)>, email id <id>
CLI: <used | skipped, because this machine's Node is older than 24 (or the CLI was not logged in), so domains are added in the dashboard>
Set in your hosting environment (not only the local env file):
  - MAILFULLY_API_KEY: a live key once the domain is verified
  - EMAIL_PROVIDER=mailfully: a migration, only after your account is approved; a new Django or Rails integration, once the domain is verified
  - MAILFULLY_WEBHOOK_SECRET: only if a webhook handler was added
Sending domain: <domain>, status <status>; records <printed for you | written to ZONE with your yes>
From domains: <domain>: verified | not added (one line each)
Suppressions carried over: yes | no | n/a
Marketing and bulk sends stay on <old provider>: <file:line list, or none>
Left alone (auth service or SMTP-only mail): <what, or none>
Rollback: unset EMAIL_PROVIDER. Keep the old provider's settings (<exact env var names, or none>) until you have run on Mailfully for a while.
Account: New accounts are reviewed before full-volume sending; the dashboard shows where yours stands.
```

Then:

- Name the hosting environment variables plainly. Setting them only in the local env file leaves
  production on the old setup.
- State no sending limit, review time or pacing figure in the report.
- Next steps: say that opens and clicks are tracked by default, which rewrites links, and that the
  domain's Tracking switch in the dashboard turns tracking off.
- Commit only if the user agrees, on the branch from phase 1. List the files you created or
  changed, stage only those, by path (`git add <path> …`), and commit the same paths
  (`git commit -m "<message>" -- <path> …`), so changes the user had already staged stay out;
  never `git add -A`, `git add .` or `git commit -a`. Check that `git status --short` shows no env
  file staged. Without git, skip this.

## References

- `references/api-essentials.md`: before any code. Send body, keys, `canceled`, status words, errors.
- `references/rest-clients.md`: not Node 24 or later. Helpers per language, Django and Rails adapters.
- `references/webhooks.md`: phase 5. Event names, headers, tested verifiers, the test vector.
- `references/migrate-resend.md`: from Resend (React Email, attachments by URL, scheduled sends).
- `references/migrate-sendgrid.md`: from SendGrid, and `sendEach` for any per-recipient send.
- `references/migrate-postmark.md`: from Postmark (message streams, tracking flags, templates).
- `references/migrate-nodemailer.md`: from Nodemailer, `smtplib` or any framework's SMTP settings.
- `references/dns-providers.md`: phase 6. Provider detection, conflict check, commands, verification.
