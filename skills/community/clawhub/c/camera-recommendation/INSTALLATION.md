# Camera Recommendation Skill - 安装指南

## 技能概述

这是一个相机购买推荐AI技能，帮助用户根据预算、使用场景和技术水平选择最适合的相机设备。

## 文件结构

```
camera-recommendation-skill/
├── README.md              # 技能概览
├── skill.md               # 技能详细说明
├── skill-config.json     # 技能配置主文件 (NEW)
└── INSTALLATION.md       # 本安装指南 (NEW)
```

## 安装说明

### 方法一：通过CodeBuddy/Copilot界面安装

1. **将技能文件夹放置在正确位置**：
   将整个 `camera-recommendation-skill/` 文件夹复制到以下位置之一：
   - CodeBuddy技能目录: `%APPDATA%\CodeBuddy\skills\`
   - 项目内技能目录: `项目根目录/.codebuddy/skills/`

2. **重启CodeBuddy/Copilot**：
   重启IDE以加载新技能。

3. **验证技能加载**：
   在聊天中尝试使用触发词如"推荐相机"或"camera recommendation"。

### 方法二：通过配置文件安装

1. **创建技能索引**：
   在技能目录中创建或更新技能索引文件：

   ```json
   // .codebuddy/skills/skills-index.json
   {
     "camera-recommendation": {
       "name": "相机推荐",
       "description": "个性化相机购买建议",
       "config_path": "./camera-recommendation-skill/skill-config.json",
       "enabled": true
     }
   }
   ```

2. **运行技能测试**：
   在IDE命令行或技能管理器界面中执行技能刷新。

## 配置说明

### 主要配置参数

查看 `skill-config.json` 文件中的关键配置：

1. **模型配置** (`model` 部分)：
   ```json
   "model": {
     "name": "gpt-4o-mini",
     "capabilities": ["vision", "web-search"],
     "temperature": 0.7,
     "max_tokens": 2000
   }
   ```

2. **触发词配置** (`triggers` 部分)：
   - 关键词触发：匹配聊天中的关键词
   - 短语触发：匹配完整短语
   - 支持中英文触发

3. **工作流程** (`workflow` 部分)：
   - 4个步骤：需求收集 → 预算分析 → 场景匹配 → 推荐生成
   - 每个步骤有专门的prompt

## 使用方式

### 1. 直接触发

在IDE聊天中输入以下任意内容：
- "推荐相机"
- "我想买相机，预算1万左右"
- "帮我选一台适合旅游的相机"
- "camera recommendation for portrait photography"

### 2. 调用格式

技能会按照标准格式输出推荐：
```
📷 **相机购买方案**

**📊 需求分析**
- 预算: [具体金额]
- 主要用途: [场景]
- 技术水平: [级别]
- 便携性: [要求]

**🎯 推荐方案**
[方案1详情]
[方案2详情]

**📝 购买建议**
[购买指导]
```

## 故障排除

### 常见问题

1. **技能未触发**
   - 检查技能配置文件路径
   - 确认触发词配置正确
   - 重启CodeBuddy/Copilot

2. **AGENT_INVOKABLE_CUSTOM_MODEL_NOT_FOUND 错误**
   - 确保 `model.name` 配置的是支持的模型 (如 gpt-4o-mini)
   - 检查是否有权限使用该模型
   - 可能需要联系CodeBuddy管理员配置模型访问

3. **响应不符合预期**
   - 检查skill-config.json文件格式是否有效
   - 验证workflow中的prompt是否清晰
   - 确保知识库信息是最新的

### 测试技能

运行以下命令测试技能配置：
```bash
# 检查JSON格式
python -m json.tool skill-config.json

# 测试技能触发
# 在CodeBuddy聊天中输入："测试相机推荐技能"
```

## 更新和维护

### 数据更新

1. **价格更新**：
   定期更新 `knowledge_base` 中的价格信息
   参考京东、天猫等平台官方价格

2. **产品线更新**：
   当有新相机发布时更新推荐列表
   关注Canon、Sony、Nikon、Fujifilm等品牌新品

3. **市场趋势**：
   关注市场反馈和用户评论
   更新场景推荐策略

### 技能改进

1. **添加新功能**：
   - 二手相机推荐
   - 租赁方案建议
   - 配件搭配优化

2. **扩展触发方式**：
   - 添加更多用户场景
   - 支持多语言
   - 集成到代码提示中

## 许可证

本技能使用MIT许可证开放。

---

## 联系支持

如果遇到安装或使用问题：
1. 检查本指南的故障排除部分
2. 查看CodeBuddy官方文档
3. 在项目issue中提出问题

**最后更新**: 2026-03-28