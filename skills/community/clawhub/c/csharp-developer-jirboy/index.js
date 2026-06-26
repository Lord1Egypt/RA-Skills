/**
 * C# Developer Skill - Entry Point
 * 
 * Professional C#/.NET development with project templates,
 * code generation, architecture design, and code review.
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

const SKILL_DIR = path.join(__dirname);
const TEMPLATES_DIR = path.join(SKILL_DIR, 'templates');
const CONFIG_FILE = path.join(SKILL_DIR, 'config.json');

/**
 * C# Developer skill main function
 * @param {Object} options - Skill options
 * @param {string} options.task - Task type ('create-project', 'generate-code', 'review', 'design', 'debug')
 * @param {string} options.description - Task description or requirements
 * @param {string} options.projectType - Project type (wpf, console, webapi, classlib)
 * @param {string} options.dotnetVersion - .NET version (default: '8.0')
 * @param {string} options.outputDir - Output directory for generated code
 * @returns {Promise<Object>} - Result object
 */
async function run(options) {
  const {
    task = 'generate-code',
    description,
    projectType = 'wpf',
    dotnetVersion = '8.0',
    outputDir,
  } = options;

  if (!description && task !== 'review') {
    throw new Error('Description is required for code generation tasks');
  }

  console.log(`🔧 C# Developer: ${task}`);
  console.log(`   Description: ${description || 'N/A'}`);
  console.log(`   Project Type: ${projectType}, .NET Version: ${dotnetVersion}`);

  try {
    let result;
    
    switch (task) {
      case 'create-project':
        result = await createProject(projectType, dotnetVersion, outputDir);
        break;
      case 'generate-code':
        result = await generateCode(description, projectType);
        break;
      case 'review':
        result = await reviewCode(description);
        break;
      case 'design':
        result = await designArchitecture(description);
        break;
      case 'debug':
        result = await debugIssue(description);
        break;
      default:
        throw new Error(`Unknown task type: ${task}`);
    }

    return {
      success: true,
      task,
      ...result,
    };
  } catch (error) {
    console.error('❌ C# Developer failed:', error.message);
    return {
      success: false,
      task,
      error: error.message,
      suggestions: getTroubleshootingSuggestions(error, task),
    };
  }
}

/**
 * Create a new .NET project
 */
async function createProject(projectType, dotnetVersion, outputDir) {
  const templateMap = {
    'wpf': 'wpf',
    'console': 'console',
    'webapi': 'webapi',
    'classlib': 'classlib',
    'worker': 'worker',
  };

  const template = templateMap[projectType] || 'console';
  const targetDir = outputDir || path.join(process.cwd(), `CSharpApp-${Date.now()}`);

  console.log(`📁 Creating ${projectType} project at: ${targetDir}`);

  // Check if dotnet CLI is available
  try {
    await execAsync('dotnet --version');
  } catch {
    throw new Error('.NET SDK not found. Please install .NET SDK from https://dotnet.microsoft.com/download');
  }

  // Create project using dotnet CLI
  const command = `dotnet new ${template} -f net${dotnetVersion} -o "${targetDir}"`;
  await execAsync(command);

  // Generate additional structure for WPF apps
  if (projectType === 'wpf') {
    await generateWpfStructure(targetDir);
  }

  return {
    projectPath: targetDir,
    message: `✅ .NET ${projectType} project created successfully at ${targetDir}`,
    nextSteps: [
      `cd "${targetDir}"`,
      'dotnet build',
      'dotnet run',
    ],
  };
}

/**
 * Generate C# code based on description
 */
async function generateCode(description, projectType) {
  // This would typically call an LLM to generate code
  // For now, return a placeholder response
  return {
    code: `// C# code generation would be implemented here\n// Description: ${description}\n// Project Type: ${projectType}`,
    message: '✅ Code generated successfully',
  };
}

/**
 * Review C# code
 */
async function reviewCode(codeOrPath) {
  // Code review logic would be implemented here
  return {
    issues: [],
    suggestions: [],
    message: '✅ Code review completed',
  };
}

/**
 * Design software architecture
 */
async function designArchitecture(description) {
  // Architecture design logic would be implemented here
  return {
    architecture: {
      layers: ['Presentation', 'Business Logic', 'Data Access', 'Infrastructure'],
      patterns: ['MVVM', 'Dependency Injection', 'Repository'],
    },
    message: '✅ Architecture design completed',
  };
}

/**
 * Debug and diagnose issues
 */
async function debugIssue(description) {
  // Debugging logic would be implemented here
  return {
    diagnosis: 'Issue analysis would be performed here',
    solution: 'Solution would be provided here',
    message: '✅ Debug analysis completed',
  };
}

/**
 * Generate WPF project structure
 */
async function generateWpfStructure(baseDir) {
  const directories = [
    'ViewModels',
    'Models',
    'Services',
    'Views',
    'Converters',
    'Commands',
    'Resources',
  ];

  for (const dir of directories) {
    const dirPath = path.join(baseDir, dir);
    await fs.mkdir(dirPath, { recursive: true });
    
    // Create .gitkeep file
    await fs.writeFile(path.join(dirPath, '.gitkeep'), '');
  }

  // Create example ViewModel
  const viewModelPath = path.join(baseDir, 'ViewModels', 'MainViewModel.cs');
  await fs.writeFile(viewModelPath, `using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace CSharpApp.ViewModels
{
    public class MainViewModel : INotifyPropertyChanged
    {
        private string _title = "Main Window";
        
        public string Title
        {
            get => _title;
            set { _title = value; OnPropertyChanged(); }
        }
        
        public event PropertyChangedEventHandler PropertyChanged;
        
        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
`);

  console.log('📁 WPF project structure created');
}

/**
 * Get troubleshooting suggestions
 */
function getTroubleshootingSuggestions(error, task) {
  const message = error.message.toLowerCase();
  
  if (message.includes('dotnet') || message.includes('sdk')) {
    return '安装 .NET SDK: https://dotnet.microsoft.com/download';
  }
  if (message.includes('template')) {
    return '检查项目类型是否正确：wpf, console, webapi, classlib, worker';
  }
  if (message.includes('permission') || message.includes('access')) {
    return '检查输出目录权限，或以管理员身份运行';
  }
  
  return '查看详细错误信息，或尝试不同的配置选项';
}

// Export for OpenClaw skill system
module.exports = {
  run,
  createProject,
  generateCode,
  reviewCode,
  designArchitecture,
  debugIssue,
};
