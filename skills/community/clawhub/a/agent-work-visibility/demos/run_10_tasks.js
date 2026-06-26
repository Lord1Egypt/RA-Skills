/**
 * Phase 2: 10 个真实任务模拟运行
 * 
 * 模拟 Research Agent 执行 10 个真实任务，覆盖不同场景
 * 保存 artifacts 用于验证
 */

const { createResearchAdapter } = require('../src/adapters/research_agent_adapter');
const { withHooks, registerLoggingHooks } = require('../src/hooks/simple_hooks');
const { withSnapshotHistory } = require('../src/history/snapshot_history');
const { TaskVisibilityManager } = require('../src/index');

// ==================== 创建增强型 Manager ====================

function createEnhancedManager() {
  const manager = new TaskVisibilityManager();
  
  // 添加钩子支持
  withHooks(manager);
  registerLoggingHooks(manager, '[TaskRunner]');
  
  // 添加历史记录
  withSnapshotHistory(manager);
  
  return manager;
}

// ==================== 任务运行器 ====================

class TaskRunner {
  constructor() {
    this.manager = createEnhancedManager();
    this.completedTasks = [];
    this.failedTasks = [];
  }

  /**
   * 运行单个任务
   */
  async runTask(taskConfig) {
    const { taskId, title, scenario, events } = taskConfig;
    
    console.log(`\n════════════════════════════════════════`);
    console.log(`  任务：${title}`);
    console.log(`  ID: ${taskId}`);
    console.log(`  场景：${scenario}`);
    console.log(`════════════════════════════════════════\n`);
    
    // 使用增强型 manager 创建 adapter
    const { ResearchAgentAdapter } = require('../src/adapters/research_agent_adapter');
    const adapter = new ResearchAgentAdapter(this.manager);
    adapter.bindTask(taskId, title);
    
    // 执行事件序列
    for (const event of events) {
      console.log(`  → ${event.type}`);
      adapter.handleEvent(event);
      
      // 模拟执行延迟
      if (event.delay) {
        await new Promise(resolve => setTimeout(resolve, event.delay));
      }
    }
    
    // 记录结果
    const finalStatus = this.manager.getTask(taskId);
    if (finalStatus.overall_status === 'completed') {
      this.completedTasks.push(taskId);
    } else if (finalStatus.overall_status === 'failed') {
      this.failedTasks.push(taskId);
    }
    
    // 导出任务报告
    const report = this.manager.exportTaskReport(taskId);
    console.log(`\n✅ 任务完成，Snapshot 已保存\n`);
    
    return finalStatus;
  }

  /**
   * 运行所有任务
   */
  async runAll(taskConfigs) {
    console.log('\n╔════════════════════════════════════════╗');
    console.log('║  Phase 2: 10 个真实任务验证运行        ║');
    console.log('╚════════════════════════════════════════╝\n');
    
    for (const config of taskConfigs) {
      await this.runTask(config);
    }
    
    // 输出统计
    this.printSummary();
    
    return {
      completed: this.completedTasks,
      failed: this.failedTasks,
      total: taskConfigs.length
    };
  }

  /**
   * 打印总结
   */
  printSummary() {
    console.log('\n════════════════════════════════════════');
    console.log('  运行总结');
    console.log('════════════════════════════════════════\n');
    
    console.log(`总任务数：${this.completedTasks.length + this.failedTasks.length}`);
    console.log(`✅ 完成：${this.completedTasks.length}`);
    console.log(`❌ 失败：${this.failedTasks.length}`);
    console.log('');
    
    const stats = this.manager.getHistoryStats();
    console.log(`Snapshot 总数：${stats.totalSnapshots}`);
    console.log(`任务数：${stats.totalTasks}`);
    console.log('');
    
    console.log('已完成任务:', this.completedTasks.join(', ') || '无');
    console.log('失败任务:', this.failedTasks.join(', ') || '无');
    console.log('');
  }
}

// ==================== 10 个任务配置 ====================

const TASK_CONFIGS = [
  // ─────────────────────────────────────────────────────
  // A 组：正常完成任务（3 个）
  // ─────────────────────────────────────────────────────
  {
    taskId: 'task-001',
    title: '调研 AI Agent 基础设施项目：LangChain',
    scenario: 'A1: 正常完成 - 单个项目调研',
    events: [
      { type: 'task_start', data: { title: '调研 LangChain' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务', summary: '已明确任务目标' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'search_query_built', data: { query: 'LangChain AI Agent infrastructure' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划', summary: '已确定搜索策略' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://langchain.com', pageNumber: 1 } },
      { type: 'page_fetch_success', data: { pageNumber: 1 } },
      { type: 'page_fetch_start', data: { url: 'https://docs.langchain.com', pageNumber: 2 } },
      { type: 'page_fetch_success', data: { pageNumber: 2 } },
      { type: 'extraction_done', data: { itemCount: 5 } },
      { type: 'phase_complete', data: { phase: '收集信息', summary: '已收集 5 个数据点' } },
      { type: 'phase_start', data: { phase: '分析与比较' } },
      { type: 'compare_start', data: { itemCount: 1 } },
      { type: 'phase_complete', data: { phase: '分析与比较', summary: '已完成分析' } },
      { type: 'phase_start', data: { phase: '形成输出' } },
      { type: 'draft_start', data: {} },
      { type: 'report_created', data: { pages: 3 } },
      { type: 'phase_complete', data: { phase: '形成输出', summary: '已生成报告' } },
      { type: 'task_complete', data: {} }
    ]
  },
  
  {
    taskId: 'task-002',
    title: '比较 3 个 AI Agent 框架（LangChain vs LlamaIndex vs AutoGen）',
    scenario: 'A2: 正常完成 - 多项目比较',
    events: [
      { type: 'task_start', data: { title: '比较 3 个框架' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务', summary: '已明确对比维度' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'search_query_built', data: { query: 'LangChain LlamaIndex AutoGen comparison' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://langchain.com', pageNumber: 1 } },
      { type: 'page_fetch_success', data: { pageNumber: 1 } },
      { type: 'page_fetch_start', data: { url: 'https://llamaindex.ai', pageNumber: 2 } },
      { type: 'page_fetch_success', data: { pageNumber: 2 } },
      { type: 'page_fetch_start', data: { url: 'https://microsoft.github.io/autogen', pageNumber: 3 } },
      { type: 'page_fetch_success', data: { pageNumber: 3 } },
      { type: 'extraction_done', data: { itemCount: 12 } },
      { type: 'phase_complete', data: { phase: '收集信息', summary: '已收集 12 个数据点' } },
      { type: 'phase_start', data: { phase: '分析与比较' } },
      { type: 'compare_start', data: { itemCount: 3 } },
      { type: 'phase_complete', data: { phase: '分析与比较', summary: '已完成对比分析' } },
      { type: 'phase_start', data: { phase: '形成输出' } },
      { type: 'report_created', data: { pages: 5 } },
      { type: 'phase_complete', data: { phase: '形成输出' } },
      { type: 'task_complete', data: {} }
    ]
  },
  
  {
    taskId: 'task-003',
    title: '搜索并整理最近 3 个月 AI Agent 行业新闻',
    scenario: 'A3: 正常完成 - 新闻整理',
    events: [
      { type: 'task_start', data: { title: '整理 AI Agent 新闻' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'search_query_built', data: { query: 'AI Agent news last 3 months' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://techcrunch.com', pageNumber: 1 } },
      { type: 'page_fetch_success', data: { pageNumber: 1 } },
      { type: 'page_fetch_start', data: { url: 'https://theverge.com', pageNumber: 2 } },
      { type: 'page_fetch_success', data: { pageNumber: 2 } },
      { type: 'page_fetch_start', data: { url: 'https://venturebeat.com', pageNumber: 3 } },
      { type: 'page_fetch_success', data: { pageNumber: 3 } },
      { type: 'extraction_done', data: { itemCount: 20 } },
      { type: 'shortlist_done', data: { count: 10 } },
      { type: 'phase_complete', data: { phase: '收集信息', summary: '已筛选 10 条新闻' } },
      { type: 'phase_start', data: { phase: '分析与比较' } },
      { type: 'compare_start', data: { itemCount: 10 } },
      { type: 'phase_complete', data: { phase: '分析与比较' } },
      { type: 'phase_start', data: { phase: '形成输出' } },
      { type: 'report_created', data: { pages: 4 } },
      { type: 'task_complete', data: {} }
    ]
  },
  
  // ─────────────────────────────────────────────────────
  // B 组：中途等待/重试（3 个）
  // ─────────────────────────────────────────────────────
  {
    taskId: 'task-004',
    title: '抓取响应慢的 API 数据源',
    scenario: 'B1: API 超时后恢复',
    events: [
      { type: 'task_start', data: { title: '抓取慢 API' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://slow-api.example.com', pageNumber: 1 } },
      { type: 'page_fetch_timeout', data: { url: 'https://slow-api.example.com' } },
      { type: 'retry_start', data: { attempt: 1, operation: 'API 请求' } },
      { type: 'page_fetch_timeout', data: {} },
      { type: 'retry_start', data: { attempt: 2, operation: 'API 请求' } },
      { type: 'page_fetch_success', data: { pageNumber: 1 } },
      { type: 'retry_success', data: { operation: 'API 请求' } },
      { type: 'extraction_done', data: { itemCount: 8 } },
      { type: 'phase_complete', data: { phase: '收集信息' } },
      { type: 'phase_start', data: { phase: '分析与比较' } },
      { type: 'phase_complete', data: { phase: '分析与比较' } },
      { type: 'phase_start', data: { phase: '形成输出' } },
      { type: 'report_created', data: { pages: 2 } },
      { type: 'task_complete', data: {} }
    ]
  },
  
  {
    taskId: 'task-005',
    title: '访问限流的数据源',
    scenario: 'B2: Rate Limited 后恢复',
    events: [
      { type: 'task_start', data: { title: '访问限流 API' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://rate-limited-api.com', pageNumber: 1 } },
      { type: 'page_fetch_error', data: { reason: '429 Too Many Requests' } },
      { type: 'retry_start', data: { attempt: 1, operation: 'API 请求' } },
      { type: 'page_fetch_success', data: { pageNumber: 1 } },
      { type: 'extraction_done', data: { itemCount: 6 } },
      { type: 'phase_complete', data: { phase: '收集信息' } },
      { type: 'phase_start', data: { phase: '分析与比较' } },
      { type: 'phase_complete', data: { phase: '分析与比较' } },
      { type: 'phase_start', data: { phase: '形成输出' } },
      { type: 'task_complete', data: {} }
    ]
  },
  
  {
    taskId: 'task-006',
    title: '部分内容加载失败后恢复',
    scenario: 'B3: 部分失败后继续',
    events: [
      { type: 'task_start', data: { title: '部分加载失败' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://source1.com', pageNumber: 1 } },
      { type: 'page_fetch_success', data: { pageNumber: 1 } },
      { type: 'page_fetch_start', data: { url: 'https://source2.com', pageNumber: 2 } },
      { type: 'page_fetch_error', data: { reason: '404 Not Found' } },
      { type: 'retry_start', data: { attempt: 1, operation: 'API 请求' } },
      { type: 'retry_failed', data: { attempt: 1, operation: 'API 请求' } },
      { type: 'page_fetch_start', data: { url: 'https://source3.com', pageNumber: 3 } },
      { type: 'page_fetch_success', data: { pageNumber: 3 } },
      { type: 'extraction_done', data: { itemCount: 10 } },
      { type: 'phase_complete', data: { phase: '收集信息', summary: '部分数据源不可用，已继续' } },
      { type: 'phase_start', data: { phase: '分析与比较' } },
      { type: 'phase_complete', data: { phase: '分析与比较' } },
      { type: 'phase_start', data: { phase: '形成输出' } },
      { type: 'task_complete', data: {} }
    ]
  },
  
  // ─────────────────────────────────────────────────────
  // C 组：需要用户介入（2 个）
  // ─────────────────────────────────────────────────────
  {
    taskId: 'task-007',
    title: '发现多个深入方向需要选择',
    scenario: 'C1: 方向选择 Ask Human',
    events: [
      { type: 'task_start', data: { title: '多方向选择' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://example.com', pageNumber: 1 } },
      { type: 'page_fetch_success', data: { pageNumber: 1 } },
      { type: 'extraction_done', data: { itemCount: 15 } },
      { type: 'phase_complete', data: { phase: '收集信息' } },
      { type: 'phase_start', data: { phase: '分析与比较' } },
      { type: 'user_input_required', data: {
        inputType: 'direction_choice',
        question: '发现 3 个方向都可继续深入，你要优先看哪一个？',
        options: ['A: 技术架构', 'B: 商业模式', 'C: 生态发展']
      }},
      // 模拟用户响应
      { type: 'user_responded', data: { answer: 'A' } },
      { type: 'compare_start', data: { itemCount: 3 } },
      { type: 'phase_complete', data: { phase: '分析与比较' } },
      { type: 'phase_start', data: { phase: '形成输出' } },
      { type: 'task_complete', data: {} }
    ]
  },
  
  {
    taskId: 'task-008',
    title: '任务范围扩大需要确认',
    scenario: 'C2: 范围确认 Ask Human',
    events: [
      { type: 'task_start', data: { title: '范围确认' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://example.com', pageNumber: 1 } },
      { type: 'page_fetch_success', data: { pageNumber: 1 } },
      { type: 'scope_expansion_detected', data: {
        description: '发现 5 个相关子领域',
        inputType: 'scope_confirmation',
        question: '发现重要扩展内容，是否深入分析？',
        options: ['是，深入分析', '否，保持原范围']
      }},
      // 模拟用户响应
      { type: 'user_responded', data: { answer: '是' } },
      { type: 'extraction_done', data: { itemCount: 25 } },
      { type: 'phase_complete', data: { phase: '收集信息' } },
      { type: 'phase_start', data: { phase: '分析与比较' } },
      { type: 'phase_complete', data: { phase: '分析与比较' } },
      { type: 'phase_start', data: { phase: '形成输出' } },
      { type: 'task_complete', data: {} }
    ]
  },
  
  // ─────────────────────────────────────────────────────
  // D 组：失败/卡住任务（2 个）
  // ─────────────────────────────────────────────────────
  {
    taskId: 'task-009',
    title: '访问需要登录的资源（权限不足）',
    scenario: 'D1: 权限不足失败',
    events: [
      { type: 'task_start', data: { title: '权限不足' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://premium-api.com', pageNumber: 1 } },
      { type: 'page_fetch_error', data: { reason: '401 Unauthorized - Login Required' } },
      { type: 'user_input_required', data: {
        inputType: 'auth_required',
        question: '需要登录才能访问此资源，请提供账号授权',
        options: ['已登录，继续', '跳过此资源', '终止任务']
      }},
      // 模拟用户未响应，任务失败
      { type: 'task_failed', data: { reason: '权限不足，无法继续' } }
    ]
  },
  
  {
    taskId: 'task-010',
    title: '关键数据源不可用',
    scenario: 'D2: 资源不可用失败',
    events: [
      { type: 'task_start', data: { title: '资源不可用' } },
      { type: 'phase_start', data: { phase: '理解任务' } },
      { type: 'phase_complete', data: { phase: '理解任务' } },
      { type: 'phase_start', data: { phase: '制定搜索计划' } },
      { type: 'phase_complete', data: { phase: '制定搜索计划' } },
      { type: 'phase_start', data: { phase: '收集信息' } },
      { type: 'page_fetch_start', data: { url: 'https://critical-source.com', pageNumber: 1 } },
      { type: 'page_fetch_error', data: { reason: '503 Service Unavailable' } },
      { type: 'retry_start', data: { attempt: 1, operation: 'API 请求' } },
      { type: 'page_fetch_error', data: { reason: '503 Service Unavailable' } },
      { type: 'retry_start', data: { attempt: 2, operation: 'API 请求' } },
      { type: 'page_fetch_error', data: { reason: '503 Service Unavailable' } },
      { type: 'retry_failed', data: { attempt: 2, operation: 'API 请求' } },
      { type: 'retry_start', data: { attempt: 3, operation: 'API 请求' } },
      { type: 'retry_failed', data: { attempt: 3, operation: 'API 请求' } },
      { type: 'task_failed', data: { reason: '关键数据源不可用，多次重试失败' } }
    ]
  }
];

// ==================== 主函数 ====================

async function main() {
  const runner = new TaskRunner();
  const results = await runner.runAll(TASK_CONFIGS);
  
  console.log('\n════════════════════════════════════════');
  console.log('  Phase 2 验证运行完成');
  console.log('════════════════════════════════════════\n');
  
  console.log('Artifacts 保存位置：~/.openclaw/skills/agent-work-visibility/artifacts/phase2/');
  console.log('');
  console.log('下一步：');
  console.log('1. 检查 artifacts/phase2/ 目录中的 snapshot 文件');
  console.log('2. 查看每个任务的 snapshot_*.json');
  console.log('3. 编写 validation_report_phase2.md');
  console.log('');
  
  return results;
}

// 运行
main().catch(console.error);
