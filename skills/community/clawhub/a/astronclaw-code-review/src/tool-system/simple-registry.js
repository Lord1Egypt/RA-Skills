/**
 * 简化版工具注册表 - 专为Code Review Assistant设计
 */

export class SimpleToolRegistry {
  constructor() {
    this.tools = new Map(); // name -> tool definition
    this.categories = new Map(); // category -> [tool names]
    this.stats = {
      totalTools: 0,
      totalCalls: 0,
      totalErrors: 0
    };
  }
  
  /**
   * 注册工具
   */
  registerTool(toolDef) {
    const { name, description, category = 'uncategorized', execute } = toolDef;
    
    if (!name || !execute) {
      throw new Error('Tool must have name and execute function');
    }
    
    const tool = {
      name,
      description: description || `Tool: ${name}`,
      category,
      execute,
      metadata: toolDef.metadata || {},
      createdAt: new Date().toISOString(),
      callCount: 0,
      errorCount: 0
    };
    
    this.tools.set(name, tool);
    
    if (!this.categories.has(category)) {
      this.categories.set(category, []);
    }
    this.categories.get(category).push(name);
    
    this.stats.totalTools++;
    
    console.log(`✅ 注册工具: ${name} (${category})`);
    return tool;
  }
  
  /**
   * 获取工具
   */
  getTool(name) {
    return this.tools.get(name);
  }
  
  /**
   * 列出所有工具
   */
  listTools(filter = {}) {
    let tools = Array.from(this.tools.values());
    
    if (filter.category) {
      tools = tools.filter(t => t.category === filter.category);
    }
    
    if (filter.namePattern) {
      const pattern = new RegExp(filter.namePattern, 'i');
      tools = tools.filter(t => pattern.test(t.name));
    }
    
    return tools;
  }
  
  /**
   * 执行工具
   */
  async executeTool(toolName, args, context = {}) {
    const tool = this.getTool(toolName);
    
    if (!tool) {
      throw new Error(`工具不存在: ${toolName}`);
    }
    
    this.stats.totalCalls++;
    tool.callCount++;
    
    try {
      console.log(`🔧 执行工具: ${toolName}`);
      const startTime = Date.now();
      
      const result = await tool.execute(args, {
        ...context,
        toolName,
        toolCategory: tool.category
      });
      
      const duration = Date.now() - startTime;
      
      return {
        success: true,
        result,
        metadata: {
          toolName,
          toolCategory: tool.category,
          duration,
          timestamp: new Date().toISOString()
        }
      };
      
    } catch (error) {
      this.stats.totalErrors++;
      tool.errorCount++;
      
      console.error(`❌ 工具执行失败: ${toolName}`, error.message);
      
      return {
        success: false,
        error: {
          message: error.message,
          code: error.code || 'TOOL_EXECUTION_ERROR',
          stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
        },
        metadata: {
          toolName,
          toolCategory: tool.category,
          timestamp: new Date().toISOString()
        }
      };
    }
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      toolsByCategory: Object.fromEntries(this.categories),
      toolDetails: Array.from(this.tools.values()).map(t => ({
        name: t.name,
        category: t.category,
        callCount: t.callCount,
        errorCount: t.errorCount,
        description: t.description
      }))
    };
  }
  
  /**
   * 按类别获取工具
   */
  getToolsByCategory(category) {
    const toolNames = this.categories.get(category) || [];
    return toolNames.map(name => this.tools.get(name));
  }
}