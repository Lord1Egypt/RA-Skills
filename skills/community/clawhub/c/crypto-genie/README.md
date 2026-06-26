# 🧞 Crypto Genie

**Your AI-powered cryptocurrency safety assistant**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green.svg)](https://openclaw.ai)

A powerful AI-powered cryptocurrency safety assistant that protects users from fraud including phishing attacks, honeypots, rug pulls, and ponzi schemes. Delivers instant risk assessments with comprehensive blockchain analysis and smart contract verification.

## ✨ Key Features

- ⚡ **Lightning Fast** - Database queries complete in <5ms (500-1000x faster than API calls)
- 🔄 **Real-Time Sync** - Unknown addresses fetched and analyzed on-demand
- 🎯 **Deep Analysis** - Decodes transaction messages and detects suspicious keywords
- 🛡️ **Multi-Source Detection** - Combines Etherscan, ChainAbuse, and local databases
- 🔐 **Secure** - AES-256 encrypted API key storage with PBKDF2
- 📊 **Smart Risk Scoring** - Advanced algorithm with 0-100 risk scores
- 🔍 **Transaction Analysis** - Identifies exploit groups like Lazarus, phishing attempts, and more
- 🌐 **Multi-Chain Ready** - Ethereum support with expandable architecture

## 🚀 Quick Start

### 1. Installation

**Option A: Via ClawHub (Recommended)**
```bash
clawhub install crypto-genie
```

**Option B: Manual Installation**
```bash
# Clone or navigate to the directory
cd crypto-genie

# Run auto-installer (creates venv, installs dependencies, initializes database)
bash install.sh
```

**Requirements:**
- Python 3.8 or higher
- pip
- Virtual environment support (python3-venv)

### 2. Configure API Key (Optional but Recommended)

Get a free Etherscan API key: https://etherscan.io/myapikey

**Option A: Interactive Setup (Recommended)**
```bash
./setup.sh
# Follow the wizard - your API key will be encrypted with AES-256
```

**Option B: Environment Variable**
```bash
export ETHERSCAN_API_KEY="your_api_key_here"
```

### 3. Start Using

**Check any Ethereum address instantly:**
```bash
# Direct check (uses database + real-time sync if needed)
python3 crypto_check_db.py 0x1234567890abcdef1234567890abcdef12345678

# With JSON output
python3 crypto_check_db.py 0x1234... --json

# Convenience script (syncs in background if needed)
./check_address.sh 0x1234...
```

### 4. Optional: Background Sync Worker

For bulk processing or scheduled syncs:

```bash
# Run continuously (processes queue)
python3 sync_worker.py

# Process N addresses then stop
python3 sync_worker.py --max-jobs 20

# Add to crontab for periodic syncing
# Every 10 minutes, process 30 addresses
*/10 * * * * cd /path/to/crypto-genie && source venv/bin/activate && python3 sync_worker.py --max-jobs 30
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[SKILL.md](SKILL.md)** | Complete usage guide with examples and commands |
| **[DATABASE_ARCHITECTURE.md](DATABASE_ARCHITECTURE.md)** | Technical deep dive into database schema and architecture |
| **[SECURITY.md](SECURITY.md)** | Security best practices and encryption details |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history and migration guides |

## 🎨 Example Output

### Critical Risk Detection

```
🚨 Analysis for 0x098b716b8aaf21512996dc57eb0615e2383e2f96

Risk Score: 100/100 - CRITICAL RISK
Last Updated: 2026-02-20 07:14:32

🚨 KNOWN SCAM DETECTED!

⚙️ Smart Contract
⚠️ NOT VERIFIED on Etherscan
   Transactions: 38
   Balance: 101.802430 ETH

🚨 5 Scam Indicator(s) Detected:
   • Suspicious keyword detected: 'lazarus' (confidence: 80%)
   • Suspicious keyword detected: 'hack' (confidence: 80%)
   • Suspicious keyword detected: 'exploit' (confidence: 80%)

⚠️ 5 Suspicious Transaction(s):
   • 0x74f7fbfe5a0bd3...
     Reason: Suspicious keyword detected: 'lazarus'
     Message: "Greetings Lazarus Vanguard..."

📋 Recommendations:
  🚫 DO NOT send funds to this address
  ⚠️ This address has been flagged as high risk
  📞 Report the source that gave you this address
```

## 🏗️ How It Works

### Architecture Overview

```
                    User Query
                        ↓
              crypto_check_db.py
                        ↓
            ┌───────────┴───────────┐
            ↓                       ↓
    Found in Database         Not in Database
            ↓                       ↓
    Instant Result          Real-Time Sync
      (<5ms)                 (5-10 seconds)
                                    ↓
                            Etherscan API
                              • Balance
                              • TX Count
                              • TX Analysis
                              • Contract Code
                                    ↓
                              Store in DB
                                    ↓
                           Return Analysis
```

### Key Benefits

1. **Instant Results for Known Addresses** - Database queries complete in <5ms
2. **Real-Time Sync for New Addresses** - Automatic fetch from Etherscan with progress updates
3. **No Manual Queue Management** - System handles unknown addresses automatically
4. **Smart Caching** - Future checks of the same address are instant
5. **Full Transaction Analysis** - Decodes transaction messages and identifies suspicious patterns
6. **Background Worker (Optional)** - For bulk processing and scheduled updates

## 🔍 Detection Capabilities

### Scam Types Detected

| Scam Type | Detection Method | Examples |
|-----------|------------------|----------|
| **Phishing** | Keyword analysis | "private key", "seed phrase", "verify wallet", "urgent action" |
| **Honeypot Contracts** | Contract verification status | Unverified contracts, suspicious code patterns |
| **Rug Pull** | Transaction pattern analysis | Sudden large withdrawals, liquidity drains |
| **Exploit Groups** | Transaction message analysis | "Lazarus Vanguard", "Orbit Bridge Hacker", exploit mentions |
| **Social Engineering** | Suspicious keywords | "claim reward", "airdrop winner", "limited time" |
| **Hack/Breach Indicators** | Historical data | Known compromised addresses, hack mentions |

### Risk Scoring Algorithm

Risk scores are calculated based on multiple factors:

- **Suspicious Transactions** (+25 per TX, max +50)
- **Account Age** (new accounts: +10)
- **Balance Patterns** (high balance + suspicious activity: +20)
- **Contract Status** (unverified contracts: +30)
- **Known Scam Database** (flagged addresses: +100)
- **Keyword Confidence** (80% confidence per detection)

### Risk Levels

| Score | Level | Icon | Action |
|-------|-------|------|--------|
| **0-19** | Low Risk | ✅ | Generally safe, proceed with caution |
| **20-49** | Medium Risk | ℹ️ | Exercise caution, verify source |
| **50-79** | High Risk | ⚠️ | High concern, avoid interaction |
| **80-100** | Critical Risk | 🚨 | DO NOT INTERACT - Known scam |

## 🔧 Configuration & Commands

### Database Location

Default: `~/.config/crypto-genie/crypto_data.db`

Override with environment variable:
```bash
export CRYPTO_GENIE_DB_PATH="/custom/path/to/crypto_data.db"
```

### Command Reference

#### Address Checking

```bash
# Check address (human-readable output)
python3 crypto_check_db.py 0x1234567890abcdef1234567890abcdef12345678

# JSON output (for integration)
python3 crypto_check_db.py 0x1234... --json

# Convenience script (auto-handles syncing)
./check_address.sh 0x1234...
```

#### Sync Worker Commands

```bash
# Add address to queue manually
python3 sync_worker.py --add-address 0x1234...

# Run worker continuously (processes entire queue)
python3 sync_worker.py

# Process N addresses then exit
python3 sync_worker.py --max-jobs 20

# Custom delay between API calls (default: 1.5s)
python3 sync_worker.py --delay 2.0

# View database statistics
python3 sync_worker.py --stats

# Initialize/verify database
python3 database.py
```

### Scheduled Sync (Optional)

For bulk processing or periodic updates, add to crontab:

```bash
# Edit crontab
crontab -e

# Add this line (every 10 minutes, process 30 addresses)
*/10 * * * * cd /path/to/crypto-genie && source venv/bin/activate && ETHERSCAN_API_KEY="your_key" python3 sync_worker.py --max-jobs 30 --delay 2.0 >> logs/sync.log 2>&1
```

### Etherscan API Rate Limits

| Tier | Rate Limit | Daily Limit |
|------|------------|-------------|
| **Free** | 5 calls/sec | 100,000 calls/day |
| **Standard** | 10 calls/sec | Higher limits |

**Note:** Each address sync requires 4 API calls (balance, TX count, TX list, contract code)

## 🛡️ Security & Privacy

- ✅ **AES-256 Encryption** - API keys encrypted with PBKDF2 (100,000 iterations)
- ✅ **Local Processing** - All analysis happens on your machine
- ✅ **No Third-Party Sharing** - API key only sent to Etherscan (HTTPS)
- ✅ **Open Source** - Fully auditable code
- ✅ **No Telemetry** - Zero data collection or tracking
- ✅ **No Logging** - API keys never logged or exposed

See [SECURITY.md](SECURITY.md) for detailed security practices.

## 🐛 Troubleshooting

### Address Not Yet Synced

**Problem:** Address shows as "UNKNOWN" or "not in database"

**Solution:**
```bash
# The system will automatically sync it when you check
python3 crypto_check_db.py 0x...
# Wait 5-10 seconds for real-time sync

# Or use convenience script
./check_address.sh 0x...
```

### API Key Not Configured

**Problem:** Error message about missing Etherscan API key

**Solution:**
```bash
# Interactive setup (recommended)
./setup.sh

# Or set environment variable
export ETHERSCAN_API_KEY="your_key_here"

# Or add to ~/.bashrc for persistence
echo 'export ETHERSCAN_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

### Rate Limit Errors

**Problem:** Etherscan API rate limit exceeded

**Solution:**
```bash
# Increase delay between requests
python3 sync_worker.py --delay 3.0

# Or reduce batch size
python3 sync_worker.py --max-jobs 10 --delay 2.5
```

### Database Issues

**Problem:** Database corruption or initialization errors

**Solution:**
```bash
# Reinitialize database
python3 database.py

# If problems persist, backup and recreate
mv ~/.config/crypto-genie/crypto_data.db ~/.config/crypto-genie/crypto_data.db.backup
python3 database.py
```

### Permission Errors

**Problem:** Cannot write to database or config directory

**Solution:**
```bash
# Fix permissions
chmod 755 ~/.config/crypto-genie/
chmod 644 ~/.config/crypto-genie/crypto_data.db

# Or run with proper user permissions
sudo chown -R $USER:$USER ~/.config/crypto-genie/
```

## 📈 Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Cached Address Check** | <5ms | Database query only |
| **New Address Sync** | 5-10 seconds | Includes 4 Etherscan API calls |
| **Database Size** | ~1KB per address | Includes transactions and indicators |
| **Capacity** | Millions of addresses | SQLite handles large datasets efficiently |
| **API Calls** | 0 for cached | 4 for new addresses (balance, TX count, TX list, code) |
| **Improvement vs Direct API** | 500-1000x faster | For cached addresses |

### Performance Comparison

| Scenario | Old Method (v1) | New Method (v2+) | Improvement |
|----------|-----------------|------------------|-------------|
| **Known address** | 2-5 seconds (4 API calls) | <5ms (database) | **500-1000x faster** |
| **New address** | 2-5 seconds | 5-10 seconds (with real-time sync) | Similar, but cached for future |
| **Repeated checks** | 2-5 seconds each time | <5ms each time | **Massive improvement** |
| **Rate limits** | Hit on every check | Never hit on cached addresses | **No limits** |

## 📁 Project Structure

```
crypto-genie/
├── README.md                    # This file
├── CHANGELOG.md                 # Version history and migration guides
├── SECURITY.md                  # Security best practices
├── SKILL.md                     # Complete usage documentation
├── DATABASE_ARCHITECTURE.md     # Technical deep dive
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── package.json                 # npm metadata
├── clawhub-manifest.json        # ClawHub metadata
├── install.sh                   # Auto-installer script
├── setup.sh                     # API key setup wizard
├── check_address.sh             # Convenience script
├── verify_package.sh            # Package verification
├── database.py                  # SQLite database layer (4 tables)
├── crypto_check_db.py           # Main checker (database-first)
├── sync_worker.py               # Background Etherscan sync worker
├── secure_key_manager.py        # AES-256 encrypted key storage
├── scam_database.py             # Known scam address database
├── blockchain_detector.py       # Multi-chain address detection (optional)
└── venv/                        # Virtual environment (created on install)
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs** - Open an issue with details and reproduction steps
2. **Suggest Features** - Share your ideas for improvements
3. **Submit Pull Requests**
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/amazing-feature`)
   - Commit your changes (`git commit -m 'Add amazing feature'`)
   - Push to the branch (`git push origin feature/amazing-feature`)
   - Open a Pull Request
4. **Improve Documentation** - Help make docs clearer and more comprehensive
5. **Add Scam Data** - Contribute to the known scam database

### Development Setup

```bash
# Install in development mode
bash install.sh

# Run tests (if available)
python3 -m pytest tests/

# Check code style
python3 -m pylint *.py
```

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

Free to use, modify, and distribute. No warranty provided.

## 🏆 Credits & Acknowledgments

**Developed by Trust Claw Team**

**Built with:**
- **SQLite** - Lightweight, serverless database
- **Etherscan API** - Ethereum blockchain data
- **ChainAbuse API** - Community-reported scams
- **Python 3.8+** - Core language
- **Cryptography** - AES-256 encryption
- **httpx** - Async HTTP client

**Inspired by:**
- OpenClaw AI framework
- NeoClaw Hackathon 2026
- Community feedback and security researchers

## 🔗 Links & Resources

- 🌐 **ClawHub:** https://clawhub.com/crypto-genie
- 📖 **Documentation:** [SKILL.md](SKILL.md)
- 🔐 **Security:** [SECURITY.md](SECURITY.md)
- 💬 **Discord:** https://discord.com/invite/clawd
- 🔑 **Get Etherscan API Key:** https://etherscan.io/myapikey

## 📞 Support

Need help? Here's how to get support:

1. **Read the docs** - Check [SKILL.md](SKILL.md) for detailed usage
2. **Join Discord** - Get help from the community
3. **Check ClawHub** - Community discussions and updates

## ⚠️ Disclaimer

This tool provides risk assessments based on available data and pattern analysis. It should be used as **one factor** in your decision-making process, not the sole factor. Always:

- ✅ Do your own research
- ✅ Verify information from multiple sources
- ✅ Never send funds to unverified addresses
- ✅ Be cautious with new or unverified projects
- ✅ Keep your private keys secure

**Not financial advice. Use at your own risk.**

---

**🔐 Stay safe in crypto! Always verify addresses before sending funds.**

**Made with ❤️ by the Trust Claw Team**
