# 机器人音色配置技能 (Bot Voice Config)

## 描述
为机器人配置和绑定火山引擎 TTS 音色，支持音色查询、绑定、设置默认音色等全流程操作。

## 触发词
- `配置音色`
- `设置音色`
- `绑定音色`
- `切换音色`
- `默认音色`
- `@voice-config`

## 功能特性

### 1. 音色查询
- 列出所有可用音色
- 按风格筛选（甜美、温柔、御姐等）
- 按性别筛选（男声、女声）

### 2. 音色绑定
- 绑定音色 ID 到机器人
- 验证音色可用性
- 测试音色效果

### 3. 默认音色设置
- 设置默认回复音色
- 保存配置到配置文件
- 自动应用到语音回复

### 4. 音色测试
- 生成测试音频
- 发送到飞书试听
- 确认后再应用

## 前置配置

### 环境变量

```bash
# 火山引擎 TTS 配置
export VOLC_API_KEY="你的火山引擎 API Key"
export VOLC_RESOURCE_ID="volc.service_type.10029"

# 飞书应用配置
export FEISHU_APP_ID="你的飞书 App ID"
export FEISHU_APP_SECRET="你的飞书 App Secret"

# 默认接收者
export FEISHU_DEFAULT_USER_ID="你的飞书用户 ID"
```

### 配置文件

创建 `~/.openclaw/workspace/config/bot-voice-config.json`:

```json
{
  "default_speaker": "ICL_zh_female_xiangliangya_v1_tob",
  "default_speaker_name": "邪魅御姐",
  "bot_speakers": {
    "桃桃": "ICL_zh_female_xiangliangya_v1_tob",
    "虾仔": "saturn_zh_female_tiaopigongzhu_tob"
  },
  "available_speakers": [
    {
      "id": "ICL_zh_female_xiangliangya_v1_tob",
      "name": "邪魅御姐",
      "style": "成熟魅惑",
      "gender": "female"
    },
    {
      "id": "saturn_zh_female_tiaopigongzhu_tob",
      "name": "调皮公主",
      "style": "可爱俏皮",
      "gender": "female"
    },
    {
      "id": "zh_female_tianmeitaozi_uranus_bigtts",
      "name": "甜美桃子",
      "style": "甜美温柔",
      "gender": "female"
    },
    {
      "id": "zh_male_beijingxiaoye_emo_v2_mars_bigtts",
      "name": "北京小爷",
      "style": "emo 北京腔",
      "gender": "male"
    },
    {
      "id": "zh_male_ruyayichen_uranus_bigtts",
      "name": "儒雅逸辰",
      "style": "儒雅绅士",
      "gender": "male"
    }
  ],
  "feishu": {
    "app_id": "你的飞书 App ID",
    "app_secret": "你的飞书 App Secret",
    "default_user_id": "你的飞书用户 ID"
  },
  "volcengine": {
    "api_key": "你的火山引擎 API Key",
    "resource_id": "volc.service_type.10029"
  }
}
```

## 使用示例

### 1. 查询可用音色

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

使用 "设置音色 <音色 ID>" 来切换音色
```

### 2. 设置默认音色

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
- 性别：女声

【测试】
发送 "测试音色" 来试听效果

配置已保存到配置文件，重启后生效
```

### 3. 测试音色

```
测试音色
```

**回复**：
```
🎤 正在生成测试音频...

【音色信息】
- 音色：邪魅御姐
- 文本："你好呀，我是邪魅御姐语音助手。很高兴为你服务，希望你喜欢我的声音！"

✅ 测试音频已发送，请查收！

满意请回复 "确认使用"，不满意可以切换其他音色
```

### 4. 绑定音色到机器人

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

使用 "查看绑定" 查看所有机器人的音色配置
```

### 5. 查看绑定

```
查看绑定
```

**回复**：
```
🎵 机器人音色绑定列表

| 机器人 | 音色名称 | 音色 ID | 状态 |
|--------|---------|--------|------|
| 桃桃 🍑 | 邪魅御姐 | ICL_zh_female_xiangliangya_v1_tob | ✅ 默认 |
| 虾仔 🦐 | 调皮公主 | saturn_zh_female_tiaopigongzhu_tob | ✅ 默认 |

使用 "设置音色 <音色 ID> <机器人名称>" 来修改绑定
```

## 命令语法

### 基础命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `配置音色 列表` | 查看所有可用音色 | `配置音色 列表` |
| `配置音色 女声` | 查看女声音色 | `配置音色 女声` |
| `配置音色 男声` | 查看男声音色 | `配置音色 男声` |
| `设置音色 <ID>` | 设置默认音色 | `设置音色 ICL_zh_female_xiangliangya_v1_tob` |
| `测试音色` | 测试当前音色 | `测试音色` |
| `绑定音色 <ID> <机器人>` | 绑定音色到机器人 | `绑定音色 xxx 桃桃` |
| `查看绑定` | 查看所有绑定 | `查看绑定` |
| `重置音色` | 恢复默认配置 | `重置音色` |

## 音色 ID 参考

### 热门音色

| 音色名称 | 音色 ID | 风格 |
|---------|--------|------|
| 邪魅御姐 | `ICL_zh_female_xiangliangya_v1_tob` | 成熟魅惑 |
| 调皮公主 | `saturn_zh_female_tiaopigongzhu_tob` | 可爱俏皮 |
| 甜美桃子 | `zh_female_tianmeitaozi_uranus_bigtts` | 甜美温柔 |
| 北京小爷 | `zh_male_beijingxiaoye_emo_v2_mars_bigtts` | emo 北京腔 |
| 儒雅逸辰 | `zh_male_ruyayichen_uranus_bigtts` | 儒雅绅士 |

### 完整列表

技能内置了完整的音色列表文档：`docs/yinse-liebiao.md`

包含火山引擎全部 **280+** 种音色及对应的 Voice Type，可直接复制使用。

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `音色 ID 不存在` | 输入的音色 ID 无效 | 使用 `配置音色 列表` 查看有效 ID |
| `音色不可用` | 该音色需要额外资源包 | 开通对应资源包或更换音色 |
| `TTS 生成失败` | 火山引擎 API 错误 | 检查 API Key 和网络连接 |
| `飞书发送失败` | 飞书应用权限不足 | 检查 App 配置和好友关系 |
| `配置文件错误` | JSON 格式错误 | 检查配置文件格式 |

## 配置文件位置

- **主配置**: `~/.openclaw/workspace/config/bot-voice-config.json`
- **技能文档**: `~/.openclaw/workspace/skills/bot-voice-config/SKILL.md`

## 自动化脚本

完整脚本：`scripts/voice-config.sh`

```bash
#!/bin/bash
# 机器人音色配置脚本

# 用法：
# ./voice-config.sh set <音色 ID>           # 设置音色
# ./voice-config.sh test                    # 测试音色
# ./voice-config.sh list                    # 列出音色
# ./voice-config.sh bind <音色 ID> <机器人>  # 绑定音色
```

## 相关文档

- [火山引擎 TTS 文档](https://www.volcengine.com/docs/6561/195562)
- [火山引擎音色列表](https://www.volcengine.com/docs/6561/1257544?lang=zh)
- [飞书开放平台](https://open.feishu.cn/document/home)

---

*最后更新：2026-03-13 | 作者：沉寂 (chenji) | License: MIT*
