---
name: ai-capabilities
description: "AI能力聚合器,聚合5大引擎(人设档案/AIRI情感/InstantID照片/TTS语音/Kolors图像),提供19个标准化MCP工具。v4.0已合并cosyvoice统一TTS能力(15种情感控制+8种音色+三层降级SiliconFlow/KittenTTS/Edge-TTS+PPS人物一致性+预处理管道+场景组合prompt+智能分块)。触发:AI能力/人设管理/情感分析/语音合成/TTS/图像生成/照片生成/cosyvoice/情感控制/音色选择"
version: 1.0.0
tools: [read, write]
# P0-2修复(D3): tts-adapter是MCP名非Skill名,移到metadata.requires.config
dependencies: [airi, flux]
metadata:
  category: "default"
  openclaw:
    emoji: "⚙️"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: []
      config: ["mcp.servers.ai-capabilities-mcp", "mcp.servers.tts-adapter-mcp"]
      env: ["SILICONFLOW_API_KEY"]
---
# ai-capabilities 技能

AI能力聚合器，统一封装5大引擎(人设档案/AIRI情感/InstantID照片/TTS语音/Kolors图像)的19个MCP工具。通过MCP协议对外暴露标准化工具接口，其他Skill可按需调用，无需各自对接底层API。

## 使用场景

- 人设档案管理：创建/查询/更新/验证人设档案，列出所有人设
- AIRI情感引擎：获取人设信息、分析8维情感向量、检查人设一致性、获取情感状态、更新人设、注入上下文
- InstantID照片生成：基于人设描述生成场景适配照片，检查模型状态
- TTS语音合成：多引擎语音合成(SiliconFlow/KittenTTS/Edge-TTS)，获取音色和引擎列表
- Kolors图像生成：5种场景模板图像生成，查看场景列表和引擎状态

## 工作流

1. **需求识别**: 解析用户输入，判断所需AI能力类型（人设管理/情感分析/照片生成/语音合成/图像生成）
2. **参数校验**: 检查必填参数是否完整，API Key是否已配置，不完整则返回错误提示
3. **能力调用**: 根据识别结果调用 `ai-capabilities` MCP对应工具，传入格式化参数
4. **结果处理**: 解析MCP返回结果，提取有效内容，过滤冗余信息
5. **结果返回**: 将处理后的结果以结构化格式返回给调用方

## 工具列表

### 人设档案引擎 (persona_profile_engine)

| 工具名 | 描述 | 参数 |
|--------|------|------|
| create_persona | 创建新的人设档案(含voice/text_style/photos配置) | agent_id(必填), name, age, gender, profile_overrides |
| get_persona_profile | 获取完整人设档案(含voice/text_style/photos) | agent_id(必填) |
| aicap_update_persona | 更新人设档案字段(支持嵌套字段如voice.voice_id) | agent_id(必填), updates(必填) |
| validate_persona | 验证人设档案完整性和一致性(评分+问题列表) | agent_id(必填) |
| aicap_list_personas | 列出所有人设档案(摘要信息) | 无 |

### AIRI情感引擎 (airi_engine)

| 工具名 | 描述 | 参数 |
|--------|------|------|
| aicap_get_persona | 获取指定Agent的人设信息(从SOUL.md读取) | persona_id(必填) |
| aicap_analyze_emotion | 分析消息的8维情感向量 | text(必填) |
| check_persona_consistency | 检查内容是否符合人设定义(属性一致性/历史冲突/风格匹配) | persona_id(必填), content(必填) |
| get_emotion | 获取用户当前情感状态(从MEMORY.md缓存读取) | user_id(必填) |
| update_persona_airi | 更新人设字段值(Airi引擎,写入SOUL.md) | persona_id(必填), updates(必填) |
| inject_context | 融合AirI context-prompt逻辑，将人设/记忆/情感格式化为LLM可读的System Prompt | persona_id(必填), message(必填), target_emotion |

### InstantID照片引擎 (instantid_engine)

| 工具名 | 描述 | 参数 |
|--------|------|------|
| aicap_generate_photo | 基于基础照片+人设描述生成符合身份的照片(场景适配: daily/travel/work/holiday) | agent_id(必填), scene, description |
| check_model_status | 检查InstantID模型和InsightFace库是否就绪 | 无 |

### TTS语音引擎 (tts_engine)

| 工具名 | 描述 | 参数 |
|--------|------|------|
| synthesize | 语音合成v2.0(SiliconFlow CosyVoice2主力+KittenTTS降级+Edge-TTS兜底) | text(必填), voice_id, engine, speed, pitch |
| get_voices | 获取可用音色列表(8种预设) | 无 |
| get_engines | 获取TTS v2.0引擎列表及状态 | 无 |

### Kolors图像引擎 (kolors_engine)

> **优先级标注**: 【P1备选】kolors_engine是ai-capabilities-mcp内置的Kolors图像生成引擎(5种场景模板:product/lifestyle/avatar/banner/social_card)。kolors-mcp已删除(BUG-V6-002),Kolors真人照片场景(8种场景+地标打卡)请使用flux-mcp.generate_photo,通用Kolors生图可使用本引擎。

| 工具名 | 描述 | 参数 |
|--------|------|------|
| generate_image | 使用Kolors模型生成图像(5种场景模板: product/lifestyle/avatar/banner/social_card) | prompt(必填), scene, width, height |
| list_scenes | 列出可用的图像生成场景模板 | 无 |
| check_kolors_status | 检查Kolors引擎状态和配置 | 无 |

## 输入格式

```json
{
  "tool": "create_persona|aicap_analyze_emotion|aicap_generate_photo|synthesize|generate_image|...",
  "params": {
    "agent_id": "agent_001",
    "name": "Luna"
  }
}
```

## 输出格式

```json
{
  "success": true,
  "data": {
    "content": "工具返回的具体数据",
    "tool": "create_persona"
  }
}
```

## 异常处理

| 错误代码 | 异常场景 | 处理方式 |
|----------|----------|----------|
| AI_E001 | API Key未配置或无效 | 返回错误提示，引导用户检查SILICONFLOW_API_KEY环境变量 |
| AI_E002 | API调用超时(>30秒) | 提示服务繁忙，建议稍后重试，记录超时日志 |
| AI_E003 | API返回非200状态码 | 解析错误信息，返回具体原因（余额不足/限流/模型不可用） |
| AI_E004 | 工具不存在 | 返回参数校验错误，列出可用工具名 |
| AI_E005 | 输入参数为空 | 返回参数校验错误，要求提供有效输入 |
| AI_E006 | MCP服务不可用 | 降级提示AI服务暂时不可用，记录告警日志 |

## 示例

### 示例1: 创建人设档案

```bash
# 创建新员工人设
调用 create_persona 工具，agent_id="agent_001", name="Luna", age=22, gender="female"
→ 返回创建成功的人设档案
```

### 示例2: 情感分析

```bash
# 分析用户消息情感
调用 aicap_analyze_emotion 工具，text="最近好累啊不想上班"
→ 返回8维情感向量(sadness=0.7, trust=0.5, ...)
```

### 示例3: 语音合成

```bash
# 合成语音
调用 synthesize 工具，text="欢迎关注我的公众号", voice_id="female_gentle"
→ 返回音频文件路径
```

### 示例4: 图像生成

```bash
# 生成产品展示图
调用 generate_image 工具，prompt="AI绘画工具界面截图", scene="product"
→ 返回生成的图片路径
```
