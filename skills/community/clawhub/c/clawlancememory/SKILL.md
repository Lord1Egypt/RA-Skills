# 🧠 OpenClaw LanceDB Memory System

基于 LanceDB 向量数据库的智能记忆系统，为 OpenClaw Agent 提供长期记忆和语义检索能力。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![LanceDB](https://img.shields.io/badge/lancedb-0.30+-green.svg)

## ✨ 特性

- 🔍 **语义检索** - 理解意思，不只是关键词匹配
- 🧠 **自动分类** - preference/fact/task/general 四种记忆类型
- 🤖 **自动抽取** - 从对话中自动识别重要信息
- 💾 **长期存储** - 持久化存储，跨 session 使用
- ⚡ **毫秒响应** - 向量检索，快速响应
- 🔌 **即插即用** - OpenClaw Hook 集成，自动加载

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/asbinbin/claw_lance.git
cd claw_lance

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
# 获取智谱 AI API Key: https://open.bigmodel.cn/
export ZHIPU_API_KEY="your-api-key-here"
```

### 3. 启用 Hook

```bash
# 方法 1: 使用启用脚本
bash enable.sh

# 方法 2: OpenClaw 命令
openclaw hooks enable memory-system
```

### 4. 测试

```bash
# 查看用户画像
python3 skill.py profile

# 添加记忆
python3 skill.py add --content "我喜欢简洁" --type preference

# 检索记忆
python3 skill.py search --query "项目"
```

## 📚 文档

- [安装指南](docs/INSTALL.md)
- [使用手册](docs/USAGE.md)
- [API 参考](docs/API.md)
- [Hook 集成](docs/HOOK.md)
- [常见问题](docs/FAQ.md)

## 🎯 记忆类型

| 类型 | 说明 | 触发词 | 例子 |
|------|------|--------|------|
| **preference** | 偏好、习惯 | 我喜欢/我偏好/我习惯 | "我喜欢简洁的汇报风格" |
| **fact** | 事实、背景 | 我是/我负责/我擅长 | "我负责 POC 项目" |
| **task** | 任务、待办 | 我需要/别忘了/明天要 | "每周四提交 OKR 周报" |
| **general** | 其他 | - | 对话历史、临时信息 |

## 🔧 命令行使用

```bash
# 查看用户画像
python3 skill.py profile

# 检索记忆
python3 skill.py search --query "项目" --k 5

# 添加记忆
python3 skill.py add --content "我喜欢 Markdown" --type preference

# 自动抽取（从消息中识别记忆）
python3 skill.py auto --message "我负责 POC 项目，喜欢简洁的代码"

# 查看统计信息
python3 skill.py stats

# 清理过期记忆
python3 skill.py cleanup
```

## 💻 Python API

```python
from skills.memory.openclaw_integration import OpenClawMemoryIntegration

# 初始化
mem = OpenClawMemoryIntegration(user_id="ou_xxx")

# 生成 system prompt（包含记忆）
prompt = mem.get_session_system_prompt("你是小美式")

# 检索记忆
results = mem.search_memory("项目", k=5)
for r in results:
    print(f"{r['type']}: {r['content']}")

# 添加记忆
mem.add_memory("我喜欢简洁", type="preference", importance=0.8)

# 获取用户画像
profile = mem.get_user_profile()
print(f"偏好：{profile['preferences']}")
print(f"事实：{profile['facts']}")
print(f"任务：{profile['tasks']}")
```

## 🏗️ 架构

```
┌─────────────────────────────────────────┐
│          OpenClaw Agent                  │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Memory Hook (handler.js)          │ │
│  │  - 拦截 agent:bootstrap 事件         │ │
│  │  - 调用 Python 脚本                  │ │
│  │  - 注入 USER_MEMORY.md             │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│       Python 记忆模块                     │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  openclaw_integration.py           │ │
│  │  - OpenClaw 集成接口                │ │
│  │  - 生成 system prompt              │ │
│  └────────────────────────────────────┘ │
│              ↓                           │
│  ┌────────────────────────────────────┐ │
│  │  lancedb_memory.py                 │ │
│  │  - LanceDB 记忆管理                 │ │
│  │  - 向量检索                        │ │
│  └────────────────────────────────────┘ │
│              ↓                           │
│  ┌────────────────────────────────────┐ │
│  │  auto_memory.py                    │ │
│  │  - 自动记忆抽取                    │ │
│  │  - 模式匹配                        │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│        LanceDB 向量数据库                │
│        memory_lancedb/                  │
│                                          │
│  - 向量存储（智谱 AI Embedding）         │
│  - 语义检索                             │
│  - 多用户隔离                           │
└─────────────────────────────────────────┘
```

## 📊 成本

**智谱 AI Embedding**:
- 免费额度：100 万 tokens（注册就送）
- 价格：¥0.0005/1K tokens
- 记忆系统用量：~50 tokens/条
- **100 万 tokens ≈ 20,000 条记忆**

**LanceDB**:
- 本地部署，完全免费
- 内存占用：~200MB
- 磁盘占用：~100MB（每 1000 条记忆）

## 🔒 隐私与安全

- ✅ **本地存储**: 所有记忆数据存储在本地
- ✅ **API 加密**: 使用 HTTPS 调用智谱 AI API
- ✅ **多用户隔离**: 不同用户的数据完全隔离
- ✅ **无数据上传**: 记忆数据不会上传到任何服务器

## 🛠️ 开发

### 项目结构

```
claw_lance/
├── README.md                 # 项目说明
├── requirements.txt          # Python 依赖
├── enable.sh                 # 启用脚本
├── skill.py                  # 命令行入口
├── hooks/
│   └── memory-system/
│       ├── HOOK.md           # Hook 元数据
│       └── handler.js        # Hook 处理器
├── skills/
│   └── memory/
│       ├── lancedb_memory.py        # LanceDB 核心
│       ├── openclaw_integration.py  # OpenClaw 集成
│       ├── auto_memory.py           # 自动记忆抽取
│       └── session_start.py         # Session 启动脚本
├── docs/                     # 文档目录
│   ├── INSTALL.md
│   ├── USAGE.md
│   ├── API.md
│   ├── HOOK.md
│   └── FAQ.md
└── tests/                    # 测试目录
    └── test_memory.py
```

### 运行测试

```bash
# 安装测试依赖
pip install pytest

# 运行测试
pytest tests/
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2026-03-31)
- ✨ 初始版本发布
- 🔍 语义检索功能
- 🧠 自动记忆抽取
- 🔌 OpenClaw Hook 集成
- 📚 完整文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [LanceDB](https://lancedb.com/) - 向量数据库
- [智谱 AI](https://open.bigmodel.cn/) - Embedding 服务
- [OpenClaw](https://openclaw.ai/) - Agent 框架

## 📮 联系方式

- GitHub Issues: [提问](https://github.com/asbinbin/claw_lance_memory/issues)
- 项目主页：https://github.com/asbinbin/claw_lance_memory

---

**Made with ❤️ by 小美式 ☕**
