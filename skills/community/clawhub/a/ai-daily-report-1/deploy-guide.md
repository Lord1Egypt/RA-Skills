# AI日报Skill部署指南

## 部署架构

```
用户 → 飞书机器人 → 中间服务 → AI服务（加载Skill） → 返回日报
```

## 方案一：使用Coze平台部署（最简单）

### 1. 上传Skill到Coze
- 访问：https://www.coze.cn
- 创建Bot
- 上传 `ai-daily-report.skill` 文件
- 配置Bot说明和触发词

### 2. 连接飞书
- 在Coze平台配置飞书机器人
- 获取Webhook地址
- 在飞书开放平台配置机器人

### 3. 使用方式
- 用户在飞书群聊中@机器人："生成今天的AI日报"
- 机器人自动返回日报内容

## 方案二：自建服务部署

### 1. 技术栈
```
Python + Flask/FastAPI
飞书开放平台SDK
AI模型API（如OpenAI、Claude等）
```

### 2. 核心代码示例

#### 接收飞书消息
```python
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_feishu_message():
    # 1. 验证签名
    signature = request.headers.get('X-Lark-Signature')
    timestamp = request.headers.get('X-Lark-Request-Timestamp')
    nonce = request.headers.get('X-Lark-Request-Nonce')
    body = request.data
    
    # 2. 解析消息
    data = request.json
    message = data.get('event', {}).get('message')
    content = message.get('content')
    
    # 3. 调用AI生成日报
    daily_report = generate_ai_daily_report()
    
    # 4. 返回结果
    return jsonify({
        "msg_type": "text",
        "content": {
            "text": daily_report
        }
    })
```

#### 生成日报
```python
import os
from openai import OpenAI

def generate_ai_daily_report():
    # 加载Skill内容
    with open('ai-daily-report.skill', 'r', encoding='utf-8') as f:
        skill_content = f.read()
    
    # 调用AI模型
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": skill_content},
            {"role": "user", "content": "生成今天的AI日报"}
        ]
    )
    
    return response.choices[0].message.content
```

### 3. 部署步骤
```bash
# 安装依赖
pip install flask openai

# 设置环境变量
export OPENAI_API_KEY="your-api-key"

# 运行服务
python app.py

# 使用ngrok暴露到公网
ngrok http 5000
```

### 4. 配置飞书机器人
- 在飞书开放平台设置消息接收地址：`https://your-domain.com/webhook`
- 配置权限：接收消息、发送消息
- 发布应用

## 方案三：使用Serverless部署

### 1. 使用腾讯云函数/阿里云函数
```python
# 云函数入口
def main_handler(event, context):
    # 解析飞书消息
    # 调用AI生成日报
    # 返回结果
    pass
```

### 2. 优势
- 无需维护服务器
- 按调用次数计费
- 自动扩缩容

## 方案四：使用现成的Bot框架

### 1. 使用LangChain Bot
```python
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI

# 加载Skill作为工具
# 配置飞书机器人
# 自动处理消息
```

### 2. 使用Dify平台
- 访问：https://dify.ai
- 创建应用
- 上传Skill文件
- 配置飞书集成

## 推荐方案

### 个人使用：方案一（Coze平台）
- 最简单快速
- 无需编程
- 免费使用

### 企业使用：方案二（自建服务）
- 完全控制
- 可定制化
- 数据安全

### 快速验证：方案三（Serverless）
- 低成本
- 快速上线
- 易于维护

## 费用估算

### Coze平台
- 免费版：每天100次调用
- 专业版：99元/月，10000次调用

### 自建服务
- 服务器：100-300元/月
- AI API：按使用量计费（GPT-4约0.03元/次）
- 总计：200-500元/月

### Serverless
- 云函数：免费额度足够
- AI API：按使用量计费
- 总计：< 100元/月

## 下一步建议

1. **快速验证**：先使用Coze平台上传Skill，测试效果
2. **收集反馈**：让用户试用，收集改进建议
3. **优化迭代**：根据反馈优化Skill内容
4. **正式部署**：选择合适的方案正式上线

## 联系支持

如有问题，可以：
- 查看飞书开放平台文档：https://open.feishu.cn/document
- 查看Coze平台文档：https://www.coze.cn/docs
- 加入技术社区寻求帮助
