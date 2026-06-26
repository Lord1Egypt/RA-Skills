#!/usr/bin/env node

// Content Workflow Engine - Node.js wrapper for Python skill
// Provides OpenClaw compatibility for Python-based skill

const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('📝 Content Workflow Engine');
console.log('Version: 1.0.0');
console.log('Runtime: Python 3');
console.log('');

// Check if Python 3 is available
function checkPython() {
  return new Promise((resolve, reject) => {
    exec('python3 --version', (error, stdout, stderr) => {
      if (error) {
        reject(new Error('Python 3 is required but not found'));
      } else {
        resolve(stdout.trim());
      }
    });
  });
}

// Run a Python script from the scripts directory
function runPythonScript(scriptName, args = []) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, 'scripts', scriptName);
    
    if (!fs.existsSync(scriptPath)) {
      reject(new Error(`Script not found: ${scriptPath}`));
      return;
    }
    
    const cmd = `python3 "${scriptPath}" ${args.join(' ')}`;
    
    console.log(`🚀 Running: ${cmd}`);
    
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(`Script failed: ${error.message}`));
      } else {
        resolve(stdout);
      }
    });
  });
}

// Main function
async function main() {
  try {
    // Check Python
    const pythonVersion = await checkPython();
    console.log(`✅ ${pythonVersion}`);
    
    // Parse command line arguments
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
      // Show help
      console.log('\n📋 Available commands:');
      console.log('  create-workflow --name <name> --type <type>');
      console.log('    Create a new content workflow');
      console.log('');
      console.log('  run-workflow --workflow <name> --input <input>');
      console.log('    Run an existing workflow');
      console.log('');
      console.log('  brainstorm --topic <topic>');
      console.log('    Generate content ideas');
      console.log('');
      console.log('  help');
      console.log('    Show this help message');
      console.log('');
      console.log('📖 For detailed documentation, see SKILL.md');
      return;
    }
    
    const command = args[0];
    
    switch (command) {
      case 'create-workflow':
        await runPythonScript('create_workflow.py', args.slice(1));
        break;
        
      case 'run-workflow':
        await runPythonScript('run_workflow.py', args.slice(1));
        break;
        
      case 'brainstorm':
        await runPythonScript('brainstorm.py', args.slice(1));
        break;
        
      case 'help':
        // Help already shown above
        break;
        
      default:
        console.log(`❌ Unknown command: ${command}`);
        console.log('💡 Use "help" to see available commands');
        process.exit(1);
    }
    
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

// Run main function
if (require.main === module) {
  main();
}

module.exports = {
  checkPython,
  runPythonScript,
  main
};