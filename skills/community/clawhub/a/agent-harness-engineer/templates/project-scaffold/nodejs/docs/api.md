# API文档

## Agent Core API

### AgentCore

```javascript
class AgentCore {
  constructor(llmConfig)
  /**
   * 初始化Agent
   * 
   * @param {Object} llmConfig - LLM配置
   * @param {string} llmConfig.provider - 供应商 (anthropic | openai | azure | local)
   * @param {string} llmConfig.model - 模型名称
   * @param {string} llmConfig.apiKey - API密钥
   * @param {string} llmConfig.baseUrl - 自定义API端点
   * @param {number} llmConfig.maxTokens - 最大token数
   * @param {number} llmConfig.temperature - 温度参数
   */
  
  async run(userInput)
  /**
   * 运行Agent
   * 
   * @param {string} userInput - 用户输入
   * @returns {Promise<string>} - Agent响应
   */
  
  reset()
  /**
   * 重置Agent状态
   */
}
```

## LLM Client API

### LLMClient

```javascript
class LLMClient {
  constructor(config)
  /**
   * 初始化LLM客户端
   * 
   * @param {Object} config - 配置
   */
  
  async chat(messages, tools)
  /**
   * 发送聊天请求
   * 
   * @param {Array} messages - 消息列表
   * @param {Array} tools - 工具定义列表
   * @returns {Promise<LLMResponse>} - LLM响应
   */
  
  validateConfig()
  /**
   * 验证配置是否有效
   * 
   * @returns {boolean}
   */
}
```

### createLLMClient

```javascript
function createLLMClient(config)
/**
 * 根据配置创建对应的LLM客户端
 * 
 * @param {Object} config - 配置字典
 * @returns {LLMClient} - LLMClient实例
 */
```

## Tool Registry API

### ToolRegistry

```javascript
class ToolRegistry {
  register(name, description, inputSchema, handler, isConcurrencySafe)
  /**
   * 注册工具
   * 
   * @param {string} name - 工具名称
   * @param {string} description - 工具描述
   * @param {Object} inputSchema - 输入参数Schema
   * @param {Function} handler - 处理函数
   * @param {boolean} isConcurrencySafe - 是否支持并发执行
   */
  
  execute(name, inputData)
  /**
   * 执行工具
   * 
   * @param {string} name - 工具名称
   * @param {Object} inputData - 输入参数
   * @returns {any} - 工具执行结果
   */
  
  getDefinitions()
  /**
   * 获取所有工具定义
   * 
   * @returns {Array} - 工具定义列表
   */
}
```

## Permission API

### PermissionManager

```javascript
class PermissionManager {
  constructor(config)
  /**
   * 初始化权限管理器
   * 
   * @param {Object} config - 权限配置
   * @param {string} config.mode - 权限模式 (allow | deny | ask)
   * @param {Array} config.rules - 权限规则列表
   */
  
  checkPermission(toolName, toolInput)
  /**
   * 检查权限
   * 
   * @param {string} toolName - 工具名称
   * @param {Object} toolInput - 工具输入
   * @returns {boolean} - True if allowed, False if denied
   */
}
```

### SandboxManager

```javascript
class SandboxManager {
  constructor(config)
  /**
   * 初始化沙箱管理器
   * 
   * @param {Object} config - 沙箱配置
   * @param {boolean} config.enabled - 是否启用
   * @param {Array} config.allowedDirectories - 允许的目录列表
   * @param {Array} config.deniedPatterns - 拒绝的模式列表
   */
  
  validatePath(path)
  /**
   * 验证路径是否在允许范围内
   * 
   * @param {string} path - 要验证的路径
   * @returns {boolean} - True if allowed, False if denied
   */
  
  validateCommand(command)
  /**
   * 验证命令是否安全
   * 
   * @param {string} command - 要验证的命令
   * @returns {boolean} - True if allowed, False if denied
   */
}
```
