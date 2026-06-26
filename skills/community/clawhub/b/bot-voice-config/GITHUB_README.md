# 机器人音色配置技能 (Bot Voice Config)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.0+-blue.svg)](https://openclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-ready-green.svg)](https://clawhub.com)

为 OpenClaw 机器人配置和绑定火山引擎 TTS 音色的完整解决方案。

## ✨ 特性

- 🎵 **音色查询** - 按性别、风格筛选可用音色
- 🔧 **音色绑定** - 为不同机器人绑定不同音色
- 🎤 **音色测试** - 生成测试音频并发送到飞书试听
- ⚙️ **配置管理** - 保存和加载音色配置
- 📱 **飞书集成** - 直接发送语音消息到飞书

## 🚀 快速开始

### 安装

```bash
# 克隆或下载技能到 OpenClaw 技能目录
git clone https://github.com/chenji/openclaw-skills.git
cd openclaw-skills/bot-voice-config-clean

# 复制配置模板
cp config/bot-voice-config.json.template \
   ~/.openclaw/workspace/config/bot-voice-config.json

# 编辑配置
nano ~/.openclaw/workspace/config/bot-voice-config.json

# 设置环境变量
export VOLC_API_KEY="你的火山引擎 API Key"
export VOLC_RESOURCE_ID="volc.service_type.10029"
export FEISHU_APP_ID="你的飞书 App ID"
export FEISHU_APP_SECRET="你的飞书 App Secret"
export FEISHU_DEFAULT_USER_ID="你的飞书用户 ID"

# 设置脚本权限
chmod +x scripts/voice-config.sh
```

### 使用

```bash
# 查看可用音色
./scripts/voice-config.sh list

# 设置默认音色
./scripts/voice-config.sh set ICL_zh_female_xiangliangya_v1_tob

# 测试音色
./scripts/voice-config.sh test

# 绑定音色到机器人
./scripts/voice-config.sh bind ICL_zh_female_xiangliangya_v1_tob 桃桃

# 查看当前配置
./scripts/voice-config.sh status
```

### 在 OpenClaw 中使用

```
配置音色 列表
设置音色 ICL_zh_female_xiangliangya_v1_tob
测试音色
绑定音色 ICL_zh_female_xiangliangya_v1_tob 桃桃
```

## 🎵 热门音色

| 音色名称 | 音色 ID | 风格 |
|---------|--------|------|
| 邪魅御姐 | `ICL_zh_female_xiangliangya_v1_tob` | 成熟魅惑 |
| 调皮公主 | `saturn_zh_female_tiaopigongzhu_tob` | 可爱俏皮 |
| 甜美桃子 | `zh_female_tianmeitaozi_uranus_bigtts` | 甜美温柔 |
| 北京小爷 | `zh_male_beijingxiaoye_emo_v2_mars_bigtts` | emo 北京腔 |
| 儒雅逸辰 | `zh_male_ruyayichen_uranus_bigtts` | 儒雅绅士 |

完整音色列表参考 [火山引擎官方文档](https://www.volcengine.com/docs/6561/1257544?lang=zh)。

## 📁 文件结构

```
bot-voice-config-clean/
├── SKILL.md                          # 技能说明
├── README.md                         # 本文件
├── package.json                      # 包配置
├── .gitignore                        # Git 忽略文件
├── scripts/
│   └── voice-config.sh               # 配置脚本
└── config/
    └── bot-voice-config.json.template # 配置模板
```

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `VOLC_API_KEY` | 火山引擎 API Key | ✅ |
| `VOLC_RESOURCE_ID` | 火山引擎资源 ID | ✅ |
| `FEISHU_APP_ID` | 飞书应用 App ID | ✅ |
| `FEISHU_APP_SECRET` | 飞书应用 App Secret | ✅ |
| `FEISHU_DEFAULT_USER_ID` | 默认接收者 ID | ❌ |

### 配置文件

位置：`~/.openclaw/workspace/config/bot-voice-config.json`

```json
{
  "default_speaker": "ICL_zh_female_xiangliangya_v1_tob",
  "bot_speakers": {
    "桃桃": "ICL_zh_female_xiangliangya_v1_tob"
  },
  "feishu": {
    "app_id": "cli_xxxxxx",
    "app_secret": "xxxxxxxx",
    "default_user_id": "ou_xxxxxx"
  },
  "volcengine": {
    "api_key": "xxxxxxxx",
    "resource_id": "volc.service_type.10029"
  }
}
```

## ⚠️ 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `VOLC_API_KEY 未设置` | 环境变量缺失 | 设置环境变量 |
| `音色 ID 不存在` | 输入的音色 ID 无效 | 使用 `list` 命令查看 |
| `TTS 生成失败` | API 错误 | 检查 API Key 和网络 |
| `飞书发送失败` | 权限不足 | 检查 App 配置 |

## 📖 相关文档

- [火山引擎 TTS 文档](https://www.volcengine.com/docs/6561/195562)
- [火山引擎音色列表](https://www.volcengine.com/docs/6561/1257544?lang=zh)
- [飞书开放平台](https://open.feishu.cn/document/home)
- [OpenClaw 文档](https://docs.openclaw.ai)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

- **沉寂 (chenji)**
- GitHub: [@chenji](https://github.com/chenji)

## 🔗 相关技能

### 推荐搭配使用

- **[feishu-voice-reply](https://github.com/chenji/feishu-voice-reply)** - 飞书语音回复技能
  - 使用火山引擎 TTS 生成特色音色语音
  - 通过飞书 API 发送语音消息
  - 支持 MP3 转 Opus 格式、自动上传和发送
  - **本技能与飞书语音回复技能配合使用效果更佳！**

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - AI 助手框架
- [火山引擎](https://www.volcengine.com/) - TTS 服务
- [飞书](https://www.feishu.cn/) - 消息平台

---

**Made with ❤️ for OpenClaw Community**

**💡 提示**: 本技能专为配合 [飞书语音回复技能](https://github.com/chenji/feishu-voice-reply) 使用而设计，推荐一起安装使用！
