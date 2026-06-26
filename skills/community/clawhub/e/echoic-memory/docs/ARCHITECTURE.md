# EchoMemory 架构设计文档

## 1. 整体架构

EchoMemory 遵循 AgentSkills 开放标准，兼容 Claude Code 和 OpenClaw。

```
┌─────────────────────────────────────────────────────────────┐
│                     用户交互层                                │
│         (Claude Code / OpenClaw / 其他 MCP 客户端)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     SKILL.md (主入口)                        │
│  - 触发条件                                                  │
│  - 主流程控制                                                │
│  - 工具调用                                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────┐    ┌─────────────────────┐
│   Life Memory       │    │      Persona        │
│   (Part A)          │ +  │      (Part B)       │
│                     │    │                     │
│ - 共同经历          │    │ - Layer 0: 硬规则    │
│ - 日常习惯          │    │ - Layer 1: 身份      │
│ - 重要时刻          │    │ - Layer 2: 说话风格  │
│ - 教诲影响          │    │ - Layer 3: 情感模式  │
│                     │    │ - Layer 4: 行为模式  │
└─────────────────────┘    └─────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     生成的回应                               │
│         (符合 ta 的风格 + 结合共同记忆)                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 核心概念

### 2.1 双层架构

EchoMemory 的核心创新是**双层架构**：

#### Life Memory (人生记忆)
- **作用**：提供事实性上下文
- **内容**：时间线、地点、事件、对话记录
- **更新频率**：低（仅在追加新材料时更新）

#### Persona (人物性格)
- **作用**：决定回应方式和风格
- **内容**：5 层性格结构
- **更新频率**：中（可在对话中纠正）

### 2.2 5 层性格结构

优先级从高到低：

```
Layer 0: 硬规则（不可违背）
    ↓
Layer 1: 身份锚定（你是谁）
    ↓
Layer 2: 说话风格（怎么说）
    ↓
Layer 3: 情感模式（怎么感受）
    ↓
Layer 4: 行为模式（怎么做）
```

### 2.3 运行逻辑

```
用户输入
    ↓
[Layer 0] 检查是否违反硬规则
    ↓
[Layer 1-4] 判断 ta 会如何回应
    ↓
[Life Memory] 查找相关共同记忆
    ↓
生成回应（风格 + 记忆）
```

---

## 3. 文件组织

### 3.1 项目结构

```
create-echo/
├── SKILL.md                    # Skill 主入口
├── README.md                   # 项目说明
├── INSTALL.md                  # 安装指南
├── requirements.txt            # Python 依赖
├── .gitignore                  # Git 忽略规则
│
├── prompts/                    # 提示词模板
│   ├── intake.md              # 信息录入引导
│   ├── memory_analyzer.md     # 记忆分析指南
│   ├── persona_analyzer.md    # 性格分析指南
│   ├── memory_builder.md      # 记忆生成模板
│   ├── persona_builder.md     # 性格生成模板
│   ├── merger.md              # 增量合并逻辑
│   └── correction_handler.md  # 纠正处理
│
├── tools/                      # Python 工具
│   ├── wechat_parser.py       # 微信解析
│   ├── qq_parser.py           # QQ 解析
│   ├── social_parser.py       # 社交媒体解析
│   ├── photo_analyzer.py      # 照片分析
│   ├── media_analyzer.py      # 音视频分析
│   ├── skill_writer.py        # Skill 管理
│   └── version_manager.py     # 版本管理
│
├── docs/                       # 文档
│   ├── PRD.md                 # 产品需求
│   ├── ARCHITECTURE.md        # 架构设计
│   └── preview.png            # 预览图
│
└── echoes/                     # 生成的 Skill（gitignore）
    └── {slug}/
        ├── SKILL.md           # 可运行的 Skill
        ├── memory.md          # 人生记忆
        ├── persona.md         # 人物性格
        ├── meta.json          # 元数据
        ├── versions/          # 版本备份
        └── memories/          # 原始素材
```

### 3.2 生成的 Skill 结构

```
echoes/{slug}/
├── SKILL.md                    # 完整的可运行 Skill
├── memory.md                   # Life Memory (Part A)
├── persona.md                  # Persona (Part B)
├── meta.json                   # 元数据和配置
├── versions/                   # 版本历史
│   ├── v1/
│   ├── v2/
│   └── ...
└── memories/                   # 原始素材（可选保留）
    ├── chats/
    ├── photos/
    ├── social/
    └── media/
```

---

## 4. 数据流

### 4.1 创建流程

```
用户输入基础信息
    ↓
导入原材料（聊天记录、照片等）
    ↓
[tools/] 解析原材料
    ↓
[prompts/memory_analyzer.md] 分析记忆
[prompts/persona_analyzer.md] 分析性格
    ↓
[prompts/memory_builder.md] 生成 memory.md
[prompts/persona_builder.md] 生成 persona.md
    ↓
合并生成 SKILL.md
    ↓
写入 echoes/{slug}/
```

### 4.2 对话流程

```
用户发送消息 /{slug} ...
    ↓
加载 echoes/{slug}/SKILL.md
    ↓
[SKILL.md 运行规则]
    ↓
读取 persona.md → 判断回应方式
读取 memory.md  → 补充上下文
    ↓
生成回应
```

### 4.3 进化流程

```
用户提供新材料/纠正
    ↓
[prompts/merger.md] 或 [prompts/correction_handler.md]
    ↓
[tools/version_manager.py] 备份当前版本
    ↓
更新 memory.md 或 persona.md
    ↓
重新生成 SKILL.md
    ↓
更新 meta.json 版本号
```

---

## 5. 关键技术决策

### 5.1 为什么选择 Markdown 作为存储格式？
- **可读性**：人类可以直接阅读和编辑
- **结构化**：可以通过标题层级组织内容
- **兼容性**：与 AgentSkills 标准兼容
- **版本友好**：Git 友好，易于 diff

### 5.2 为什么使用双层架构？
- **分离关注点**：事实 vs 风格
- **独立更新**：可以单独纠正性格或记忆
- **可解释性**：知道为什么 AI 这样回应
- **灵活性**：不同场景可以使用不同组合

### 5.3 为什么需要版本管理？
- **安全性**：错误的更新可以回滚
- **实验性**：可以尝试不同的性格调整
- **情感价值**：保留不同阶段的理解

---

## 6. 扩展性设计

### 6.1 添加新的数据源

1. 在 `tools/` 下创建新的解析器
2. 在 `SKILL.md` 的 Step 2 中添加新选项
3. 在 `prompts/` 中更新分析指南

### 6.2 添加新的性格维度

1. 在 `prompts/persona_builder.md` 中添加新 Layer 或子章节
2. 在 `prompts/persona_analyzer.md` 中添加分析指南
3. 更新生成的 `SKILL.md` 模板

### 6.3 支持新的客户端

EchoMemory 遵循 AgentSkills 标准，理论上支持任何兼容的客户端：
- Claude Code
- OpenClaw
- 其他 MCP 客户端

---

## 7. 安全与隐私

### 7.1 数据存储
- 所有数据本地存储
- 不上传任何服务器
- 敏感目录（echoes/）在 .gitignore 中

### 7.2 访问控制
- 依赖操作系统的文件权限
- 建议设置适当的文件权限

### 7.3 数据删除
- 提供 `/delete-echo` 和 `/farewell` 命令
- 彻底删除相关目录

---

## 8. 性能考虑

### 8.1 加载性能
- SKILL.md 是主要加载文件
- 大型记忆文件可能影响性能
- 建议定期归档旧版本

### 8.2 生成性能
- 解析大型聊天记录可能需要时间
- 照片/视频分析是可选的
- 提供进度提示

---

## 9. 未来架构演进

### 9.1 可能的改进方向
1. **向量数据库**：用于更智能的记忆检索
2. **语音识别**：自动转录音频内容
3. **多模态**：支持图片理解和生成
4. **协作编辑**：多人共同完善一个 Skill

### 9.2 与其他系统的集成
- 与备份系统集成
- 与家谱系统连接
- 与纪念网站同步

---

**架构设计是活的文档，会随着项目发展而演进。**
