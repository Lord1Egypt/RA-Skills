# 系统接入模板 · 新增业务系统标准化规范

> 新增任何业务系统时，按此模板创建
> 参考：skills/agent-pool/SKILL.md（Agent池）+ skills/tool-pool/SKILL.md（工具池）
> 最后更新：2026-04-11

---

## 新增系统清单

| 系统名称 | 代号 | 创建日期 | 核心Agent | 备注 |
|---------|------|---------|---------|------|
| 市场部获客系统 | system-lead-generation | 2026-04-11 | 虾调度/虾调查/虾写作等 | 已存在 |
| 市场部早报系统 | system-morning-report | 2026-04-11 | 虾调查 | 已存在 |

---

## 新增系统标准流程

### Step 1：确定核心Agent

从 `skills/agent-pool/SKILL.md` 的Agent注册表中选择所需Agent：

```
例：客户管理系统
→ 需要「虾调查」（数据采集）
→ 需要「虾写作」（报告生成）
```

### Step 2：创建系统目录

```
workspace/
└── system-xxx/                    ← 新建系统目录
    ├── MEMORY.md                  ← 系统记忆（必填）
    ├── logs/                      ← 独立日志（必填）
    ├── data/                      ← 独立数据（必填）
    └── scripts/                   ← 专用脚本（如有）
```

### Step 3：关联知识库目录

```
knowledge-base/
└── xxx/                           ← 与系统目录同名（必填）
    ├── data/                      ← 系统归档数据
    ├── logs/                      ← 系统归档日志
    ├── scripts/                   ← 脚本备份
    └── config/                    ← 配置备份
```

### Step 4：编写系统MEMORY.md（流程编排）

```markdown
# system-xxx / MEMORY.md

## 系统身份
| 属性 | 值 |
|------|-----|
| 系统名称 | [系统名称] |
| 系统代号 | system-xxx |
| 定位 | [一句话描述] |
| 核心链路 | [流程链路] |

## 流程编排（调用Agent）

### 流程步骤

#### Step 1: [执行什么业务动作]
  → 调用Agent：`虾调查`（能力描述：...）
    - 工具：按需临时声明（查 skills/tool-pool/SKILL.md）
    - 输出：[描述输出物]

#### Step 2: [执行什么业务动作]
  → 调用Agent：`虾写作`（能力描述：...）
    - 工具：按需临时声明
    - 输出：[描述输出物]

...（按实际流程继续）
```

### 工具引用说明

- **Agent声明工具**：由被调用的Agent自行声明工具依赖
- **系统只做编排**：系统不预分配任何Agent，不预声明任何工具
- **工具池查询**：`skills/tool-pool/SKILL.md`

### Step 5：更新清单

在本文件顶部「新增系统清单」中追加新系统信息。

---

## 接入示例：新增「客户跟进系统」

### 需求
销售团队每次跟进客户后录入系统，Agent自动生成跟进报告。

### Step 1：确定Agent
- `虾写作`：生成跟进报告
- `虾调查`（可选）：收集客户背景信息

### Step 2：创建目录
```
workspace/system-crm-followup/
├── MEMORY.md
├── logs/
└── data/
knowledge-base/crm-followup/
├── data/
└── logs/
```

### Step 3：编写MEMORY.md

```markdown
# system-crm-followup / MEMORY.md

## 系统身份
| 属性 | 值 |
|------|-----|
| 系统名称 | 客户跟进系统 |
| 系统代号 | system-crm-followup |
| 定位 | 销售跟进记录 → 自动生成跟进报告 |
| 触发 | 人工录入后自动触发 |

## 流程编排

### Step 1: 收集客户背景
  → 调用Agent：`虾调查`
    - 工具：tavily, openclaw-serper（临时声明）
    - 输出：客户基本信息/近期动态

### Step 2: 生成跟进报告
  → 调用Agent：`虾写作`
    - 工具：read, write（临时声明）
    - 输出：结构化跟进报告

### 工具池
工具清单：skills/tool-pool/SKILL.md
```

### Step 4：更新清单
在「新增系统清单」中追加：
```
| 客户跟进系统 | system-crm-followup | 2026-04-11 | 虾调查/虾写作 |
```

---

## 模板参考文件

| 文件 | 路径 |
|------|------|
| Agent池 | `skills/agent-pool/SKILL.md` |
| Agent详细注册表 | `skills/agent-pool/references/agent-registry.md` |
| 工具池 | `skills/tool-pool/SKILL.md` |
| 获客系统MEMORY | `system-lead-generation/MEMORY.md` |
| 早报系统MEMORY | `system-morning-report/MEMORY.md` |

---

## 注意事项

1. **Agent由池统一管理** — 新增Agent在池中注册，系统直接引用
2. **系统只做流程编排** — 不预分配Agent，不预声明工具
3. **数据隔离** — 工具调用产生的数据 → 写入发起系统的目录
4. **知识库共享** — 所有系统可读取，仅写入自身归档目录
