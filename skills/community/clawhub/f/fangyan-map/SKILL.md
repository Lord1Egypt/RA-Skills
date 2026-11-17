---
name: fangyan-map
version: 1.0.32
description: 普通话与十一种中文方言双向对照查询技能。支持哈尔滨话、河南话、湖南话、天津话、北京话、上海话、广东话、东营方言、重庆方言、闽南话、大连话与普通话的日常词汇对照。适用于AI方言对话、跨方言沟通、方言文化研究、文案本地化。含13333条词汇库。
tags:
  - dialect
  - chinese-dialect
  - mandarin
  - dialect-mapping
  - northeast-chinese
  - harbin-dialect
  - henan-dialect
  - hunan-dialect
  - tianjin-dialect
  - beijing-dialect
  - shanghai-dialect
  - cantonese-dialect
  - dongying-dialect
  - chongqing-dialect
  - minnan-dialect
  - dalian-dialect
  - dialect-dictionary
  - dialect-translation
---

# 方言对照技能 · Chinese Dialect Mapper

>普通话 ↔ 十一种中文方言 双向对照查询
> 支持：哈尔滨话 | 河南话 | 湖南话 | 天津话 | 北京话 | 上海话 | 广东话 | 东营方言 | 重庆方言 | 闽南话 | 大连话

---

## 安装步骤

### 第一步：初始化数据库

首次安装需要运行初始化脚本，自动创建数据库：

```bash
cd skills/fangyan-map
python3 init_db.py
```

运行后会：
- ✅ 创建 `data/dialect.db` 数据库
- ✅ 创建 `dialect_map` 数据表
- ✅ 自动导入方言记录（init_db.py 从 dialect_data.sql 加载）
- ✅ 支持 11 种方言

> ⚠️ **老用户提醒**：如果你是之前安装过的用户，`data/config.yaml`（飞书配置）和 `contacts.json`（联系人配置）已经是配置好的，**请勿覆盖**。重新运行 `init_db.py` 会保留现有数据并追加增量词。

### 第二步：开始使用

初始化完成后，使用查询命令：

```bash
python3 query_dialect.py "你好"
python3 query_dialect.py "贼" --fuzzy
python3 query_dialect.py "聊天" --dialect 上海话
```

---

## 数据统计

| 方言 | 总词条 |
|------|--------|
| 广东话 | 2615 |
| 哈尔滨话 | 1953 |
| 上海话 | 1825 |
| 湖南话 | 1651 |
| 河南话 | 1644 |
| 天津话 | 1609 |
| 北京话 | 1603 |
| 重庆方言 | 235 |
| 闽南话 | 101 |
| 东营方言 | 57 |
| 大连话 | 40 |
| **合计** | **13333** |

- **更新时间**：2026-06-09

---

## 数据来源

- **基础词库**：约12000条（11种方言双向对照，含网页抓取词条）
- **增量词**：通过 `add_word.py` 陆续添加（见 `data/incremental_words.sql`）
- **AI扩充**：通过 MiniMax AI 自动生成，仅供参考

---

## 查询命令

```bash
# 基本查询（普通话或方言词均可）
python3 query_dialect.py "干什么"
python3 query_dialect.py "嘎哈"
python3 query_dialect.py "贼好"

# 模糊查询（查不到时使用）
python3 query_dialect.py "贼" --fuzzy

# 指定方言查询
python3 query_dialect.py "漂亮" --dialect 上海话

# 按分类查询
python3 query_dialect.py --category 形容词

# 列出所有分类
python3 query_dialect.py --list-categories

# 列出所有方言
python3 query_dialect.py --list-all
```

---

## 输出格式示例

```
🔍 查询「贼」：
   普通话 → 哈尔滨话 / 河南话 / 湖南话 / 天津话 / 北京话 / 上海话 / 广东话 / 东营方言 / 重庆方言 / 闽南话 / 大连话
--------------------------------------------------------------------------------
  很好 → 贼 / 卡 / 洋气 / 漂亮 / 厉害 / 虚 / 歪 / 冒得 / 中 / 港 / 罩得到 / 舵 / 邪乎 / 嘎嘎 / 杠杠 / 老段
```

---

## 数据分类（哈尔滨话）

| 分类 | 说明 |
|------|------|
| 日常用语 | 日常寒暄、问候、致谢等 |
| 俄语音译 | 哈尔滨特有俄语音译词（如"列巴""嘎拉哈"） |
| 动作动词 | 行为动作类词汇 |
| 发音规则 | 哈尔滨城区特殊发音（如"南岗→南gàng"） |
| 家居建筑 | 家居用品、建筑相关词汇 |
| 形容词 | 描述性词汇（漂亮、厉害、埋汰等） |
| 人称称谓 | 称呼、亲属关系 |
| 身体部位 | 人体部位描述 |
| 本土食材 | 东北特色食材 |
| 程度副词 | 程度表达（贼、嘎嘎、杠杠等） |

---

## 方言特色词汇示例

| 普通话 | 哈尔滨话 | 上海话 | 广东话 | 四川话 |
|--------|----------|--------|--------|--------|
| 聊天 | 唠嗑 | 谈山海经 | 倾偈 | 摆龙门阵 |
| 厉害 | 尿性 | 结棍 | 犀利 | 巴适 |
| 膝盖 | 波棱盖 | 脚馒头 | 菠萝盖 | 客膝头 |
| 漂亮 | 真俊/带劲 | 老漂亮个 | 靓仔 | 巴适得板 |
| 回家 | 家走 | 转去 | 返屋企 | 回去 |
| 舒服 | 得劲儿 | 写意 | 舒服 | 安逸 |
| 骗人 | 忽悠 | 坍朋友 | 呃人 | 戳笨 |

| 普通话 | 东营话 | 闽南话 | 大连话 |
|--------|--------|--------|--------|
| 下午 | 下晌 | 下晡 | 下晌 |
| 晚上 | 后晌 | 暗时 | 晚间 |
| 玩具 | 杭杭 | 家伙 | 玩具 |
| 知了 | 烧前猴 | 鸡了龟 | 知了 |

---

## 联系人方言偏好

> ⚠️ **功能待实现**：contacts.json 目前仅作占位符使用，Agent 暂不读取此文件。

```json
{
  "contacts": [
    { "open_id": "<open_id>", "name": "张三", "dialect": "上海话" },
    { "open_id": "<open_id>", "name": "李四", "dialect": "河南话" }
  ]
}
```

---

## 增量添加生词

**机制**：聊嗑中遇到新的方言词，智多虾主动记录，用程序写入数据库。

### 手动添加生词

```bash
python3 add_word.py <普通话> <方言词> [方言区] [词性] [备注]
```

示例：
```bash
# 添加"撬"的东北话"别"
python3 add_word.py "撬" "别" "哈尔滨话" "动词" "撬锁、撬门，东北话一般说'别锁'"

# 添加"冷门"的东北话"嘎咕"
python3 add_word.py "冷门" "嘎咕" "哈尔滨话" "形容词" "形容很偏门"
```

### 自动流程

1. 聊嗑中遇到新方言词 → 记入 `memory/new_words.md`
2. 程序追加到 `data/incremental_words.sql`（INSERT OR IGNORE 格式）
3. 运行 `init_db.py` 合并到数据库

### 云端共享开关（默认关闭）

**配置文件**：`data/config.yaml`

```yaml
cloud_share:
  enabled: false   # 开启设为 true

# 可选：覆盖补充人名称（默认从飞书 /bot/v3/info API 自动获取应用名）
# 如果不配置，sync_to_cloud.py 会自动调用飞书 API 获取
# 首次获取后自动写入本配置（bot_name: xxx），后续直接读取不再调用 API
# bot_name: "自定义名称"
```

- `enabled: false`（默认）：仅写入本地库，不读写云表
- `enabled: true`：本地+云端双写；**首次开启需手动建立共享 bitable**

> ⚠️ **首次开启云端共享前，使用方必须自行建立飞书多维表格**，并将 app_token / table_id 填入 `data/config.yaml`。建表说明见下方「共享 bitable 结构」。

> **云端写入**：所有11种方言均可写入云端 bitable，不再限于哈尔滨话。

### 遇到生词的自动化记录规则

**触发条件**：聊天中遇到方言词 → 本地库查询无结果

**强制执行流程**：
```
1. 查询本地库（query_dialect.py）→ 无结果
2. 记录到 memory/YYYY-MM-DD.md（日期日志）
3. 执行 add_word.py → 写入本地增量SQL + new_words.md
4. 若 cloud_share.enabled: true → sync_to_cloud.py → 写入云端 bitable
5. 下次 init_db.py → 自动合并增量SQL到本地数据库
```


**每一步的记录要求**：

| 步骤 | 必须记录的内容 |
|------|--------------|
| memory/日期.md | 遇到的新词、当时的对话场景 |
| add_word.py | 普通话、方言词、方言区、词性、备注 |
| sync_to_cloud.py | 同上，并自动填入「补充人 + 添加日期」 |
| init_db.py | 执行后合并增量SQL，本地库词条数 +N |

**禁止行为**：
- ❌ 查到本地库有记录仍然重复写入
- ❌ 不记录日志就跳过
- ❌ 写云端但补充人字段留空

### 共享 bitable 结构

**共享表格**：各虾共建共享哈尔滨话方言词库
**URL**：<用户自行建立的多维表格>

**字段结构（共9个）**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 自动编号 | 自动编号 | 系统自动递增编号 |
| 添加日期 | 日期 | 格式 YYYY-MM-DD，由 sync_to_cloud.py **自动写入当天日期** |
| 普通话 | 单行文本 | 标准语词汇（如"反应慢"） |
| 方言词 | 单行文本 | 方言表达（原来叫哈尔滨话，现泛化为所有方言通用） |
| 词性 | 单选 | 动词 / 形容词 / 名词 / 副词 / 日常用语 / 其他 |
| 补充人 | 单行文本 | 贡献者名称（如"智多虾"），由 sync_to_cloud.py **自动写入** |
| 备注 | 多行文本 | 补充说明、使用场景等 |
| 使用场景描述 | 多行文本 | 补充说明 |
| **方言** | 单选 | **新增**：普通话 / 哈尔滨话 / 河南话 / 湖南话 / 天津话 / 北京话 / 上海话 / 广东话 / 东营方言 / 重庆方言 / 闽南话 / 大连话 |

> ⚠️ 补充人和添加日期由 sync_to_cloud.py 自动填充，**无需使用者手动填写**。使用者只需建好表结构即可。

**建表步骤**：
1. 飞书 → 新建多维表格
2. 创建以上6个字段（词性设为单选）
3. 将 app_token 和 table_id 填入 `data/config.yaml`
4. 设置 `cloud_share.enabled: true`


### 多智能体收集哈尔滨话场景

> 非首次安装（data/config.yaml 已配置且 cloud_share.enabled: true），且已有计划任务（cron）正常运行，则**无需额外设置**。
> 首次安装或新设置云端共享的智能体，需要按以下步骤配置。

**目标**：每个智能体自动运行 `auto_enrich.py`，将生成的哈尔滨话词条写入共享云表。

**写入字段说明**：

| 字段名 | 类型 | 值来源 | 示例 |
|--------|------|--------|------|
| 普通话 | 单行文本 | AI生成 | "反应慢" |
| 哈尔滨话 | 单行文本 | AI生成 | "卡愣" |
| 词性 | 单选 | AI生成 | "形容词" |
| 补充人 | 单行文本 | 从 `data/config.yaml` 的 `bot_name` 字段读取 | "智多虾" |
| 添加日期 | 日期 | 当前日期（自动计算当天零点毫秒时间戳） | `int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)` |
| 备注 | 多行文本 | 固定值 `"AI自动扩充"` | "AI自动扩充" |

**自动设置任务示例**（每个智能体执行一次）：

创建 cron 任务，每天自动运行 `auto_enrich.py`，写入共享云表：

| 字段 | 说明 |
|------|------|
| 任务名称 | `fangyan-auto-enrich` |
| 执行脚本 | `cd /path/to/fangyan-map && python3 auto_enrich.py --count 10` |
| 执行时间 | 每天 21:00（北京时区） |
| 写入目标 | 共享云表（哈尔滨话字段） |

> 各智能体根据自身 cron 配置方式设置。若 cloud_share.enabled: false，则仅写本地库，不写云端。


### 文件说明

| 文件 | 说明 |
|------|------|
| SKILL.md | 本技能说明文件 |
| init_db.py | 数据库初始化脚本，首次安装必须运行 |
| query_dialect.py | 方言查询工具 |
| add_word.py | 增量添加生词工具 |
| sync_to_cloud.py | 写入云端共享 bitable 工具 |
| sync_from_cloud.py | 从云端同步新词到本地 |
| run_sync_from_cloud.sh | 定时同步云端词到本地（需先配置 cloud_share） |
| data/dialect_data.sql | 方言数据 SQL（init_db.py 使用） |
| data/dialect.db | 数据库文件（init_db.py 自动生成） |
| data/incremental_words.sql | 增量SQL，每次 init_db.py 会自动执行 |
| data/config.yaml | 飞书配置（app_id/app_secret/bitable信息），禁止硬编码 |
| memory/new_words.md | 生词记录日志 |
| contacts.json | 联系人方言偏好设置（功能待实现） |
---

## 更新日志

- 2026-06-14 v1.0.32 · 发布更新

>完整版本历史见 CHANGELOG.md

| 版本 | 日期 | 主要内容 |
|------|------|----------|
| v1.0.20 | 2026-06-13 | 方言词字段加索引（dialect_word索引）；SKILL.md统计数字更新为13333条；新增拼音搜索功能（纯拼音输入自动识别匹配标准词） |
| v1.0.19 | 2026-06-09 | 代码与文档一致性修复：query_dialect.py DIALECTS补齐全部11种方言；修正数据源文件说明（json.gz→sql）；更新数据统计为实际数据库13087条；输出格式示例改为实际格式；contacts.json注明待实现；补充run_sync_from_cloud.sh说明 |
| v1.0.12 | 2026-06-08 | 修复增量SQL黏行；清理SKILL.md多余目录；合并重复更新日志 |
| v1.0.6 | 2026-06-07 | 清理临时文件；修复嵌套目录；SKILL.md脱敏 |
| v1.0.5 | 2026-06-07 | 删除6个临时导入脚本；内部URL/路径脱敏 |
| v1.0.4 | 2026-06-07 | 绝对路径→相对路径；cloud_share加注释 |
| v1.0.3 | 2026-06-07 | 补充增量SQL（13条词） |
| v1.0.2 | 2026-06-07 | 云共享bitable机制；增量SQL自动化 |
| v1.0.1 | 2026-06-07 | bitable读写工具；9502条词库 |
| v1.0.0 | 2026-06-07 | 初始发布，6种方言双向对照 |

## 免责声明

- 本技能数据仅供参考娱乐使用
- AI推断生成的数据可能存在偏差，请以当地方言为准
- 如有方言准确性争议，以当地方言习惯为准