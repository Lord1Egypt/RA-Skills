---
name: assistant-configurator
description: 管理和优化OpenClaw配置，包括模型选择、技能管理、工具配置和系统调优。使用场景：当需要调整AI助手行为、优化性能、添加新功能、或解决配置问题时使用此技能。
---

# 智能助手配置技能

## 概述

此技能提供OpenClaw系统的完整配置管理方案，特别适合：
- 模型选择和切换
- 技能管理和优化
- 工具配置和扩展
- 系统性能调优

## 核心功能

### 1. 模型管理
**当前可用模型：**
- **MiniMax M2.1** (主要模型) - 中文优化，200K上下文
- **Claude Sonnet 4.5** (备用) - 强大推理，多模态
- **DeepSeek Chat/Reasoner** (备用) - 免费，推理能力强
- **Qwen Plus** (备用) - 阿里云，中文优秀
- **Gemini 2.5 Flash** (OpenRouter) - 快速响应

**模型切换指南：**
```javascript
// 临时切换模型
session_status({model: "deepseek/deepseek-chat"})

// 永久配置更改
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    agents: {
      defaults: {
        model: {
          primary: "deepseek/deepseek-chat",
          fallbacks: ["minimax/MiniMax-M2.1", "qwen-portal/qwen-plus"]
        }
      }
    }
  })
})
```

### 2. 技能管理
**技能目录结构：**
```
/opt/homebrew/lib/node_modules/openclaw/skills/
├── healthcheck/      # 安全检查和系统健康
├── skill-creator/    # 技能创建工具
├── weather/          # 天气查询
├── financial-data-collector/  # 金融数据收集
├── voice-interaction/         # 语音交互
└── assistant-configurator/    # 本技能
```

**技能使用原则：**
1. **精确匹配** - 选择最具体的技能
2. **渐进加载** - 只加载需要的部分
3. **定期更新** - 保持技能最新
4. **自定义扩展** - 添加个性化技能

### 3. 工具配置
**关键工具配置：**
- `web_search` - 需要Brave API密钥
- `browser` - Chrome扩展或独立浏览器
- `message` - 渠道特定配置
- `tts` - 语音引擎选择

## 工作流程

### 配置优化流程：
1. **需求分析** - 确定优化目标
2. **现状评估** - 检查当前配置
3. **方案设计** - 选择最佳配置
4. **实施测试** - 应用并测试
5. **监控调整** - 持续优化

### 问题诊断流程：
1. **症状识别** - 明确问题表现
2. **日志检查** - 查看错误信息
3. **配置验证** - 检查配置正确性
4. **工具测试** - 逐个测试工具
5. **解决方案** - 实施修复

## 工具使用指南

### 配置查看和修改：
```javascript
// 查看完整配置
gateway({action: "config.get"})

// 部分配置更新
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    channels: {
      feishu: {
        capabilities: {
          inlineButtons: "allowlist"
        }
      }
    }
  })
})

// 重启服务应用更改
gateway({action: "restart"})
```

### 模型性能测试：
```javascript
// 测试不同模型响应
async function testModels(prompt) {
  const models = [
    "minimax/MiniMax-M2.1",
    "deepseek/deepseek-chat", 
    "qwen-portal/qwen-plus",
    "anthropic/claude-sonnet-4.5"
  ]
  
  for (const model of models) {
    session_status({model: model})
    // 发送测试prompt并记录结果
  }
}
```

## 最佳实践

### 模型选择策略：
1. **中文任务** - MiniMax或Qwen优先
2. **复杂推理** - Claude Sonnet或DeepSeek Reasoner
3. **快速响应** - Gemini 2.5 Flash
4. **成本考虑** - DeepSeek免费版

### 技能管理原则：
1. **最小化加载** - 只加载必要技能
2. **定期清理** - 移除无用技能
3. **版本控制** - 记录技能版本
4. **备份配置** - 重要配置备份

### 性能优化：
1. **上下文管理** - 控制token使用
2. **缓存策略** - 减少重复计算
3. **并发控制** - 合理设置并发数
4. **错误重试** - 网络异常处理

## 常见配置场景

### 场景1：添加新消息渠道
```javascript
// 添加Telegram支持
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    channels: {
      telegram: {
        botToken: "YOUR_BOT_TOKEN",
        enabled: true
      }
    }
  })
})
```

### 场景2：配置Web搜索
```bash
# 设置Brave API密钥
openclaw configure --section web --key BRAVE_API_KEY --value "your-api-key"
```

### 场景3：优化内存使用
```javascript
// 调整上下文窗口
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    agents: {
      defaults: {
        compaction: {
          mode: "aggressive",
          maxTokens: 32000
        }
      }
    }
  })
})
```

## 故障排除

### 常见问题及解决方案：

**问题1：模型响应慢**
```
原因：网络延迟或模型负载高
解决：
1. 切换到本地模型（如DeepSeek）
2. 增加超时时间
3. 使用更轻量模型
```

**问题2：技能不触发**
```
原因：描述不匹配或技能损坏
解决：
1. 检查技能描述准确性
2. 重新安装技能
3. 查看技能日志
```

**问题3：工具调用失败**
```
原因：配置错误或权限问题
解决：
1. 检查工具配置
2. 验证API密钥
3. 检查网络连接
```

**问题4：内存使用过高**
```
原因：上下文过大或内存泄漏
解决：
1. 启用压缩模式
2. 清理历史会话
3. 重启服务
```

## 监控和维护

### 系统状态监控：
```bash
# 查看会话状态
openclaw status

# 检查服务运行
openclaw gateway status

# 查看日志
tail -f ~/.openclaw/logs/openclaw.log
```

### 定期维护任务：
1. **配置备份** - 每周备份配置文件
2. **技能更新** - 每月检查技能更新
3. **模型评估** - 每季度评估模型性能
4. **日志清理** - 每月清理旧日志

## 输出示例

### 配置报告示例：
```
📊 系统配置报告
时间：2026-02-07 02:45
状态：正常

🔧 当前配置：
- 主要模型：MiniMax M2.1
- 备用模型：DeepSeek Chat, Qwen Plus
- 活动技能：3个
- 消息渠道：飞书
- 内存使用：25%

🎯 优化建议：
1. 考虑添加Web搜索API密钥
2. 可以启用更多消息渠道
3. 建议定期备份配置
```

### 模型对比报告：
```
🤖 模型性能对比测试
测试prompt："解释量子计算的基本原理"

1. Claude Sonnet 4.5
   质量：★★★★★
   速度：★★★☆☆
   成本：高

2. DeepSeek Chat
   质量：★★★★☆
   速度：★★★★★
   成本：免费

3. MiniMax M2.1
   质量：★★★★☆
   速度：★★★★☆
   成本：中等

推荐：日常使用DeepSeek，重要任务用Claude
```

## 注意事项

1. **安全第一** - 谨慎修改核心配置
2. **备份先行** - 修改前备份原配置
3. **逐步实施** - 一次只改一个配置项
4. **测试验证** - 修改后充分测试
5. **文档记录** - 记录所有配置变更

---

**技能维护者：** 比比拉布 (BiBiLaBu)
**最后更新：** 2026-02-07
**版本：** 1.0.0