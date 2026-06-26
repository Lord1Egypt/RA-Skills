# FX SDK Skill

Agent skill for integrating the **FX Protocol TypeScript SDK** (`@aladdindao/fx-sdk`) with AI coding assistants. Use it to query positions, build transaction plans (increase/reduce/adjust leverage, deposit/mint, repay/withdraw), and generate runnable agent-ready code on Ethereum mainnet.

## About f(x) Protocol

f(x) Protocol is a decentralized on-chain trading platform that enables stress-free leverage on ETH and WBTC while delivering the highest organic & sustainable yield on stablecoins.

### Key Features

- **Up to 7X Leverage**: Long or short exposure with minimum liquidation risk & funding costs
- **fxUSD Stablecoin**: Scalable & decentralized stablecoin with a strong peg to the dollar
- **Overcollateralized**: Backed by wstETH and WBTC

🌐 **Website**: [https://fx.aladdin.club/](https://fx.aladdin.club/)

## Install

**Cursor**  
Copy this repo into project or personal skills:

```bash
# Project scope — skill only in this repo
git clone https://github.com/AladdinDAO/fx-sdk-skill.git .cursor/skills/fx-sdk-skill

# Personal scope — skill in all your projects
git clone https://github.com/AladdinDAO/fx-sdk-skill.git ~/.cursor/skills/fx-sdk-skill
```

**Claude Code**  
```bash
# Project
git clone https://github.com/AladdinDAO/fx-sdk-skill.git .claude/skills/fx-sdk-skill

# Personal
git clone https://github.com/AladdinDAO/fx-sdk-skill.git ~/.claude/skills/fx-sdk-skill
```

**Codex CLI**  
```bash
git clone https://github.com/AladdinDAO/fx-sdk-skill.git ~/.codex/skills/fx-sdk-skill
```

The assistant will load `SKILL.md` from the skill directory when the context matches (e.g. “integrate fx-sdk”, “FX position”, “depositAndMint”, “fxSAVE”, “bridge”).

## When to Use

- Integrate `@aladdindao/fx-sdk` into an agent or tool.
- Generate transaction execution code for positions (increase/reduce/adjust), deposit/repay, bridge (Base <-> Ethereum), and fxSAVE (config/totals, balance, redeem status, claimable, deposit, withdraw, claim).
- Debug SDK parameters or validate FX trading workflows.
- Build adapter functions with typed input, dry-run, and nonce-ordered execution.

## Repo Structure

| Path                                  | Purpose                                                                 |
| ------------------------------------- | ----------------------------------------------------------------------- |
| `SKILL.md`                            | Main skill instructions (required).                                    |
| `references/README.md`                | Index of reference files and when to use each.                          |
| `references/sdk-playbook.md`          | Request shapes for all methods, minimal snippets, validation checklist.  |
| `references/agent-adapter-example.ts` | Typed adapter: FxAction union, runFxAction, sample payloads.            |
| `agents/openai.yaml`                  | Chip/config for agent UIs.                                             |

## Requirements

- Node.js with `@aladdindao/fx-sdk`.
- Ethereum mainnet (or configured RPC); use `FxSdk({ rpcUrl, chainId: 1 })` when a custom RPC is provided.


## Disclaimer

**IMPORTANT LEGAL NOTICE**

This software is provided "as is" without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

**RISK WARNING**

- **Financial Risk**: Trading leveraged positions involves significant financial risk. You may lose all or more than your initial investment. Only trade with funds you can afford to lose.
- **Smart Contract Risk**: This SDK interacts with smart contracts on the blockchain. Smart contracts may contain bugs, vulnerabilities, or may not function as intended. Always audit and verify smart contracts before interacting with them.
- **Market Risk**: Cryptocurrency markets are highly volatile. Prices can change rapidly, and slippage may occur during transaction execution.
- **Technical Risk**: Network congestion, RPC failures, or other technical issues may cause transactions to fail or execute at unexpected prices.
- **Regulatory Risk**: Cryptocurrency regulations vary by jurisdiction. Ensure compliance with local laws and regulations.
- **No Financial Advice**: This SDK is a technical tool and does not constitute financial, investment, or trading advice. Always conduct your own research and consult with qualified financial advisors before making investment decisions.

**USE AT YOUR OWN RISK**

By using this SDK, you acknowledge that you understand and accept all risks associated with trading leveraged positions and interacting with smart contracts. The developers and contributors of this SDK are not responsible for any losses, damages, or liabilities that may arise from the use of this software.

## License

MIT
