本章将详细描述如何在 RTC 的实时对话式 AI 中，使用 Viking 长期记忆 和 Viking 知识库。

## 什么是实时对话式 AI
火山引擎的实时对话式 AI场景方案，让人与 AI 的交互不再局限于文字，还能进行自然、流畅、真人感的实时语音对话，可应用于 AI 智能助手、AI 客服、AI 陪伴、AI 口语教学、AI 游戏 NPC、智能硬件等场景。
通过火山引擎 RTC 实现音视频数据的高效采集、自定义处理和超低时延传输。在云端，提供了智能音视频处理模块，包括音频 3A、AI降噪和抽帧截图等能力，以减少环境噪音和设备性能对对话式 AI 体验的影响。此外，方案搭载火山方舟大模型服务平台，深度整合语音识别（ASR）、语音合成（TTS）、大语言模型（LLM），**记忆，知识库 RAG** 等服务，简化语音到文本及文本到语音的转换过程，提供强大的智能对话、自然语言处理和多模态交互能力，助力应用快速实现用户与云端大模型之间的实时语音通话和多模态交互。
更多介绍可参考：[什么是实时对话式 AI](https://www.volcengine.com/docs/6348/1310537)
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/9642efbf73434e74bd3ee15f6efd1cdd~tplv-goo7wpa0wc-image.image)

## 接入 Viking 长期记忆
通过集成 Viking 长期记忆，可赋予智能体跨会话的长期记忆能力。在接收到用户问题后，系统会先从记忆库中检索相关的历史记忆（如用户的身份、偏好等），然后将「用户问题 +过渡语（若有）+ 检索到的记忆」拼接成一个信息更丰富的上下文，交由大语言模型处理，从而生成更个性化和精准的回复。
### 工作原理
当启用 Viking 长期记忆后，每一轮对话的处理流程会变为：

1. 用户的语音问题被 ASR 转换为文本。
2. 系统自动根据配置的 filter 规则，去 Viking 长期记忆中检索与当前用户和问题相关的历史记忆。
3. 将 `用户问题 + 过渡语 + 检索到的记忆` 拼接成一个新的、更丰富的上下文。
4. 将这个新上下文送给 LLM 进行处理，生成回复。

### 实现步骤
获取与智能体的历史对话记录。具体操作，请参见[实时字幕（对话记录）](https://www.volcengine.com/docs/6348/1337284)。
#### 步骤 1：创建并填充记忆库

1. **开通 Viking 长期记忆**

通过[注册账号及开通服务](https://www.volcengine.com/docs/84313/1254444)页面操作完成注册账号及开通服务。

2. **创建记忆库并定义规则**：在火山引擎 [Viking 长期记忆 控制台](https://console.volcengine.com/vikingdb/region:vikingdb+cn-beijing/home?projectName=default) ，创建一个**事件规则**的记忆库。具体操作，请参见[创建记忆库](https://www.volcengine.com/docs/84313/1817506)。

![Image](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_c566abda7e39e9df46a950414f922d2b.png)

3. **向记忆库中添加记忆**：具体操作，可参见[添加记忆](https://www.volcengine.com/docs/84313/1827248)。

> 成功添加记忆后，可在控制台查看记忆详情。具体操作请参见[查看记忆详情](https://www.volcengine.com/docs/84313/1827249)。

#### 步骤 2：为服务授权访问记忆库
为了让实时对话式 AI 服务能够访问你的记忆库，你需要为服务角色 `VoiceChatRoleForRTC` 添加对向量数据库（VikingDB）的访问权限。

1. 登录火山引擎[访问控制（](https://console.volcengine.com/iam/)[IAM](https://console.volcengine.com/iam/)[）控制台](https://console.volcengine.com/iam/)。
2. 在左侧导航栏中，选择 **角色管理**，搜索并找到 `VoiceChatRoleForRTC`，单击操作栏的**添加权限**。
3. 在权限策略列表中，搜索并勾选 `MLPlatformVikingDBFullAccess` 和 `VikingdbFullAccess` 两个权限。
4. 单击 **提交** 完成授权。

#### 步骤 3：配置 StartVoiceChat 接口
调用 [StartVoiceChat](https://www.volcengine.com/docs/6348/1558163) 接口时，在 `Config` 对象中配置 `MemoryConfig` 参数。`StartVoiceChat` 配置示例如下：
> 详细参数说明，请参见 [StartVoiceChat](https://www.volcengine.com/docs/6348/1558163) 。

```JSON
POST https://rtc.volcengineapi.com?Action=StartVoiceChat&Version=2024-12-01
{
    "AppId": "Your_RTC_AppId",
    "RoomId": "Your_RoomId",
    "TaskId": "Your_TaskId",
    "Config": {
    "MemoryConfig": {
        "Enable": true,
        "Provider": "volc",
        "ProviderParams": {
            "collection_name": "customer_service_memory", // 来源于步骤 1 在 Viking 长期记忆 控制台创建的记忆库名称
            "limit": 3,
            "filter": {
                "user_id": ["current_user_id"],          // user_id 和 assistant_id 至少填一个
               // "assistant_id": ["assistant_123"],     
                "memory_type": ["order_event"]          // 来源于步骤 1 在 Viking 长期记忆 的事件规则定义
            },
            "transition_words": "根据您的历史记录："
        }
    },
    // ... ASRConfig, TTSConfig, LLMConfig
  }
}
```



## 接入 Viking 知识库
### 实现步骤
#### 步骤 1：创建并验证知识库

1. **开通 Viking 知识库**

通过[注册账号及开通服务](https://www.volcengine.com/docs/84313/1254444)页面操作完成注册账号及开通服务。

2. **创建知识库并进行验证**

导入相关的知识文档，通过问答或者检索， 验证知识库功能。

#### **步骤 2：生成知识库 MCP Server 地址**
参考[【知识库】MCP Server](https://www.volcengine.com/docs/84313/1828972)，创建 MCP Server， 获取MCP Remote URL
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/71cfd95ab9a847838b25f6c082d51e9c~tplv-goo7wpa0wc-image.image)

1. 正确填写 火山 ak 和 sk 信息； 知识库的 ProjectName； region为 cn-north-1
2. 开始部署， 即在 veFaaS服务（函数计算）上部署知识库的 MCP Server
3. 获取 云部署-知识库-MCP Server 地址


#### 步骤 3：配置 StartVoiceChat 接口
调用 [StartVoiceChat](https://www.volcengine.com/docs/6348/1558163) 接口时，在 `Config` 对象中，配置 `LLMConfig` 参数。`StartVoiceChat` 配置示例如下：
> 详细参数说明，请参见 [StartVoiceChat](https://www.volcengine.com/docs/6348/1558163) 。

```JSON
{
    "AppId": "Your_RTC_AppId",
    "RoomId": "Your_RoomId",
    "TaskId": "Your_TaskId",
    "AgentConfig": {},
    "Config": {
        "WebSearchConfig": {},
        "SubtitleConfig": {},
        "ASRConfig": {},
        "TTSConfig": {},
        "LLMConfig": {
            "MCP": [
                {
                    "URL" :"https://knowledge-mcp-server.com/test/123", // 远端 MCP Server 访问地址
                    "Name" : "knowledge", // MCP Server 名称
                    "ComfortWords" : "正在处理中", // 触发MCP 调用工具时， AIGC服务播放安抚语内容
                    "InterestedTools": ["search_knowledge"] // RTC-AIGC 关注工具列表。数组为空，mcp server工具列表中的所有工具都会参考，添加到LLM上下文中；数组不为空，数组中的工具会添加到 LLM上下文中。
                }
            ],
        }
    }
}
```


### 注意事项

1. 知识库 MCP Server 提供工具列表为：
   * add_doc
   * get_doc
   * get_collection
   * list_collections
   * search_knowledge
2. RTC-AIGC 服务对话中， 只需要查询已有知识库的内容， 所以只会对 `search_knowledge` 进行调用，并且只有在`"InterestedTools"` 中配置，智能体才会触发调用。
3. LLM 没有知识库内容的先验知识， 为了准确触发知识库的查询， 所以需要在 SystemPrompts 中详细定义知识库相关内容和参数，比如：

```JSON
"UserPrompts": [
    {
        "Role" : "system",
        "Content" : "知识库中包含视频编码的相关知识，H264编码标准和技术， 可以通过search_knowledge方法查询相关内容。 search_knowledge方法有两个参数，其中query存放的是查询内容, collection_name是voicechat_knowledge"
    }
}
```

