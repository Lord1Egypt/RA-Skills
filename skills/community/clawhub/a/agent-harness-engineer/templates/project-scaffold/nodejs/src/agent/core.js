/**
 * ============================================
 * 类型: 核心框架
 * 模块: agent.core
 * 说明: Agent核心循环实现
 * 修改建议: 如需扩展，继承AgentCore类或注册Hook
 * ============================================

const { createLLMClient } = require('../llm/factory');
const { ToolRegistry } = require('../tools/registry');

class AgentCore {
  constructor(llmConfig) {
    this.llmClient = createLLMClient(llmConfig);
    this.model = llmConfig.model || 'default';
    this.tools = new ToolRegistry();
    this.state = {
      messages: [],
      turnCount: 0,
      maxTurns: 50,
      stopped: false
    };
    this._registerDefaultTools();
  }
  
  _registerDefaultTools() {
    const { FileTools } = require('../tools/file_tools');
    const { NetworkTools } = require('../tools/network_tools');
    
    const fileTools = new FileTools();
    const networkTools = new NetworkTools();
    
    this.tools.register('read_file', '读取文件内容', fileTools.readFileSchema, fileTools.readFile.bind(fileTools));
    this.tools.register('write_file', '写入文件内容', fileTools.writeFileSchema, fileTools.writeFile.bind(fileTools));
    this.tools.register('list_files', '列出文件', fileTools.listFilesSchema, fileTools.listFiles.bind(fileTools));
    this.tools.register('web_fetch', '获取网页内容', networkTools.webFetchSchema, networkTools.webFetch.bind(networkTools));
    this.tools.register('http_request', '发送HTTP请求', networkTools.httpRequestSchema, networkTools.httpRequest.bind(networkTools));
  }
  
  async run(userInput) {
    this.state.messages.push({ role: 'user', content: userInput });
    this.state.turnCount++;
    
    if (this.state.turnCount > this.state.maxTurns) {
      return 'Error: Maximum turns reached';
    }
    
    try {
      const response = await this.llmClient.chat(
        this.state.messages,
        this.tools.getDefinitions()
      );
      
      if (response.toolCalls && response.toolCalls.length > 0) {
        const toolResults = [];
        for (const toolCall of response.toolCalls) {
          try {
            const result = this.tools.execute(toolCall.name, toolCall.arguments);
            toolResults.push({
              toolUseId: toolCall.id,
              content: String(result)
            });
          } catch (error) {
            toolResults.push({
              toolUseId: toolCall.id,
              content: `Error: ${error.message}`,
              isError: true
            });
          }
        }
        
        this.state.messages.push({
          role: 'user',
          content: JSON.stringify(toolResults)
        });
        
        return `Tool results: ${JSON.stringify(toolResults)}`;
      }
      
      return response.content;
    } catch (error) {
      console.error('LLM call failed:', error);
      return `Error: ${error.message}`;
    }
  }
  
  reset() {
    this.state = {
      messages: [],
      turnCount: 0,
      maxTurns: 50,
      stopped: false
    };
    console.log('Agent state reset');
  }
}

module.exports = { AgentCore };
