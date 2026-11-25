# Operations: a project that is already deployed

Commands are run in the project's root directory and read applicationId from deploy.manifest.json. Their full syntax and output are in section 5 of the [appcli reference](appcli-reference.md); the project's states are in its section 3.

Contents: everyday commands · a project that is asleep · runtime parameters · public access and the domain's prefix · restoring data · deleting a project · rolling back

## Everyday commands

~~~bash
appcli status --json            # the project's state, the live version, a task in progress
appcli logs --tail 200 --json
appcli logs --follow
appcli deployments --json       # earlier deployments; which can be rolled back to
appcli deployment <id> --wait --json
appcli cancel <id>
appcli backups --json
appcli console                  # a one-time sign-in link that opens the console
appcli wake --wait --json       # wakes a sleeping project
appcli restart --wait --json    # restarts the live version as it is, for an application that hangs
appcli plan --json              # the plan, its limits, what is used, and the projects that take its places
~~~

Redact logs before showing them (SKILL.md, rule 5).

## A project that is asleep

When `status` in `appcli status` is `sleeping`, the platform has stopped the project. Its data, its address and its earlier versions are all kept, and it still takes one of the plan's places. `sleepReason` says why:

- `idle`: nobody visited it for days in a row (the plan's `sleepAfterDays`). The platform wakes it when someone opens the address; that first visit takes ten seconds or so. `appcli wake --wait --json` wakes it too. When the user asks why the site "does not open" or "says it is starting", look for this state first.
- `plan`: the plan has no room for it (the plan ran out and the user is back on the free plan, there are too many projects, or it uses a database service the plan does not include). `appcli wake` then returns `PLAN_LIMIT_EXCEEDED` and the address shows a "paused" page. Once the user renews or upgrades, the platform wakes it by itself; nothing needs to be deployed again.

`sleepNote` in `appcli status` says, for the project in hand, which of these it is and what brings it back; pass it on.

While a project is asleep:

- Its status, logs and deployments can be read, and runtime parameters can be saved.
- Restarting, rolling back, applying parameters and restoring data need it awake first.
- When waking fails (the application does not come up) the project stays asleep: report the error code and the logs and suggest contacting the administrator.

## Runtime parameters

~~~bash
appcli config get --json
appcli config set NAME          # the value is typed in: the user runs this in their own terminal
appcli config regenerate NAME   # a new signing secret
appcli config apply --wait --json
~~~

- `set`, `unset` and `regenerate` only save; `appcli config apply` is what makes the saved parameters live. Never report a save as being live.
- After `regenerate` and `apply`, signed-in users are signed out; tell the user before doing it.
- The rules are in [personal project configuration](personal-configuration.md).

## Public access and the domain's prefix

~~~bash
appcli access --json                # the address, and whether public access is on
appcli access external off --json   # turns public access off, at once
appcli access external on --json    # turns it on again
appcli access name <prefix> --json  # changes the domain's prefix
~~~

- Before turning public access off, say what follows: the address is the application's only one, so it cannot be reached until public access is turned on again.
- A prefix is 3 to 63 lower-case letters, digits and hyphens. `SUBDOMAIN_UNAVAILABLE` means it is reserved or taken: ask the user for another.
- Before changing the prefix, tell the user: the old address stops working afterwards and may be taken by someone else. `PUBLIC_URL` inside the application changes with the next deployment or `appcli config apply`.

## Restoring data

Only when the user explicitly asks, and after the user has confirmed which backup (which point in time) to restore:

~~~bash
appcli restore --backup <backupId> --confirm <applicationId> --wait --json
~~~

Tell the user:

- A restore replaces only what the backup contains. A pre-deployment backup holds the database only and does not touch attachments.
- There are no scheduled backups. A project with pre-deployment backups turned off has only "pre-restore" backups.
- The application stops briefly during the restore.
- The data that is replaced is kept as a "pre-restore" backup for 14 days and can be restored with the same command.
- A restore that fails is undone automatically.
- A project that has never been deployed successfully cannot be restored.

## Deleting a project

Only when the user explicitly asks, and after the user has confirmed the project ID:

~~~bash
appcli delete --confirm <applicationId> --wait --json
~~~

Tell the user:

- This deactivates the project; it does not delete it at once. The container stops and the address closes.
- The data, the port and the address are kept for 30 days, during which the platform's administrator can bring it back (same address). Only after 30 days can the administrator delete it for good.
- A deactivated project no longer takes one of the plan's places.
- A deactivated project cannot be deployed again, unless the applicationId in the manifest is emptied and it is deployed as a new project.

## Rolling back

Only when the user explicitly asks:

~~~bash
appcli deployments --json
appcli rollback --to <deploymentId> --wait --json
~~~

- Only versions that `appcli deployments` lists with `canRollback: true` can be gone back to: the plan keeps a number of earlier versions (`versionsKept` in `appcli plan`) and the images of older ones are cleaned up. A rollback to one of those returns `ROLLBACK_NOT_ALLOWED` with `details.reason` `versions_kept`; offer the user the versions that are still kept, or deploying that code again.
- Report the version before and after.
- A rollback uses the target version's own settings (port, storage, resources) with the runtime parameters as they are saved now. Before it, the server backs up the database as the project is set (backupBeforeDeploy).
- A rollback does not restore the database or the attachments. When the newer version made a migration that is not backward compatible, warn the user of the risk, and when needed combine it with a restore of the pre-deployment backup.
