# Operations

Fires: when the project has CI, deployment or infrastructure config

Leading word: **3am page**. It broke in production at 3am: did anything notice, can on-call find out why, and can they put it back? Every gate here should be able to go **red**.

Artifact: a path-to-production list (change → CI gates it passes → how it deploys → how it is watched → how it is undone).

- **ci-gates**: Gates that cannot fail: `continue-on-error`, `|| true`, `allow_failure`, `--passWithNoTests`, tests or type checks that exist but never run in CI, required checks that are not required on the default branch.
- **backup-restore** (when the project keeps data it cannot regenerate): Backups exist, cover every store (database, object storage, auth users), and a restore has been run recently enough that someone knows how long it takes. An untested restore is a finding.
- **alerting** (when the project runs in production): Each critical path from recon raises an alert someone receives when it fails or slows: error rates, failed jobs, webhook failures, payment errors, queue depth. A failure the logs record but nothing pages on is silent.
- **runbooks** (when the project runs in production): For each alert, the first steps, the dashboards, and who owns it are written down where on-call will look.
- **cost-runaway** (when the project uses usage-billed services): A loop, retry storm, abusive user or leaked key that would multiply the bill (model calls, egress, function invocations, SMS, email) hits a budget alert or a hard cap first.
- **secrets-handling**: Secrets come from the platform's secret store, scoped per environment, rotatable without a code change, and never printed in CI logs or baked into build artifacts.
- **dependency-updates**: Dependencies get updated on a schedule (Dependabot, Renovate, a recurring task), and the CI gates are trusted enough that an update PR can merge.

Done: the path-to-production list covers every deployable in the repo, and every critical path from recon has an alerting answer.
