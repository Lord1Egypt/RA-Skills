/**
 * Agent Work Visibility - Basic Tests
 * 
 * 基础功能测试
 */

const { 
  TaskVisibilityManager, 
  OVERALL_STATUS, 
  BLOCKER_TYPE, 
  USER_INPUT_TYPE 
} = require('../src/index');

// ==================== 测试工具 ====================

function assert(condition, message) {
  if (!condition) {
    throw new Error(`❌ 测试失败：${message}`);
  }
}

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   ${error.message}`);
    throw error;
  }
}

// ==================== 测试用例 ====================

function runTests() {
  console.log('\n🧪 Agent Work Visibility - 基础测试\n');
  
  // --- 任务创建 ---
  
  test('创建 Research 任务', () => {
    const manager = new TaskVisibilityManager();
    const task = manager.createTask('test-001', '测试任务', 'research');
    
    assert(task.task_id === 'test-001', '任务 ID 正确');
    assert(task.task_title === '测试任务', '任务标题正确');
    assert(task.phases.length === 5, 'Research 任务有 5 个阶段');
    assert(task.overall_status === OVERALL_STATUS.PENDING, '初始状态为 pending');
  });
  
  // --- 阶段管理 ---
  
  test('开始阶段', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-002', '测试任务', 'research');
    
    manager.startPhase('test-002', '理解任务');
    const task = manager.getTask('test-002');
    
    assert(task.current_phase === '理解任务', '当前阶段正确');
    assert(task.overall_status === OVERALL_STATUS.RUNNING, '状态变为 running');
  });
  
  test('完成阶段自动进入下一阶段', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-003', '测试任务', 'research');
    
    manager.startPhase('test-003', '理解任务');
    const result = manager.completePhase('test-003', '理解任务', '已完成');
    
    assert(result.completed.phase_name === '理解任务', '完成的阶段正确');
    assert(result.next.phase_name === '制定搜索计划', '自动进入下一阶段');
  });
  
  test('更新阶段进度', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-004', '测试任务', 'research');
    
    // 完成前两个阶段
    manager.startPhase('test-004', '理解任务');
    manager.completePhase('test-004', '理解任务');
    manager.startPhase('test-004', '制定搜索计划');
    manager.completePhase('test-004', '制定搜索计划');
    manager.startPhase('test-004', '收集信息');
    
    manager.updatePhaseProgress('test-004', '收集信息', 50);
    const task = manager.getTask('test-004');
    
    const phase = task.phases.find(p => p.phase_name === '收集信息');
    assert(phase.phase_progress === 50, '阶段进度正确');
    // 理解 10% + 计划 15% + 收集 50%*30%=15% = 40%
    assert(task.progress_percent >= 40, `总体进度应 >= 40%，实际 ${task.progress_percent}%`);
  });
  
  // --- 进度计算 ---
  
  test('进度计算 - 加权完成度', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-005', '测试任务', 'research');
    
    // 完成前两个阶段
    manager.startPhase('test-005', '理解任务');
    manager.completePhase('test-005', '理解任务');
    manager.startPhase('test-005', '制定搜索计划');
    manager.completePhase('test-005', '制定搜索计划');
    
    const task = manager.getTask('test-005');
    
    // 理解 10% + 计划 15% = 25%
    assert(task.progress_percent === 25, `进度应为 25%，实际 ${task.progress_percent}%`);
  });
  
  // --- 阻塞管理 ---
  
  test('报告阻塞', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-006', '测试任务', 'research');
    
    manager.block('test-006', BLOCKER_TYPE.API_TIMEOUT, 'API 超时');
    const task = manager.getTask('test-006');
    
    assert(task.blocker_status !== 'none', '阻塞状态已设置');
    assert(task.overall_status === OVERALL_STATUS.BLOCKED, '整体状态变为 blocked');
    assert(task.recommended_user_action !== null, '有推荐用户操作');
  });
  
  test('清除阻塞', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-007', '测试任务', 'research');
    
    manager.block('test-007', BLOCKER_TYPE.API_TIMEOUT);
    manager.unblock('test-007');
    const task = manager.getTask('test-007');
    
    assert(task.blocker_status === 'none', '阻塞状态已清除');
    assert(task.overall_status === OVERALL_STATUS.RUNNING, '状态恢复为 running');
  });
  
  // --- 用户介入 ---
  
  test('请求用户介入', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-008', '测试任务', 'research');
    
    manager.ask('test-008', USER_INPUT_TYPE.DIRECTION_CHOICE, 
      '请选择方向', 
      ['A: 方向 1', 'B: 方向 2']
    );
    const task = manager.getTask('test-008');
    
    assert(task.needs_user_input === true, '需要用户输入');
    assert(task.user_question === '请选择方向', '问题正确');
    assert(task.user_options.length === 2, '选项正确');
    assert(task.overall_status === OVERALL_STATUS.WAITING, '状态变为 waiting');
  });
  
  test('用户响应后清除介入状态', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-009', '测试任务', 'research');
    
    manager.ask('test-009', USER_INPUT_TYPE.DIRECTION_CHOICE, '请选择');
    manager.respond('test-009');
    const task = manager.getTask('test-009');
    
    assert(task.needs_user_input === false, '介入状态已清除');
    assert(task.overall_status === OVERALL_STATUS.RUNNING, '状态恢复为 running');
  });
  
  // --- 日志管理 ---
  
  test('记录动作日志', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-010', '测试任务', 'research');
    
    manager.log('test-010', '动作1');
    manager.log('test-010', '动作2');
    manager.log('test-010', '动作3');
    
    const task = manager.getTask('test-010');
    
    // createTask 会自动记录一条启动日志，所以总共 4 条
    assert(task.action_log.length === 4, '日志数量正确（含启动日志）');
    assert(task.action_log[0].message === '动作3', '最新日志在最前');
  });
  
  test('日志数量限制', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-011', '测试任务', 'research');
    
    // 记录 15 条日志（加上 createTask 的启动日志共 16 条）
    for (let i = 1; i <= 15; i++) {
      manager.log('test-011', `动作${i}`);
    }
    
    const task = manager.getTask('test-011');
    
    assert(task.action_log.length === 10, '最多保留 10 条日志');
    assert(task.action_log[0].message === '动作15', '最新日志在最前');
  });
  
  // --- 视图渲染 ---
  
  test('渲染默认视图', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-012', '测试任务', 'research');
    manager.startPhase('test-012', '理解任务');
    manager.log('test-012', '正在分析需求');
    
    const view = manager.getDefaultView('test-012');
    
    // V2 格式：带图标和任务标题
    assert(view.includes('测试任务'), '包含任务标题');
    assert(view.includes('状态：'), '包含状态');
    assert(view.includes('阶段：理解任务'), '包含当前阶段');
    assert(view.includes('是否需要你'), '包含用户介入提示');
  });
  
  test('渲染完整视图', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-013', '测试任务', 'research');
    manager.startPhase('test-013', '理解任务');
    
    const view = manager.getFullView('test-013');
    
    assert(view.includes('【阶段进度】'), '包含阶段进度');
    assert(view.includes('【最近动作】'), '包含动作日志');
    assert(view.includes('【阻塞状态】'), '包含阻塞状态');
  });
  
  // --- 健康检查 ---
  
  test('任务健康检查', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-014', '测试任务', 'research');
    manager.startPhase('test-014', '理解任务');
    
    // 刚创建的任务应该是健康的
    const healthy = manager.isHealthy('test-014', 5);
    assert(healthy === true, '新任务是健康的');
  });
  
  // --- 系统事件翻译 ---
  
  test('系统事件翻译为用户语言', () => {
    const manager = new TaskVisibilityManager();
    manager.createTask('test-015', '测试任务', 'research');
    manager.startPhase('test-015', '收集信息');
    
    manager.event('test-015', 'page_fetch_started', { url: 'https://example.com', pageNumber: 3 });
    
    const task = manager.getTask('test-015');
    const latestLog = task.action_log[0];
    
    assert(latestLog.message.includes('网页'), '事件已翻译为用户语言');
    assert(latestLog.raw_event.type === 'page_fetch_started', '保留原始事件');
  });
  
  // ==================== 测试结果 ====================
  
  console.log('\n✅ 所有测试通过！\n');
}

// 运行测试
try {
  runTests();
} catch (error) {
  console.log('\n💥 测试失败，请检查代码\n');
  process.exit(1);
}
