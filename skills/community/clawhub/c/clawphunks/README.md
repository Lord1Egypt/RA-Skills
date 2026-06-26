# ClawPhunks

10,000 left-facing pixel punks with OpenClaw red backgrounds. The first NFT collection for AI agents.

## Setup

```bash
npm install
```

## Generate Art

Downloads the phunks sprite sheet, slices into 10k PNGs with #C83232 backgrounds:

```bash
npm run generate-art
```

Output goes to `/output` directory.

## Run Server

```bash
cp .env.example .env
# Edit .env with your keys
npm run dev
```

## Deploy

```bash
vercel
```

## API

- `GET /collection` - Collection info
- `GET /marketplace` - Active listings
- `POST /mint` - Mint a phunk (x402)
- `POST /buy/:id` - Buy a listing (x402)
- `POST /list` - List for sale
- `POST /delist` - Remove listing

## ClawHub Skill

Copy `SKILL.md` to your ClawHub skills directory or publish to the registry.
