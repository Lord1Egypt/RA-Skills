# Config Schema

## Minimal Example

```json
{
  "games": [
    {
      "name": "某游戏",
      "aliases": ["某某", "SomeGame"],
      "genre": "card",
      "current_version": "1.2.3",
      "focus_topics": ["周年庆", "新角色"]
    }
  ],
  "scope": {
    "region": "domestic",
    "language": "zh",
    "channels": ["weibo", "bilibili", "zhihu", "tieba", "nga", "reddit", "media"]
  },
  "schedule": {
    "mode": "daily",
    "window": "24h",
    "timezone": "Asia/Shanghai"
  },
  "report": {
    "language": "zh-CN",
    "audience": "mixed",
    "delivery": ["markdown", "feishu-summary"]
  },
  "alert": {
    "threshold": "P1",
    "quiet_hours": ["23:00", "08:00"],
    "cross_platform_escalation": false
  },
  "sampling": {
    "max_per_channel": 50
  },
  "keywords": {
    "custom": [],
    "competitor": []
  }
}
```

## Field Reference

### games[]
| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| name | ✅ | — | Game name (primary) |
| aliases | — | [] | Short names, English name, abbreviations |
| genre | — | — | RPG / card / SLG / FPS / anime-gacha etc. |
| current_version | — | — | Current version number |
| focus_topics | — | [] | Current events, characters, version themes |
| competitors | — | [] | Competitor game names (v1: record only) |

### scope
| Field | Default | Options |
|-------|---------|---------|
| region | domestic | domestic / overseas / global |
| language | zh | zh / en / multi |
| channels | [weibo, bilibili, zhihu, tieba, nga, reddit, media] | See channel-strategy.md |

### schedule
| Field | Default | Options |
|-------|---------|---------|
| mode | daily | daily / 4h / weekly / custom cron |
| window | 24h (daily), 6h (4h mode) | Custom override allowed for manual tasks |
| timezone | Asia/Shanghai | Any valid timezone |

### report
| Field | Default | Options |
|-------|---------|---------|
| language | zh-CN | zh-CN / en |
| audience | mixed | management / ops / dev-qa / mixed |
| delivery | [markdown, feishu-summary] | markdown / feishu-summary / both |

### alert
| Field | Default | Options |
|-------|---------|---------|
| threshold | P1 | P1 / P1+P2 / none |
| quiet_hours | [23:00, 08:00] | [start, end] in config timezone |
| cross_platform_escalation | false | Whether cross-platform spread triggers separate urgent alert |

### sampling
| Field | Default | Description |
|-------|---------|-------------|
| max_per_channel | 50 | Max samples to collect per channel per run |

## Default Values Summary

| Config | Default |
|--------|---------|
| Region | domestic |
| Language | zh |
| Schedule | daily |
| Scan window | 24h (daily) / 6h (4h mode) |
| Report language | zh-CN |
| Audience | mixed |
| Alert threshold | P1 only |
| Quiet hours | 23:00-08:00 |
| Channels | weibo, bilibili, zhihu, tieba, nga, reddit, media |
| Max samples/channel | 50 |

## Interruption Handling

- User can exit config flow at any point
- Filled fields are saved; unfilled fields use defaults above
- Config is immediately usable after partial setup
- User can re-enter guided setup or edit config.json directly at any time
- Manual ad-hoc tasks can override scan window without modifying saved config
