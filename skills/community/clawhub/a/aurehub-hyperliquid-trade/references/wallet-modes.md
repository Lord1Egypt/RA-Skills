# Wallet Modes

## WDK Mode

- **Storage**: Encrypted vault (`~/.aurehub/.wdk_vault`) — PBKDF2-SHA256 + XSalsa20-Poly1305
- **Encryption**: PBKDF2 with 100k iterations, seed never stored as plaintext
- **Dependencies**: Node.js >= 20.19.0 only — no external tools required
- **Config**: `WALLET_MODE=wdk` + `WDK_PASSWORD_FILE` in `.env`
- **Shared**: Same vault used by xaut-trade and other aurehub skills

## Note on Hyperliquid address

Hyperliquid uses EVM-compatible addresses. Your wallet address is the same address you use on Hyperliquid. Verify with:
```bash
node "$HL_SCRIPTS_DIR/balance.js" address
```
