# debank-skill

A [Claude Code](https://claude.ai/claude-code) skill for querying blockchain wallet data via the [DeBank Pro API](https://cloud.debank.com/).

**Skill repo**: https://github.com/lolieatapple/debank-skill
**CLI repo**: https://github.com/lolieatapple/debank-cli

## What it does

This skill enables Claude Code to query on-chain data through natural language:

- Wallet balances across all EVM chains
- DeFi protocol positions (supply, borrow, rewards)
- Token balances and prices (current & historical)
- NFT holdings
- Transaction history
- Token approvals / allowances
- Gas prices

## Install

### 1. Install the CLI

```bash
npm install -g debank-cli
```

### 2. Configure your API key

Get a key from [cloud.debank.com](https://cloud.debank.com/), then:

```bash
debank config set-key YOUR_ACCESS_KEY
```

### 3. Install the skill

**Per-project** (add to your repo):

```bash
mkdir -p .claude/skills/debank
curl -o .claude/skills/debank/SKILL.md https://raw.githubusercontent.com/lolieatapple/debank-skill/main/SKILL.md
```

**Global** (available in all projects):

```bash
mkdir -p ~/.claude/skills/debank
curl -o ~/.claude/skills/debank/SKILL.md https://raw.githubusercontent.com/lolieatapple/debank-skill/main/SKILL.md
```

## Usage

In Claude Code, use the `/debank` slash command or just ask naturally:

```
/debank user balance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

/debank gas eth

Show me the DeFi positions for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

What tokens does vitalik.eth hold on Ethereum?
```

## License

MIT
