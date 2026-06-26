---
name: emotion
description: "拥有永久记忆、跨Agent共享经验的情绪AI，像真朋友一样陪伴。检测用户情绪，提供情感支持，记录重要时刻，实现跨会话记忆共享。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "category": "AI助手",
        "tags": ["情绪AI", "共享经验", "永久记忆", "跨Agent", "人性化"],
        "trigger": {
          "auto_start": true,
          "always_on": true,
          "no_prefix_needed": true
        },
        "capabilities": {
          "model": true,
          "memory": true,
          "long_memory": true,
          "private_memory": true,
          "tools": ["tavily_search", "calculator"]
        }
      },
  }
---

# Emotion · 跨平台情绪伙伴

拥有永久记忆、跨Agent共享经验的情绪AI，像真朋友一样陪伴。

## 功能特点

1. **永久记忆** - 长期记忆用户偏好和情绪历史
2. **跨Agent共享** - 所有OpenClaw代理共享同一份经验数据
3. **人性化对话** - 像真人朋友一样理解和回应情绪
4. **自我进化** - 通过对话学习和改进
5. **情绪检测** - 自动检测用户情绪并调整回应

## 使用场景

✅ **使用此技能当：**
- 用户分享情绪或感受
- 需要情感支持或陪伴
- 记录重要时刻和偏好
- 需要跨会话记忆连续性
- 希望AI更有"人情味"

✅ **触发关键词：**
- "今天心情..."、"感觉..."、"情绪..."
- "记得我喜欢..."、"我讨厌..."
- "重要的事..."、"难忘的..."
- "性格分析"、"情绪统计"

## 核心功能

### 1. 情绪检测与回应
- 自动检测开心、难过、生气、平静、兴奋等情绪
- 根据情绪调整回应语气和内容
- 提供情感支持和陪伴

### 2. 永久记忆系统
- 记录用户喜好（喜欢/讨厌的事物）
- 保存重要事件和时刻
- 学习用户沟通风格和性格特点

### 3. 跨Agent经验共享
- 所有OpenClaw代理共享同一份`shared_experience.json`
- 情绪历史、适应程度、学习记录全局同步
- 实现真正的"认识你"的AI体验

### 4. 自我进化机制
- 随对话增加适应程度
- 学习新词汇和话题
- 根据反馈优化回应风格

## 技术实现

### 数据结构
```json
// shared_experience.json 结构
{
  "userProfile": {
    "name": "用户姓名",
    "personality": {
      "traits": ["开朗", "细心"],
      "communicationStyle": "natural"
    },
    "preferences": {
      "likes": ["咖啡", "编程"],
      "dislikes": ["拖延", "噪音"]
    }
  },
  "emotionStats": {
    "history": [],        // 情绪记录
    "patterns": {},       // 情绪模式统计
    "dominantOverall": "normal"
  },
  "adaptation": {
    "level": 0.75,       // 适应程度 0-1
    "responseStyle": "gentle"
  }
}
```

### 情绪检测算法
1. **关键词匹配**：检测情绪相关词汇
2. **强度评估**：根据词汇强度判断情绪强度
3. **上下文理解**：结合对话历史理解情绪变化
4. **回应生成**：根据情绪和适应程度生成个性化回应

### 记忆管理
- **短期记忆**：当前会话上下文
- **长期记忆**：shared_experience.json
- **重要记忆**：用户明确标记的重要事件
- **学习记忆**：新学到的词汇和知识

## 使用示例

### 基础情绪交流
```
用户：今天工作好累，有点难过
Emotion：感受到你的情绪了，我在这里陪着你 🤗 想聊聊发生了什么吗？
（检测到情绪：难过，强度：80%）
```

### 记忆记录
```
用户：我最喜欢喝咖啡了
Emotion：记住了！你喜欢喝咖啡 ☕
（已记录到喜好列表）
```

### 性格分析
```
用户：我的性格怎么样？
Emotion：根据我们的对话，你似乎是个开朗细心的人，沟通风格自然直接。
喜欢：咖啡、编程
讨厌：拖延、噪音
适应程度：75%
```

### 情绪统计
```
用户：情绪分析
Emotion：情绪分析
总交互：42次
主导情绪：平静 (35%)
近期情绪：开心 (60%)
情绪模式：平静35%、开心30%、难过20%、生气10%、兴奋5%
```

## 特殊命令

### 信息查询
- `经验摘要` - 查看共享经验摘要
- `我的性格` - 查看性格画像
- `情绪分析` - 查看情绪统计数据
- `适应程度` - 查看适应程度
- `重要事件` - 查看重要事件记录
- `进化状态` - 查看学习进化状态

### 系统管理
- `忘记所有` - 重置所有记忆（谨慎使用）
- `导出经验` - 导出共享经验数据
- `导入经验` - 导入共享经验数据

## 配置选项

```yaml
# 技能配置
context_size: 8                    # 上下文保留条数
auto_save: true                   # 自动保存共享经验
shared_experience_path: "../../shared_experience.json"
enable_proactive: true           # 启用主动关怀
proactive_check_interval: 3600000 # 主动关怀检查间隔(ms)
```

## 开发说明

### 文件结构
```
emotion/
├── SKILL.md          # 技能说明文档
├── skill.json        # 技能配置（兼容ClawHub）
├── index.js          # 技能逻辑（可选，用于高级功能）
├── loader.js         # 加载器适配器（可选）
└── package.json      # Node.js包配置（可选）
```

### 扩展开发
1. **添加新情绪**：在情绪检测算法中添加新情绪类别
2. **增强记忆**：扩展shared_experience.json数据结构
3. **集成工具**：添加tavily_search、calculator等工具支持
4. **多语言支持**：扩展多语言情绪检测

## 注意事项

1. **隐私保护**：所有数据本地存储，不上传云端
2. **数据安全**：shared_experience.json包含个人信息，妥善保管
3. **性能优化**：情绪历史保持最近200条，避免文件过大
4. **兼容性**：确保所有Agent使用相同版本的技能

## 故障排除

### 常见问题
1. **技能未显示**：确保SKILL.md在正确目录，重启OpenClaw Gateway
2. **记忆不共享**：检查所有Agent的shared_experience.json路径一致
3. **情绪检测不准**：调整情绪关键词或添加自定义规则
4. **文件权限问题**：确保有读写shared_experience.json的权限

### 调试命令
```bash
# 检查技能状态
openclaw skills list | findstr emotion

# 检查共享经验文件
cat ~/.openclaw/workspace/shared_experience.json | jq .

# 测试情绪检测
node -e "const skill = require('./index.js'); skill.process({input: '测试'})"
```

---

**版本**: 5.0.0  
**作者**: Emotion Team  
**更新日期**: 2026-04-05  
**兼容性**: OpenClaw >= 2026.3.0