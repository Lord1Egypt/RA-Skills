# 配置指南

首次安装必须配置的内容。

## 1. 安装

将整个文件夹复制到 OpenClaw 的 skills 目录。

## 2. 配置

### 2.1 创建配置文件

```bash
cd english-speaking-practice
cp config.example.json config.json
```

### 2.2 配置项说明

| 配置项 | 必填 | 说明 |
|--------|------|------|
| `user.name` | ✅ | 你的名字，用于学习记录 |
| `user.learningGoal` | - | 学习目标（可选） |
| `data.baseDir` | - | 数据存储目录，默认 `./practice-data` |
| `api.url` | ✅ | AI API 地址，用于生成推送内容 |
| `api.apiKey` | ✅ | AI API 密钥 |
| `api.model` | ✅ | AI 模型名称 |
| `api.provider` | - | API 提供商，默认 `custom` |
| `push.enabled` | - | 是否启用定时推送（默认 false） |
| `push.channel` | 推送时必填 | 推送渠道：`feishu` / `openclaw-weixin` |
| `push.targetUserId` | 推送时必填 | 目标用户 ID |

#### 详细说明

**api 配置（必填）**

```json
"api": {
  "url": "https://your-api.com/v1/chat/completions",
  "apiKey": "your-api-key",
  "model": "glm-5"
}
```

- `url`：AI 服务的 OpenAI 兼容接口地址
- `apiKey`：API 密钥
- `model`：使用的模型名称（如 `glm-5`、`gpt-4` 等）

**push 配置（可选，启用推送时必填）**

```json
"push": {
  "enabled": true,
  "channel": "feishu",
  "targetUserId": "ou_xxxxxxxx"
}
```

- `enabled`：`true` 启用定时推送，`false` 禁用
- `channel`：IM 渠道名称，需与 OpenClaw 支持的渠道一致
- `targetUserId`：目标用户的 ID
  - 飞书格式：`ou_xxxxxx`
  - 微信格式：`xxx@im.wechat`

## 3. 定时任务（可选）

启用推送后，配置 cron 定时任务：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天 10:00 执行）
0 10 * * * cd /path/to/english-speaking-practice && python3 scripts/daily-english-push.py >> /tmp/english-push.log 2>&1
```

## 4. 配置验证

### 验证配置文件格式

```bash
python3 -c "import json; json.load(open('config.json'))" && echo "配置格式正确"
```

### 验证推送脚本

如果启用了推送，可以手动测试：

```bash
python3 scripts/daily-english-push.py
```

## 5. 目录结构

```
english-speaking-practice/
├── SKILL.md                    # 技能说明
├── CONFIG.md                   # 本文件
├── config.example.json         # 配置模板
├── config.json                 # 运行时配置（需手动创建）
├── practice-data/              # 学习数据
└── scripts/
    ├── update-english-data.py  # 数据更新
    ├── daily-english-push.py   # 每日推送
    └── monthly-english-summary.sh  # 月度总结
```