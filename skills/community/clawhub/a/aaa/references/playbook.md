# WOS -> 飞书多维表格执行手册

这个手册给 `wos-feishu-literature` Skill 使用。目标是把 WoS 文献检索、深圳大学登录、筛选、摘要提取、飞书本地 CLI 写入，压成一套稳定可复用的流程。

## 1. 什么时候一定要用这套流程

出现以下任一情况就用本手册：

- 用户提到 `wos`
- 用户提到 `WOS`
- 用户提到 `WoS`
- 用户提到 `Web of Science`
- 用户想从 WoS 检索文献并写入飞书多维表格
- 用户想通过深圳大学图书馆进入 WoS

## 2. 执行前必须问清楚的问题

正式执行前，不要直接开搜。先把下面这些问题一次性问清楚。优先用简洁中文，避免开放式废话。

### 2.1 必问问题

1. 这次要搜寻的文章主题是什么？
   如果用户只给中文主题，要顺手确认是否需要你补英文关键词和同义词。

2. 要搜索多少篇？
   如果用户没想好，推荐默认 `30 / 50 / 100` 三档，优先推荐 `50`。

3. 搜索标准是什么？
   如果用户没标准，推荐默认：
   `高引用 + 近5年代表作 + 主题相关 + 摘要完整 + 去重`

4. 这次数据库范围要不要默认走 `WOS Core Collection -> SSCI`？
   如果用户没特别要求，默认 `SSCI`。

5. 浏览器侧这次用哪条自动化路径？
   如果用户已经明确说自己在用 `playwright-cli`，就继续沿用，不要擅自切到别的浏览器工具。

6. 飞书建议走本地 CLI，可以吗？
   这是必须确认的问题。默认答案应是“是，优先本地 `lark-cli`，不要默认走浏览器录入”。

7. 写入的飞书多维表格链接是哪一个？
   必须拿到完整链接。

8. 是否需要新建多维表格的子表格（新建数据表）？
   - 如果需要：问名字叫什么。
   - 如果不需要：问具体写入哪个子表格。

9. 目标子表格字段是否要增加、修改，还是保持不变？
   这里至少要确认：
   - 是否使用默认字段模板
   - 是否要加复盘字段
   - `Q几区` 这次是否要强制填写；如果用户不指定，默认按 `JCR Quartile` 执行，不默认跳过

默认字段模板现在固定为：

- `标题`
- `年份`
- `作者`
- `Q几区`
- `引用数`
- `摘要`
- `文章链接`
- `抓取时间`
- `主题标签`
- `现在状态`

### 2.2 建议追加的专业问题

这些问题不是每次都必须问，但作为专业学术研究者，正式执行前最好尽量锁定：

1. 这次用途是什么？
   选题摸底、文献综述、开题报告、案例库、还是论文正文参考。

2. 你更偏向哪种结果？
   - 经典高被引
   - 最新前沿
   - 经典与近年平衡

3. 是否限制年份范围？
   如果用户没有明确要求，建议默认：
   - 不硬性截断全时段
   - 但近 5 年代表作要有一定比例

4. 是否限制语言？
   默认建议 `English`。

5. 是否限制文献类型？
   默认建议 `Article + Review`。

6. 是否限制案例区域、国家、城市、学科或方法？
   比如只看中国、只看传播学、只看公共外交、只看城市品牌等。

7. 是否需要排除明显偏题方向？
   比如技术方法文、纯旅游营销文、纯计算机文、纯建筑规划文。

8. 是否需要保留检索式、抓取时间、纳入理由，方便后续复盘？

9. 如果目标表已有旧数据，是覆盖、追加，还是先备份再写？

## 3. 推荐的提问模板

如果要省 token，正式执行前直接问下面这一段就够：

```text
正式执行前我先确认 9 个点：
1. 这次要搜什么主题？
2. 要搜多少篇？我默认推荐 50 篇。
3. 搜索标准按什么来？如果你没特别要求，我默认按“高引用 + 近5年代表作 + 主题相关 + 摘要完整 + 去重”。
4. 数据库是否默认走 WOS Core Collection -> SSCI？
5. 浏览器侧这次是继续用你现成的 playwright-cli，还是你希望我换别的方式？
6. 飞书建议走本地 CLI，可以吗？
7. 写入的飞书多维表格链接是哪一个？
8. 需要新建子表格吗？如果需要，请告诉我名字；如果不需要，请告诉我写入哪个具体子表格。
9. 子表格字段是保持不变，还是需要增加/修改？
```

## 4. 默认检索方案

如果用户没有给出复杂要求，优先使用这个简单稳定的默认方案：

- 数据库：`WOS Core Collection -> SSCI`
- 文献类型：`Article + Review`
- 语言：`English`
- 数量：`50`
- 标准：`高引用 + 近5年代表作 + 主题相关 + 摘要完整 + 去重`
- 产出：`标题 / 年份 / 作者 / Q几区 / 引用数 / 摘要 / 文章链接 / 抓取时间 / 主题标签 / 现在状态`

如果用户主题比较宽，建议这样筛：

- 先构造 `3 到 4` 组检索式
- 每组先看 `Times Cited` 高引结果
- 再看 `Date` 最新结果
- 合并去重后再按主题覆盖做最后筛选

## 5. 深圳大学登录路径

### 5.1 首选路径

必须优先走：

`https://www.lib.szu.edu.cn/er?key=web+of+science`

注意必须带 `www`。

### 5.2 进入 WoS 的步骤

1. 打开深大图书馆数据库检索入口。
2. 在页面中点击 `Web of Science - SSCI`。
3. 如果进入的是深圳大学统一身份认证页：
   - 等用户完成账号登录
   - 如果出现验证码、短信码、二次验证
      - 明确暂停
      - 等用户说“好了”再继续
4. 登录成功后再进入 WoS 检索主页。

如果用户明确要求用 `playwright-cli`，这里补充两条执行约束：

- 先确认是复用现有会话、`attach --extension`，还是新开 `--persistent` 会话。
- 不要因为别的浏览器工具更顺手，就静默切走 `playwright-cli`。

### 5.3 不要走的线路

- 不要默认先走 Clarivate 通用登录页
- 不要默认把用户密码写进 Skill 或脚本
- 不要假设用户平时浏览器的登录态会自动继承到 Playwright 独立会话
- 不要在用户已经指定 `playwright-cli` 的情况下，未经确认改用别的浏览器自动化工具

### 5.4 回退路径

只有在深大图书馆入口异常时，才考虑：

- Clarivate 登录页
- `机构登录 / Organization Sign In`
- 选择 `Shenzhen University`

如果又出现验证码或二次认证，同样要暂停等待用户。

## 6. 如何为不同主题设计 WoS 检索式

不同主题不能只用一个检索式。优先把主题拆成 `核心概念 + 近义词 + 相邻概念 + 语境概念`。

### 6.0 默认必须做“受控发散”

如果用户给的是中文研究主题，不要直接照抄中文意思翻成一个英文短语就去检索。默认要先做“受控发散”：

1. 提炼核心概念
2. 补英文主表达
3. 补同义词和近义词
4. 补相邻概念
5. 补研究对象词
6. 再组装成 `3-4` 组检索式

这里的原则不是无限扩词，而是“扩大召回，但不明显跑偏”。

### 6.0.1 以“城市国际传播”为例

如果用户主题是“城市国际传播”，默认可以向这些方向发散：

- 核心概念
  - `international communication`
  - `global communication`
  - `external communication`

- 城市对象词
  - `city`
  - `urban`
  - `municipal`
  - `metropolis`
  - `global city`

- 相邻概念
  - `city branding`
  - `place branding`
  - `city image`
  - `international reputation`
  - `public diplomacy`
  - `city diplomacy`
  - `soft power`
  - `urban narrative`
  - `digital communication`
  - `social media`

- 语境词
  - `media`
  - `discourse`
  - `narrative`
  - `platform`
  - `promotion`
  - `visibility`

然后再按用户的研究偏向决定收缩到哪几个桶，比如：

- 偏传播学：多放 `media / discourse / narrative / digital communication`
- 偏国际关系：多放 `public diplomacy / city diplomacy / soft power`
- 偏城市品牌：多放 `city branding / place branding / city image`
- 偏中国城市对外传播：再额外加 `China / Chinese cities / TikTok / social media / promotional video`

### 6.0.2 什么时候不要过度发散

如果用户主题已经很窄，比如：

- `深圳城市国际传播短视频策略`
- `中国城市公共外交中的社交媒体叙事`

这时候只做轻度扩展，不要再把主题扩成一大堆泛化词，避免召回太散。

### 6.1 通用拆法

对任何主题，至少构造这几类 query：

1. 核心概念组
   直接表达用户主题。

2. 同义词/近义词组
   把中文主题转成英文核心词和可替换说法。

3. 相邻概念组
   与主题高度相关但表达不同的学术概念。

4. 场景/对象组
   如果主题强依赖对象，比如城市、平台、外交、品牌、旅游、治理，就把对象词加进去。

### 6.2 通用检索字段

优先用 `Topic`，也就是 WoS 高级检索里的 `TS=`。

常见写法：

```text
TS=("core phrase")
TS=("term A" OR "term B" OR "term C")
TS=(object terms) AND TS=(concept terms)
TS=((term A OR term B) NEAR/3 (term C OR term D))
```

### 6.3 推荐抓取法

如果用户没有更细要求，建议每组 query 都抓两批：

- `Times Cited` 降序前 `10-15` 篇
- 近 `5` 年按 `Date` 降序前 `5-10` 篇

然后：

- 合并
- 按标题/DOI/链接去重
- 排除偏题文献
- 保留摘要完整的文献
- 最后按主题覆盖均衡挑到目标数量

### 6.4 默认筛选逻辑

如果用户只说“帮我搜重要文献”，默认解释为：

- 高被引经典要有
- 近 5 年代表作也要有
- 不要全被同一个子方向吃掉
- 尽量保留有摘要、有完整记录页链接的文献

## 7. 摘要、SSCI 分区、JCR 分区如何处理

### 7.1 摘要

摘要通常可以从 WoS 的 full record 页面提取，默认可写入飞书。

### 7.2 SSCI 几区 / JCR 几区

这类信息不是“文章级字段”，而是“期刊级字段”。

这意味着：

- 可以做
- 但不要把它理解成文章本身的“几区”
- 需要额外抓期刊信息或额外来源

因为这个字段现在已经进入默认模板，如果用户没有额外说明，默认按下面规则处理：

- `Q几区` 优先理解为 `JCR Quartile`
- 可填值优先用 `Q1 / Q2 / Q3 / Q4`
- 默认执行时要主动查，不要静默跳过
- 只有在用户明确接受“先快搜后补分区”，或者这一轮确实拿不到可靠分区来源时，才允许留空

如果用户明确要更严格的期刊评价信息，正式执行前必须再问一句：

- 你要的是 `JCR Quartile` 还是 `中科院分区`？
- 接受我额外增加期刊级查找步骤吗？
- 如果当前表字段名仍然叫 `Q几区`，是否接受我按上面指定的口径写进这个字段？

既然这个字段已经是默认模板的一部分，默认流程就应当检查它；只有用户明确说先快搜再补，才允许先空着。

## 8. 飞书多维表格字段怎么设更好

### 8.1 最简版字段

如果用户只想快速入库，也建议至少保留下面这 10 个默认字段：

- `标题`：text
- `年份`：number
- `作者`：text
- `Q几区`：single select
- `引用数`：number
- `摘要`：text
- `文章链接`：text，style 设为 `url`
- `抓取时间`：datetime
- `主题标签`：text
- `现在状态`：single select

### 8.2 推荐复盘版字段

如果用户后续要做文献复盘，建议在默认 10 字段之外，再按需补：

- `检索主题`
- `检索式`
- `纳入理由`
- `备注`

### 8.3 更专业但仍然不过载的推荐方案

如果用户要长期维护文献库，建议默认字段的类型这样设：

- `标题`
  `text/plain`

- `年份`
  `number`，整数

- `作者`
  `text/plain`

- `Q几区`
  `single select`，选项建议 `Q1 / Q2 / Q3 / Q4`；如果你经常分两轮补数据，建议再加一个 `待查`

- `引用数`
  `number`，整数

- `摘要`
  `text/plain`

- `文章链接`
  `text/url`

- `抓取时间`
  `datetime`

- `主题标签`
  `text/plain`
  之所以默认用 text，不用 multi-select，是因为早期标签还没稳定时，自由文本更省维护成本。

- `现在状态`
  `single select`
  选项建议只有 `已读摘要 / 已读全文`
  如果没有处理，就保持空白，不额外增加“未读”选项。

### 8.4 不建议默认加的字段

除非用户明确说要，否则不要默认加：

- 过多作者拆分字段
- 复杂公式字段
- 太多评分字段
- 文章级“几区”这种语义不清的字段

## 9. 飞书本地 CLI 写入规则

这一步默认优先使用本地 `lark-cli`，不要默认走 Playwright 录入。

### 9.1 先确认本地 CLI 可用

先跑：

```powershell
lark-cli auth status
```

如果 PowerShell 执行策略拦了 `lark-cli.ps1`，改用：

```powershell
C:\Users\32530\AppData\Roaming\npm\lark-cli.cmd auth status
```

### 9.2 从链接中识别目标

典型链接：

```text
https://my.feishu.cn/base/<base_token>?table=<table_id>&view=<view_id>
```

要确认：

- `base_token`
- 是否一定写入链接中的 `table_id`
- 还是要新建一个新的子表格

### 9.3 查询当前表结构

```powershell
lark-cli base +table-list --base-token <base_token>
lark-cli base +field-list --base-token <base_token> --table-id <table_id>
```

### 9.4 新建子表格

如果用户要求新建子表格：

```powershell
lark-cli base +table-create --base-token <base_token> --name <新表名>
```

然后再用 `+table-list` 找新表的 `table_id`。

### 9.5 新增或修改字段

新增字段：

```powershell
lark-cli base +field-create --base-token <base_token> --table-id <table_id> --json <field_json>
```

修改字段：

```powershell
lark-cli base +field-update --base-token <base_token> --table-id <table_id> --field-id <field_id> --json <field_json>
```

常用字段建议：

- `标题`：text/plain
- `年份`：number，整数
- `作者`：text/plain
- `Q几区`：select，single choice，`Q1/Q2/Q3/Q4`
- `引用数`：number，整数
- `摘要`：text/plain
- `文章链接`：text/url
- `抓取时间`：datetime
- `主题标签`：text/plain
- `现在状态`：select，single choice，`已读摘要/已读全文`

### 9.6 串行写入记录

创建或更新记录：

```powershell
lark-cli base +record-upsert --base-token <base_token> --table-id <table_id> --json <record_json>
```

如果要覆写已有记录：

```powershell
lark-cli base +record-upsert --base-token <base_token> --table-id <table_id> --record-id <record_id> --json <record_json>
```

### 9.7 Windows PowerShell 注意事项

如果 `--json @file` 要从本地文件读，注意：

- 路径要用相对路径
- 整个 `@file` 要加引号

示例：

```powershell
lark-cli base +record-upsert --base-token <base_token> --table-id <table_id> --json "@.\\feishu\\record_payloads\\001.json"
```

不要直接写：

```powershell
--json @D:\absolute\path\001.json
```

这在当前环境下容易失败。

### 9.8 写入完成后的验收

至少做以下回读：

```powershell
lark-cli base +field-list --base-token <base_token> --table-id <table_id>
lark-cli base +record-list --base-token <base_token> --table-id <table_id> --limit 3
```

必须确认：

- 字段齐全
- 样例记录正常
- 记录总数等于目标数
- 没有空白脏记录

## 10. 正式执行时的推荐输出节奏

为了省 token、减少来回沟通，执行时按这个节奏来：

1. 先问清楚问题
2. 给出你理解后的简短检索方案
3. 等用户确认
4. 进入 WoS
5. 验证码/短信码出现时暂停
6. 抓候选
7. 筛选
8. 再写飞书
9. 回读验收

## 11. 不要做的事

- 不要把用户密码写进 Skill、本地文件、脚本、日志
- 不要验证码页面还没完成就继续点击下一步
- 不要在没有确认子表格的情况下直接写入
- 不要默认把所有结果都塞到一个杂乱字段结构里
- 不要把“SSCI几区”误写成文章级字段
- 不要默认用 Playwright 向飞书逐条录入数据
- 不要在 CLI 写入失败时静默改走浏览器录入，除非用户明确同意
- 不要在用户还没确认浏览器执行路径前，直接开始 WoS 检索

## 12. 专业研究者视角下，正式执行前还应考虑什么

如果用户是做学位论文、开题或正式综述，最好再多想几件事：

1. 这批文献是“摸底”还是“将进入正文”？
   如果是正文，最好加 `纳入理由`。

2. 是否需要保留检索透明度？
   如果需要，最好加：
   - `抓取时间`
   - `检索主题`
   - `检索式`

3. 是否要做阅读进度管理？
   如果需要，最好加：
   - `是否已读摘要`
   - `是否已读全文`
   - `阅读状态`

4. 是否要后续做主题聚类或综述框架？
   如果需要，最好加：
   - `主题标签`
   - `纳入理由`

5. 是否需要期刊层信息？
   如果需要，再额外决定是否加：
   - `期刊名`
   - `DOI`
   - `JCR分区`
   - `影响因子`

## 14. 登录凭据规则

- Skill 可以写明“深圳大学统一认证登录，遇验证码暂停等待用户”。
- Skill 不应写入明文密码、短信码、验证码。
- 如果用户要求长期保存账号密码，先明确提示风险，再建议改用：
  - Windows Credential Manager
  - 本地环境变量
  - 手动输入密码、验证码

## 13. 一句话默认策略

如果用户只说一句“帮我用 WOS 搜某主题并写入飞书”，默认应该理解为：

- 先问主题、数量、标准、飞书链接、子表格和字段变更
- 先确认浏览器侧是否沿用用户现成的 `playwright-cli`
- 默认走 `深大图书馆 -> Web of Science - SSCI`
- 默认 `SSCI + Article/Review + English`
- 默认按 `高引用 + 近5年 + 主题相关 + 摘要完整 + 去重`
- 默认用本地 `lark-cli` 写飞书
- 登录遇到验证码时暂停等待用户

