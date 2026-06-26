本节将说明如何基于多轮历史对话，使用大语言模型进行回答生成
# 概述
chat_completions 用于向大模型发起一次对话请求，与新升级的search_knowledge 联通，可以完成标准的检索生成链路。
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| model | -- | str | 是 | Doubao-1-5-pro-32k | **想要用于在线生成的大模型** <br>  <br> * 当指定为 doubao 系列模型时默认使用系统的公共推理接入点，适合调试场景，有 tpm 限流 <br> * 或指定为在方舟上创建的推理接入点 ID，适合生产场景，tpm 配置可在创建推理接入点时自行调整 <br>  <br> 公共推理接入点模型可选范围见[对话模型](/c8p1dfoq/k0rwwzxq)和[图像理解模型](/c8p1dfoq/k0rwwzxq)。 <br> 私有推理接入点 ID 形如： <br> *ep-202406040*****-***** <br> 注意当使用私有接入点时，需要配合传入 API key 进行鉴权 <br> > 注：默认值可能随版本更新而变化。为确保产品效果稳定，建议用户指定模型版本 |
| model_version | -- | Optional[str] | 否 | -- | 对话模型和图像理解模型的可选范围见[对话模型](/c8p1dfoq/k0rwwzxq)和[图像理解模型](/c8p1dfoq/k0rwwzxq)。 |
| thinking | -- | Optional[Dict[str, Any]] | 否 | enabled | **控制模型是否开启深度思考模式** <br> 取值范围： <br>  <br> * enabled：开启思考模式，模型一定先思考后回答。 <br> * disabled：关闭思考模式，模型直接回答问题，不会进行思考。 <br> * auto：自动思考模式，模型根据问题自主判断是否需要思考，简单题目直接回答。 <br>  <br> 当前支持的模型详情见：[thinking](https://www.volcengine.com/docs/82379/1449737#%E5%85%B3%E9%97%AD%E6%B7%B1%E5%BA%A6%E6%80%9D%E8%80%83) <br> **示例：** <br> ```bash <br> extra_body={ <br>          "thinking": { <br>              "type": "disabled",  # 不使用深度思考能力 <br>              # "type": "enabled", # 使用深度思考能力 <br>              # "type": "auto", # 模型自行判断是否使用深度思考能力 <br>          } <br>      } <br> ``` <br>  |
| api_key | -- | Optional[str] | 否 | -- | **接入点 API Key** <br> 当需要使用私有模型接入点时，需传入对应 API key 进行鉴权 |
| messages | -- | List[ChatMessage] | 是 | -- | 发出消息的对话参与者角色，可选值包括： <br>  <br> * system：System Message 系统消息 <br> * user：User Message 用户消息 <br> * assistant：Assistant Message 对话助手消息 <br>  <br> **多轮文本问答**： 串联脚本示例可参考[知识库多轮检索问答样例](/c8p1dfoq/gxcxfxt6) <br> ```json <br> [ <br>      {"role": "system", "content": "你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内，你需要根据参考资料给出准确，简洁的回答。"}, <br>      {"role": "user", "content": "推荐一个适合 3 岁小孩的玩具"}, <br>      {"role": "assistant", "content": "您好！3 岁宝宝正处于身体、智力、情感多方面快速发展的阶段，您可以看看以下几款类型的玩具：乐高积木、拼图、消防局与消防直升机套装、医疗玩具套装、儿童滑板车"} <br>      {"role": "user", "content": "详细介绍下乐高积木有哪些合适的系列"}, <br>  ] <br> ``` <br>  <br> **多轮图文理解**：串联脚本示例可参考[知识库图文问答样例](/c8p1dfoq/xz2geoew) <br> ```plain-text <br> [ <br>      { <br>          "role": "system", <br>          "content": "你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内，你需要根据参考资料给出准确，简洁的回答。参考资料中可能会包含图片信息，图片的引用说明在<img></img>XML tags 之内，参考资料内的图片顺序与用户上传的图片顺序一致。" <br>      }, <br>      { <br>          "role": "user", <br>          "content": [ <br>              { <br>                  "type": "text", <br>                  "text": "推荐一个适合 3岁小孩的玩具" <br>              }, <br>              { <br>                  "type": "image_url", <br>                  "image_url": { <br>                      "url": "https://ark-project.tos-cn-beijing.volces.XXX.jpeg" #从知识库中召回的 top1 图片 url <br>                  } <br>              }, <br>              { <br>                  "type": "image_url", <br>                  "image_url": { <br>                      "url": "https://ark-project.tos-cn-beijing.volcess.XXX.jpeg" #从知识库中召回的 top2 图片 url <br>                  } <br>              } <br>          ] <br>      } <br>  ] <br> ``` <br>  |
| stream | -- | Optional[bool] | 否 | False | **响应内容是否流式返回** <br>  <br> * false：模型生成完所有内容后一次性返回结果 <br> * true：按 SSE 协议逐块返回模型生成内容，并以一条 data: [DONE] 消息结束 |
| max_tokens | -- | Optional[int] | 否 | 4096 | **模型可以生成的最大 token 数量** <br> > 注意 <br>  <br> > * **模型回复最大长度（单位 token），取值范围各个模型不同，详细见**[模型列表](https://www.volcengine.com/docs/82379/1330310)**。** <br> > * **输入 token 和输出 token 的总长度还受模型的上下文长度限制。** |
| return_token_usage | -- | Optional[bool] | 否 | False | **是否返回token用量统计** |
| temperature | -- | Optional[float] | 否 | 0.1 | **采样温度** <br> 控制了生成文本时对每个候选词的概率分布进行平滑的程度。取值范围为 [0, 1]。当取值为 0 时模型仅考虑对数概率最大的一个 token。 <br> 较高的值（如 0.8）会使输出更加随机，而较低的值（如 0.2）会使输出更加集中确定。通常建议仅调整 temperature 或 top_p 其中之一，不建议两者都修改。 |
## **对话模型**
| 模型名称 | 可选版本 |
| --- | --- |
| Doubao-1-5-thinking-pro | 250415 |
| Deepseek-V3-128k | 250324, 241226 |
| Deepseek-R1-128k | 250528, 250120 |
| Doubao-1-5-pro-256k | 250115 |
| Doubao-1-5-pro-32k | 250115（默认）, character-250715, character-250228 |
| Doubao-1-5-lite-32k | 250115 |
| Doubao-pro-256k | 241115, 240828 |
| Doubao-pro-32k | 241215, 240828, 240615, character-241215, character-240828, character-240528 |
| Doubao-pro-128k | 240628, 240515（即将下线） |
| Doubao-lite-32k | 240828，240628, 240428（即将下线）, character-250228, character-241015 |
| Doubao-lite-128k | 240828, 240428 |
## **图像理解模型**
| 模型名称 | 可选版本 |
| --- | --- |
| Doubao-seed-1-8 | 251228 |
| Doubao-seed-1-6-vision | 240428, 240828 |
| Doubao-seed-1-6-thinking | 250715, 250615 |
| Doubao-seed-1-6 | 251015, 250615 |
| Doubao-seed-1-6-flash | 250828, 250715, 250615 |
| Doubao-1-5-thinking-pro | m-250428, m-250415 |
| Doubao-1-5-vision-pro | 250328 |
| Doubao-1-5-vision-lite | 250315 |
| Doubao-1-5-vision-pro-32k | 250115 |
| Doubao-vision-pro-32k | 241028 |
# **响应消息**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Optional[int] | 状态码 |
| message | Optional[str] | 返回信息 |
| request_id | Optional[str] | 标识每个请求的唯一标识符 |
| data | Optional[ChatCompletionResult] | ChatCompletionResult |
### **ChatCompletionResult**
| **字段** | **类型** | **参数说明** |
| --- | --- | --- |
| reasoning_content | Optional[str] | 推理模型生成的内容 |
| generated_answer | Optional[str] | 模型生成的回答 |
| usage | Optional[Dict[str, Any]] | token 用量统计 |
| prompt | Optional[str] | prompt 内容 |
| model | Optional[str] | 模型名称 |
| finish_reason | Optional[str] | 结束原因 |
| total_tokens | Optional[int] | 总 token 数量 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 缺乏鉴权信息 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
# 请求示例
请先完成SDK初始化，再运行代码，详见[初始化SDK](/c8p1dfoq/2bmatkc9)
请将 main 函数中的 accessKey、secretKey 分别替换为您自己的 AK 和 SK。
```Python
import os
from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM
from vikingdb.knowledge.models.chat import ChatCompletionRequest, ChatMessage


def main():
    access_key = os.getenv("VIKINGDB_AK")
    secret_key = os.getenv("VIKINGDB_SK")
    endpoint = "api-knowledgebase.mlp.cn-beijing.volces.com"
    region = "cn-beijing"
    
    client = VikingKnowledge(
        host=endpoint,
        region=region,
        auth=IAM(ak=access_key, sk=secret_key),
        scheme="https"
    )
    
    # 1. Prepare messages
    messages = [
        ChatMessage(role="user", content="Hello, who are you?")
    ]
    
    # 2. Call ChatCompletion
    try:
        resp = client.chat_completion(ChatCompletionRequest(
            model="Doubao-1-5-pro-32k", # Replace with your model endpoint
            messages=messages
        ))
        print(f"Response: {resp}")
    except Exception as e:
        print(f"ChatCompletion failed, err: {e}")

    # 3. Call ChatCompletion Stream
    stream = True
    try:
        resp = client.chat_completion(ChatCompletionRequest(
            model="Doubao-1-5-pro-32k", # Replace with your model endpoint
            messages=messages,
            stream=stream
        ))
        for chunk in resp:
            print(f"Chunk: {chunk}")
    except Exception as e:
        print(f"ChatCompletionStream failed, err: {e}")

if __name__ == "__main__":
    main()
```


