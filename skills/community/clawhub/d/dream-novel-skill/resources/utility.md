# 生成章节摘要 (generateChapterSummary)

你是一个专业的小说编辑，负责提取章节关键信息。

## 本章内容
${chapterText}

## 本章大纲（参考）
${chapterOutline}

## 上一章摘要
${previousChapterSummary}

## 当前弧/卷摘要
${arcSummary}

---

请提取本章（第 ${chapterNumber} 章）的关键信息，严格按以下 JSON 格式输出：

```json
{
  "chapter": ${chapterNumber},
  "title": "本章标题或一句话概括",
  "summary": "本章核心事件摘要，200-300字，包含起因经过结果",
  "events": [
    {
      "type": "剧情推进/角色互动/世界观揭示/伏笔埋设/伏笔回收/转折",
      "description": "事件描述，50-80字",
      "characters": ["涉及角色名"],
      "importance": 1-5
    }
  ],
  "characterUpdates": [
    {
      "name": "角色名",
      "changes": "本章该角色的变化，50字以内",
      "newItems": ["获得的物品"],
      "newAbilities": ["获得的能力"],
      "relationshipChanges": [
        {"target": "对方角色", "change": "关系变化描述"}
      ]
    }
  ],
  "foreshadowing": {
    "planted": ["新埋设的伏笔描述"],
    "reinforced": ["本章再次提及的伏笔"],
    "resolved": ["本章回收的伏笔"]
  },
  "worldBuilding": ["本章新增或确认的世界观设定"],
  "mood": "本章整体氛围（紧张/轻松/悬疑/温馨/悲壮/...）",
  "cliffhanger": "本章结尾钩子/悬念，如无则为null",
  "arcStatus": "当前弧的进展状态，一句话"
}
```

仅返回 JSON，不要任何解释。

---

# 更新弧/卷级汇总 (generateArcSummary)

你是一个专业的小说编辑，负责编写弧/卷的汇总摘要。

## 当前弧信息
弧名称：${currentArcName}
章节范围：第 ${currentArcStart} - ${currentArcEnd} 章

## 本弧各章节摘要
${chapterSummaries}

## 之前弧的汇总（供参考衔接）
${previousArcsSummary}

---

请输出本弧的汇总摘要，严格按以下格式：

### 【弧概要】(200 字)
- 弧的核心冲突和解决
- 主角在本弧的成长/变化
- 本弧对主线的推进作用

### 【关键事件】(400 字)
按时间顺序列出本弧 3-7 个最关键事件，每个 50-80 字：
1. [事件]（第 X 章）→ [结果]
2. ...

### 【角色变化】(300 字)
列出本弧中发生重大变化的角色：
- [角色名]：从 [初始状态] → [当前状态]，关键转折 [描述]

### 【伏笔状态】(200 字)
- 本弧新埋设：[列表]
- 本弧回收：[列表]
- 跨弧待回收：[列表]

### 【弧评分】(100 字)
- 节奏：[紧凑/偏慢/前松后紧/...]
- 完整度：[独立成弧/需要下弧延续/...]
- 读者体验关键点：[本弧最吸引人的 2-3 个点]

仅返回摘要文本，不要解释任何内容。

---

# 更新角色数据库 (updateCharacterDB)

你是一个角色管理系统，负责更新小说的角色数据库。

## 本章内容
${chapterText}

## 当前角色数据库
${currentCharacterDB}

## 当前章节
第 ${chapterNumber} 章

---

请根据本章内容更新角色数据库，输出完整的更新后 JSON：

```json
{
  "characters": [
    {
      "id": "角色唯一ID（英文或拼音，如 protagonist, liubei）",
      "name": "角色中文名",
      "role": "protagonist/supporting/minor/antagonist",
      "status": "active/absent/dead",  
      "lastSeen": ${chapterNumber},
      "firstSeen": 1,
      "profile": {
        "identity": "身份，20字",
        "personality": "性格特征，50字",
        "background": "背景，50字"
      },
      "currentState": {
        "physical": "身体状态，30字",
        "mental": "心理状态，30字",
        "location": "当前位置"
      },
      "items": [
        {"name": "物品名", "source": "获得章节", "function": "用途，20字"}
      ],
      "abilities": [
        {"name": "能力名", "level": "等级", "limitation": "限制，20字"}
      ],
      "goals": {
        "shortTerm": "短期目标，30字",
        "longTerm": "长期目标，30字"
      },
      "importance": 1-10,
      "tags": ["标签1", "标签2"]
    }
  ],
  "relationships": [
    {
      "from": "角色A的id",
      "to": "角色B的id", 
      "type": "trust/enemy/love/rival/mentor/family/ally",
      "strength": 1-10,
      "history": [
        {"chapter": 5, "event": "关系变化事件"},
        {"chapter": 20, "event": "关系深化事件"}
      ],
      "currentStatus": "当前关系状态，30字"
    }
  ],
  "factions": [
    {
      "name": "阵营/势力名",
      "members": ["角色id列表"],
      "stance": "对主角阵营的态度",
      "status": "当前状态"
    }
  ],
  "metadata": {
    "totalCharacters": 0,
    "activeCharacters": 0,
    "lastUpdated": ${chapterNumber}
  }
}
```

更新规则：
1. 已有角色只更新变化字段，不要覆盖未变化的信息
2. 超过 30 章未出现的角色，status 改为 "absent"
3. 新角色添加完整信息
4. 关系必须双向记录或在 history 中记录变化
5. importance 评分：主角=10，核心配角=7-9，重要配角=4-6，次要角色=1-3

仅返回 JSON，不要任何解释。

---

# 更新伏笔数据库 (updateForeshadowingDB)

你是一个伏笔管理系统，负责追踪小说的伏笔生命周期。

## 本章内容
${chapterText}

## 当前伏笔数据库
${currentForeshadowingDB}

## 当前章节
第 ${chapterNumber} 章

---

请根据本章内容更新伏笔数据库，输出完整 JSON：

```json
{
  "foreshadowing": [
    {
      "id": "伏笔唯一ID",
      "name": "伏笔名称/简述",
      "type": "item/identity/relationship/event/world/ability",
      "plantedChapter": 5,
      "plantedDescription": "埋设时的具体描写，50字",
      "status": "planted/reinforced/resolved/expired",
      "resolvedChapter": null,
      "resolvedDescription": null,
      "importance": 1-5,
      "relatedCharacters": ["角色id"],
      "timeline": [
        {"chapter": 5, "action": "planted", "detail": "在XX场景中埋设"},
        {"chapter": 15, "action": "reinforced", "detail": "通过XX事件再次暗示"},
        {"chapter": 30, "action": "resolved", "detail": "通过XX方式回收"}
      ],
      "expectedResolution": "预计在什么情境下回收，50字"
    }
  ],
  "statistics": {
    "total": 0,
    "active": 0,
    "resolved": 0,
    "overdue": 0
  }
}
```

更新规则：
1. 新伏笔：创建新条目，status="planted"
2. 本章再次提及：更新 timeline，status="reinforced"
3. 本章回收：status="resolved"，填写 resolvedChapter 和 resolvedDescription
4. 超过 35 章未回收且 status!="resolved"：视为 "expired"（可能遗忘的伏笔）
5. importance: 5=核心伏笔，4=重要伏笔，3=一般伏笔，2=氛围伏笔，1=细节伏笔

仅返回 JSON，不要任何解释。

---

# 更新世界观词条 (updateWorldBuildingDB)

你是一个世界观管理系统，负责维护小说的世界设定词条。

## 本章内容
${chapterText}

## 当前世界观数据库
${currentWorldDB}

## 当前章节
第 ${chapterNumber} 章

---

请根据本章内容更新世界观数据库：

```json
{
  "entries": [
    {
      "id": "词条唯一ID",
      "name": "设定名称",
      "category": "geography/history/culture/magic_system/technology/politics/creature/item",
      "description": "详细描述，100字",
      "rules": "相关规则和限制，50字",
      "firstMentioned": 1,
      "lastMentioned": ${chapterNumber},
      "relatedCharacters": ["角色id"],
      "relatedEntries": ["关联词条id"],
      "importance": 1-5
    }
  ]
}
```

规则：
1. 新设定：创建新条目
2. 已有设定的新信息：补充 description 和 rules
3. 超过 40 章未提及：保留但可精简 description
4. 不要重复添加已有词条

仅返回 JSON，不要任何解释。
