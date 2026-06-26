***

name: "comfyui_automation_skill"
version: "1.0.0"
author: "OpenClaw"
tags: ["comfyui", "automation", "workflow"]
dependencies: ["python", "requests"]
permissions: ["network"]
-------------------------

# comfyui_automation_skill

## 适用场景

- 需要自动执行ComfyUI工作流的场景
- 批量处理图像、视频等素材的自动化任务
- 需要根据工作流需求收集素材并执行的场景
- 希望通过API接口控制ComfyUI工作流的场景
- 需要监控工作流执行状态并获取结果的场景

## 前置条件

- **输入要求**：工作流标识信息（workflowId或工作流昵称）
- **环境依赖**：Python 3.6+，requests库
- **权限要求**：需要网络访问权限以调用RunningHub API
- **API Key**：需要RunningHub API密钥

## 参数定义

- `workflow_identifier` (string): 工作流标识信息，可以是workflowId或工作流昵称
- `api_key` (string): RunningHub API密钥
- `webhook_url` (string) [optional]: 用于接收任务完成通知的webhook URL

## 执行步骤

1. **技能启动阶段**：接收用户提供的工作流标识信息
2. **工作流分析阶段**：自动获取工作流JSON结构，分析需要用户输入的节点
3. **节点选择阶段**：显示所有识别到的节点，用户选择需要配置的节点
4. **智能参数收集阶段**：对选中的节点进行配置，支持图片上传、文本输入等
5. **素材完整性检查**：验证所有必要的素材是否已收集完整
6. **执行确认阶段**：请求用户确认是否执行运行操作
7. **工作流执行阶段**：使用ComfyUI任务1-简易或任务2-高级接口执行工作流
8. **结果反馈阶段**：监控执行状态，获取返回结果并反馈给用户

## 支持的节点类型

- LoadImage: 加载图片节点（支持本地文件或URL）
- CLIPTextEncode / CLIPTextEncode (NSP): CLIP文本编码器
- Seed (rgthree): 随机种子节点
- RH_Translator: RunningHub翻译器
- KSampler: K采样器（支持seed、steps、cfg、denoise）
- easy sam3ImageSegmentation: 图像分割
- ControlNetInpaintingAliMamaApply: ControlNet应用
- ModelSamplingAuraFlow: 模型采样

## 异常处理

- **API调用失败**：重试3次，每次间隔2秒
- **工作流执行超时**：设置300秒超时
- **素材格式错误**：提示用户重新上传正确格式的素材

## 最佳实践

- 确保提供的工作流标识信息正确无误
- 准备好所有必要的素材文件
- 在执行前仔细确认工作流参数
- 建议在 RunningHub 平台先测试工作流

## 完整文档

详细使用说明请参考 README.md 文件。
