import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export interface EnvironmentInfo {
    framework: string;
    confidence: number;
    components: string[];
    auth: {
        status: 'detected' | 'not_detected';
        type?: string;
    };
    layout: {
        type: 'sidebar' | 'topnav' | 'dashboard' | 'unknown';
        hasSidebar: boolean;
        hasHeader: boolean;
    };
}

export class EnvironmentDetector {
    
    private _outputChannel: vscode.OutputChannel;
    
    constructor() {
        this._outputChannel = vscode.window.createOutputChannel('AVG Environment Detector');
    }
    
    public async detect(
        progress?: { report: (value: { increment: number; message: string }) => void },
        token?: vscode.CancellationToken
    ): Promise<EnvironmentInfo> {
        
        const workspaceFolders = vscode.workspace.workspaceFolders;
        
        if (!workspaceFolders || workspaceFolders.length === 0) {
            throw new Error('No workspace folder open');
        }
        
        const rootPath = workspaceFolders[0].uri.fsPath;
        
        progress?.report({ increment: 10, message: "Scanning project files..." });
        
        if (token?.isCancellationRequested) throw new Error('Cancelled');
        
        // Detect framework from package.json, dependencies, etc.
        const framework = await this._detectFramework(rootPath);
        
        progress?.report({ increment: 30, message: `Detected framework: ${framework.name}` });
        
        if (token?.isCancellationRequested) throw new Error('Cancelled');
        
        // Detect UI components used
        const components = await this._detectComponents(rootPath);
        
        progress?.report({ increment: 50, message: `Found ${components.length} component types` });
        
        if (token?.isCancellationRequested) throw new Error('Cancelled');
        
        // Detect authentication pattern
        const auth = await this._detectAuth(rootPath);
        
        progress?.report({ increment: 70, message: "Analyzing layout patterns..." });
        
        if (token?.isCancellationRequested) throw new Error('Cancelled');
        
        // Detect layout structure
        const layout = await this._detectLayout(rootPath);
        
        progress?.report({ increment: 90, message: "Compiling results..." });
        
        if (token?.isCancellationRequested) throw new Error('Cancelled');
        
        const result: EnvironmentInfo = {
            framework: framework.name,
            confidence: framework.confidence,
            components: components,
            auth: auth,
            layout: layout,
        };
        
        // Log results
        this._logDetectionResult(result);
        
        progress?.report({ increment: 100, message: "Complete!" });
        
        return result;
    }
    
    private async _detectFramework(rootPath: string): Promise<{name: string, confidence: number}> {
        let scores: Record<string, number> = {
            'Vue + Ant Design Vue': 0,
            'React + Ant Design': 0,
            'Element UI': 0,
            'Vuetify': 0,
            'Naive UI': 0,
            'Arco Design': 0,
            'Unknown': 0,
        };
        
        // Check package.json
        const pkgPath = path.join(rootPath, 'package.json');
        if (fs.existsSync(pkgPath)) {
            try {
                const pkgContent = fs.readFileSync(pkgPath, 'utf-8');
                const pkg = JSON.parse(pkgContent);
                const deps = { ...pkg.dependencies, ...pkg.devDependencies };
                
                if (deps['ant-design-vue']) scores['Vue + Ant Design Vue'] += 40;
                if (deps['antd'] || deps['@ant-design/pro-components']) scores['React + Ant Design'] += 40;
                if (deps['element-plus'] || deps['element-ui']) scores['Element UI'] += 40;
                if (deps['vuetify']) scores['Vuetify'] += 40;
                if (deps['naive-ui']) scores['Naive UI'] += 40;
                if (deps['@arco-design/web-vue']) scores['Arco Design'] += 40;
                
                if (deps['vue'] && !deps['react']) {
                    scores['Vue + Ant Design Vue'] += 10;
                    scores['Naive UI'] += 5;
                    scores['Arco Design'] += 5;
                }
                
                if (deps['react'] && !deps['vue']) {
                    scores['React + Ant Design'] += 10;
                }
                
            } catch (e) {
                console.error('Error reading package.json:', e);
            }
        }
        
        // Check source files for imports
        const sourceFiles = await this._findSourceFiles(rootPath);
        
        for (const file of sourceFiles.slice(0, 20)) { // Limit to first 20 files
            try {
                const content = fs.readFileSync(file, 'utf-8').toLowerCase();
                
                if (content.includes('ant-design-vue') || content.includes('antdv')) 
                    scores['Vue + Ant Design Vue'] += 5;
                    
                if (content.includes('antd') || content.includes('@ant-design')) 
                    scores['React + Ant Design'] += 5;
                    
                if (content.includes('element-plus') || content.includes('element-ui'))
                    scores['Element UI'] += 5;
                    
                if (content.includes('vuetify'))
                    scores['Vuetify'] += 5;
                    
                if (content.includes('naive-ui'))
                    scores['Naive UI'] += 5;
                    
                if (content.includes('arco-design'))
                    scores['Arco Design'] += 5;
                    
            } catch (e) {
                // Skip files that can't be read
            }
        }
        
        // Find highest scoring framework
        let maxScore = 0;
        let detectedFramework = 'Unknown';
        
        for (const [framework, score] of Object.entries(scores)) {
            if (score > maxScore) {
                maxScore = score;
                detectedFramework = framework;
            }
        }
        
        return {
            name: detectedFramework,
            confidence: Math.min(maxScore / 100, 1.0),
        };
    }
    
    private async _detectComponents(rootPath: string): Promise<string[]> {
        const components: Set<string> = new Set();
        const sourceFiles = await this._findSourceFiles(rootPath);
        
        const componentPatterns: Record<string, RegExp[]> = {
            'Table': [/a-table|el-table|v-data-table|a-table|n-data-table/],
            'Form': [/a-form|el-form|v-form|n-form/],
            'Modal/Dialog': [/a-modal|el-dialog|v-dialog|n-modal/],
            'DatePicker': [/a-datepicker|el-date-picker|v-date-picker|n-date-picker/],
            'Upload': [/a-upload|el-upload|v-file-input|n-upload/],
            'Tabs': [/a-tabs|el-tabs|v-tabs|n-tabs/],
            'Tree': [/a-tree|el-tree|v-tree-view|n-tree/],
            'Chart': [/echarts|chart\.js|highcharts|d3/i],
            'Button': [/a-button|el-button|v-btn|n-button/],
            'Input': [/a-input|el-input|v-text-field|n-input/],
        };
        
        for (const file of sourceFiles.slice(0, 30)) {
            try {
                const content = fs.readFileSync(file, 'utf-8');
                
                for (const [componentName, patterns] of Object.entries(componentPatterns)) {
                    for (const pattern of patterns) {
                        if (pattern.test(content)) {
                            components.add(componentName);
                        }
                    }
                }
            } catch (e) {
                // Skip unreadable files
            }
        }
        
        return Array.from(components).sort();
    }
    
    private async _detectAuth(rootPath: string): Promise<{
        status: 'detected' | 'not_detected',
        type?: string
    }> {
        const authIndicators = [
            { pattern: /jwt|json.?web.?token/i, type: 'JWT' },
            { pattern: /oauth|openid/i, type: 'OAuth' },
            { pattern: /session|cookie.*auth/i, type: 'Session' },
            { pattern: /login|authenticate/i, type: 'Basic Auth' },
        ];
        
        const sourceFiles = await this._findSourceFiles(rootPath);
        
        for (const file of sourceFiles.slice(0, 15)) {
            try {
                const content = fs.readFileSync(file, 'utf-8');
                
                for (const indicator of authIndicators) {
                    if (indicator.pattern.test(content)) {
                        return {
                            status: 'detected',
                            type: indicator.type,
                        };
                    }
                }
            } catch (e) {
                continue;
            }
        }
        
        return { status: 'not_detected' };
    }
    
    private async _detectLayout(rootPath: string): Promise<{
        type: 'sidebar' | 'topnav' | 'dashboard' | 'unknown',
        hasSidebar: boolean,
        hasHeader: boolean
    }> {
        let sidebarScore = 0;
        let topnavScore = 0;
        let dashboardScore = 0;
        
        const sourceFiles = await this._findSourceFiles(rootPath);
        
        const sidebarPatterns = [
            /sidebar|sider|side-menu/i,
            /layout-sider|el-aside/i,
            /v-navigation-drawer/i,
        ];
        
        const headerPatterns = [
            /header|navbar|topbar/i,
            /layout-header|el-header/i,
            /v-app-bar|v-toolbar/i,
        ];
        
        const dashboardPatterns = [
            /dashboard|overview|home-page/i,
            /grid-layout|card-grid/i,
            /statistics|analytics/i,
        ];
        
        for (const file of sourceFiles.slice(0, 25)) {
            try {
                const content = fs.readFileSync(file, 'utf-8');
                
                for (const pattern of sidebarPatterns) {
                    if (pattern.test(content)) sidebarScore++;
                }
                
                for (const pattern of headerPatterns) {
                    if (pattern.test(content)) topnavScore++;
                }
                
                for (const pattern of dashboardPatterns) {
                    if (pattern.test(content)) dashboardScore++;
                }
            } catch (e) {
                continue;
            }
        }
        
        let type: 'sidebar' | 'topnav' | 'dashboard' | 'unknown' = 'unknown';
        
        if (sidebarScore > topnavScore && sidebarScore > dashboardScore) {
            type = 'sidebar';
        } else if (topnavScore > sidebarScore && topnavScore > dashboardScore) {
            type = 'topnav';
        } else if (dashboardScore > 2) {
            type = 'dashboard';
        }
        
        return {
            type,
            hasSidebar: sidebarScore > 0,
            hasHeader: topnavScore > 0,
        };
    }
    
    private async _findSourceFiles(rootPath: string): Promise<string[]> {
        const extensions = ['.vue', '.tsx', '.jsx', '.ts', '.js'];
        const files: string[] = [];
        
        async function scanDir(dir: string, depth: number = 0) {
            if (depth > 3) return; // Limit depth to avoid performance issues
            
            try {
                const entries = fs.readdirSync(dir, { withFileTypes: true });
                
                for (const entry of entries) {
                    if (entry.name.startsWith('.') || 
                        entry.name === 'node_modules' ||
                        entry.name === 'dist' ||
                        entry.name === '.git') {
                        continue;
                    }
                    
                    const fullPath = path.join(dir, entry.name);
                    
                    if (entry.isDirectory()) {
                        await scanDir(fullPath, depth + 1);
                    } else if (extensions.some(ext => entry.name.endsWith(ext))) {
                        files.push(fullPath);
                    }
                }
            } catch (e) {
                // Skip directories that can't be read
            }
        }
        
        await scanDir(rootPath);
        return files;
    }
    
    private _logDetectionResult(result: EnvironmentInfo) {
        this._outputChannel.clear();
        this._outputChannel.show(true);
        
        this._outputChannel.appendLine('=' .repeat(60));
        this._outputChannel.appendLine('ENVIRONMENT DETECTION REPORT');
        this._outputChannel.appendLine(`Time: ${new Date().toLocaleString()}`);
        this._outputChannel.appendLine('=' .repeat(60));
        this._outputChannel.appendLine('');
        
        this._outputChannel.appendLine('[FRAMEWORK]');
        this._outputChannel.appendLine(`  Name:       ${result.framework}`);
        this._outputChannel.appendLine(`  Confidence: ${(result.confidence * 100).toFixed(1)}%`);
        this._outputChannel.appendLine('');
        
        this._outputChannel.appendLine('[COMPONENTS]');
        if (result.components.length > 0) {
            result.components.forEach(comp => {
                this._outputChannel.appendLine(`  - ${comp}`);
            });
        } else {
            this._outputChannel.appendLine('  No specific components detected');
        }
        this._outputChannel.appendLine('');
        
        this._outputChannel.appendLine('[AUTHENTICATION]');
        this._outputChannel.appendLine(`  Status: ${result.auth.status.toUpperCase()}`);
        if (result.auth.type) {
            this._outputChannel.appendLine(`  Type:   ${result.auth.type}`);
        }
        this._outputChannel.appendLine('');
        
        this._outputChannel.appendLine('[LAYOUT]');
        this._outputChannel.appendLine(`  Type:     ${result.layout.type}`);
        this._outputChannel.appendLine(`  Sidebar:  ${result.layout.hasSidebar ? 'Yes' : 'No'}`);
        this._outputChannel.appendLine(`  Header:   ${result.layout.hasHeader ? 'Yes' : 'No'}`);
        this._outputChannel.appendLine('');
        
        this._outputChannel.appendLine('=' .repeat(60));
    }
}
