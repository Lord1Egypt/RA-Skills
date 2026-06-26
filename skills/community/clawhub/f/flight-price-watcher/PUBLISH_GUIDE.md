# 📦 发布 flight-price-watcher 到 ClawHub 指南

---

## ✅ 技能已准备就绪

**技能路径**: `~/.openclaw/skills/flight-price-watcher/`

**文件清单**:
```
flight-price-watcher/
├── SKILL.md              ✅ 主文件（包含触发词、介绍、使用示例）
├── package.json          ✅ 依赖配置
├── scripts/
│   ├── monitor.js        ✅ 价格监控主逻辑
│   ├── task_manager.js   ✅ 任务管理
│   └── init_skill.py     ✅ 初始化脚本
├── references/
│   ├── flyai-cli-docs.md ✅ FlyAI CLI 文档
│   └── pricing-strategy.md ✅ 价格策略说明
└── data/
    └── tasks.json        ✅ 任务数据存储
```

---

## 🚀 发布步骤

### 步骤 1: 安装 ClawHub CLI

```bash
sudo npm i -g clawhub
```

或

```bash
sudo pnpm add -g clawhub
```

---

### 步骤 2: 登录 ClawHub

```bash
clawhub login
```

会打开浏览器登录，登录后返回终端。

---

### 步骤 3: 发布技能

**方式 A: 发布单个技能（推荐）**

```bash
cd ~/.openclaw/skills/flight-price-watcher

clawhub publish . \
  --slug flight-price-watcher \
  --name "Flight Price Watcher - 机票价格监控" \
  --version 2.2.2 \
  --tags "机票，监控，降价提醒，飞猪，旅行" \
  --changelog "v2.2.2 完整版：
- 支持用户自定义选择监控航班
- 提醒加入完整航班信息（起飞/到达/机场）
- 展示所有监控航班价格（即使未触发阈值）
- 智能推荐标识（早班/晚班/低价/短时）
- 多航班降价聚合提醒
- 购票链接直达
- 自动检测 FlyAI CLI 安装状态
- 友好的安装引导"
```

**方式 B: 使用 sync 批量发布**

```bash
cd ~/.openclaw/skills
clawhub sync --all --bump patch
```

---

### 步骤 4: 验证发布

访问 [clawhub.ai](https://clawhub.ai) 搜索 "flight-price-watcher" 或 "机票监控" 查看你的技能。

---

## 📋 技能元数据建议

### Slug（技能标识）
```
flight-price-watcher
```

### 显示名称
```
Flight Price Watcher - 机票价格监控
```

### 版本
```
2.2.2
```

### 标签
```
机票，监控，降价提醒，飞猪，旅行，价格跟踪，自动提醒
```

### 简介
```
帮你持续跟踪机票价格，降价了立刻通知！支持多航班监控、智能降价提醒、购票链接直达。一句话创建："监控北京到上海 4 月 15 日的机票"
```

---

## 🎯 安装测试

发布后，测试安装：

```bash
# 新建一个测试目录
mkdir ~/test-clawhub && cd ~/test-clawhub

# 安装技能
clawhub install flight-price-watcher

# 验证安装
ls -la skills/flight-price-watcher/
```

---

## 💡 注意事项

1. **GitHub 账号** - 需要至少 7 天以上的 GitHub 账号才能发布
2. **版本号** - 首次发布用 `1.0.0` 或 `2.2.2`，后续更新递增
3. **公开可见** - ClawHub 上所有技能都是公开的，任何人都可以查看和安装
4. **不可删除** - 发布后无法彻底删除，只能隐藏或标记为废弃

---

## 🦈 需要我帮你做什么？

**我可以帮你**：
1. ✅ 生成完整的发布命令（上面已提供）
2. ✅ 优化技能元数据（slug、名称、标签等）
3. ✅ 创建 README.md 放到技能根目录
4. ❌ 直接执行发布（需要你的 ClawHub 账号登录）

**你需要自己做的**：
- 安装 clawhub CLI
- 登录你的账号
- 执行发布命令

---

## 📝 如果需要我生成 README.md

告诉我，我可以帮你创建一个漂亮的 README.md 放在技能根目录，包含：
- 功能介绍
- 安装方法
- 使用示例
- 截图说明（可选）

---

_最后更新：2026-04-02 | 版本：2.2.2_
