# digital-team

管理数字员工（子 agent）的 skill，支持快速创建角色、启动、记忆管理。

## 触发方式

说"创建数字员工"、"管理数字员工"、"启动 XX 角色"等

---

## 核心逻辑：启动前自动检查

**用户说"启动 XXX"时的处理流程：**

1. **解析角色**：从用户指令中提取角色名（支持别名）
2. **检查记忆**：查看 `workspace/agents/{角色}/` 是否存在
3. **存在** → 正常启动，读取记忆
4. **不存在** → 询问用户是否创建新角色

```
用户：启动 design 做登录页面
↓
1. 识别角色：design
2. 检查：agents/design/ 不存在
3. 询问："还没创建 design 角色，要现在创建吗？"
↓
用户：好的
↓
4. 自动创建 agents/design/{profile,memory,current}.md
5. 继续启动流程
```

---

## 功能列表

### 1. 列出所有角色
```
列出所有数字员工
```
显示所有已创建的角色及其状态。

### 2. 创建新角色
```
创建角色 {角色名}: {核心职责描述}
```
例如：`创建角色 design: UI/UX设计、交互优化`

会在 `workspace/agents/{角色名}/` 下自动创建：
- `profile.md` - 角色设定
- `memory.md` - 长期记忆
- `current.md` - 当前状态

### 3. 启动数字员工 ⚡（核心功能）
```
启动 {角色名}
启动 {角色名} 执行 {任务描述}
```

**启动流程：**
1. 解析角色名（支持别名匹配）
2. 检查 `agents/{角色}/` 是否存在
3. **不存在** → 询问用户："还没创建 {角色} 角色，要现在创建吗？"
   - 用户确认 → 创建角色 → 继续启动
   - 用户拒绝 → 取消启动
4. **存在** → 读取记忆文件：
   - `agents/{角色}/profile.md`
   - `agents/{角色}/memory.md`
   - `agents/{角色}/current.md`
   - `knowledge/project.md`
   - `knowledge/team.md`
5. 创建子 agent 并注入记忆
6. 任务完成后自动更新记忆

### 4. 查看角色状态
```
{角色名} 状态
查看 {角色名} 记忆
```

### 5. 更新角色记忆
```
{角色名} 记住 {内容}
```

### 6. 批量创建角色
```
创建数字员工团队：{角色1}, {角色2}, {角色3}
```

---

## 文件结构

```
workspace/agents/
├── ROLES.md          # 角色别名映射
├── TEMPLATE.md       # 启动模板
├── pm/
│   ├── profile.md    # 角色设定
│   ├── memory.md     # 长期记忆
│   └── current.md    # 当前任务
├── arch/
│   └── ...
├── qa/
│   └── ...
└── {新角色}/
    └── ...

workspace/knowledge/
├── project.md        # 项目背景
├── decisions.md      # 已决策事项
└── team.md           # 协作规则
```

---

## 内部命令

本 skill 内部使用：

- `exec ls` - 检查角色目录是否存在
- `exec mkdir` - 创建角色目录
- `read/write` - 读写记忆文件
- `sessions_spawn` - 启动子 agent

---

## 使用示例

**示例 1：启动已有角色**

**用户：** "启动 pm 做一个用户登录功能"

**skill 执行：**
1. 识别角色：pm
2. 检查：`agents/pm/` 存在 ✅
3. 读取记忆文件
4. 创建子 agent
5. 任务完成后更新 `agents/pm/memory.md` 和 `current.md`

---

**示例 2：启动新角色（自动询问）**

**用户：** "启动 design 做登录页面"

**skill 执行：**
1. 识别角色：design
2. 检查：`agents/design/` 不存在 ❌
3. 询问用户："还没创建 design 角色，要现在创建吗？"

**用户：** "好的"

4. 自动创建：
   - `agents/design/profile.md`
   - `agents/design/memory.md`
   - `agents/design/current.md`
   - 更新 `ROLES.md` 添加 design 映射
5. 继续启动流程，读取新建的记忆文件
6. 创建子 agent 执行任务

---

**示例 3：取消创建**

**用户：** "启动 design 做登录页面"

**skill：** "还没创建 design 角色，要现在创建吗？"

**用户：** "算了"

→ 取消启动，不创建角色