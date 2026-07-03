/**
 * ============================================
 * 类型: 核心框架
 * 模块: tools.registry
 * 说明: 工具注册表，管理所有可用工具
 * 修改建议: 如需添加新工具，调用register方法
 * ============================================

class ToolRegistry {
  constructor() {
    this.tools = new Map();
  }
  
  register(name, description, inputSchema, handler, isConcurrencySafe = false) {
    this.tools.set(name, {
      name,
      description,
      inputSchema,
      handler,
      isConcurrencySafe
    });
    console.log(`Registered tool: ${name}`);
  }
  
  getDefinitions() {
    return Array.from(this.tools.values()).map(tool => ({
      type: 'custom',
      name: tool.name,
      description: tool.description,
      input_schema: tool.inputSchema
    }));
  }
  
  execute(name, inputData) {
    if (!this.tools.has(name)) {
      throw new Error(`Unknown tool: ${name}`);
    }
    
    const tool = this.tools.get(name);
    console.log(`Executing tool: ${name}`);
    
    try {
      return tool.handler(inputData);
    } catch (error) {
      console.error(`Tool execution failed: ${name} - ${error.message}`);
      throw error;
    }
  }
  
  listTools() {
    return Array.from(this.tools.keys());
  }
  
  getToolInfo(name) {
    if (!this.tools.has(name)) {
      throw new Error(`Unknown tool: ${name}`);
    }
    
    const tool = this.tools.get(name);
    return {
      name: tool.name,
      description: tool.description,
      isConcurrencySafe: tool.isConcurrencySafe
    };
  }
}

module.exports = { ToolRegistry };
