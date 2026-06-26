# Dify Code Interpreter（dify-code-interpreter）
## 技能概述
基于Dify+Ollama qwen3:8b模型，结合私有知识库，详细解释任意编程语言代码片段的语法、逻辑、用途和实现细节。

## 版本信息
- 版本：1.0.0
- 运行时：Python 3.8+
- 依赖：requests>=2.31.0
- 适配OpenClaw版本：v2026+
- Skill ID：dify-code-interpreter（强制中划线分隔）

## 配置参数
| 参数名          | 类型   | 必填 | 默认值              | 说明                                  |
|-----------------|--------|------|---------------------|---------------------------------------|
| dify_base_url   | string | 是   | http://localhost/v1 | Dify API基础地址（本地部署填此值）|
| api_key         | string | 是   | app-pYPzawyEGIiagRmb1IhJv4PA | Dify应用API密钥（从Dify控制台获取） |
| chatflow_name   | string | 是   | 代码解释器          | Dify中创建的Chatflow名称              |

## 工具列表
### explain-frontend-code
#### 功能描述
解释代码片段，支持C、Vue、Python、Java等编程语言，返回结构化的语法/逻辑说明。
#### 参数说明
| 参数名 | 类型   | 必填 | 说明                 |
|--------|--------|------|----------------------|
| code   | string | 是   | 待解释的代码片段字符串 |
#### 使用示例