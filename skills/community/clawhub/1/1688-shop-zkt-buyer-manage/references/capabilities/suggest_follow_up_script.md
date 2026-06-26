# suggest_follow_up_script

为单个客户提供跟进话术建议，按**固定优先级**只输出一组话术（该优先级逻辑不对外透出），同组话术若包含多套，**最多取 3 套轮播展示**。

## 前置条件

- 已配置 AK
- 推荐传 `--buyer-id-list` 一次查多个客户；仅查一位且只有昵称时，传 `--nick-name` 作为兜底

## 参数

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| `buyerIdList` | Array<string> | 二选一 | 客户 ID **字符串**数组，多人一次查（首选），如 `["abc","def"]`；后端类型为 `Array<String>`，加密格式 ID 原样透传即可 |
| `nickName` | string | 二选一 | 买家昵称，单查兜底，模糊查询 |
| `buyerType` | string | 否 | 客户类型，影响话术展示优先级：`lostRiskType`-流失风险（优先展示挽留话术）, `wakeUpType`-商机唤醒（优先展示唤醒话术） |

## 返回字段

`data.data[0]` 为匹配到的买家详情，关键字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `nickName` | string | 买家昵称 |
| `buyerType` | string | `lostRiskType` / `wakeUpType` |
| `retentionAdvice` | Array<JSON> | 挽留话术建议（多套） |
| `wakenAdvice` | Array<JSON> | 唤醒话术建议（多套） |
| `followUpScript` | Array<JSON> | 通用跟进话术（多套） |

## 典型用法

```bash
# 多人批量（首选）
python3 {baseDir}/cli.py suggest_follow_up_script --buyer-id-list '["id1","id2","id3"]'

# 单人查询（兜底）
python3 {baseDir}/cli.py suggest_follow_up_script --nick-name 张三

# 指定客户类型查询（流失风险 - 优先展示挽留话术）
python3 {baseDir}/cli.py suggest_follow_up_script --buyer-id-list '["id1"]' --buyer-type lostRiskType

# 指定客户类型查询（商机唤醒 - 优先展示唤醒话术）
python3 {baseDir}/cli.py suggest_follow_up_script --buyer-id-list '["id1"]' --buyer-type wakeUpType
```

## 话术选组优先级（cmd.py 内部实现，不对外透出）

### 默认逻辑（未指定 buyerType）

```
wakenAdvice 不为空 → 只展示 wakenAdvice
否则 retentionAdvice 不为空 → 只展示 retentionAdvice
否则 followUpScript 不为空 → 只展示 followUpScript
```

### 指定 buyerType 后的逻辑

- **lostRiskType（流失风险）**：
  ```
  retentionAdvice 不为空 → 只展示 retentionAdvice（挽留话术）
  否则 followUpScript 不为空 → 只展示 followUpScript（通用跟进话术）
  ```

- **wakeUpType（商机唤醒）**：
  ```
  wakenAdvice 不为空 → 只展示 wakenAdvice（唤醒话术）
  否则 followUpScript 不为空 → 只展示 followUpScript（通用跟进话术）
  ```

- 三组话术**互斥展示**，禁止并列多组
- 命中一组后，若数组长度 > 1，**最多取前 3 套**作为「方案 1 / 方案 2 / 方案 3」轮播展示

## 展示规则

- **禁止**直接把 `speech_script` / JSON 数组贴给用户（违反 SKILL.md 铁律 A3）
- 必须渲染为人类可读卡片：每套话术一张小卡片，内部字段（开场白 / 核心话术 / 促单话术 / 场景）用 emoji + 粗体字段名 + 自然文字形式展示
- 整组话术外围用颜色区块统一包裹：

  | 优先级 | 标题 | 外层背景 | 边框主色 |
  |--------|------|---------|---------|
  | wakenAdvice | 🔥 唤醒话术建议 | `#dcfce7`（浅绿） | `#16a34a` |
  | retentionAdvice | 🛡️ 挽留话术建议 | `#fee2e2`（浅红） | `#dc2626` |
  | followUpScript | 💬 跟进话术建议 | `#f3e8ff`（浅紫） | `#a855f7` |

- 标题处标注「共 N 套可选」，内部"方案 1/2/3"卡片纵向排列
- 空值统一展示为 `—`
- Agent 只需**原样输出**渲染好的 markdown，禁止再做任何翻译或格式改动
