# Swarming Channel Config — OpenClaw Examples

## Single Guild, Two Agents on Different Gateways

### Gateway 1 (Agent A — e.g., Harrison on Mini 1)
```json
{
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "guilds": {
            "YOUR_GUILD_ID": {
              "requireMention": true,
              "channels": {
                "SWARMING_CHANNEL_ID": {
                  "requireMention": true
                }
              }
            }
          }
        }
      }
    }
  },
  "agents": {
    "list": [
      {
        "id": "agent-a",
        "name": "AgentA",
        "groupChat": {
          "mentionPatterns": [
            "<@BOT_USER_ID_A>",
            "<@!BOT_USER_ID_A>"
          ]
        }
      }
    ]
  }
}
```

### Gateway 2 (Agent B — e.g., Prometheus on Mini 3)
Same structure, different bot ID and agent ID.

## Two Agents on the Same Gateway (Advanced)

When both agents share one gateway, you need separate Discord accounts:

```json
{
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "token": "BOT_TOKEN_A",
          "guilds": {
            "YOUR_GUILD_ID": {
              "requireMention": true,
              "channels": {
                "SWARMING_CHANNEL_ID": { "requireMention": true }
              }
            }
          }
        },
        "secondary": {
          "token": "BOT_TOKEN_B",
          "guilds": {
            "YOUR_GUILD_ID": {
              "requireMention": true,
              "channels": {
                "SWARMING_CHANNEL_ID": { "requireMention": true }
              }
            }
          }
        }
      }
    }
  },
  "agents": {
    "list": [
      {
        "id": "agent-a",
        "accountId": "default",
        "groupChat": {
          "mentionPatterns": ["<@BOT_USER_ID_A>"]
        }
      },
      {
        "id": "agent-b",
        "accountId": "secondary",
        "groupChat": {
          "mentionPatterns": ["<@BOT_USER_ID_B>"]
        }
      }
    ]
  }
}
```

**Key**: The `accountId` field binds each agent to its own Discord bot account. Without this, messages may route to the wrong agent.

## Channel Permissions

In Discord Server Settings → Channels → #swarming:
- Both bot roles need: View Channel, Send Messages, Read Message History, Add Reactions
- Set channel topic to describe its purpose (helps agents understand context)
- Consider slow mode (5-10 seconds) to prevent rapid-fire loops during development
