# AGENTS.md - Global Development Environment

This file provides an overview of the development environment at `/Users/ryanmolinich`.

## Directory Structure

```
/Users/ryanmolinich/
├── Projects/                    # Active development projects
│   ├── agave/                  # Solana validator (Rust workspace)
│   ├── solana-arbitrage/       # Funding rate arbitrage bot
│   ├── pocket-options-bot/     # Binary options trading bot
│   └── ...                     # Other projects
├── .openclaw/skills/           # OpenClaw AI skills
├── .cargo/                     # Rust/Cargo configuration
├── .bun/                       # Bun JavaScript runtime
├── .config/                    # Tool configurations
└── .solana/keys/              # Secure wallet storage
```

## Active Projects

### 1. Agave (`~/Projects/agave/`)
**Type:** Rust workspace  
**Purpose:** Solana blockchain validator by Anza  
**Size:** 6.8 GB  
**Status:** Primary development project

**Key Commands:**
```bash
cd ~/Projects/agave
./ci/test-checks.sh      # Run all checks
./ci/test-sanity.sh      # Sanity checks
cargo build              # Build workspace
cargo test               # Run tests
```

**See:** `~/Projects/agave/AGENTS.md`

### 2. Solana Arbitrage Bot (`~/Projects/solana-arbitrage/`)
**Type:** TypeScript/Node.js  
**Purpose:** Cross-DEX funding rate arbitrage  
**Strategy:** Delta-neutral funding arbitrage  
**Status:** Standalone project (extracted from OpenClaw skill)

**Key Commands:**
```bash
cd ~/Projects/solana-arbitrage/scripts
npm install
npm run scan             # Run scanner
npm run trade:dry        # Dry run mode
```

**See:** `~/Projects/solana-arbitrage/AGENTS.md`

### 3. Pocket Options Bot (`~/Projects/pocket-options-bot/`)
**Type:** TypeScript/Node.js  
**Purpose:** Binary options trading automation  
**Strategy:** Martingale + technical indicators  
**Status:** Recovered from Zenflow worktree

**Key Commands:**
```bash
cd ~/Projects/pocket-options-bot
npm install
npm run dev              # Development mode
npm run build            # Production build
```

**See:** `~/Projects/pocket-options-bot/AGENTS.md`

### 4. My Solana Wallet (`~/.solana/keys/`)
**Type:** Keypair storage  
**Purpose:** Secure wallet key storage  
**Security:** chmod 600 permissions

## AI Tools & Skills

### OpenClaw Skills (`~/.openclaw/skills/`)
9 skill packages for OpenClaw AI assistant:
- `solana-funding-arb-2.1.0.zip` - Also extracted to standalone project
- `base-trader-1.1.1.zip` - Base chain trading
- `hyperliquid-prime-0.1.4.zip` - Hyperliquid perps
- `browser-use-1.0.0.zip` - Cloud browser automation
- `telegram-1.0.1.zip` - Telegram bot builder
- `mac-notes-agent-1.1.0.zip` - macOS Notes integration
- `minara-1.1.9.zip` - Crypto trading intelligence
- `agent-browser-clawdbot-0.1.0.zip` - Browser automation
- `theswarm-1.0.0.zip` - AI agent social network

**All scanned and verified safe.**

### Global AI Tools
Installed via Bun:
- `openclaw` - AI assistant CLI
- `opencode` - AI coding assistant
- `gemini` - Google Gemini CLI
- `mcporter` - MCP server
- `context7` - Live documentation MCP server (via mcporter)

## Toolchains

### Rust/Cargo
- **Version:** 1.93.0 (pinned)
- **Location:** `~/.rustup/`, `~/.cargo/`
- **Binaries:** `~/.cargo/bin/`
- **Primary use:** Agave validator development

### Bun/Node.js
- **Version:** Latest (via Bun)
- **Location:** `~/.bun/`
- **Global packages:** `~/.bun/bin/`
- **Primary use:** Trading bots, web tools

### Python
- **Manager:** uv (Astral)
- **Location:** `~/.local/bin/uv`
- **Primary use:** Solana tools, data analysis

## Security

### Secure Storage
- **SSH Keys:** `~/.ssh/` (restricted permissions)
- **Solana Keys:** `~/.solana/keys/` (chmod 600)
- **Secrets:** Load from `~/.secrets/` (create as needed)

### Environment
- Never commit `.env` files
- Use `.env.example` as templates
- Keep API keys in environment variables

## Cross-Project Relationships

### Trading Bots
Both trading projects share concepts but operate independently:
- **Solana Arbitrage** - DEX funding rates, Solana ecosystem
- **Pocket Options** - Binary options, browser automation

### Solana Ecosystem
- **Agave** - Validator code (read-only reference for bots)
- **Solana Arbitrage** - Uses Solana Web3.js
- **Wallet Keys** - Shared across Solana projects

## Useful Aliases

Add to `.zshrc`:
```bash
# Project shortcuts
alias agave='cd ~/Projects/agave'
alias arbitrage='cd ~/Projects/solana-arbitrage/scripts'
alias pocket='cd ~/Projects/pocket-options-bot'

# Development
alias lint='./ci/test-checks.sh'
alias skills='ls ~/.openclaw/skills/'
```

## Maintenance

### Cleanup Commands
```bash
# Clean npm cache
npm cache clean --force

# Clean bun cache
bun pm cache rm

# Clean cargo (use with caution)
cargo cache --autoclean

# Remove test ledgers
rm -rf ~/test-ledger
```

### Health Checks
```bash
# Before committing changes in agave
./ci/test-sanity.sh
./ci/test-checks.sh

# Check disk usage
du -sh ~/{.bun,.rustup,.cargo,.npm,.cache} 2>/dev/null
```

## Support Resources

- **Agave:** See `~/Projects/agave/CONTRIBUTING.md`
- **Git Config:** `~/.gitconfig`
- **Global Gitignore:** `~/.gitignore`
- **Shell Config:** `~/.zshrc`

---

**Environment Status:** ✅ Organized and secured

**Last Updated:** 2026-02-13
