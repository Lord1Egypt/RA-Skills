# 飞书语音回复技能

使用火山引擎 TTS 生成特色音色语音，通过飞书 API 发送语音消息的完整流程技能。

## 📁 文件结构

```
feishu-voice-reply-clean/
├── SKILL.md                      # 技能说明
├── README.md                     # 本文件
├── package.json                  # 包配置
├── scripts/
│   └── feishu-voice-reply.sh     # 自动化脚本
└── config/
    └── feishu-voice-config.json  # 配置模板
```

## 🚀 快速开始

### 1. 配置环境变量

```bash
# 编辑 ~/.openclaw/.env 文件
nano ~/.openclaw/.env

# 添加以下内容（替换为你的实际配置）
export VOLC_API_KEY="你的火山引擎 API Key"
export VOLC_RESOURCE_ID="volc.service_type.10029"
export FEISHU_APP_ID="你的飞书 App ID"
export FEISHU_APP_SECRET="你的飞书 App Secret"
export FEISHU_DEFAULT_USER_ID="你的 Open ID（可选）"

# 使配置生效
source ~/.openclaw/.env
```

### 2. 测试技能

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/feishu-voice-reply-clean

# 运行测试
bash scripts/feishu-voice-reply.sh "你好呀，这是测试语音"
```

### 3. 使用技能

```bash
# 基本用法
bash scripts/feishu-voice-reply.sh "你好呀，这是测试语音"

# 指定音色
bash scripts/feishu-voice-reply.sh "你好" "ICL_zh_female_tiaopigongzhu_tob"

# 指定音色和接收者
bash scripts/feishu-voice-reply.sh "你好" "ICL_zh_female_tiaopigongzhu_tob" "ou_xxxxxx"
```

## 🎵 可用音色

### 已测试音色

| 音色 ID | 名称 | 风格 | 性别 |
|--------|------|------|------|
| `ICL_zh_female_tiaopigongzhu_tob` | 调皮公主 | 活泼可爱 | 女 |
| `zh_male_beijingxiaoye_emo_v2_mars_bigtts` | 北京小爷 | emo 北京腔 | 男 |

### 更多音色

访问 [火山引擎音色列表](https://www.volcengine.com/docs/6561/1257544?lang=zh) 查看完整列表。

## 🔧 配置说明

### 必需配置

| 配置项 | 环境变量 | 获取方式 |
|--------|----------|----------|
| 火山引擎 API Key | `VOLC_API_KEY` | 火山引擎控制台 |
| 火山引擎资源 ID | `VOLC_RESOURCE_ID` | 火山引擎控制台 |
| 飞书 App ID | `FEISHU_APP_ID` | 飞书开放平台 |
| 飞书 App Secret | `FEISHU_APP_SECRET` | 飞书开放平台 |

### 可选配置

| 配置项 | 环境变量 | 默认值 |
|--------|----------|--------|
| 默认接收者 | `FEISHU_DEFAULT_USER_ID` | 当前会话用户 |

## ⚠️ 错误处理

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `resource ID is mismatched` | 音色不在资源包中 | 更换可用音色 |
| `99991661` | 缺少 access token | 检查飞书应用配置 |
| `ffmpeg not found` | 未安装 ffmpeg | `sudo apt install ffmpeg` |
| `VOLC_API_KEY not set` | 未配置环境变量 | 设置环境变量 |

## 📖 使用示例

### 示例 1：发送测试语音

```bash
bash scripts/feishu-voice-reply.sh "你好，这是测试语音"
```

### 示例 2：使用不同音色

```bash
# 调皮公主（女声）
bash scripts/feishu-voice-reply.sh "你好呀" "ICL_zh_female_tiaopigongzhu_tob"

# 北京小爷（男声）
bash scripts/feishu-voice-reply.sh "你好" "zh_male_beijingxiaoye_emo_v2_mars_bigtts"
```

### 示例 3：发送给指定用户

```bash
bash scripts/feishu-voice-reply.sh "你好" "ICL_zh_female_tiaopigongzhu_tob" "ou_xxxxxx"
```

## 🔐 安全提示

- ⚠️ **不要将 API Key 和 App Secret 提交到代码仓库**
- ⚠️ **使用环境变量存储敏感信息**
- ✅ 配置模板已提供，实际配置需自行创建
- ✅ 生产环境使用独立的密钥管理

## 📚 相关文档

- [火山引擎 TTS 文档](https://www.volcengine.com/docs/6561/195562)
- [火山引擎音色列表](https://www.volcengine.com/docs/6561/1257544?lang=zh)
- [飞书开放平台](https://open.feishu.cn/document/home)
- [飞书消息类型](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

*最后更新：2026-03-13 | 作者：沉寂 (chenji)*
