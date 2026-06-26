---
name: gateway-restart-protection
description: "Gateway 重启保护钩子 - 保存配置并等待用户指令"
homepage: https://docs.openclaw.ai/automation/hooks
metadata:
  { 
    "openclaw": { 
      "emoji": "🛡️", 
      "events": ["gateway:restart:before"],
      "priority": 100
    } 
  }
---

# Gateway 重启保护钩子

## 功能

在 Gateway 重启前自动保存各项配置，生成保存明细报告，等待用户指令后才能重启。

## 触发事件

- `gateway:restart:before` - Gateway 重启前

## 保护机制

1. **配置保存检查** - 检查所有重要配置
2. **自动备份** - 备份关键配置文件
3. **生成报告** - 生成保存明细报告
4. **等待指令** - 等待用户确认后才能重启
5. **禁止擅自重启** - 阻止自动重启

## 配置检查清单

| 配置项 | 路径 | 必需 | 备份 |
|--------|------|------|------|
| Embedding 配置 | openclaw.json.embedding | ✅ | ✅ |
| 钩子配置 | hooks/ | ✅ | ✅ |
| 技能配置 | skills/ | ✅ | ❌ |
| 记忆文件 | memory/ | ✅ | ✅ |
| 向量数据库 | chroma_db/ | ❌ | ✅ |

## 使用示例

1. 启用钩子：
   ```bash
   openclaw hooks enable gateway-restart-protection
   ```

2. 尝试重启 Gateway：
   ```bash
   openclaw gateway restart
   ```

3. 钩子触发：
   - 自动保存配置
   - 生成保存明细报告
   - 等待用户指令

4. 用户确认后：
   ```bash
   openclaw gateway restart --confirmed
   ```

## 注意事项

- **禁止擅自重启 Gateway** - 这是自杀行为
- **必须等待用户指令** - 用户确认后才能重启
- **备份文件保留 7 天** - 7 天后自动清理
