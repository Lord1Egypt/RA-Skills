# 游戏化习惯养成 - 用户数据

## 数据说明

本目录存储各用户的游戏化习惯数据，每个用户独立文件。

## 🎯 自动用户识别

系统会自动根据 **OpenClaw 渠道 + 账号 ID** 识别用户：

```
用户 ID = ${channel}-${account_id}

示例：
- dingtalk-0124046821484330  (万万在钉钉)
- wecom-xyz123               (万万在企业微信)
- telegram-456789            (其他用户)
```

## 📁 文件命名

| 文件名 | 用户 |
|--------|------|
| `dingtalk-0124046821484330.json` | 万万（钉钉）|
| `wecom-xxx.json` | 万万（企业微信）|
| `{channel}-{user_id}.json` | 其他用户 |

## 数据结构

```json
{
  "user": {
    "level": 2,
    "xp": 240,
    "attributes": {
      "physical": 2,
      "intellectual": 0,
      "wealth": 1,
      "spiritual": 0,
      "social": 0
    }
  },
  "habits": [...],
  "achievements": [...],
  "checkinHistory": [...]
}
```

## 🔧 多用户使用

### 1. 自动识别（推荐）
系统会根据 OpenClaw 渠道和账号自动识别用户，无需手动指定。

### 2. 命令行指定用户
```bash
habits status --user=wanwan
habits checkin 早起 --user=wanwan
```

### 3. 环境变量
```bash
export GAMIFIED_HABITS_USER=wanwan
habits status
```

### 4. 查看当前用户
```bash
habits whoami
```

## 备份

备份整个 `data/` 目录即可。

## 迁移历史

- 2026-03-25: 从 `~/.gamified-habits/user-data.json` 迁移到技能目录
- 2026-03-25: 实现多用户支持

---
*最后更新：2026-03-25*
