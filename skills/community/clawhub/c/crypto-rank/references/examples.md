# CryptoRank Radar Examples

## Example Queries

- “给我今天的 CryptoRank 中文雷达”
- “帮我看最新融资里最值得追踪的项目”
- “把 Upcoming 和空投活动压成一个中文摘要”
- “我要一份适合发 X 的短版简报”

## Example Commands

### Market Radar

```bash
python3 scripts/run_skill.py --mode radar --lang zh --limit 5 --output json
```

### Funding Radar

```bash
python3 scripts/run_skill.py --mode funding --lang zh --limit 8 --output markdown
```

### Airdrop Watchlist

```bash
python3 scripts/run_skill.py --mode airdrops --lang zh --limit 10 --output json
```

### Daily Brief

```bash
python3 scripts/run_skill.py --mode brief --lang zh --limit 5 --output text
```

## Suggested Agent Behaviors

- 对中文用户，默认将 `lang` 设为 `zh`
- 如果用户只说“看今天有什么机会”，优先调用 `brief`
- 如果用户更关注空投和执行动作，优先调用 `airdrops`
- 如果用户更关注机构动向和投研清单，优先调用 `funding`
