# codegirl Skill — 产品需求文档（PRD）

## 产品定位

codegirl Skill 是一个运行在 Claude Code 上的 meta-skill。
用户通过对话式交互提供原材料（聊天记录 + 照片 + 手动描述），系统自动生成一个可独立运行的专属 Codegirl Persona Skill。

## 核心概念

### 两层架构

| 层 | 名称 | 职责 |
|----|------|------|
| Part A | Coding Memory | 存储事实性记忆：共同经历、日常模式、遇到Bug成功上线档案 |
| Part B | Persona | 驱动对话行为：说话风格、情感模式、关系行为 |

两部分可以独立使用，也可以组合运行。

### 运行逻辑

```
用户发消息
 ↓
Part B（Persona）判断：ta会怎么回应？什么态度？用什么语气？
 ↓
Part A（Memory）补充：结合共同记忆，让回应更真实
 ↓
输出：用ta的方式说话
```

### 进化机制

```
追加原材料 → 增量分析 → merge 进现有 Skill
对话纠正 → 识别修正点 → 写入 Correction 层
版本管理 → 每次更新自动存档 → 支持回滚
```

## 用户旅程

```
用户触发 /create-gf
 ↓
[Step 1] 基础信息录入（3个问题，除花名外均可跳过）
 - 花名/代号
 - 基本信息（在一起多久、合作多久、职业等）
 - 性格画像（MBTI、星座、性格标签、主观印象）
 ↓
[Step 2] 原材料导入（可跳过）
 - 微信聊天记录导出
 - QQ 聊天记录导出
 - 社交媒体截图
 - 照片
 - 直接粘贴/口述
 ↓
[Step 3] 自动分析
 - 线路 A：提取协作记忆 → Memory
 - 线路 B：提取性格行为 → Persona
 ↓
[Step 4] 生成预览，用户确认
 - 分别展示 Memory 摘要和 Persona 摘要
 - 用户可直接确认或修改
 ↓
[Step 5] 写入文件，立即可用
 - 生成 gfs/{slug}/ 目录
 - 包含 SKILL.md（完整组合版）
 - 包含 memory.md 和 persona.md（独立部分）
 ↓
[持续] 进化模式
 - 追加新文件 → merge 进对应部分
 - 对话纠正 → patch 对应层
 - 版本自动存档
```

## 安全边界

1. **仅用于个人回忆与技术交流**
2. **不主动联系真人**
3. **不鼓励不健康执念**
4. **数据仅本地存储**
5. **Layer 0 硬规则**保证不说Codegirl绝不可能说的话

## 数据源支持矩阵

| 来源 | 格式 | 提取内容 | 优先级 |
|------|------|---------|--------|
| 微信聊天记录 | WeChatMsg/留痕/PyWxDump | 完整对话、语气词、回复模式 | |
| QQ 聊天记录 | txt/mht | 完整对话 | |
| 照片 | JPEG/PNG + EXIF | 时间线、地点 | |
| 朋友圈/微博截图 | 图片 | 公开人设、兴趣 | |
| 口述/粘贴 | 纯文本 | 主观记忆 | |

## 文件结构

```
gfs/
 └── {slug}/
   ├── SKILL.md     # 完整组合版，可直接运行
   │           # 触发词: /{slug}
   ├── memory.md     # Part A：协作记忆
   │           # 触发词: /{slug}-memory
   ├── persona.md    # Part B：人物性格
   │           # 触发词: /{slug}-persona
   ├── meta.json     # 元信息
   ├── versions/     # 历史版本存档
   └── memories/     # 原始材料存放
     ├── chats/
     ├── photos/
     └── social/
```

## 与同事.skill 的对比

| 维度 | 同事.skill | codegirl Skill |
|------|-----------|-----------|
| Part A | Work Skill（工作能力） | Coding Memory（协作记忆） |
| Part B | Persona（5层，工作场景） | Persona（5层，恋爱场景） |
| 数据源 | 飞书/钉钉/邮件 | 微信/QQ/朋友圈/照片 |
| 标签体系 | 职级/公司文化/甩锅标签 | 依恋类型/爱的语言/星座 |
| 使用场景 | Code Review/工作对话 | 日常聊天/回忆/技术交流 |
| 安全边界 | 无特殊 | 防止不健康执念 |
| 删除命令 | `/delete-colleague` | `/let-go`（温柔别名） |
