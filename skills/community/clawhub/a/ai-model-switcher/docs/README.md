# 🎩 AI模型切换器 - 使用文档

## 概述

智能模型切换系统是一个为OpenClaw用户设计的AI模型智能切换工具。采用**方案C：日常本地模型 + 复杂任务云模型**的混合使用策略，根据任务类型自动选择最优模型，实现成本优化和性能平衡。

## 快速开始

### 安装
```bash
# 技能已包含在OpenClaw中，无需额外安装
# 确保OpenClaw版本为2026.3.13或更高
```

### 基本使用
```bash
# 查看系统状态
openclaw skill intelligent-model-switch status

# 日常对话模式（本地模型，零成本）
openclaw skill intelligent-model-switch chat

# 研究模式（推理云模型）
openclaw skill intelligent-model-switch research

# 编程模式（云模型）
openclaw skill intelligent-model-switch code
```

## 详细功能

### 1. 模型管理

#### 查看可用模型
```bash
openclaw skill intelligent-model-switch models
```

#### 强制切换模型
```bash
# 切换到本地模型
openclaw skill intelligent-model-switch force local

# 切换到DeepSeek云模型
openclaw skill intelligent-model-switch force deepseek

# 切换到推理云模型
openclaw skill intelligent-model-switch force reasoner

# 切换到Kimi云模型
openclaw skill intelligent-model-switch force kimi
```

### 2. 任务类型

系统支持以下任务类型：

| 任务类型 | 命令 | 推荐模型 | 描述 |
|---------|------|---------|------|
| 日常对话 | `chat` | 本地模型 | 日常聊天、简单问答 |
| 简单问答 | `simple` | 本地模型 | 信息查询、基础问题 |
| 研究分析 | `research` | 推理云模型 | 复杂推理、研究任务 |
| 长文档处理 | `longdoc` | Kimi云模型 | 长文本分析、多文件处理 |
| 编程开发 | `code` | DeepSeek云模型 | 代码生成、技术问题 |
| 数据分析 | `analysis` | 推理云模型 | 数据分析、统计计算 |
| 创意写作 | `creative` | DeepSeek云模型 | 创意写作、内容生成 |

### 3. 统计与监控

#### 查看使用统计
```bash
# 查看模型使用统计
openclaw skill intelligent-model-switch stats

# 查看token消耗
openclaw skill intelligent-model-switch tokens

# 查看切换历史
openclaw skill intelligent-model-switch history
```

#### 查看日志
```bash
# 查看切换日志
openclaw skill intelligent-model-switch logs
```

### 4. 配置管理

#### 查看当前配置
```bash
openclaw skill intelligent-model-switch config
```

#### 编辑配置
```bash
# 配置文件位置
notepad "C:\Users\Administrator\.openclaw\skills\intelligent-model-switch\config\config.json"
```

## 配置说明

### 模型配置
```json
{
  "local": {
    "id": "ollama:deepseek-r1:14b",
    "name": "本地模型",
    "type": "local",
    "cost": 0,
    "enabled": true
  }
}
```

- **id**: 模型ID，与OpenClaw配置一致
- **name**: 模型显示名称
- **type**: 模型类型（local/cloud）
- **cost**: 每1000个token的成本（美元）
- **enabled**: 是否启用该模型

### 任务配置
```json
{
  "chat": {
    "name": "日常对话",
    "recommendedModel": "local",
    "description": "日常聊天、简单问答"
  }
}
```

- **name**: 任务类型名称
- **recommendedModel**: 推荐使用的模型键名
- **description**: 任务描述

### 系统配置
- **costStrategy**: 成本策略（aggressive/balanced/performance）
- **autoSwitch**: 是否启用自动切换
- **logSwitches**: 是否记录切换日志

## 使用示例

### 示例1：日常工作流程
```bash
# 开始工作，查看状态
openclaw skill intelligent-model-switch status

# 处理日常对话任务
openclaw skill intelligent-model-switch chat

# 遇到编程任务时切换
openclaw skill intelligent-model-switch code

# 完成后查看统计
openclaw skill intelligent-model-switch stats
```

### 示例2：研究项目
```bash
# 开始研究模式
openclaw skill intelligent-model-switch research

# 处理长文档
openclaw skill intelligent-model-switch longdoc

# 分析数据
openclaw skill intelligent-model-switch analysis

# 查看token消耗
openclaw skill intelligent-model-switch tokens
```

### 示例3：成本优化
```bash
# 设置激进成本策略（尽可能使用本地模型）
# 编辑config.json，设置"costStrategy": "aggressive"

# 查看当前成本
openclaw skill intelligent-model-switch stats

# 禁用昂贵模型
# 编辑config.json，设置"kimi.enabled": false
```

## 故障排除

### 常见问题

#### 1. 命令无法识别
```bash
# 重新加载技能
openclaw skills reload

# 检查技能是否正确安装
openclaw skills list
```

#### 2. 模型切换失败
```bash
# 检查OpenClaw配置
openclaw config

# 验证模型ID是否正确
openclaw skill intelligent-model-switch config
```

#### 3. 本地模型不可用
```bash
# 检查Ollama服务
ollama list

# 如果未安装Ollama，编辑配置禁用本地模型
# 设置"local.enabled": false
```

### 调试模式
```bash
# 启用调试输出
openclaw skill intelligent-model-switch debug
```

## 高级功能

### 自定义任务类型
1. 编辑`config.json`文件
2. 在`tasks`部分添加新任务
3. 指定`recommendedModel`
4. 保存配置

### 自定义模型
1. 编辑`config.json`文件
2. 在`models`部分添加新模型
3. 配置模型参数
4. 保存配置

### 成本策略调整
- **aggressive**: 尽可能使用本地模型，最小化成本
- **balanced**: 平衡本地和云模型使用
- **performance**: 优先使用高性能云模型

## 性能优化

### 缓存机制
- 相同任务类型使用缓存决策
- 缓存有效期：1小时
- 可手动清除缓存

### 网络优化
- 本地模型：零网络延迟
- 云模型：自动选择最优API端点
- 支持连接重试和超时设置

### 资源监控
- 自动监控模型使用资源
- 防止过度使用云模型token
- 提供使用建议和警告

## 版本历史

### v1.0.0 (2026-03-27)
- ✅ 初始版本发布
- ✅ 智能任务识别和模型选择
- ✅ 快速命令系统
- ✅ 成本优化策略
- ✅ 使用统计和日志记录

## 支持与反馈

如有问题或建议，请：
1. 查看本文档
2. 检查配置是否正确
3. 联系技能作者
4. 在OpenClaw社区反馈

---

**智能模型切换系统** - 让AI助手使用更智能、更经济！ 🎩