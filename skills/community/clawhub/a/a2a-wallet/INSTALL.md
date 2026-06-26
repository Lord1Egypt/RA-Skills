# a2a-wallet Installation Guide

## macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/planetarium/a2a-x402-wallet/main/scripts/install.sh | sh
```

Supported platforms: macOS (Apple Silicon, Intel), Linux (x64, arm64).

## Windows

Download `a2a-wallet-windows-x64.exe` from the [Releases](https://github.com/planetarium/a2a-x402-wallet/releases/latest) page, rename it to `a2a-wallet.exe`, and place it in a folder on your PATH.

## Verify

```bash
a2a-wallet --version
```

## First-time setup

Create a local wallet — this is the recommended default:

```bash
a2a-wallet wallet create
# → Wallet created successfully. (set as default)
#   Name:    wallet-1
#   Address: 0x...
#   Path:    m/44'/60'/0'/0/0
```

The new wallet is automatically set as the default. You're ready to go.

If you have multiple local wallets and want to switch between them, use `wallet use`:

```bash
a2a-wallet wallet use <name>
# → Active wallet set to "wallet-1" (0x...).
```
