# Book Video Maker 2.0

书单爆款短视频生成器 - 精准字幕语音对齐版

## 快速开始

```bash
python scripts/generate.py -b "穷爸爸富爸爸" -a "罗伯特·清崎" -q templates/rich_dad_poor_dad.json
```

## 配置API Key

**方式1 - 创建配置文件**:
```
~/.qclaw/workspace/kdjojodsi.md
```
内容写入：
```
豆包 API Key: `你的UUID格式Key`
```

**方式2 - 环境变量**:
```bash
export ARK_API_KEY='你的API Key'
```

**获取API Key**: 访问火山引擎控制台开通豆包图片生成服务

## 参数说明

| 参数 | 说明 |
|------|------|
| `-b` | 书名（必需） |
| `-a` | 作者（必需） |
| `-q` | 金句JSON文件 |
| `-o` | 输出目录 |

## 内置模板

- `rich_dad_poor_dad.json` - 《穷爸爸富爸爸》22句

## 视频效果

- 分辨率: 1080x1920 (竖屏)
- Ken Burns特效
- 精准字幕语音对齐
- AI配图 + TTS语音

---

**版本**: 2.0.0
