// AI Agent Team Manager - 使用示例

const { 
  TaskAllocator, 
  ProgressTracker, 
  QualityController,
  PerformanceEvaluator,
  TeamCoordinator,
  WorkflowManager,
  ProjectManager
} = require('./index');

// 1. 创建团队管理实例
const teamManager = new TeamCoordinator({
  teamName: "Otter Camp Team",
  members: [
    { name: "小吕", role: "运维监控专家", skills: ["monitoring", "devops"] },
    { name: "老狗", role: "程序开发专家", skills: ["coding", "debugging"] },
    { name: "小朱", role: "AI产品经理", skills: ["product", "design"] },
    { name: "小秋", role: "商业价值调研专家", skills: ["research", "analysis"] }
  ]
});

// 2. 创建项目
const project = new ProjectManager({
  projectName: "OpenClaw Skill Development",
  description: "开发赚钱的OpenClaw技能包",
  deadline: "2026-03-10"
});

// 3. 分配任务
const tasks = [
  {
    id: "task-001",
    title: "Chinese Content Creator 开发",
    assignee: "小朱",
    priority: "high",
    estimatedHours: 8
  },
  {
    id: "task-002", 
    title: "Security Auditor 开发",
    assignee: "老狗",
    priority: "high",
    estimatedHours: 12
  },
  {
    id: "task-003",
    title: "E-commerce Automation 开发", 
    assignee: "小秋",
    priority: "medium",
    estimatedHours: 10
  }
];

const allocator = new TaskAllocator(teamManager);
allocator.assignTasks(tasks);

// 4. 跟踪进度
const tracker = new ProgressTracker(project);
tracker.updateProgress("task-001", 100); // 完成
tracker.updateProgress("task-002", 80);  // 进行中
tracker.updateProgress("task-003", 60);  // 进行中

// 5. 质量控制
const qualityController = new QualityController();
qualityController.reviewTask("task-001", {
  codeQuality: 95,
  documentation: 90,
  testing: 85
});

// 6. 性能评估
const evaluator = new PerformanceEvaluator(teamManager);
const performanceReport = evaluator.generateReport();

// 7. 工作流管理
const workflow = new WorkflowManager({
  stages: ["planning", "development", "review", "testing", "deployment"]
});
workflow.advanceStage("task-001", "deployment");

console.log("AI Agent Team Manager 使用示例完成！");
console.log("项目进度:", tracker.getOverallProgress());
console.log("团队绩效:", performanceReport.overallScore);