/**
 * ANFSF V1.5.0 - 内存模块示例和使用指南
 */

import { 
  HierarchicalMemoryRetriever,
  TemporalKnowledgeGraph 
} from './index';

// ============================================================================
// 示例 1: 基础使用
// ============================================================================

async function basicExample() {
  // 初始化检索器
  const retriever = new HierarchicalMemoryRetriever();
  await retriever.initialize();

  // 存储记忆
  await retriever.store(
    '用户决定使用 PostgreSQL 而不是 SQLite，因为需要同时写入',
    'wing_jieyue_project',
    'hall_facts',
    { 
      type: 'decision', 
      priority: 'high',
      timestamp: '2026-04-09T10:00:00Z'
    }
  );

  // 搜索
  const results = await retriever.search('数据库 decision', {
    topK: 5,
    minScore: 0.7
  });

  console.log('搜索结果:', results);
  await retriever.close();
}

// ============================================================================
// 示例 2: 层级导航搜索
// ============================================================================

async function navigateExample() {
  const retriever = new HierarchicalMemoryRetriever();
  await retriever.initialize();

  // 在特定 wing 和 room 中搜索
  const wingResults = await retriever.navigateSearch(
    'PostgreSQL 决策',
    'wing_jieyue_project',
    'hall_facts'
  );

  console.log('层级导航搜索:', wingResults);
  await retriever.close();
}

// ============================================================================
// 示例 3: 时间感知搜索
// ============================================================================

async function temporalExample() {
  const kg = new TemporalKnowledgeGraph();

  // 添加事实
  await kg.addTriple(
    '用户', 
    '居住', 
    '上海',
    '2025-01-01T00:00:00Z'
  );

  await kg.addTriple(
    '用户', 
    '居住', 
    '北京',
    '2026-04-01T00:00:00Z'
  );

  // 查询当前事实
  const currentCity = await kg.queryRelation('用户', '居住');
  console.log('当前居住地:', currentCity);

  // 查询历史事实
  const historyCity = await kg.queryRelation(
    '用户', 
    '居住',
    '2026-01-15'  // 查看 2026年1月15日
  );
  console.log('2026-01-15 居住地:', historyCity);

  await kg.cleanup();
}

// ============================================================================
// 示例 4: 完整用例 - 捷阅证券项目
// ============================================================================

async function jieyueProjectExample() {
  const retriever = new HierarchicalMemoryRetriever();
  await retriever.initialize();

  // 存储项目决策
  await retriever.store(
    '选择 PostgreSQL 而不是 SQLite，因为需要并发写入支持',
    'wing_jieyue_project',
    'hall_facts',
    { type: 'decision', priority: 'high' }
  );

  await retriever.store(
    '用户偏好使用 VS Code 进行开发',
    'wing_jieyue_project',
    'hall_preferences',
    { type: 'preference' }
  );

  await retriever.store(
    '部署流程：Docker 构建 -> 自动部署',
    'wing_jieyue_project',
    'hall_events',
    { type: 'event', category: 'deployment' }
  );

  // 搜索
  const results = await retriever.search('数据库 decision');

  // 时间感知搜索
  const history = await retriever.temporalSearch(
    '部署流程',
    '2026-04-09'
  );

  console.log('项目搜索结果:', results);
  console.log('历史部署:', history);

  await retriever.close();
}

// ============================================================================
// 示例 5: 统计和报告
// ============================================================================

async function statsExample() {
  const retriever = new HierarchicalMemoryRetriever();
  await retriever.initialize();

  // 存储多条记录
  for (let i = 0; i < 10; i++) {
    await retriever.store(
      `记忆 ${i}`,
      'wing_general',
      'general_chat'
    );
  }

  // 获取统计
  const stats = await retriever.stats();
  console.log('内存统计:', stats);

  await retriever.close();
}

// ============================================================================
// 示例 7: 高级检索 - 混合查询 (语义 + 时间 + 层级)
// ============================================================================

async function advancedHybridSearchExample() {
  const retriever = new HierarchicalMemoryRetriever();
  await retriever.initialize();

  // 存储项目记忆
  await retriever.store(
    '用户决定使用 PostgreSQL 而不是 SQLite，因为需要并发写入支持',
    'wing_jieyue_project',
    'hall_facts',
    { type: 'decision' }
  );

  await retriever.store(
    '项目部署使用 Docker 容器化方案',
    'wing_jieyue_project',
    'hall_events',
    { type: 'deployment' }
  );

  await retriever.store(
    '用户偏好使用 VS Code 进行开发',
    'wing_jieyue_project',
    'hall_preferences',
    { type: 'preference' }
  );

  // 高级混合查询
  const hybridResults = await retriever.search('PostgreSQL decision', {
    topK: 5,
    minScore: 0.65,
    includeTemporal: true
  });

  // 限定 wing 的层级搜索
  const wingFiltered = await retriever.navigateSearch(
    'deployment',
    'wing_jieyue_project',
    'hall_events'
  );

  // 时间点查询
  const timeQuery = await retriever.temporalSearch(
    'PostgreSQL decision',
    '2026-04-09'
  );

  console.log('混合查询结果:', hybridResults.length);
  console.log('Wing 过滤结果:', wingFiltered.length);
  console.log('时间查询结果:', timeQuery.length);

  await retriever.close();
}

// ============================================================================
// 示例 8: 实体时间线查询
// ============================================================================

async function entityTimelineExample() {
  const kg = new TemporalKnowledgeGraph();

  // 构建实体时间线
  await kg.addTriple(
    'PostgreSQL',
    '用于',
    '捷阅证券项目',
    '2026-04-01T00:00:00Z'
  );

  await kg.addTriple(
    'PostgreSQL',
    '版本',
    '16.0',
    '2026-04-05T00:00:00Z'
  );

  await kg.addTriple(
    'Docker',
    '用于',
    '捷阅证券部署',
    '2026-04-08T00:00:00Z'
  );

  // 查询时间线
  const timeline = await kg.timeline('PostgreSQL');
  console.log('PostgreSQL 时间线:', timeline);

  // 查询实体关系
  const relations = await kg.querySubject('PostgreSQL');
  console.log('PostgreSQL 关系:', relations);

  await kg.cleanup();
}

// ============================================================================
// 示例 9: 批量导入和统计
// ============================================================================

async function batchImportExample() {
  const retriever = new HierarchicalMemoryRetriever();
  await retriever.initialize();

  // 批量导入记忆
  const memories = [
    { text: '决策1: 使用 PostgreSQL', wing: 'wing_jieyue', room: 'hall_facts' },
    { text: '决策2: 使用 Docker', wing: 'wing_jieyue', room: 'hall_facts' },
    { text: '偏好1: VS Code', wing: 'wing_jieyue', room: 'hall_preferences' },
    { text: '事件1: 项目启动', wing: 'wing_jieyue', room: 'hall_events' },
    { text: '事件2: 首次部署', wing: 'wing_jieyue', room: 'hall_events' }
  ];

  for (const mem of memories) {
    await retriever.store(
      mem.text,
      mem.wing,
      mem.room,
      { type: 'imported' }
    );
  }

  // 获取完整统计
  const stats = await retriever.stats();
  console.log('批量导入统计:', stats);

  // 全局搜索
  const allResults = await retriever.search('PostgreSQL', {
    topK: 10,
    minScore: 0.5
  });

  console.log('全局搜索结果数:', allResults.length);

  await retriever.close();
}

// ============================================================================
// 示例 10: 实战 - 捷阅证券项目完整用例
// ============================================================================

async function jieyueProjectFullExample() {
  const retriever = new HierarchicalMemoryRetriever();
  await retriever.initialize();

  // 1. 存储项目决策
  await retriever.store(
    '数据库选型: PostgreSQL 而不是 SQLite，因为需要并发写入支持',
    'wing_database',
    'hall_decisions',
    { type: 'decision', priority: 'critical' }
  );

  // 2. 存储技术栈偏好
  await retriever.store(
    '用户偏好: VS Code 进行开发',
    'wing_preferences',
    'hall_tools',
    { type: 'preference', category: 'ide' }
  );

  // 3. 存储部署流程
  await retriever.store(
    '部署流程: Docker 构建 -> 自动部署到生产环境',
    'wing_deployment',
    'hall_procedures',
    { type: 'procedure', category: 'ci_cd' }
  );

  // 4. 存储架构决策
  await retriever.store(
    '架构模式: 微服务 + Docker 容器化',
    'wing_architecture',
    'hall_decisions',
    { type: 'decision', priority: 'high' }
  );

  // 5. 存储团队安排
  await retriever.store(
    '团队: 后端团队负责 API 服务，前端团队负责 UI',
    'wing_team',
    'hall_structure',
    { type: 'structure', category: 'team' }
  );

  // 6. 搜索项目文档
  console.log('=== 捷阅证券项目查询 ===');

  const dbDecisions = await retriever.search('PostgreSQL decision');
  console.log('数据库决策:', dbDecisions.map(r => r.content).join('\n'));

  const deploymentProcedures = await retriever.navigateSearch(
    '部署流程',
    'wing_deployment',
    'hall_procedures'
  );
  console.log('部署流程:', deploymentProcedures.map(r => r.content).join('\n'));

  // 7. 时间感知搜索
  const history = await retriever.temporalSearch('架构', '2026-04-09');
  console.log('历史架构记录:', history.length);

  // 8. 获取项目统计
  const stats = await retriever.stats();
  console.log('项目统计:', stats);

  await retriever.close();
}

// ============================================================================
// 导出示例
// ============================================================================

export {
  basicExample,
  navigateExample,
  temporalExample,
  jieyueProjectExample,
  statsExample,
  advancedHybridSearchExample,
  entityTimelineExample,
  batchImportExample,
  jieyueProjectFullExample
};
