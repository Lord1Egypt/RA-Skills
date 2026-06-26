import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn, ChildProcess } from 'child_process';

export class VideoGeneratorManager {
    
    private _context: vscode.ExtensionContext;
    private _currentProcess: ChildProcess | null = null;
    private _outputChannel: vscode.OutputChannel;
    private _isGenerating: boolean = false;
    
    constructor(context: vscode.ExtensionContext) {
        this._context = context;
        this._outputChannel = vscode.window.createOutputChannel('AVG Video Generator');
    }
    
    public async generateFromFile(filePath: string): Promise<string> {
        const fileUri = vscode.Uri.file(filePath);
        
        return await this._generateWithProgress(async (progress) => {
            progress.report({ 
                increment: 0, 
                message: `Preparing: ${path.basename(filePath)}` 
            });
            
            // Read file content
            const document = await vscode.workspace.openTextDocument(fileUri);
            const htmlContent = document.getText();
            
            progress.report({ increment: 10, message: "Analyzing page structure..." });
            
            // Generate video using Python script
            const outputPath = await this._runPythonScript(
                'generate_from_file',
                ['--file', filePath]
            );
            
            return outputPath;
        }, path.basename(filePath));
    }
    
    public async generateFromURL(url: string): Promise<string> {
        return await this._generateWithProgress(async (progress) => {
            progress.report({ 
                increment: 0, 
                message: `Fetching: ${url}` 
            });
            
            const outputPath = await this._runPythonScript(
                'generate_from_url',
                ['--url', url]
            );
            
            return outputPath;
        }, url);
    }
    
    public async generateFromPRD(prdPath: string): Promise<string> {
        return await this._generateWithProgress(async (progress) => {
            progress.report({ 
                increment: 0, 
                message: `Parsing PRD: ${path.basename(prdPath)}` 
            });
            
            const outputPath = await this._runPythonScript(
                'generate_from_prd',
                ['--prd', prdPath]
            );
            
            return outputPath;
        }, path.basename(prdPath));
    }
    
    public isGenerating(): boolean {
        return this._isGenerating;
    }
    
    public cancelGeneration() {
        if (this._currentProcess) {
            this._currentProcess.kill();
            this._currentProcess = null;
            this._isGenerating = false;
            this._outputChannel.appendLine('\n[Cancelled] Generation cancelled by user');
        }
    }
    
    private async _generateWithProgress(
        generatorFn: (progress: Progress<{message?: string}>) => Promise<string>,
        sourceName: string
    ): Promise<string> {
        
        if (this._isGenerating) {
            throw new Error('Another generation is already in progress');
        }
        
        this._isGenerating = true;
        this._outputChannel.clear();
        this._outputChannel.show(true);
        this._outputChannel.appendLine('=' .repeat(60));
        this._outputChannel.appendLine('VIDEO GENERATION STARTED');
        this._outputChannel.appendLine(`Source: ${sourceName}`);
        this._outputChannel.appendLine(`Time: ${new Date().toLocaleString()}`);
        this._outputChannel.appendLine('=' .repeat(60));
        
        try {
            const result = await vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: "Generating Video...",
                    cancellable: true,
                },
                async (progress, token) => {
                    token.onCancellationRequested(() => {
                        this.cancelGeneration();
                    });
                    
                    return await generatorFn(progress);
                }
            );
            
            this._outputChannel.appendLine('\n' + '='.repeat(60));
            this._outputChannel.appendLine('GENERATION COMPLETED SUCCESSFULLY!');
            this._outputChannel.appendLine(`Output: ${result}`);
            this._outputChannel.appendLine('=' .repeat(60));
            
            return result;
            
        } catch (error) {
            this._outputChannel.appendLine('\n' + '='.repeat(60));
            this._outputChannel.appendLine('GENERATION FAILED');
            this._outputChannel.appendLine(`Error: ${error}`);
            this._outputChannel.appendLine('=' .repeat(60));
            
            throw error;
            
        } finally {
            this._isGenerating = false;
            this._currentProcess = null;
        }
    }
    
    private async _runPythonScript(
        command: string,
        args: string[]
    ): Promise<string> {
        return new Promise((resolve, reject) => {
            this._outputChannel.appendLine(`\n[Command] python integrated_video_generator.py ${args.join(' ')}`);
            
            // Find the Python script location
            const extensionPath = this._context.extensionPath;
            const scriptPath = path.join(
                extensionPath, 
                '..', 
                'integrated_video_generator.py'
            );
            
            if (!fs.existsSync(scriptPath)) {
                reject(new Error(`Script not found: ${scriptPath}`));
                return;
            }
            
            this._currentProcess = spawn('python', [scriptPath, ...args], {
                cwd: path.dirname(scriptPath),
                env: { ...process.env },
            });
            
            let stdout = '';
            let stderr = '';
            
            this._currentProcess.stdout?.on('data', (data) => {
                const output = data.toString();
                stdout += output;
                this._outputChannel.append(output);
            });
            
            this._currentProcess.stderr?.on('data', (data) => {
                const output = data.toString();
                stderr += output;
                this._outputChannel.append(`[STDERR] ${output}`);
            });
            
            this._currentProcess.on('close', (code) => {
                this._currentProcess = null;
                
                if (code === 0) {
                    // Extract output path from stdout
                    const match = stdout.match(/Output:\s*(.+\.mp4)/i);
                    const outputPath = match ? match[1].trim() : 'video_output/demo.mp4';
                    resolve(outputPath);
                } else {
                    reject(new Error(`Process exited with code ${code}: ${stderr || stdout}`));
                }
            });
            
            this._currentProcess.on('error', (err) => {
                this._currentProcess = null;
                reject(new Error(`Failed to start process: ${err.message}`));
            });
        });
    }
}

interface Progress<T> {
    report(value: T): void;
}
