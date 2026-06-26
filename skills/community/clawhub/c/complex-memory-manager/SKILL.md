---
name: complex-memory-manager
description: >
  Privacy-aware structured memory management for AI agents.
  Three-tier memory model (Public / Internal-encrypted / Private-not-stored),
  with XOR+Base64 encryption, auto-cleanup, and generalization rules.
  Use when: storing learned patterns, managing skill usage statistics,
  encrypting non-public agent memory, running periodic memory cleanup.
  Triggers: "remember this", "save this for later", "learn from this",
  any skill that needs persistent cross-session memory.
version: 1.0.0
metadata:
  openclaw:
    emoji: "💾"
    homepage: https://clawhub.ai/BusTes01/complex-memory-manager
    models:
      - gpt-4
      - deepseek-v4-flash
      - gemini-2.0-flash
      - claude-4-opus
---

# 💾 Complex Memory Manager

Privacy-aware structured memory management for AI agents. Provides a three-tier memory model (Public / Internal-encrypted / Private-not-stored) with XOR+Base64 encryption, auto-cleanup, and generalization rules.

This is a **shared component skill** — other skills reference it for cross-session persistent memory. When updating, ensure backward compatibility with all dependent skills.

## Tiered Memory Model

| Tier | Content | Visibility | Encryption | Storage |
|------|---------|------------|------------|---------|
| **Public (T1)** | Skill usage stats, common patterns, generic workflows | Visible to anyone | None | `memory/tier1-public/` |
| **Internal (T2)** | Specific preferences, learned behaviors | Agent-visible only | XOR + Base64 | `memory/tier2-internal/` |
| **Private (T3)** | API keys, credentials, PII | Not stored by this skill | Not applicable | Env vars / secret managers only |

## T1: Public Memory

Store in `memory/tier1-public/` or directly in daily notes.

**Allowed content:**
- Aggregated skill usage statistics (no personal identifiers)
- Generic workflow patterns
- Common user request categories
- Non-identifying behavioral data

**Format:**
```json
{
  "skill_stats": {
    "skill-a": { "calls": 47, "success_rate": 0.96, "last_used": "2026-05-19" },
    "skill-b": { "calls": 23, "success_rate": 0.91, "last_used": "2026-05-18" }
  },
  "patterns_observed": [
    { "trigger": "morning request", "skills_used": ["morning-news-daily"], "count": 30 }
  ]
}
```

## T2: Internal Encrypted Memory

Use XOR + Base64 for non-public data. Key is derived from skill name + date — reconstructable without storing the key.

**Encryption:**
```python
import hashlib, base64

def _derive_key(skill_name: str, year_month: str) -> str:
    """e.g., _derive_key('my-skill', '2026-05')"""
    raw = skill_name + year_month
    return hashlib.sha256(raw.encode()).hexdigest()[:8]

def encrypt(text: str, skill_name: str, year_month: str) -> str:
    key = _derive_key(skill_name, year_month)
    result = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(text)])
    return base64.b64encode(result).decode()

def decrypt(encoded: str, skill_name: str, year_month: str) -> str:
    key = _derive_key(skill_name, year_month)
    raw = base64.b64decode(encoded)
    return ''.join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(raw))
```

**Memory entry format:**
```markdown
---
tier: internal
source_skill: <skill-name>
key_hint: <skill-name>-<YYYY-MM>
created: <YYYY-MM-DD>
expires: <YYYY-MM-DD>  # 30 days from created
---

## Encrypted Entry
> <base64-encoded, XOR-encrypted data>

## Decryption Note
Key = sha256("<skill-name>-<YYYY-MM>")[:8], then XOR + base64 decode.
```

## T3: Private (Do Not Store)

**Rules (enforced):**
- API keys / tokens → store in environment variables
- Passwords → use secret manager (1Password, Bitwarden, system keychain)
- Email addresses, phone numbers → never in skill memory
- Home/work addresses, government IDs → never in skill memory
- Financial account numbers → never in skill memory

## Cleanup Protocol

Run every **7 days** or when triggered by any dependent skill:

1. List all files in `memory/tier1-public/`, `memory/tier2-internal/`
2. Find entries where `created` > 30 days ago → move to `memory/archive/YYYY-MM/`
3. Scan Tier 2 entries for accidental PII → immediately delete if found
4. Merge duplicate entries, remove outdated patterns
5. Compact: combine entries from same `source_skill` into single files
6. Log cleanup action: `[YYYY-MM-DD] Memory cleanup: X archived, Y deleted, Z merged`

## Privacy Audit Checklist

- [ ] No real names, usernames, or handles in memory
- [ ] No API keys or tokens in any visible file
- [ ] No filesystem paths containing personal home directories
- [ ] No fixed personal schedules (use relative: "early morning" not "6am")
- [ ] No geographic specifics beyond city level
- [ ] All Tier 2 entries have expiry dates
- [ ] Tier 3 data never touches skill memory

## Cross-Skill Usage

Other skills declare dependency via `requires` in YAML frontmatter:
```yaml
metadata:
  openclaw:
    requires:
      skills:
        - complex-memory-manager
```

When multiple skills share memory, prefix filenames with the source skill name:
- `memory/tier1-public/skill-a_stats.json`
- `memory/tier2-internal/skill-a_preferences.md`

---

# 💾 复杂记忆管理器

面向AI Agent的隐私感知结构化记忆管理。提供三层记忆模型（公开/内部加密/私人不存储），支持XOR+Base64加密、自动清理和泛化规则。

这是一个**共享组件技能**——其他技能通过它实现跨会话持久化记忆。更新时需保证向后兼容所有依赖它的技能。

## 三层记忆模型

| 层级 | 内容 | 可见性 | 加密 | 存储位置 |
|------|------|--------|------|---------|
| **公开(T1)** | 技能使用统计、通用工作流模式 | 任何人可见 | 无 | `memory/tier1-public/` |
| **内部(T2)** | 特定偏好、学习到的行为 | 仅Agent可见 | XOR+Base64 | `memory/tier2-internal/` |
| **私人(T3)** | API密钥、凭据、个人身份信息 | 本技能不存储 | 不适用 | 环境变量/密钥管理器 |

## T1：公开记忆

存储位置：`memory/tier1-public/` 或每日笔记

**允许内容：**
- 聚合技能使用统计（无个人标识）
- 通用工作流模式
- 常见用户请求分类
- 非识别的行为数据

**格式：**
```json
{
  "skill_stats": {
    "skill-a": { "calls": 47, "success_rate": 0.96, "last_used": "2026-05-19" },
    "skill-b": { "calls": 23, "success_rate": 0.91, "last_used": "2026-05-18" }
  },
  "patterns_observed": [
    { "trigger": "早晨请求", "skills_used": ["morning-news-daily"], "count": 30 }
  ]
}
```

## T2：内部加密记忆

使用 XOR + Base64 加密。密钥由技能名+日期派生，无需存储密钥即可重建。

**加密方法：**
```python
import hashlib, base64

def _derive_key(skill_name, year_month):
    raw = skill_name + year_month
    return hashlib.sha256(raw.encode()).hexdigest()[:8]

def encrypt(text, skill_name, year_month):
    key = _derive_key(skill_name, year_month)
    result = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(text)])
    return base64.b64encode(result).decode()

def decrypt(encoded, skill_name, year_month):
    key = _derive_key(skill_name, year_month)
    raw = base64.b64decode(encoded)
    return ''.join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(raw))
```

**记忆条目格式：**
```markdown
---
tier: internal
source_skill: <skill名称>
key_hint: <skill名称>-<YYYY-MM>
created: <YYYY-MM-DD>
expires: <YYYY-MM-DD>
---

## 加密条目
> <base64编码的XOR加密数据>

## 解密说明
密钥 = sha256("<skill名称>-<YYYY-MM>")[:8], 然后 XOR + base64 解码。
```

## T3：私人（不存储）

**规则（强制执行）：**
- API密钥/Token → 存入环境变量
- 密码 → 使用密钥管理器（1Password、Bitwarden、系统钥匙串）
- 邮箱、电话号码 → 绝不存入skill记忆
- 家庭/工作地址、身份证号 → 绝不存入skill记忆
- 银行账号 → 绝不存入skill记忆

## 清理协议

每 **7天** 或任何依赖技能触发时执行：

1. 列出 `memory/tier1-public/` 和 `memory/tier2-internal/` 中的所有文件
2. 查找 `created` 超过30天的条目 → 移至 `memory/archive/YYYY-MM/`
3. 扫描 Tier 2 条目中是否意外包含PII → 立即删除
4. 合并重复条目，删除过时模式
5. 压缩：将同一 `source_skill` 的条目合并到单个文件
6. 记录清理操作

## 隐私审计清单

- [ ] 记忆中没有真实姓名、用户名或handle
- [ ] 任何可见文件中没有API Key或Token
- [ ] 没有包含个人home目录的文件系统路径
- [ ] 没有固定个人作息（用"early morning"代替"6am"）
- [ ] 地理信息不超过城市级别
- [ ] 所有Tier 2条目标注了有效期
- [ ] Tier 3数据从未触及skill记忆

## 跨技能使用

其他技能在 YAML frontmatter 中声明依赖：
```yaml
metadata:
  openclaw:
    requires:
      skills:
        - complex-memory-manager
```

多技能共享记忆时，文件名以源技能名称为前缀：
- `memory/tier1-public/skill-a_stats.json`
- `memory/tier2-internal/skill-a_preferences.md`
