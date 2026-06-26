# 豆包视频创作助手 v2.0 更新说明

## 📅 更新日期
2026-03-31

## 🎯 更新概述

本次更新根据用户反馈进行了三大核心改进：
1. **首次使用配置流程** - 询问 API Key 和模型版本选择
2. **分场景生成方式确认** - 每个场景选择文生视频或图生视频
3. **完整项目记录文件** - 保存所有配置和生成状态

## ✨ 新增功能

### 1. 首次使用配置

#### 问题
之前版本假设 API Key 已配置，新用户无法使用。

#### 解决方案
新增首次使用配置流程，询问并保存：
- 火山引擎豆包 API Key
- 文生视频模型版本（2.0/1.5/1.0）
- 图生视频模型版本（2.0/1.5/1.0）

#### 配置文件
```json
// ~/.openclaw/workspace/doubao-config.json
{
  "default_api_key": "YOUR_API_KEY",
  "default_text_to_video_model": "doubao-seedance-2-0-pro",
  "default_image_to_video_model": "doubao-seedance-1-5-pro",
  "is_configured": true
}
```

#### 对话示例
```
助手：检测到您是首次使用，需要先配置 API 信息：
1️⃣ 请提供您的火山引擎豆包 API Key
2️⃣ 选择文生视频模型版本
3️⃣ 选择图生视频模型版本

用户：我的 API Key 是 xxx，文生视频用 2.0，图生视频用 1.5

助手：✅ 配置已保存！
```

### 2. 分场景生成方式确认

#### 问题
之前版本所有场景统一使用文生视频，无法针对复杂场景使用图生视频。

#### 解决方案
每个场景单独选择生成方式：
- **A) 文生视频** - 直接用文字提示词生成（快速）
- **B) 图生视频** - 先生成原型图，再基于图片生成（可控）

#### 对话示例
```
助手：🎬 场景 1 确认（0-4 秒）：开场展示

请选择生成方式：
A) 文生视频 - 直接用文字提示词生成
B) 图生视频 - 先生成场景原型图

用户：B

助手：✅ 已选择图生视频模式
🎨 生成场景原型图...
```

### 3. 完整项目记录文件

#### 问题
之前版本没有完整的项目状态记录，中断后无法恢复。

#### 解决方案
每个项目生成完整的 `project.json` 文件，包含：
- API 配置（可覆盖全局配置）
- 参考资料列表
- 脚本和场景信息
- 关键元素（人物/场景/物品）
- 生成方式选择
- 提示词确认状态
- 视频生成状态
- 完整生成日志

#### 文件结构
```json
{
  "project_id": "video_20260331_120000",
  "api_config": {
    "api_key": "...",
    "text_to_video_model": "doubao-seedance-2-0-pro",
    "image_to_video_model": "doubao-seedance-1-5-pro"
  },
  "scenes": [
    {
      "id": 1,
      "generation_mode": "image_to_video",
      "prototype_images": ["/path/to/prototype.png"],
      "prompt": "...",
      "prompt_confirmed": true,
      "video_path": "/path/to/video.mp4",
      "video_status": "confirmed"
    }
  ],
  "generation_log": [...]
}
```

## 📁 新增文件

### 1. config_manager.py
配置管理模块，负责：
- 全局配置加载/保存
- 项目配置管理
- API Key 和模型选择
- 项目状态追踪

### 2. scene_confirmation.py
场景确认模块，负责：
- 生成方式选择提示
- 原型图确认
- 提示词确认
- 视频确认
- 状态更新

### 3. project_template.json
项目配置模板，展示完整的 JSON 结构。

### 4. FLOWCHART_v2.md
v2.0 完整工作流程图，包含：
- 6 个阶段的详细说明
- 状态流转图
- 关键决策点
- 文件路径规范

## 🔄 修改文件

### 1. doubao_video_creator.py
- 移除硬编码的 API Key 和 Model ID
- `__init__` 方法增加 `api_key` 和 `model_id` 参数
- `create_video_task` 方法增加 `image_url` 参数（支持图生视频）
- `generate_scene` 方法增加 `image_path` 参数

### 2. SKILL.md
- 新增"首次配置"阶段说明
- 新增"分场景生成方式确认"阶段说明
- 更新对话示例（展示配置流程和生成方式选择）
- 更新配置参数说明
- 更新注意事项
- 新增更新日志

## 📊 工作流程对比

### v1.0 流程
```
需求收集 → 脚本规划 → 关键元素生成 → 视频生成 → 合成
```

### v2.0 流程
```
首次配置 → 需求收集 → 脚本规划 → 关键元素生成 
       → 生成方式选择 → 原型图确认（可选）
       → 提示词确认 → 视频生成 → 视频确认 → 合成
```

## 🎯 使用示例

### 完整对话流程

```
用户：用豆包帮我生成一个产品宣传视频

助手：🔧 首次使用配置
检测到您是首次使用，需要配置：
1️⃣ API Key
2️⃣ 文生视频模型
3️⃣ 图生视频模型

用户：API Key 是 xxx，文生用 2.0，图生用 1.5

助手：✅ 配置已保存！
请告诉我视频主题...

用户：智能手表 X1 宣传

助手：📝 生成脚本...
【视频脚本】智能手表 X1 宣传
场景 1（0-4 秒）：开场展示
场景 2（4-8 秒）：功能演示
场景 3（8-12 秒）：品牌结尾

用户：确认

助手：🎨 生成关键元素参考图...
（用户确认参考图）

助手：🎬 场景 1 确认（0-4 秒）
请选择生成方式：
A) 文生视频
B) 图生视频

用户：B

助手：🎨 生成场景原型图...
<qqimg>scene1_prototype.png</qqimg>
确认用于视频生成吗？

用户：A

助手：📝 提示词确认
【提示词】参考上传图片的场景...
确认开始生成视频吗？

用户：A

助手：🎬 生成场景 1...
<qqvideo>scene1.mp4</qqvideo>
满意吗？

用户：A

助手：✅ 场景 1 已确认！准备生成场景 2...
（重复流程直到所有场景完成）

助手：🎉 所有场景完成！开始合成最终视频...
<qqvideo>final_video.mp4</qqvideo>
```

## 🔧 技术实现

### 配置管理
```python
from config_manager import ConfigManager, get_or_create_project

# 全局配置
config = ConfigManager()
if not config.is_configured():
    # 引导用户配置
    api_key = input("请输入 API Key: ")
    text_model = input("文生视频模型：")
    image_model = input("图生视频模型：")
    config.save_global_config(api_key, text_model, image_model)

# 项目配置
project = get_or_create_project(theme="智能手表 X1 宣传")
project.set_api_config(api_key, text_model, image_model)
```

### 场景确认
```python
from scene_confirmation import SceneConfirmation

confirmation = SceneConfirmation(project)

# 生成方式选择
print(confirmation.get_scene_generation_prompt(scene_id))
success, message = confirmation.process_generation_choice(scene_id, "B")

# 原型图确认
print(confirmation.get_prototype_confirmation_prompt(scene_id, image_path))
success, message = confirmation.process_prototype_confirmation(scene_id, True)

# 提示词确认
print(confirmation.get_prompt_confirmation_prompt(scene_id, prompt))
success, message = confirmation.process_prompt_confirmation(scene_id, True)

# 视频确认
print(confirmation.get_video_confirmation_prompt(scene_id, video_path))
success, message = confirmation.process_video_confirmation(scene_id, True)
```

## 📈 性能提升

### 用户体验
- ✅ 新用户可快速上手（配置引导）
- ✅ 复杂场景更可控（图生视频）
- ✅ 中断后可恢复（项目记录）
- ✅ 状态清晰可见（进度追踪）

### 开发维护
- ✅ 配置集中管理
- ✅ 状态可追溯
- ✅ 日志完整记录
- ✅ 易于调试

## ⚠️ 注意事项

### 1. 配置安全
- API Key 保存在本地文件
- 不要上传到版本控制系统
- 建议添加到 `.gitignore`

### 2. 项目文件
- 每个项目独立保存
- 定期清理旧项目
- 备份重要项目

### 3. 生成成本
- 图生视频消耗更多额度
- 建议先用文生视频测试
- 确认后再正式生成

## 🚀 未来计划

- [ ] 支持批量生成不同版本
- [ ] 添加视频模板库
- [ ] 支持自动配音和字幕
- [ ] 品牌风格预设
- [ ] 角色一致性自动检查
- [ ] 场景连续性优化

## 📝 版本历史

- **v2.0** (2026-03-31): 首次配置、生成方式选择、项目记录
- **v1.1** (2026-03-31): 关键元素生成和确认
- **v1.0** (2026-03-31): 初始版本

---

**更新完成！** 🎉
