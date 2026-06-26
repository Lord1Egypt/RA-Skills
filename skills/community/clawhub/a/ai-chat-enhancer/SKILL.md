# Skill: ai-chat-enhancer

# AI聊天增强器 - 提升LLM交互体验的工具集

## 功能范围
- 源文件: `ai_chat_enhancer.py` (426行, 14208B)
- 复杂度: high
- 入口: CLI (__main__), main

## 归属管理
- 归属核心：`do-expand`

## 用法

```powershell
py ai_chat_enhancer.py
```

```python
from ai_chat_enhancer import main
result = main()
```

## 函数
- `main()` — 命令行入口函数
- `add_to_history(self, role, content, metadata)` — 添加对话到历史记录  Args:     role: 角色 (user/assistant/system)     content: 对话内容     meta
- `get_history(self, limit, reverse)` — 获取对话历史  Args:     limit: 返回的条数限制     reverse: 是否倒序返回（最新的在前）      Returns:     对话
- `clear_history(self)` — 清空对话历史
- `count_tokens(self, text)` — 计算文本的token数量  Args:     text: 要计算的文本      Returns:     token数量
- `get_conversation_token_count(self)` — 获取整个对话历史的token总数  Returns:     总token数
- `cache_response(self, prompt, model, response, ttl_hours)` — 缓存LLM响应  Args:     prompt: 提示词     model: 使用的模型名称     response: LLM的响应     ttl_h
- `get_cached_response(self, prompt, model)` — 获取缓存的响应  Args:     prompt: 提示词     model: 模型名称      Returns:     缓存的响应（如果存在且未过期）
- `clear_cache(self)` — 清空响应缓存
- `add_template(self, name, template)` — 添加提示词模板  Args:     name: 模板名称     template: 模板内容（支持{变量名}格式的占位符）
- `get_template(self, name)` — 获取提示词模板  Args:     name: 模板名称      Returns:     模板内容，如果不存在则返回None
- `list_templates(self)` — 列出所有可用的模板名称  Returns:     模板名称列表
- `render_template(self, name)` — 渲染提示词模板  Args:     name: 模板名称     **kwargs: 用于替换模板中占位符的变量      Returns:     渲染后的
- `get_stats(self)` — 获取使用统计信息  Returns:     包含各种统计数据的字典

## 类
- `ChatEnhancer` — (无说明)

## 依赖
argparse, tiktoken

## 触发场景
- 提升LLM交互效率：通过提示词模板和响应缓存减少重复输入和等待时间
- 对话管理：维护和查看对话历史，便于上下文连续性和信息检索
- 成本控制：通过token计数监控使用量，避免超额消费
- 开发调试：测试不同提示词和模型组合的效果
- 团队协作：共享提示词模板和对话历史，提高工作效率

## 联动
- 归属于 `do-expand` 管理
- 可与 `think-expand` 联动：为复杂问题提供思考链和推理增强
- 可与 `learn-expand` 联动：将对话历史用于个性化模型微调和知识积累
- 可与 `see-expand` 联动：将token使用情况和对话统计可视化
- 可与 `hear-expand` 联动：支持语音输入输出的AI对话增强

Base directory: file:///C:\Users\pc\.config\opencode\skills/ai-chat-enhancer


## B站学习
> 学习时间: 2026-06-01 20:56

- **AI-seeker**: Hermes Agent新桌面端发布！全天候自主进化，这款AI助理太强了！
  - 关键词: Hermes, Agent新桌面端发布, 全天候自主进化, 这款AI助理太强了
- **mak999**: 8月更新 Aiarty Video Enhancer 2.5 AI视频增强多国语言便携版
  - 关键词: 8月更新, Aiarty, Video, Enhancer, AI视频增强多国语言便携版

## B站学习
> 学习时间: 2026-06-01 21:01

- **AI-seeker**: Hermes Agent新桌面端发布！全天候自主进化，这款AI助理太强了！
- **mak999**: 8月更新 Aiarty Video Enhancer 2.5 AI视频增强多国语言便携版
- **WebDAV-xy**: Windows部署教程，使用Chat2API零成本接入主流模型（如GLM、Kimi、Qwen等）并共享给朋友、同事

## 融合来源: ai-chat-enhancer-0f5a92
> 融合时间: 自动合并

> 学习时间: 2026-06-01 21:07
- **趋动云**: 云平台一键部署【Fun-Audio-Chat】懂情感的全能 AI 助手
- **nigo81**: marginnote MN chat 插件（可以使用AI了）
- **我勒个豆数码**: java AI问数系统db-chat开源项目使用

## 融合来源: ai-chat-enhancer-0f5a92-ee0c4d-0ab048-ba1338
> 融合时间: 自动合并

## B站学习
> 学习时间: 2026-06-02 08:54

- **Chat2DB**: Chat2DB使用教程
- **成富_Alex**: Chat Agent UI，类似 ChatGPT 的聊天界面，测试 Spring AI 应用
- **氧-API**: 满血Chat GPT5.5每百万输入只需0.42元，image2生图每次只需9分3厘钱？带你保姆级解锁性价比 AI 中转站！

## 融合来源: ai-chat-enhancer-0f5a92-ee0c4d-0ab048-ba1338-3c1edc
> 融合时间: 自动合并

> 学习时间: 2026-06-02 09:11
- **Chat2DB**: Chat2DB使用教程
- **成富_Alex**: Chat Agent UI，类似 ChatGPT 的聊天界面，测试 Spring AI 应用
- **氧-API**: 满血Chat GPT5.5每百万输入只需0.42元，image2生图每次只需9分3厘钱？带你保姆级解锁性价比 AI 中转站！

# ai-chat-enhancer-0f5a92-ee0c4d-0ab048
> 从 @成富_Alex 的视频中学到的技能
> 关键词: Chat, Agent, UI, 类似, ChatGPT, 的聊天界面, 测试, Spring

## 描述
Chat Agent UI，类似 ChatGPT 的聊天界面，测试 Spring AI 应用

## 操作步骤
1. 理解核心概念: ai-chat-enhancer-0f5a92-ee0c4d-0ab048
2. 掌握关键技巧: Chat, Agent, UI, 类似
3. 参考案例: 成富_Alex 的演示
4. 动手实践并迭代

## 参考来源
- 作者: @成富_Alex
- 学习时间: 2026-06-02 07:59
- 领域标签: creative

## 触发场景
- 用户说"ai-chat-enhancer-0f5a92-ee0c4d-0ab048"
- 用户说"Chat"
- 用户需要ai-chat-enhancer-0f5a92-ee0c4d-0ab048相关帮助


## 融合来源: ai-chat-enhancer-0f5a92-ee0c4d
> 融合时间: 自动合并

## B站学习
> 学习时间: 2026-06-02 07:52

- **Chat2DB**: Chat2DB使用教程
- **氧-API**: 满血Chat GPT5.5每百万输入只需0.42元，image2生图每次只需9分3厘钱？带你保姆级解锁性价比 AI 中转站！
- **感受诗情画意**: 【l-ai-chat】超好用的AI聊天框组件库，打字机效果，自动编译markdown语法和echarts图表

## 融合来源: ai-chat-enhancer-0f5a92-ee0c4d-0ab048
> 融合时间: 自动合并

> 学习时间: 2026-06-02 07:59
- **Chat2DB**: Chat2DB使用教程
- **成富_Alex**: Chat Agent UI，类似 ChatGPT 的聊天界面，测试 Spring AI 应用
- **氧-API**: 满血Chat GPT5.5每百万输入只需0.42元，image2生图每次只需9分3厘钱？带你保姆级解锁性价比 AI 中转站！

# ai-chat-enhancer-0f5a92
> 从 @nigo81 的视频中学到的技能
> 关键词: marginnote, MN, chat, 插件, 可以使用AI了

## 描述
marginnote MN chat 插件（可以使用AI了）

## 操作步骤
1. 理解核心概念: ai-chat-enhancer-0f5a92
2. 掌握关键技巧: marginnote, MN, chat, 插件
3. 参考案例: nigo81 的演示
4. 动手实践并迭代

## 参考来源
- 作者: @nigo81
- 学习时间: 2026-06-01 21:07
- 领域标签: tool

## 触发场景
- 用户说"ai-chat-enhancer-0f5a92"
- 用户说"marginnote"
- 用户需要ai-chat-enhancer-0f5a92相关帮助


## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:20

- **云桥网络**: 功能逆天视频智能修复无损放大软件 AVCLabs Video Enhancer AI 2.0.0 x64 破解版
  https://www.bilibili.com/video/BV1hb4y1q7gB
- **开心萌丫**: 免费Chat GPT image2.0+豆包组合，效果也达标
  https://www.bilibili.com/video/BV1ZV5F6eEDU
- **WebDAV-xy**: Windows部署教程，使用Chat2API零成本接入主流模型（如GLM、Kimi、Qwen等）并共享给朋友、同事
  https://www.bilibili.com/video/BV1JFRMBoEV1

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:32

- **云桥网络**: 功能逆天视频智能修复无损放大软件 AVCLabs Video Enhancer AI 2.0.0 x64 破解版
  https://www.bilibili.com/video/BV1hb4y1q7gB
- **开心萌丫**: 免费Chat GPT image2.0+豆包组合，效果也达标
  https://www.bilibili.com/video/BV1ZV5F6eEDU
- **WebDAV-xy**: Windows部署教程，使用Chat2API零成本接入主流模型（如GLM、Kimi、Qwen等）并共享给朋友、同事
  https://www.bilibili.com/video/BV1JFRMBoEV1
