---
name: Douyin Influencer Outreach | 抖音达人私信拓展
description: Search for Douyin influencers matching criteria (followers < N, high engagement), browse their content, and send personalized DMs. 搜索符合条件的抖音达人（粉丝低于 N、高互动），浏览作品，发送个性化私信。自动去重，已联系的达人不会重复私信。
---

# Douyin Influencer Outreach | 抖音达人私信拓展

通过抖音精选页面搜索达人，筛选符合条件的账号（粉丝少、互动高），浏览最新作品后发送个性化私信。

**适用场景：**
- 寻找垂直领域的小微达人（KOC）合作
- 批量拓展团购/探店/带货达人
- 建立达人资源库

---

## 🔑 核心工作原则

1. **先确认后执行** — 每次私信前必须与用户确认所有参数
2. **找到一个发一个** — 找到符合条件的达人立即发送私信，不等凑齐
3. **真实键盘输入** — 用 `type` + `press` 模拟真实输入，不用 `evaluate` 设 `textContent`
4. **自动去重** — 已联系的达人不会重复私信
5. **不依赖作品数统计** — 抖音主页的作品 tab 数字不可靠，改用实际能看到的作品卡片判断

---

## 📋 第一步：执行前确认（必须与用户确认）

在开始搜索和发送私信之前，**必须向用户确认以下参数**，展示确认列表后再执行：

### 确认项

| 参数 | 说明 | 示例 |
|------|------|------|
| **搜索话题** | 抖音搜索关键词 | `省钱团购`、`探店`、`好物推荐` |
| **私信人数** | 本次计划发送私信的达人数量 | 5、10、20 |
| **粉丝数范围** | 达人粉丝数区间 | `0-2000`、`500-5000` |
| **最新发布互动** | 最新作品的点赞/评论数要求 | `>3`、`>100` |
| **发布时间和内容形式** | 搜索筛选条件（见下方默认值） | 默认不限 |

### 搜索筛选条件（默认值，对应抖音筛选面板）

打开搜索页后，点击右上角 **筛选** 按钮，设置以下默认条件：

| 筛选项 | 默认选择 | 说明 |
|--------|---------|------|
| 排序依据 | 最新发布 | 优先看最新内容 |
| 发布时间 | 不限 | 不过滤时间 |
| 视频时长 | 不限 | 不过滤时长 |
| 搜索范围 | 不限 | 全部用户 |
| 内容形式 | 视频 | 只看视频类达人 |

### 确认模板

```
📋 私信拓展计划确认

🔍 搜索话题：省钱达人
👥 计划私信：2 人
📊 筛选条件：
  - 粉丝数：300 ~ 2000
  - 最新作品互动：> 3
  - 排序：最新发布
  - 发布时间：不限
  - 内容形式：视频

是否确认执行？（回复"确认"或修改参数）
```

**⚠️ 未得到用户确认，不得自动发送任何私信！**

---

## 📋 联系人追踪 CSV

**文件路径：** `~/.openclaw/workspace/skills/douyin-influencer-outreach/contacted.csv`

**CSV 格式：**
```
昵称,抖音号,sec_uid,粉丝数,获赞数,IP属地,简介,私信内容,私信时间,回复状态,最新作品标题,最新作品互动
```

**去重规则：** 通过 `sec_uid`（达人主页 URL 中的唯一标识）判断是否已联系过。每次私信前必须检查 CSV，已存在的 sec_uid 直接跳过。

### 检查达人是否已联系

```bash
# 读取 CSV，检查 sec_uid 是否已存在
grep -F "{sec_uid}" ~/.openclaw/workspace/skills/douyin-influencer-outreach/contacted.csv
# 有输出 = 已联系，跳过；无输出 = 未联系，可私信
```

### 记录已联系的达人

```bash
# 追加一行到 CSV（注意：昵称和简介中若含逗号需用双引号包裹）
echo '"{昵称}","{抖音号}","{sec_uid}",{粉丝数},{获赞数},"{IP属地}","{简介}","{私信内容}","{私信时间}","未回复","{最新作品标题}","{最新作品互动}"' \
  >> ~/.openclaw/workspace/skills/douyin-influencer-outreach/contacted.csv
```

### 查看已联系人数

```bash
# 统计已联系的达人数量（不含表头）
tail -n +2 ~/.openclaw/workspace/skills/douyin-influencer-outreach/contacted.csv | wc -l | tr -d ' '
```

---

## 🔄 完整工作流

### 阶段 0：确认参数（与用户交互）

1. 向用户展示确认列表（搜索话题、私信人数、筛选条件）
2. 等待用户确认或修改参数
3. 用户确认后，进入阶段 1

### 阶段 1：搜索达人 + 设置筛选

```bash
# 打开抖音精选搜索页面（type=general 获取综合搜索结果）
browser action=open profile=openclaw targetUrl="https://www.douyin.com/jingxuan/search/{关键词}?type=general"
browser action=act request={"kind": "wait", "timeMs": 3000} targetId={tabId}
```

**⚠️ 关键：`type=general` 而非 `type=user`，这样可以获得更丰富的搜索结果（包含视频+用户混合），再通过快照筛选用户信息。**

**设置筛选条件（点击筛选按钮）：**

```bash
# 获取快照，找到"筛选"按钮 ref
browser action=snapshot targetId={tabId}
# 从快照中找到"筛选"按钮 ref

# 点击筛选
browser action=act request={"kind": "click", "ref": "{筛选按钮ref}"} targetId={tabId}
browser action=act request={"kind": "wait", "timeMs": 1000} targetId={tabId}

# 再次快照，找到筛选面板中的选项 ref
browser action=snapshot targetId={tabId}

# 设置筛选条件（根据用户确认的参数）：
# - 排序依据：最新发
# - 内容形式：视频
browser action=act request={"kind": "click", "ref": "{最新发布ref}"} targetId={tabId}
browser action=act request={"kind": "click", "ref": "{视频ref}"} targetId={tabId}
```

### 阶段 2：获取快照，提取达人信息

```bash
# 获取搜索结果快照
browser action=snapshot targetId={tabId}
```

**从快照中提取达人信息：**
- 查找包含"抖音号"和"粉丝"的 link 元素
- 提取：昵称、抖音号、sec_uid（从 URL 提取）、粉丝数、获赞数、简介
- 注意：`type=general` 返回的是混合结果，需过滤出用户类型的条目

### 阶段 3：逐个检查，找到一个发一个 ⚡

**核心逻辑：不收集全部候选人，而是逐个处理，找到符合条件的立即发送。**

```
已发送计数 = 0

对搜索结果中的每个达人条目：
  1. 提取 sec_uid，检查是否已在 CSV 中 → 已联系则跳过
  2. 打开达人主页 → 提取粉丝数 → 检查是否在范围内 → 不在则跳过
  3. 找到主页上的作品卡片 → 点击最新作品 → 查看点赞/评论 → 互动不达标则跳过
  4. ✅ 全部达标 → 立即发送私信 → 记录 CSV → 计数 +1
  5. 计数达到目标人数 → 停止
  6. 结果不够 → 回到搜索页，加载更多结果，继续
```

### 阶段 4：打开主页，检查粉丝

```bash
# 打开达人主页
browser action=open profile=openclaw targetUrl="https://www.douyin.com/user/{sec_uid}"
browser action=act request={"kind": "wait", "timeMs": 2000} targetId={tabId}

# 提取粉丝数（从主页信息区域）
browser action=act request={
  "kind": "evaluate",
  "fn": "() => {
    const text = document.body.innerText;
    const fanMatch = text.match(/(\\d+(\\.\\d+)?万?)粉丝/);
    const likeMatch = text.match(/(\\d+(\\.\\d+)?万?)获赞/);
    const ipMatch = text.match(/IP属地[：:]([^\\n]+)/);
    const bioMatch = text.match(/抖音号[^\\n]*\\n([^\\n]{1,100})/);
    return JSON.stringify({
      fans: fanMatch ? fanMatch[1] : '0',
      likes: likeMatch ? likeMatch[1] : '0',
      ip: ipMatch ? ipMatch[1].trim() : '',
      bio: bioMatch ? bioMatch[1].trim() : ''
    });
  }"
} targetId={tabId}
```

**筛选判断：**
- 粉丝数在用户指定范围内 → 继续
- 不在范围内 → 跳过，处理下一个达人

### 阶段 5：查看最新作品，检查互动

```bash
# 找到主页上的作品区域，点击最新作品
browser action=act request={
  "kind": "evaluate",
  "fn": "() => {
    const links = document.querySelectorAll('a[href*=\"/video/\"]');
    if (links.length > 0) {
      return links[0].href;
    }
    return '';
  }"
} targetId={tabId}

# 打开最新作品页
browser action=open profile=openclaw targetUrl="{作品URL}"
browser action=act request={"kind": "wait", "timeMs": 2000} targetId={tabId}
```

**提取作品互动数据：**

```bash
browser action=act request={
  "kind": "evaluate",
  "fn": "() => {
    const text = document.body.innerText;
    const lines = text.split('\\n');
    let result = {};
    for (let line of lines) {
      const lm = line.match(/(\\d+(\\.\\d+)?万?)\\s*(?:赞|喜欢)/);
      const cm = line.match(/(\\d+)\\s*评论/);
      const colm = line.match(/(\\d+)\\s*收藏/);
      if (lm) result.likes = lm[1];
      if (cm) result.comments = cm[1];
      if (colm) result.collects = colm[1];
      if (line.length > 10 && line.length < 200 && !line.match(/\\d/)) {
        result.title = line.substring(0, 100);
      }
    }
    return JSON.stringify(result);
  }"
} targetId={tabId}
```

**筛选判断：**
- 最新作品点赞数 > 用户指定的最低互动数 → 继续
- 互动不达标 → 返回搜索页，处理下一个达人

### 阶段 6：发送私信

```bash
# 返回达人主页
browser action=open profile=openclaw targetUrl="https://www.douyin.com/user/{sec_uid}"
browser action=act request={"kind": "wait", "timeMs": 2000} targetId={tabId}

# 找到并点击私信按钮
browser action=act request={
  "kind": "evaluate",
  "fn": "() => {
    const btns = document.querySelectorAll('button');
    for (let b of btns) {
      const t = b.textContent || '';
      if (t.includes('私信')) {
        const r = b.getBoundingClientRect();
        if (r.width > 0 && r.height > 0) {
          return {x: Math.round(r.left+r.width/2), y: Math.round(r.top+r.height/2)};
        }
      }
    }
    return 'not found';
  }"
} targetId={tabId}

# 点击私信按钮
browser action=act request={"kind": "clickCoords", "x": {x}, "y": {y}} targetId={tabId}
browser action=act request={"kind": "wait", "timeMs": 1500} targetId={tabId}

# 确认输入框存在
browser action=act request={
  "kind": "evaluate",
  "fn": "() => {
    const input = document.querySelector('[contenteditable=\"true\"]');
    return input ? 'found' : 'not found';
  }"
} targetId={tabId}

# 输入消息（根据最新作品内容定制）
browser action=act request={"kind": "type", "selector": "[contenteditable=\"true\"]", "text": "{定制私信内容}"} targetId={tabId}

# 发送（Enter 键）
browser action=act request={"kind": "press", "key": "Enter"} targetId={tabId}

# 确认发送成功
browser action=act request={
  "kind": "evaluate",
  "fn": "() => {
    const input = document.querySelector('[contenteditable=\"true\"]');
    return input ? (input.textContent.trim() === '' ? 'SENT_OK' : 'NOT_SENT') : 'not found';
  }"
} targetId={tabId}
```

### 阶段 7：记录到 CSV

```bash
# 发送成功后，立即追加到 contacted.csv
echo '"{昵称}","{抖音号}","{sec_uid}",{粉丝数},{获赞数},"{IP属地}","{简介}","{私信内容}","{datetime}","未回复","{最新作品标题}","{最新作品互动}"' \
  >> ~/.openclaw/workspace/skills/douyin-influencer-outreach/contacted.csv
```

### 阶段 8：检查进度

- 已发送人数 = 目标人数 → **任务完成，汇总结果**
- 已发送人数 < 目标人数 → 返回搜索页，加载/翻页获取更多结果，继续处理

---

## 💬 私信话术模板（基于作品内容定制）

陌生人私信限制：对方回复/关注前，只能发**1 条消息**。每条消息必须自成一体，说清价值、降低门槛。

### A 类：作品切入（最推荐 ⭐）

**根据最新作品内容定制，提及具体产品/话题**

```
嗨～看到你分享的{作品中的具体产品/内容}，看起来很不错！我这边有个省钱团购群，专门组织大家拼单购买，刚好有你提到的这款，价格能便宜不少，要不要一起呀？
```

```
你的{作品标题/内容}分享好真实呀！我也是一直在找靠谱的购买渠道，最近建了个小群专门团这类产品，都是自己用着好的才推，不强制购买，想了解的话可以进来看看～
```

### B 类：简介切入

```
看到你简介里说"{简介关键词}"，感觉咱们方向挺一致的～我这边建了个团购群，想找真正需要的朋友一起拼单，有兴趣可以进来看看呀～
```

### C 类：通用型（备用）

```
你好呀，看到你经常分享{领域}相关的内容，内容很用心！我这边有个省钱团购群，专门帮大家对接品牌团购价，都是官方发货，有需要可以拉你进来看看～
```

### 选择策略

| 场景 | 推荐 | 理由 |
|------|------|------|
| 达人有明确的作品内容 | **A 类** ⭐ | 提及具体作品，最自然，回复率最高 |
| 达人作品较少但简介丰富 | B 类 | 从简介切入 |
| 不确定对方情况 | C 类 | 通用保底 |

### 变量替换

| 变量 | 说明 | 示例 |
|------|------|------|
| `{作品中的具体产品/内容}` | 从最新作品中提取 | 塔斯汀汉堡、辛玛奇幻乐园、某款面霜 |
| `{作品标题/内容}` | 作品描述或标题 | 那篇团购分享、那个套餐测评 |
| `{简介关键词}` | 从简介中提取 | 省钱团购、吃喝玩乐 |
| `{领域}` | 达人擅长的领域 | 团购、探店、美食 |

**⚠️ 注意事项：**
- **必须个性化**：每条私信都要提及对方的具体作品或内容
- **避免敏感词**：不要发微信、电话、二维码
- **语气自然**：日常聊天语气，不用广告腔
- **降低门槛**：强调"不强制"、"不买也没关系"

---

## ⚡ 关键优化点（v2.1）

### 1. 搜索类型改为 `type=general`

- 之前用 `type=user` 只能搜到用户列表，信息有限
- 改用 `type=general` 获得混合搜索结果（视频+用户），信息更丰富
- 通过快照从混合结果中筛选出用户类型条目

### 2. 搜索筛选条件

- 打开搜索页后点击 **筛选** 按钮设置条件
- 默认：最新发布 + 内容形式=视频 + 其他不限
- 确保按时间顺序查看，优先处理最新内容

### 3. 找到一个发一个

- 不等待收集全部候选人
- 找到符合条件的达人 → 立即发送 → 记录 → 继续找下一个
- 结果不够时返回搜索页加载更多

### 4. 不再依赖作品数统计

- 抖音主页的"作品 X"数字经常不准确（缓存、加载问题）
- 改用直接查找主页上的作品链接（`a[href*="/video/"]`）
- 能取到作品链接就说明有作品，无需统计数量
- 直接进入作品页查看实际互动数据

---

## 常见问题

### Q: 搜索页面显示 404？
A: 确保使用 `/jingxuan/search/` 路径，不需要登录。普通搜索页需要登录。

### Q: 私信按钮点了没反应？
A: 检查浏览器是否已登录抖音账号。未登录状态下无法发送私信。

### Q: 消息发送失败？
A: 抖音限制陌生人私信：对方未关注/回复前，只能发 1 条。每天发送数量有限制（约 20-30 条）。

### Q: CSV 中字段含逗号导致格式错乱？
A: 所有文本字段（昵称、简介、私信内容等）必须用双引号包裹。

### Q: 作品数显示不准怎么办？
A: v2.1 已不再依赖作品数统计，改为直接查找作品链接进入详情页查看互动。

---

## 依赖工具

- `browser` - 抖音网页操作
- `exec` (grep/echo/wc) - CSV 去重和记录
- 发送私信需要抖音账号登录

---

## 版本历史

- **v2.1** (2026-05-04): 搜索改用 `type=general` + 筛选条件面板 + 找到一个发一个 + 不再依赖作品数统计
- **v2.0** (2026-05-04): 新增执行前确认流程、作品驱动私信定制、真实键盘输入（type+press）
- **v1.1** (2026-04-27): 新增 contacted.csv 去重追踪
- **v1.0** (2026-04-26): 初始版本
