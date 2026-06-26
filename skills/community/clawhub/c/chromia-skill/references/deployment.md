# Deployment

## Prerequisites

1. **Keypair**: Generate with `chr keygen --key-id <name>`. Stored in `~/.chromia/`. Produces:
   - `~/.chromia/<name>` — private key
   - `~/.chromia/<name>.pubkey` — public key
   - `~/.chromia/<name>_mnemonic` — mnemonic backup
2. **Container**: A leased container on the target network. The user must lease a container using their pubkey through the Chromia vault/dashboard. Ask the user for the container ID.
3. **`deployments` block in `chromia.yml`**: Defines network target, container, and (after first deploy) chain RIDs.

## chromia.yml Deployment Configuration

```yaml
deployments:
  testnet:
    url: https://node0.testnet.chromia.com:7740
    container: "<container_id_hex_string>"
    chains:
      my_dapp: x"<blockchain_rid_after_first_deploy>"
```

**Important:**
- `container` must be a plain string (NOT `x"..."` hex format) — e.g. `"004c4c75..."`, not `x"004c4c75..."`
- `chains` is added AFTER the first successful deployment — the CLI outputs the blockchain RID
- `url` is the testnet node URL. For mainnet use the mainnet node URL.

## Deployment Commands

```bash
# First deployment (create)
chr deployment create \
  --network testnet \
  --blockchain <blockchain_name> \
  --key-id <key_name> \
  -s chromia.yml \
  -y

# Update existing deployment
chr deployment update \
  --network testnet \
  --blockchain <blockchain_name> \
  --key-id <key_name> \
  -s chromia.yml

# Check deployment info
chr deployment info \
  --network testnet \
  --blockchain <blockchain_name> \
  -s chromia.yml
```

**Key flags:**
- `--key-id <name>` — references a keypair in `~/.chromia/` (preferred over `--secret`)
- `--secret <path>` — path to a secret file with `pubkey=<hex>` and `privkey=<hex>` on separate lines (alternative to `--key-id`)
- `-s chromia.yml` — settings file (always include this)
- `-bc <name>` / `--blockchain <name>` — which blockchain to deploy
- `-d <name>` / `--network <name>` — which deployment target from `deployments:` in settings
- `-y` — skip confirmation prompt

## Deployment Workflow

1. If the user already has an active container and keypair, skip to step 3. Otherwise, generate a keypair: `chr keygen --key-id my-dapp`
2. Give the **public key** to the user to lease a container on testnet/mainnet
3. User provides the **container ID** and keypair name/path
4. Add `deployments:` block (with url + container) at the bottom of `chromia.yml`
5. Ensure `admin_pubkey` in `moduleArgs` matches the deployment keypair's pubkey
6. Run `chr test` to validate compilation
7. Run `chr deployment create ...` with `-y` flag
8. On success, save the returned blockchain RID into `deployments.<network>.chains.<name>` in `chromia.yml`
9. For subsequent updates, use `chr deployment update` instead of `create`

## Common Deployment Errors

| Error | Cause | Fix |
|---|---|---|
| `Container <id> not found` | Invalid or expired container ID | User must lease a valid container with their pubkey |
| `Incorrect type, expected String (location: deployments->...->container)` | Container ID uses `x"..."` hex format | Use plain string: `"abc123..."` |
| `does not contain 'pubkey' and/or 'privkey' properties` | Raw key file used with `--secret` | Use `--key-id` instead, or create a file with `pubkey=X` and `privkey=Y` lines |
| `Bad module_args for module '...'` | Wrong keys in `moduleArgs` config | Check the module's `struct module_args` for expected field names |

## Other Deployment Commands

```bash
# Pause a running blockchain
chr deployment pause --network testnet --blockchain <name> --key-id <key> -s chromia.yml

# Resume a paused blockchain
chr deployment resume --network testnet --blockchain <name> --key-id <key> -s chromia.yml

# Remove a deployment (permanent!)
chr deployment remove --network testnet --blockchain <name> --key-id <key> -s chromia.yml
```

## Validation Loop (for config/deployment)

1. Edit `chromia.yml`
2. Run `chr node start --wipe` to validate locally
3. Fix any errors reported
4. Run `chr test` to verify all tests pass
5. Repeat until clean
6. Then deploy with `chr deployment create` or `chr deployment update`
