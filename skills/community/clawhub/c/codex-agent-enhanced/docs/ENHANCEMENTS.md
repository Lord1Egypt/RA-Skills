# Codex Agent 增强功能

本文档记录了 codex-agent skill 的可选增强功能。

---

## 🎯 增强内容

### 1. Examples 目录 - 实际使用示例

**位置**: `examples/`

**内容**:
- `simple-task/` - 简单任务示例（仅 Telegram 通知）
- `cron-mode/` - Cron 巡检模式完整示例

**用途**:
- 新用户快速上手
- 参考实际配置方式
- 理解不同模式的区别

---

### 2. .env.example - 环境变量模板

**位置**: `.env.example`

**内容**:
- 所有可配置的环境变量
- 详细的注释说明
- 使用示例

**使用方法**:
```bash
# 复制模板
cp .env.example .env

# 编辑配置
vim .env

# 加载配置
source .env
```

---

### 3. scripts/setup.sh - 自动配置脚本

**位置**: `scripts/setup.sh`

**功能**:
- ✅ 自动检查依赖（Codex CLI、OpenClaw）
- ✅ 交互式配置向导
- ✅ 自动生成 .env 文件
- ✅ 自动配置 Codex notify hook
- ✅ （Cron 模式）自动创建 Cron Job 配置

**使用方式**:
```bash
# 简单模式
./scripts/setup.sh simple

# Cron 巡检模式
./scripts/setup.sh cron
```

**输出**:
- `.env` 文件
- `~/.codex/config.toml`（更新 notify 配置）
- `cron/codex-task-waker.json`（仅 Cron 模式）

---

## 📊 对比：增强前 vs 增强后

| 功能 | 增强前 | 增强后 |
|------|--------|--------|
| **配置方式** | ❌ 手动编辑文档 | ✅ 自动配置脚本 |
| **示例代码** | ❌ 无 | ✅ 2 个完整示例 |
| **环境变量** | ❌ 分散在文档中 | ✅ 统一 .env.example |
| **上手难度** | ⚠️ 需要阅读大量文档 | ✅ 一条命令完成 |
| **适用场景** | ⚠️ 通用但模糊 | ✅ 明确区分 simple/cron |

---

## 🚀 推荐工作流

### 新用户（首次使用）

```bash
# 1. 进入 skill 目录
cd /root/.openclaw/skills/codex-agent

# 2. 运行自动配置
./scripts/setup.sh simple

# 3. 加载配置
source .env

# 4. 执行第一个任务
codex exec --full-auto "say hello"
```

### 进阶用户（Cron 模式）

```bash
# 1. 进入项目目录
cd /path/to/my-project

# 2. 运行 Cron 模式配置
/root/.openclaw/skills/codex-agent/scripts/setup.sh cron

# 3. 加载配置
source .env

# 4. 添加 Cron Job
openclaw cron add /root/.openclaw/skills/codex-agent/cron/codex-task-waker.json

# 5. 执行任务
codex exec --full-auto "实现 XX 功能"
```

---

## 📁 完整文件结构

```
codex-agent/
├── .env.example                    # ✅ 新增：环境变量模板
├── scripts/
│   └── setup.sh                    # ✅ 新增：自动配置脚本
├── examples/
│   ├── simple-task/
│   │   └── README.md               # ✅ 新增：简单示例
│   └── cron-mode/
│       └── README.md               # ✅ 新增：Cron 示例
├── docs/
│   ├── CONFIG_TEMPLATE.md          # 配置模板
│   └── ENHANCEMENTS.md             # ✅ 新增：本文档
├── hooks/
│   └── on_complete.py              # Notify hook
├── tasks/
│   └── codex-task-waker.prompt.md  # Waker Prompt
├── cron/
│   └── codex-task-waker.json       # （自动生成）Cron 配置
└── ...（其他文件）
```

---

## 🧪 测试建议

### 测试 setup.sh
```bash
# 简单模式
./scripts/setup.sh simple
cat .env  # 检查配置是否正确

# Cron 模式
./scripts/setup.sh cron
cat cron/codex-task-waker.json  # 检查 Cron 配置
```

### 测试示例
```bash
# 简单示例
cd examples/simple-task
# 按照 README.md 执行

# Cron 示例
cd examples/cron-mode
# 按照 README.md 执行
```

---

## 📝 维护说明

### 更新示例
当 skill 有重大更新时，同步更新 `examples/` 中的示例。

### 更新模板
修改 `.env.example` 后，确保 `CONFIG_TEMPLATE.md` 中的说明保持一致。

### 脚本兼容性
`setup.sh` 应该：
- 向后兼容（不破坏已有配置）
- 幂等（多次运行结果一致）
- 友好（清晰的提示和错误信息）

---

**最后更新**: 2026-03-08  
**版本**: v1.0
