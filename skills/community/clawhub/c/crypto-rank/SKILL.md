---
name: cryptorank-radar
description: Chinese CryptoRank radar skill for market, funding, public sales, airdrops, and daily briefs. Invoke when the user wants a Chinese Web3 signal summary or CryptoRank-based workflow output.
version: 1.0.0
author: caroline
tags:
  - cryptorank
  - web3
  - crypto
  - chinese
  - radar
metadata:
  openclaw:
    primaryEnv: CRYPTORANK_LANG
    envVars:
      - name: CRYPTORANK_LANG
        required: false
        description: Optional default output language. Use zh for Chinese or en for English.
    requires:
      bins:
        - python3
    os:
      - macos
      - linux
    homepage: https://cryptorank.io/
---

# CryptoRank Radar

将 CryptoRank 免费层数据转成适合中文用户使用的市场雷达、融资雷达、空投雷达、Upcoming 雷达与每日摘要。

## When to Use

- 用户想快速查看 `CryptoRank` 的中文市场信号
- 用户想把融资、Upcoming、空投活动压成可执行摘要
- 用户想把 CryptoRank 接入 OpenClaw / ClawHub 的中文工作流
- 用户想生成适合 YouTube、会员区、社群更新的素材

## Interface

Parameters:

- `mode` (required): `radar` | `funding` | `upcoming` | `airdrops` | `brief` | `raw`
- `limit` (optional): 返回条数，默认 `5`
- `lang` (optional): `zh` 或 `en`，默认 `zh`
- `output` (optional): `text` | `json` | `markdown`，默认 `json`
- `raw_mode` (optional): 仅当 `mode=raw` 时使用，可选 `home` | `funding` | `upcoming` | `airdrops`

Returns:

- `text` / `markdown` 输出：适合直接展示或复制的中文雷达文本
- `json` 输出：适合工具链继续处理的结构化结果

## Quick Start

```bash
python3 scripts/run_skill.py --mode radar --lang zh --limit 5 --output json
python3 scripts/run_skill.py --mode funding --lang zh --limit 8 --output markdown
python3 scripts/run_skill.py --mode airdrops --lang zh --limit 10 --output text
```

## Recommended Usage

### 1. 中文总雷达

```bash
python3 scripts/run_skill.py --mode radar --lang zh --limit 5 --output json
```

### 2. 融资雷达

```bash
python3 scripts/run_skill.py --mode funding --lang zh --limit 8 --output markdown
```

### 3. 空投观察名单

```bash
python3 scripts/run_skill.py --mode airdrops --lang zh --limit 10 --output json
```

### 4. 原始数据调试

```bash
python3 scripts/run_skill.py --mode raw --raw-mode airdrops --lang zh --output json
```

## Output Guidance

- 默认优先使用中文输出
- 不把 CryptoRank 当作“价格站”，而是当作“内容雷达 + 机会入口”
- 在 `funding`、`airdrops`、`brief` 场景下，优先提炼“今天该看什么”
- 如果用户要内容选题，可将结果继续交给上层 prompt 做机会翻译

## Execution Logic

This skill ships with a self-contained Python wrapper and a bundled copy of the demo client.

```python
from scripts.run_skill import execute

result = execute(
    mode="radar",
    limit=5,
    lang="zh",
    output="json",
)
print(result)
```

## Files

- `scripts/run_skill.py` - ClawHub 调用入口
- `scripts/package_skill.py` - 打包 zip 文件
- `assets/cryptorank_demo.py` - 自包含的 CryptoRank Python CLI 副本
- `references/examples.md` - 示例查询与结果形式
- `references/publish.md` - 本地测试与上传建议

## Support

- 社区交流：`https://t.me/hollyink`
- 机器人版本：`https://t.me/yongzhuan_bot`
- 视频教程：`https://www.youtube.com/@0xcii`
