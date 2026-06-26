# AI搭子 Skill - 开发与使用指南

## 快速开始

### 1. 安装依赖

```bash
cd ai-dazi-skill
npm install
```

### 2. 采集数据

```bash
# 首次采集
npm run collect

# 查看采集状态
npm run status
```

### 3. 生成画像

```bash
# 生成用户画像（可选：设置 ANTHROPIC_API_KEY 获得AI增强总结）
npm run generate

# 查看画像
npm run view
```

## 在 Claude 中使用

当此 Skill 安装到 OpenClaw 后，可以在 Claude 对话中直接使用：

- **"采集我的AI使用数据"** → 运行 token-collector collect
- **"生成我的搭子画像"** → 运行 profile-generator generate
- **"查看我的玩家等级"** → 运行 profile-generator view
- **"我的AI使用报告"** → 先采集再生成画像

## 匹配逻辑

匹配标签权重配置在 `config.json` 中：

- **玩家等级** (25%): 相近等级更易匹配
- **技能标签** (30%): 互补技能产生更好匹配
- **AI风格** (20%): 相同风格便于协作
- **活跃度** (15%): 相近活跃度确保节奏一致
- **时区重叠** (10%): 活跃时段重叠便于实时交流

## 数据隐私

- 所有数据仅存储在本地 `~/.openclaw/skills/ai-dazi-skill/data/`
- 不会自动上传任何数据
- 用户画像仅在用户主动分享时才会被传输
- API 调用仅用于生成文本总结，不传输原始行为数据
