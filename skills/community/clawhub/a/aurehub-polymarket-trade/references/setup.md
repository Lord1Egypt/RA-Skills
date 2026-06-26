# Setup Reference

## First-Time Setup Checklist

1. **WDK vault** — `~/.aurehub/.wdk_vault` must exist (created by xaut-trade setup)
2. **Vault password** — `~/.aurehub/.wdk_password` must exist
3. **Environment** — `~/.aurehub/.env` with `POLYGON_RPC_URL=<url>` (copy from `.env.example`)
4. **Config** — `~/.aurehub/polymarket.yaml` (copy from `config.example.yaml`)
5. **Dependencies** — `npm install` in `scripts/` directory
6. **CLOB credentials** — `~/.aurehub/.polymarket_clob` (derived via `node scripts/setup.js`)

## Deriving CLOB Credentials

```bash
cd skills/polymarket-trade/scripts
npm install
node setup.js
```

What happens:
1. Loads vault + password from `~/.aurehub/`
2. Derives your wallet address (Polygon, BIP-44 path m/44'/60'/0'/0/0)
3. Signs an EIP-712 message to call `POST /auth/api-key` on `https://clob.polymarket.com`
4. Saves credentials to `~/.aurehub/.polymarket_clob` (chmod 600)

## Re-deriving Credentials

If credentials expire or become invalid:
```bash
rm ~/.aurehub/.polymarket_clob
node scripts/setup.js
```

## Security Notes

- Private key is decrypted from vault in memory only, never stored
- CLOB credentials (key/secret/passphrase) are stored at `~/.aurehub/.polymarket_clob` with restricted permissions
- No data is sent to any relay — all calls go directly to `https://clob.polymarket.com`
