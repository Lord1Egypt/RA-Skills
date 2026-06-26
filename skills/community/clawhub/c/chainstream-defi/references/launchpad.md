# Launchpad Reference

## Token Creation

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v2/dex/:chain/create` | Create token on launchpad |

## CLI Command

```bash
npx @chainstream-io/cli dex create --chain sol --from <wallet> --name "My Token" --symbol MT --uri "ipfs://..." [--dex pumpfun] [--image <url>]
```

## Supported Platforms

| Chain | Platforms |
|-------|-----------|
| sol | PumpFun, Raydium LaunchLab |
| bsc | FourMeme |

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | sol / bsc / eth |
| `name` | Yes | Token name |
| `symbol` | Yes | Token symbol (ticker) |
| `uri` | Yes | Metadata URI (IPFS or HTTP) |
| `dex` | No | Launchpad platform: pumpfun, raydium (default: pumpfun) |
| `image` | No | Token image URL |

## Metadata URI

Before creating a token, upload metadata to IPFS:

```bash
# Use ChainStream IPFS presign endpoint
POST /v2/ipfs/presign → { uploadUrl, ipfsUri }
# Upload image/metadata to the presigned URL
# Use the returned ipfsUri as --uri parameter
```

## PumpFun vs Raydium LaunchLab

| Aspect | PumpFun | Raydium LaunchLab |
|--------|---------|-------------------|
| Chain | Solana | Solana |
| Bonding curve | Yes (graduated → Raydium pool) | Yes (graduated → Raydium pool) |
| Fee | 0.02 SOL | Variable |
| Graduation threshold | ~$69k market cap | Variable |
