# Teardown (remove an A2A endpoint)

`npx -y a2a-exposed@latest config` shows the config directory and the saved `A2A_WORKER_NAME`, `A2A_D1_ID`, `A2A_D1_NAME`, `A2A_TUNNEL_TOKEN_FILE` (the path), and `CF_PROFILE`.

Before removal, identify the Cloudflare account with `npx cf auth whoami`, explain the resources and data being deleted, and wait for the human's explicit yes ([consent checklist](deploy.md#before-cloudflare-changes)). `--yes` passes that decision to the CLI; it does not replace human consent.

`uninstall` prints that plan before it asks. `--dry-run` prints the plan and changes nothing. Off a terminal, pass `--yes`.

```bash
npx -y a2a-exposed@latest uninstall --yes
rm -rf <config dir>                        # owner token, WAKE_* values, stored peer tokens, the Worker project
```

`uninstall` removes the Worker, then the wake tunnel when the config has one (same objects as `tunnel rm`, one line each), then the D1 database. It skips Worker secrets after it deletes the Worker, finds it already gone, or gets Cloudflare error 10000. A failed Worker delete, including Cloudflare error 10000, leaves the D1 database in place while the Worker still exists. The tunnel is still removed when that step succeeds. A DNS-only failure lists the Worker, the tunnel, the Access application, the service token, and the token file under Removed when this run removed them, and names the DNS record under Not removed. When the Worker delete did not happen in this run, the D1 line says it is untouched because the Worker delete did not happen in this run. The summary says what was removed, what was not, and that a rerun is safe. A missing object is already gone. An empty config exits 1 with `nothing is deployed from <config dir>`. The config directory stays until you remove it. The owner token and `WAKE_*` values stay in `config.env`. A later `init` reuses the owner token.

Stop `cloudflared` afterwards (`cloudflared service uninstall` when it runs as a service). After you delete the Worker, check that Worker's custom domains and routes, and the zone's DNS, and remove a custom domain that is still listed. `tunnel rm` deletes the wake hostname's DNS record. The account's workers.dev subdomain stays. A Zero Trust organization created with `--zero-trust-org` is permanent. Peers lose access immediately.

To call `cf` yourself, run it from `<config dir>/worker`, or create the cache directory named in the error (`mkdir -p node_modules/.cache/cloudflare`) in the current directory. `cf` uses that directory when it is writable. Otherwise it exits with `EACCES: mkdir '.../node_modules/.cache/cloudflare'`. Add `--profile <name>` for a named login.

```bash
npx cf workers delete <A2A_WORKER_NAME> --force
npx cf d1 delete <A2A_D1_ID> --force
```

When the config is gone, the tunnel, Access application, service token, and DNS record are still named `a2a-exposed wake <worker>`.

In the Cloudflare dashboard, open the sections for Tunnels, Access applications, Access service tokens, and the zone's DNS records. Also check that Worker's custom domains and routes.

```bash
npx cf tunnels list
npx cf tunnels connections cleanup <tunnel-id> --force
npx cf tunnels delete <tunnel-id> --force
npx cf zero-trust access applications list
npx cf zero-trust access applications delete <app-id> --force
npx cf zero-trust access service-tokens list
npx cf zero-trust access service-tokens delete <token-id> --force
npx cf dns records list -z <zone-id>
npx cf dns records delete <record-id> -z <zone-id> --force
```
