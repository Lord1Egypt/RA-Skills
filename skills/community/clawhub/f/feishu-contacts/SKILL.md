---
name: feishu-contacts
version: 1.2.0
description: "Search Feishu contacts by name/pinyin/department. Use when you need to find a person's open_id, email, or department info before sending messages or emails."
metadata:
  openclaw:
    emoji: "📇"
    requires:
      bins: ["python3"]
      pips: ["pypinyin"]
---

# Feishu Contacts Search

飞书通讯录本地缓存搜索。支持中文名、拼音、拼音首字母、英文名模糊匹配。

## Setup (first time only)

确保 `~/.openclaw/openclaw.json` 中已配置飞书应用凭据：

```json
{
  "channels": {
    "feishu": {
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  }
}
```

飞书应用需要以下权限：
- `contact:user:read` — 读取用户信息
- `contact:user:read_v2` — 读取用户详细信息
- `contact:department:read` — 读取部门信息

安装后首次使用前，执行同步：

```bash
python3 ~/.openclaw/skills/feishu-contacts/scripts/feishu-contacts.py sync
```

## Script Location

`~/.openclaw/skills/feishu-contacts/scripts/feishu-contacts.py`

## Commands

### 同步通讯录（定期执行，新入职的人需要 sync 才能搜到）

```bash
python3 ~/.openclaw/skills/feishu-contacts/scripts/feishu-contacts.py sync
```

### 搜索用户

```bash
python3 ~/.openclaw/skills/feishu-contacts/scripts/feishu-contacts.py search <人名>
```

支持：中文名、拼音（zhangsan）、拼音首字母（zs）、英文名、同音字模糊匹配。

### 搜索部门

```bash
python3 ~/.openclaw/skills/feishu-contacts/scripts/feishu-contacts.py search-dept <部门名>
```

### 列出部门所有成员

```bash
python3 ~/.openclaw/skills/feishu-contacts/scripts/feishu-contacts.py list-dept <dept_id>
```

### 获取用户详情（实时 API 调用）

```bash
python3 ~/.openclaw/skills/feishu-contacts/scripts/feishu-contacts.py get <open_id>
```

### 查看缓存信息

```bash
python3 ~/.openclaw/skills/feishu-contacts/scripts/feishu-contacts.py info
```

## CRITICAL: 人员定位规则

任何涉及"给某人做某事"的操作（发消息、发邮件、创建任务等），**必须先通过本工具定位到具体的人**。

### 强制流程

```
IF 目标是人名:
  1. 执行: search <姓名>
  2. 获取: open_id（飞书消息）/ email（邮件，需 get <open_id>）
  3. 结果唯一 → 直接使用
  4. 结果多个 → 列出候选让用户选择
  5. 结果为空 → 报告找不到，让用户提供更多信息

IF 目标是部门:
  1. 执行: search-dept <部门名>
  2. 获取: dept_id
  3. 执行: list-dept <dept_id>
  4. 获取: 所有成员的 open_id
```

### 禁止行为

- ❌ 不准说"找不到这个人"而不先执行搜索命令
- ❌ 不准猜测或编造 open_id / email
- ❌ 不准从记忆中猜测人员信息，必须执行命令获取
- ❌ 不准截断 list-dept 的输出，必须完整展示所有成员

### 使用示例

用户: "给张三发个飞书消息说开会"
```
1. search 张三 → 获得 open_id: ou_xxx
2. 发送飞书消息到 ou_xxx
```

用户: "给产品部所有人发邮件"
```
1. search-dept 产品 → 获得 dept_id: od_yyy
2. list-dept od_yyy → 获得成员列表
3. 对每个成员 get <open_id> 获取邮箱
4. 批量发送邮件
```

## Cache

- 位置: `~/.openclaw/.feishu-contacts-cache.json`
- 内容: 用户、部门、部门-用户映射
- 更新: 执行 `sync` 刷新（新入职的人搜不到时需要 sync）

## Tips

- 搜索返回 top 10 结果，按相关度排序
- `get` 命令是实时 API 调用，可获取最新的邮箱、手机号等详细信息
- 缓存跨重启持久化，但建议定期 sync 保持数据新鲜
