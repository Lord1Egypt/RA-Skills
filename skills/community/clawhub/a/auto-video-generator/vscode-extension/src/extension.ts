import * as vscode from 'vscode';
import { ConfigPanelProvider } from './configPanel';
import { VideoGeneratorManager } from './videoGenerator';
import { EnvironmentDetector } from './environmentDetector';
import { PerformanceDashboardProvider } from './performanceDashboard';

let configPanelProvider: ConfigPanelProvider;
let videoGenerator: VideoGeneratorManager;
let envDetector: EnvironmentDetector;
let perfDashboard: PerformanceDashboardProvider;
let statusBarItem: vscode.StatusBarItem;

export function activate(context: vscode.ExtensionContext) {
    console.log('Auto Video Generator extension is now active');
    
    // Initialize components
    configPanelProvider = new ConfigPanelProvider(context.extensionUri);
    videoGenerator = new VideoGeneratorManager(context);
    envDetector = new EnvironmentDetector();
    perfDashboard = new PerformanceDashboardProvider();
    
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right, 
        100
    );
    statusBarItem.text = "$(device-camera-video) AVG";
    statusBarItem.tooltip = "Auto Video Generator";
    statusBarItem.command = 'avg.openConfigPanel';
    statusBarItem.show();
    
    context.subscriptions.push(statusBarItem);
    
    // Register commands
    registerCommands(context);
    
    // Register views
    registerViews(context);
    
    // Show welcome message on first activation
    showWelcomeMessage(context);
}

function registerCommands(context: vscode.ExtensionContext) {
    
    // Generate video from current file
    const generateVideoCommand = vscode.commands.registerCommand(
        'avg.generateVideo',
        async () => await handleGenerateVideo()
    );
    context.subscriptions.push(generateVideoCommand);
    
    // Generate video from URL
    const generateFromURLCommand = vscode.commands.registerCommand(
        'avg.generateVideoFromURL',
        async () => await handleGenerateFromURL()
    );
    context.subscriptions.push(generateFromURLCommand);
    
    // Open configuration panel
    const openConfigCommand = vscode.commands.registerCommand(
        'avg.openConfigPanel',
        async () => await configPanelProvider.show()
    );
    context.subscriptions.push(openConfigCommand);
    
    // Detect environment
    const detectEnvCommand = vscode.commands.registerCommand(
        'avg.detectEnvironment',
        async () => await handleDetectEnvironment()
    );
    context.subscriptions.push(detectEnvCommand);
    
    // Show performance dashboard
    const showPerfCommand = vscode.commands.registerCommand(
        'avg.showPerformanceDashboard',
        async () => await perfDashboard.show()
    );
    context.subscriptions.push(showPerfCommand);
    
    // Export config template
    const exportConfigCommand = vscode.commands.registerCommand(
        'avg.exportConfigTemplate',
        async () => await handleExportConfigTemplate()
    );
    context.subscriptions.push(exportConfigCommand);
}

function registerViews(context: vscode.ExtensionContext) {
    
    // Register config panel webview
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            'avg-config-panel',
            configPanelProvider
        )
    );
}

async function handleGenerateVideo() {
    const editor = vscode.window.activeTextEditor;
    
    if (!editor) {
        vscode.window.showErrorMessage('No active editor. Please open an HTML/Vue file first.');
        return;
    }
    
    const fileUri = editor.document.uri;
    const filePath = fileUri.fsPath;
    
    if (!filePath.match(/\.(html|vue|tsx|jsx)$/)) {
        vscode.window.showWarningMessage(
            'AVG works best with HTML, Vue, or React files. Continue anyway?'
        );
    }
    
    // Update status bar
    statusBarItem.text = "$(sync~spin) Generating...";
    statusBarItem.tooltip = "Generating video...";
    
    try {
        const outputPath = await videoGenerator.generateFromFile(filePath);
        
        vscode.window.showInformationMessage(
            `Video generated successfully!`,
            'Open Output Folder'
        ).then(selection => {
            if (selection === 'Open Output Folder') {
                vscode.commands.executeCommand(
                    'revealFileInOS', 
                    vscode.Uri.file(outputPath)
                );
            }
        });
        
    } catch (error) {
        vscode.window.showErrorMessage(`Video generation failed: ${error}`);
    } finally {
        statusBarItem.text = "$(device-camera-video) AVG";
        statusBarItem.tooltip = "Auto Video Generator";
    }
}

async function handleGenerateFromURL() {
    const url = await vscode.window.showInputBox({
        prompt: 'Enter the URL to generate video from',
        placeHolder: 'https://example.com/demo.html',
        validateInput: (value) => {
            if (!value || !value.startsWith('http')) {
                return 'Please enter a valid URL (http:// or https://)';
            }
            return undefined;
        }
    });
    
    if (!url) return;
    
    try {
        const outputPath = await videoGenerator.generateFromURL(url);
        
        vscode.window.showInformationMessage(
            `Video generated successfully from URL!`,
            'Open File'
        ).then(selection => {
            if (selection === 'Open File') {
                vscode.commands.executeCommand(
                    'revealFileInOS', 
                    vscode.Uri.file(outputPath)
                );
            }
        });
        
    } catch (error) {
        vscode.window.showErrorMessage(`Generation failed: ${error}`);
    }
}

async function handleDetectEnvironment() {
    await vscode.window.withProgress(
        {
            location: vscode.ProgressLocation.Notification,
            title: "Detecting environment...",
            cancellable: true,
        },
        async (progress, token) => {
            progress.report({ increment: 0, message: "Analyzing workspace..." });
            
            const result = await envDetector.detect(progress, token);
            
            if (token.isCancellationRequested) {
                return;
            }
            
            // Show results in output channel
            const outputChannel = vscode.window.createOutputChannel('AVG Environment Detection');
            outputChannel.clear();
            outputChannel.appendLine('=' .repeat(60));
            outputChannel.appendLine('ENVIRONMENT DETECTION RESULTS');
            outputChannel.appendLine('=' .repeat(60));
            outputChannel.appendLine('');
            
            outputChannel.appendLine('[Framework]');
            outputChannel.appendLine(`  Detected: ${result.framework}`);
            outputChannel.appendLine(`  Confidence: ${(result.confidence * 100).toFixed(1)}%`);
            outputChannel.appendLine('');
            
            outputChannel.appendLine('[Components Found]');
            for (const comp of result.components) {
                outputChannel.appendLine(`  - ${comp}`);
            }
            outputChannel.appendLine('');
            
            outputChannel.appendLine('[Authentication]');
            outputChannel.appendLine(`  Status: ${result.auth.status}`);
            if (result.auth.type) {
                outputChannel.appendLine(`  Type: ${result.auth.type}`);
            }
            outputChannel.appendLine('');
            
            outputChannel.appendLine('[Layout]');
            outputChannel.appendLine(`  Type: ${result.layout.type}`);
            outputChannel.appendLine(`  Sidebar: ${result.layout.hasSidebar ? 'Yes' : 'No'}`);
            outputChannel.appendLine(`  Header: ${result.layout.hasHeader ? 'Yes' : 'No'}`);
            outputChannel.appendLine('');
            
            outputChannel.show(true);
            
            // Update config panel with detected info
            configPanelProvider.updateEnvironmentInfo(result);
            
            vscode.window.showInformationMessage(
                `Environment detected: ${result.framework} (${(result.confidence * 100).toFixed(0)}% confidence)`
            );
        }
    );
}

async function handleExportConfigTemplate() {
    const defaultConfig = `# Auto Video Generator Configuration
# Generated by VS Code Extension

browser:
  headless: false
  viewport_width: 1440
  viewport_height: 900

video:
  fps: 4
  format: mp4
  quality: high

audio:
  engine: edge_tts
  voice: "zh-CN-YunxiNeural"
  rate: "-5%"

recording:
  interaction_mode: real
  clip_sidebar: true
  auto_scroll: true

retry:
  max_attempts: 3
  enable_circuit_breaker: true

logging:
  level: INFO
  console_output: true
`;
    
    const saveUri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file('config.yaml'),
        filters: {
            'YAML': ['yaml'],
            'JSON': ['json']
        },
        title: 'Save AVG Configuration'
    });
    
    if (!saveUri) return;
    
    const content = saveUri.path.endsWith('.json') 
        ? JSON.stringify(parseYaml(defaultConfig), null, 2)
        : defaultConfig;
    
    await vscode.workspace.writeFile(saveUri, Buffer.from(content, 'utf-8'));
    
    const doc = await vscode.workspace.openTextDocument(saveUri);
    await vscode.window.showTextDocument(doc);
    
    vscode.window.showInformationMessage('Configuration template exported!');
}

function parseYaml(yamlStr: string): any {
    // Simple YAML to JSON conversion (for basic cases)
    const result: any = {};
    let currentSection: string | null = null;
    
    for (const line of yamlStr.split('\n')) {
        const trimmed = line.trim();
        
        if (!trimmed || trimmed.startsWith('#')) continue;
        
        if (trimmed.endsWith(':') && !trimmed.startsWith('-')) {
            currentSection = trimmed.replace(':', '').trim();
            result[currentSection] = {};
        } else if (currentSection && trimmed.includes(':')) {
            const [key, value] = trimmed.split(':').map(s => s.trim());
            if (key && value !== undefined) {
                result[currentSection][key] = convertYamlValue(value);
            }
        }
    }
    
    return result;
}

function convertYamlValue(value: string): any {
    if (value === 'true') return true;
    if (value === 'false') return false;
    if (value === 'null' || value === '') return null;
    
    const num = Number(value);
    if (!isNaN(num)) return num;
    
    return value.replace(/"/g, '');
}

function showWelcomeMessage(context: vscode.ExtensionContext) {
    const shownKey = 'avg.welcomeShown';
    
    if (context.globalState.get(shownKey)) {
        return;
    }
    
    context.globalState.update(shownKey, true);
    
    setTimeout(() => {
        vscode.window.showInformationMessage(
            'Welcome to Auto Video Generator v3.0!',
            'Quick Start Guide',
            'Open Config Panel',
            'Dismiss'
        ).then(choice => {
            switch (choice) {
                case 'Quick Start Guide':
                    vscode.env.openExternal(vscode.Uri.parse(
                        'https://github.com/your-org/auto-video-generator#quick-start'
                    ));
                    break;
                    
                case 'Open Config Panel':
                    vscode.commands.executeCommand('avg.openConfigPanel');
                    break;
            }
        });
    }, 2000);
}

export function deactivate() {
    console.log('Auto Video Generator extension deactivated');
}
