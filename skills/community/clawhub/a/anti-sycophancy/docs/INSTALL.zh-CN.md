# 安装指南

> **[English version](./INSTALL.md)**

## 前置条件

- **Claude Code**（支持 hook 的版本）— 用于 Layer 1
- **OpenClaw** — 用于 Layer 2 + Layer 3

---

## 方式一：通过 ClawhHub（推荐）

```bash
npx clawhub@latest install 0xcjl/anti-sycophancy
```

自动检测平台并安装所有适用的层。

---

## 方式二：通过 Claude Code（手动 clone 后）

```bash
# 1. Clone 仓库
git clone https://github.com/0xcjl/anti-sycophancy.git ~/.claude/skills/anti-sycophancy

# 2. 使用 Claude Code
/anti-sycophancy install
```

---

## 方式三：ClawhHub + Claude Code 组合

```bash
# 通过 ClawhHub 安装
npx clawhub@latest install 0xcjl/anti-sycophancy

# 然后部署各层
/anti-sycophancy install
```

---

## 安装了什么

### Claude Code

| 层 | 文件 | 用途 |
|----|------|------|
| Layer 1 | `~/.claude/hooks/sycophancy-transform.{sh,py}` | Hook 脚本 |
| Layer 1 | `~/.claude/settings.json` → `UserPromptSubmit` | Hook 注册 |
| Layer 2 | `~/.claude/skills/anti-sycophancy/SKILL.md` | 技能内容 |
| Layer 3 | `~/.claude/CLAUDE.md` | 持久化规则 |

### OpenClaw

| 层 | 文件 | 用途 |
|----|------|------|
| Layer 2 | `~/.claude/skills/anti-sycophancy/SKILL.md` | 技能内容 |
| Layer 3 | `{workspace}/SOUL.md` | 持久化规则 |

---

## 平台专属安装

### 仅 Claude Code

```bash
/anti-sycophancy install-claude-code
```

安装：Layer 1 (hook) + Layer 3 (CLAUDE.md 规则)

### 仅 OpenClaw

```bash
/anti-sycophancy install-openclaw
```

安装：Layer 3 (SOUL.md 规则)

---

## 验证安装

```bash
/anti-sycophancy status
```

预期输出：
```
anti-sycophancy 安装状态
├── Claude Code
│   ├── Layer 1 Hook: ✅
│   ├── Layer 2 SKILL: ✅
│   └── Layer 3 CLAUDE.md: ✅
└── OpenClaw
    ├── Layer 1 Hook: ❌ (需 Plugin SDK)
    ├── Layer 2 SKILL: ✅
    └── Layer 3 SOUL.md: ✅
```

测试 hook：
```bash
/anti-sycophancy verify
```

---

## 卸载

```bash
/anti-sycophancy uninstall
```

这将移除所有已安装的层，同时保留技能文件本身。

---

## 常见问题

### Hook 没有转换 prompt

1. 检查 `~/.claude/settings.json` → `hooks` → `UserPromptSubmit` 是否包含 `"sycophancy-transform.sh"`
2. 运行 `/anti-sycophancy verify` 测试
3. 检查 Python 3 是否可用：`python3 --version`

### 技能没有触发

- 说触发关键词："防御谄媚"、"批判模式"、"play devil's advocate"、"anti-sycophancy"
- 或描述意图："先泼冷水"、"不要迎合我"、"I want to hear counterarguments"

### Layer 3 规则没有生效

- Claude Code：规则在会话启动时从 `~/.claude/CLAUDE.md` 加载。启动新会话。
- OpenClaw：规则从 `{workspace}/SOUL.md` 加载。重启 Agent。
