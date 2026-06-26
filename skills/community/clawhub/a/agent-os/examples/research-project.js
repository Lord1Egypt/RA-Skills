const { AgentOS } = require('../core/index.js');

/**
 * Example: Research + Design + Development Project
 * 
 * Goal: Build a new feature for ClawdGym
 * Agents: Research specialist, Design specialist, Dev specialist
 * Timeline: 3 task phases, 4 subtasks each
 */
async function main() {
  console.log('');
  console.log('╔═══════════════════════════════════════════════════════════════╗');
  console.log('║                    🤖 AGENT OS v0.1                           ║');
  console.log('║        Multi-Agent Project Execution Framework                ║');
  console.log('╚═══════════════════════════════════════════════════════════════╝');
  console.log('');

  // Initialize system
  const os = new AgentOS('clawdgym-feature-2026-02-24');

  // Register agents with capabilities
  os.registerAgent('agent-research', '🔍 Research', ['research', 'planning']);
  os.registerAgent('agent-design', '🎨 Design', ['design', 'planning']);
  os.registerAgent('agent-dev', '💻 Development', ['development', 'research']);

  os.initialize();

  // Run the project
  const goal = 'Build AI-powered trial member follow-up system for ClawdGym';
  const phases = ['planning', 'design', 'development'];

  try {
    const result = await os.runProject(goal, phases);

    console.log('');
    console.log('╔═══════════════════════════════════════════════════════════════╗');
    console.log('║                    📊 PROJECT COMPLETE                        ║');
    console.log('╚═══════════════════════════════════════════════════════════════╝');
    console.log('');

    // Print results
    console.log(`Goal: ${result.goal}`);
    console.log(`Status: ${result.status.toUpperCase()}`);
    console.log(`Progress: ${result.progress}%`);
    console.log('');

    console.log('Task Summary:');
    console.log(`  ✅ Complete: ${result.taskStats.complete}/${result.taskStats.total}`);
    console.log(`  ⏳ In Progress: ${result.taskStats.inProgress}`);
    console.log(`  🚫 Blocked: ${result.taskStats.blocked}`);
    console.log(`  ⏸️  Pending: ${result.taskStats.pending}`);
    console.log('');

    console.log('Agent Summary:');
    result.agents.forEach((agent) => {
      console.log(`  ${agent.name}`);
      console.log(`    Status: ${agent.status}`);
      console.log(`    Tasks Completed: ${agent.tasksCompleted}`);
      console.log(`    Last Active: ${agent.lastActiveAt || 'Never'}`);
    });

    console.log('');
    console.log('Persisted to:');
    console.log(`  Project state: data/${os.projectId}-project.json`);
    console.log(`  Agent memory: data/agent-*.json`);
    console.log('');
  } catch (error) {
    console.error('Error running project:', error.message);
    process.exit(1);
  }
}

main();
