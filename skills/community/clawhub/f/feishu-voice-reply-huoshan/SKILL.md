# 飞书语音回复技能 (Feishu Voice Reply)

## 描述
使用火山引擎 TTS 生成特色音色语音，通过飞书 API 发送语音消息的完整流程技能。支持 MP3 转 Opus 格式、自动上传和发送。

## 触发词
- `语音回复`
- `发送语音`
- `TTS 语音`
- `飞书语音`
- `@voice`

## 前置配置

### 1. 环境变量设置

在 `~/.openclaw/.env` 或系统环境变量中配置：

```bash
# 火山引擎 TTS 配置
export VOLC_API_KEY="你的火山引擎 API Key"
export VOLC_RESOURCE_ID="volc.service_type.10029"

# 飞书应用配置
export FEISHU_APP_ID="你的飞书 App ID"
export FEISHU_APP_SECRET="你的飞书 App Secret"

# 可选：默认接收者 Open ID
export FEISHU_DEFAULT_USER_ID="ou_xxxxxx"
```

### 2. 安装依赖

```bash
# 安装 ffmpeg（用于音频格式转换）
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

### 3. 火山引擎开通

1. 访问 https://www.volcengine.com/
2. 注册/登录账号
3. 开通语音合成服务
4. 获取 API Key
5. 创建资源包并获取 Resource ID

### 4. 飞书应用配置

1. 访问 https://open.feishu.cn/app
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 添加权限：
   - `im:resource` - 上传资源文件
   - `im:message` - 发送消息
   - `contact:user.base:readonly` - 读取用户信息
5. 发布应用

## 使用方法

### 命令行方式

```bash
# 基本用法（使用默认音色）
./scripts/feishu-voice-reply.sh "你好呀，这是测试语音"

# 指定音色
./scripts/feishu-voice-reply.sh "你好" "ICL_zh_female_tiaopigongzhu_tob"

# 指定音色和接收者
./scripts/feishu-voice-reply.sh "你好" "ICL_zh_female_tiaopigongzhu_tob" "ou_xxxxxx"
```

### OpenClaw 方式

```
语音回复 "你好呀，我是语音助手"
```

## 可用音色

### 当前资源包可用音色

| 音色 ID | 名称 | 风格 | 性别 |
|--------|------|------|------|
| `ICL_zh_female_tiaopigongzhu_tob` | 调皮公主 | 活泼可爱 | 女 |
| `zh_male_beijingxiaoye_emo_v2_mars_bigtts` | 北京小爷 | emo 北京腔 | 男 |

### 更多音色

**完整音色列表**: [火山引擎音色列表](https://www.volcengine.com/docs/6561/1257544?lang=zh)

#### 女声音色（部分）
- 弯弯笑 `zh_female_wanwanxiao_mars_bigtts` - 甜美
- 晶晶 `zh_female_jingjing_mars_bigtts` - 清新
- 轻婉 `zh_female_qingwan_mars_bigtts` - 温柔
- 新晴 `zh_female_xinqing_mars_bigtts` - 阳光
- 甜美 `zh_female_tianmei_mars_bigtts` - 甜美

#### 男声音色（部分）
- 北京小爷 `zh_male_beijingxiaoye_mars_bigtts` - 北京腔
- 爽快 `zh_male_shuangkuai_mars_bigtts` - 爽朗
- 青春 `zh_male_qingchun_mars_bigtts` - 青春

> **注意**: 以上音色需要开通对应的资源包才能使用。

## 执行流程

```
用户输入文本
    ↓
1. 调用火山引擎 TTS API → 生成 MP3 音频
    ↓
2. 使用 ffmpeg 转换 → Opus 格式 (32kbps)
    ↓
3. 调用飞书 API → 获取 Access Token
    ↓
4. 上传 Opus 文件 → 获取 file_key
    ↓
5. 发送语音消息 → 飞书用户
```

## 文件结构

```
feishu-voice-reply-clean/
├── SKILL.md                      # 技能说明（本文件）
├── README.md                     # 使用文档
├── package.json                  # 包配置
├── scripts/
│   └── feishu-voice-reply.sh     # 自动化脚本
└── config/
    └── feishu-voice-config.json  # 配置模板
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `resource ID is mismatched` | 音色不在资源包中 | 更换可用音色 |
| `99991661` | 缺少 access token | 检查飞书应用配置 |
| `99992402` | 缺少 receive_id_type | 已自动处理 |
| `ffmpeg not found` | 未安装 ffmpeg | 安装 ffmpeg |
| `VOLC_API_KEY not set` | 未配置环境变量 | 设置环境变量 |

## 配置文件说明

### 环境变量

| 变量名 | 说明 | 是否必需 |
|--------|------|----------|
| `VOLC_API_KEY` | 火山引擎 API Key | ✅ 必需 |
| `VOLC_RESOURCE_ID` | 火山引擎资源 ID | ✅ 必需 |
| `FEISHU_APP_ID` | 飞书应用 App ID | ✅ 必需 |
| `FEISHU_APP_SECRET` | 飞书应用 App Secret | ✅ 必需 |
| `FEISHU_DEFAULT_USER_ID` | 默认接收者 Open ID | ❌ 可选 |

### 配置模板

复制 `config/feishu-voice-config.json` 为 `config/feishu-voice-config.local.json` 并进行个性化配置。

## 安全提示

- ⚠️ **不要将 API Key 和 App Secret 提交到代码仓库**
- ⚠️ **使用环境变量存储敏感信息**
- ✅ 配置文件已加入 `.gitignore`
- ✅ 生产环境使用独立的密钥管理

## 相关文档

- [火山引擎 TTS 文档](https://www.volcengine.com/docs/6561/195562)
- [火山引擎音色列表](https://www.volcengine.com/docs/6561/1257544?lang=zh)
- [飞书开放平台](https://open.feishu.cn/document/home)
- [飞书消息类型](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)

## 更新日志

### v1.0.0 (2026-03-13)
- ✅ 初始版本发布
- ✅ 支持火山引擎 TTS 多音色
- ✅ 支持飞书语音消息发送
- ✅ 自动 MP3 转 Opus 格式
- ✅ 完整错误处理
- ✅ 详细文档

---

*最后更新：2026-03-13 | 作者：沉寂 (chenji) | License: MIT*
