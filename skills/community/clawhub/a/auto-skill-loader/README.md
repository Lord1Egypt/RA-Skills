# Auto Skill Loader v2.0

> 即插即用 · 核心锁定 · 零配置

自动检测当前任务类型，动态加载对应的 Skill。当收到新任务时，分析任务意图，匹配最佳 Skill 并自动加载。

## 特性

- **零配置启动** - 安装即用，不需要修改任何参数
- **核心保护** - core 级 Skill 绝不被自动加载器干扰
- **通用兼容** - 不假设任何 Agent 名称、路径或环境
- **最小加载** - 只加载必要的 Skill，节省 token
- **Agent 路由** - 支持任务转发给其他 Agent

## Skill 保护等级

每个 Skill 可在 SKILL.md frontmatter 中声明 `level`：

```yaml
---
name: my-skill
level: core    # core | protected | dynamic（默认 dynamic）
---
```

| 级别 | 自动加载器行为 |
|------|---------------|
| 🔒 **core** | 完全跳过，不触碰 |
| 🛡️ **protected** | 不自动卸载，加载需显式确认 |
| 🔄 **dynamic** | 自由加载/卸载 |

## 安装

```bash
npx clawhub@latest install auto-skill-loader
```

## 使用

触发词：
- "自动加载 skill"
- "动态加载"
- "智能匹配 skill"

或直接描述任务，自动匹配最佳 Skill。

## 配置

可选配置文件 `auto-skill-loader.config.yaml`：

```yaml
# 额外标记为 core 的 Skill
coreSkills: []

# 排除不参与自动加载的 Skill
skipSkills: []

# 匹配模式: strict | normal | fuzzy
matchMode: normal

# 日志级别: silent | info | debug
logLevel: info
```

不创建配置文件 = 使用全部默认值 = 直接能用。

## 设计原则

1. **即插即用** - `clawhub install` 后直接可用
2. **零硬编码** - 不依赖特定 Agent 名、路径、端口
3. **动态发现** - 自动扫描 skills 目录
4. **合理默认** - 所有配置均有默认值

## 版本历史

- v2.0.0 - 重写核心，支持 Agent 路由，优化匹配算法
- v1.0.0 - 初始版本

## 作者

E姐 - OpenClaw 核心贡献者
