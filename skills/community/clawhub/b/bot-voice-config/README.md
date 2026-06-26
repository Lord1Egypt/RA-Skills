# 机器人音色配置技能

为机器人配置和绑定火山引擎 TTS 音色，支持音色查询、绑定、设置默认音色等全流程操作。

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

## 🚀 快速开始

### 1. 安装配置

```bash
# 复制配置模板
cp config/bot-voice-config.json.template \
   ~/.openclaw/workspace/config/bot-voice-config.json

# 编辑配置（填入你的实际配置）
nano ~/.openclaw/workspace/config/bot-voice-config.json

# 设置脚本权限
chmod +x scripts/voice-config.sh
```

### 2. 设置环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export VOLC_API_KEY="你的火山引擎 API Key"
export VOLC_RESOURCE_ID="volc.service_type.10029"
export FEISHU_APP_ID="你的飞书 App ID"
export FEISHU_APP_SECRET="你的飞书 App Secret"
export FEISHU_DEFAULT_USER_ID="你的飞书用户 ID"

# 生效
source ~/.bashrc
```

### 3. 使用技能

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

## 📋 使用示例

### 在 OpenClaw 中使用

```
配置音色 列表
```

**回复**：
```
🎵 可用音色列表

【女声】
1. 邪魅御姐 - ICL_zh_female_xiangliangya_v1_tob (成熟魅惑)
2. 调皮公主 - saturn_zh_female_tiaopigongzhu_tob (可爱俏皮)
3. 甜美桃子 - zh_female_tianmeitaozi_uranus_bigtts (甜美温柔)

【男声】
1. 北京小爷 - zh_male_beijingxiaoye_emo_v2_mars_bigtts (emo 北京腔)
2. 儒雅逸辰 - zh_male_ruyayichen_uranus_bigtts (儒雅绅士)

当前默认：邪魅御姐
```

### 设置音色

```
设置音色 ICL_zh_female_xiangliangya_v1_tob
```

**回复**：
```
✅ 音色设置成功！

【配置信息】
- 音色名称：邪魅御姐
- 音色 ID：ICL_zh_female_xiangliangya_v1_tob
- 风格：成熟魅惑

配置已保存到配置文件，重启后生效
```

### 测试音色

```
测试音色
```

**回复**：
```
🎤 正在生成测试音频...

【音色信息】
- 音色：邪魅御姐
- 文本："你好呀，我是邪魅御姐语音助手..."

✅ 测试音频已发送，请查收！
```

### 绑定音色到机器人

```
绑定音色 ICL_zh_female_xiangliangya_v1_tob 桃桃
```

**回复**：
```
✅ 音色绑定成功！

【绑定信息】
- 机器人：桃桃 🍑 ✨
- 音色：邪魅御姐
- 音色 ID：ICL_zh_female_xiangliangya_v1_tob

【状态】
- ✅ 已设置为默认回复音色
- ✅ 配置已保存
```

## 🎵 热门音色

| 音色名称 | 音色 ID | 风格 | 性别 |
|---------|--------|------|------|
| 邪魅御姐 | `ICL_zh_female_xiangliangya_v1_tob` | 成熟魅惑 | 女 |
| 调皮公主 | `saturn_zh_female_tiaopigongzhu_tob` | 可爱俏皮 | 女 |
| 甜美桃子 | `zh_female_tianmeitaozi_uranus_bigtts` | 甜美温柔 | 女 |
| 北京小爷 | `zh_male_beijingxiaoye_emo_v2_mars_bigtts` | emo 北京腔 | 男 |
| 儒雅逸辰 | `zh_male_ruyayichen_uranus_bigtts` | 儒雅绅士 | 男 |

### 完整音色列表

技能内置了完整的音色列表文档：`docs/yinse-liebiao.md`

包含火山引擎全部 **280+** 种音色，按系列分类：
- Uranus BigTTS 2.0（28 种）
- Saturn BigTTS（15 种）
- Mars BigTTS 1.0（60+ 种）
- ICL ToB 定制（80+ 种）
- Moon BigTTS（20+ 种）
- Jupiter O 版本（4 种）
- 英文系列（30+ 种）
- 多语种系列（10+ 种）
- 客服场景（20+ 种）
- 有声阅读（10+ 种）

## 🔧 配置说明

### 配置文件位置

`~/.openclaw/workspace/config/bot-voice-config.json`

### 配置项说明

```json
{
  "default_speaker": "默认音色 ID",
  "default_speaker_name": "默认音色名称",
  "bot_speakers": {
    "机器人名称": "音色 ID"
  },
  "available_speakers": [
    {
      "id": "音色 ID",
      "name": "音色名称",
      "style": "风格",
      "gender": "性别"
    }
  ],
  "feishu": {
    "app_id": "飞书 App ID",
    "app_secret": "飞书 App Secret",
    "default_user_id": "默认接收者 ID"
  },
  "volcengine": {
    "api_key": "火山引擎 API Key",
    "resource_id": "火山引擎资源 ID"
  }
}
```

## ⚠️ 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `VOLC_API_KEY 未设置` | 环境变量缺失 | 设置环境变量或检查配置文件 |
| `音色 ID 不存在` | 输入的音色 ID 无效 | 使用 `list` 命令查看有效 ID |
| `TTS 生成失败` | 火山引擎 API 错误 | 检查 API Key 和网络连接 |
| `飞书发送失败` | 飞书应用权限不足 | 检查 App 配置和好友关系 |

## 📖 相关文档

- [火山引擎 TTS 文档](https://www.volcengine.com/docs/6561/195562)
- [火山引擎音色列表](https://www.volcengine.com/docs/6561/1257544?lang=zh)
- [飞书开放平台](https://open.feishu.cn/document/home)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

*最后更新：2026-03-13 | 作者：沉寂 (chenji)*
