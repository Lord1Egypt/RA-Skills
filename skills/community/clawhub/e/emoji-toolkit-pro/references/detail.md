# 详细参考 - emoji-toolkit-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (json)

```json
{
  "emojiToolkit": {
    "batch": {
      "enabled": true,
      "parallel": 4,
      "checkpoint": true
    },
    "customCodec": {
      "enabled": true,
      "mapping": "custom-byte-map.json",
      "algorithm": "variant-selector-v2"
    },
    "encryption": {
      "enabled": true,
      "algorithm": "AES-256-GCM",
      "key_source": "env:EMOJI_ENCRYPT_KEY"
    },
    "transport": {
      "compatibility_check": true,
      "target_apps": ["telegram", "wechat", "whatsapp", "discord"]
    },
    "tokenVerify": {
      "enabled": true,
      "timeout": 5000,
      "cache_ttl": 300
    },
    "watermark": {
      "enabled": true,
      "library_path": "~/.emoji-watermarks/",
      "auto_embed": true
    }
  }
}
```

## 代码示例 (text)

```text
┌──────────────────────────────────────────────────────────────┐
│        表情符号工具箱专业版 (EMOJI TOOLKIT PRO)               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  批量编解码   │  │  自定义编码   │  │  消息加密层   │        │
│  │  Batch Codec │  │  Custom Code │  │  Encryption  │        │
│  │              │  │              │  │              │        │
│  │ 多消息并行   │  │ 自定义映射   │  │ AES加密叠加  │        │
│  │ 自动化流水线 │  │ 编码算法     │  │ 端到端安全   │        │
│  │              │  │              │  │              │        │
│  │ ✅ 专业版    │  │ ✅ 专业版    │  │ ✅ 专业版    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│          │                │                │                  │
│          └────────────────┼────────────────┘                  │
│                           ▼                                   │
│                   ┌──────────────┐                            │
│                   │  传输检测     │  ← 兼容性自动检测          │
│                   │  Transport   │    ✅ 专业版               │
│                   └──────────────┘                            │
│                           │                                   │
│                           ▼                                   │
│                   ┌──────────────┐  ┌──────────────┐          │
│                   │  代币验证     │  │  水印管理     │          │
│                   │  Token Verify│  │  Watermark   │          │
│                   │  ✅ 专业版   │  │  ✅ 专业版   │          │
│                   └──────────────┘  └──────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 完整搭建（<300秒）
配置全部高级功能：

```json
{
  "emojiToolkit": {
    "batch": {
      "enabled": true,
      "parallel": 4,
      "checkpoint": true
    },
    "customCodec": {
      "enabled": true,
      "mapping": "custom-byte-map.json",
      "algorithm": "variant-selector-v2"
    },
    "encryption": {
      "enabled": true,
      "algorithm": "AES-256-GCM",
      "key_source": "env:EMOJI_ENCRYPT_KEY"
    },
    "transport": {
      "compatibility_check": true,
      "target_apps": ["telegram", "wechat", "whatsapp", "discord"]
    },
    "tokenVerify": {
      "enabled": true,
      "timeout": 5000,
      "cache_ttl": 300
    },
    "watermark": {
      "enabled": true,
      "library_path": "~/.emoji-watermarks/",
      "auto_embed": true
    }
  }
}
```



## 架构总览
```text
┌──────────────────────────────────────────────────────────────┐
│        表情符号工具箱专业版 (EMOJI TOOLKIT PRO)               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  批量编解码   │  │  自定义编码   │  │  消息加密层   │        │
│  │  Batch Codec │  │  Custom Code │  │  Encryption  │        │
│  │              │  │              │  │              │        │
│  │ 多消息并行   │  │ 自定义映射   │  │ AES加密叠加  │        │
│  │ 自动化流水线 │  │ 编码算法     │  │ 端到端安全   │        │
│  │              │  │              │  │              │        │
│  │ ✅ 专业版    │  │ ✅ 专业版    │  │ ✅ 专业版    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│          │                │                │                  │
│          └────────────────┼────────────────┘                  │
│                           ▼                                   │
│                   ┌──────────────┐                            │
│                   │  传输检测     │  ← 兼容性自动检测          │
│                   │  Transport   │    ✅ 专业版               │
│                   └──────────────┘                            │
│                           │                                   │
│                           ▼                                   │
│                   ┌──────────────┐  ┌──────────────┐          │
│                   │  代币验证     │  │  水印管理     │          │
│                   │  Token Verify│  │  Watermark   │          │
│                   │  ✅ 专业版   │  │  ✅ 专业版   │          │
│                   └──────────────┘  └──────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```



