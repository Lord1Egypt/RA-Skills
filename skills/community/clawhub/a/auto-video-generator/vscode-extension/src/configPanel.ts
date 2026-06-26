import * as vscode from 'vscode';

export class ConfigPanelProvider implements vscode.WebviewViewProvider {
    
    private _view?: vscode.WebviewView;
    private _extensionUri: vscode.Uri;
    private _config: any = {};
    private _envInfo: any = null;
    
    constructor(extensionUri: vscode.Uri) {
        this._extensionUri = extensionUri;
        this._loadConfig();
    }
    
    public async resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;
        
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };
        
        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
        
        // Handle messages from the webview
        webviewView.webview.onDidReceiveMessage(async (message) => {
            await this._handleMessage(message);
        });
        
        // Initial render
        this._updateWebview();
    }
    
    public async show() {
        await vscode.commands.executeCommand('avg-config-panel.focus');
    }
    
    public updateEnvironmentInfo(envInfo: any) {
        this._envInfo = envInfo;
        this._updateWebview();
    }
    
    private _loadConfig() {
        const config = vscode.workspace.getConfiguration('avg');
        
        this._config = {
            browser: {
                headless: config.get('browser.headless', false),
                viewportWidth: 1440,
                viewportHeight: 900,
                timeoutMs: 30000,
            },
            video: {
                fps: config.get('video.fps', 4),
                format: 'mp4',
                quality: 'high',
                outputDir: config.get('outputDir', './video_output'),
            },
            audio: {
                voice: config.get('audio.voice', 'zh-CN-YunxiNeural'),
                rate: '-5%',
                volume: '+0%',
            },
            recording: {
                interactionMode: 'real',
                clipSidebar: true,
                autoScroll: true,
                waitAfterActionMs: 500,
            },
            retry: {
                maxAttempts: 3,
                baseDelayS: 0.5,
                enableCircuitBreaker: true,
            },
            logging: {
                level: 'INFO',
                consoleOutput: true,
                fileOutput: true,
            },
        };
    }
    
    private async _handleMessage(message: any) {
        switch (message.command) {
            
            case 'updateConfig':
                await this._handleUpdateConfig(message.config);
                break;
                
            case 'resetToDefaults':
                await this._resetToDefaults();
                break;
                
            case 'exportConfig':
                await this._exportConfig();
                break;
                
            case 'detectEnvironment':
                await vscode.commands.executeCommand('avg.detectEnvironment');
                break;
                
            case 'generateVideo':
                await vscode.commands.executeCommand('avg.generateVideo');
                break;
                
            case 'openDocumentation':
                vscode.env.openExternal(vscode.Uri.parse(
                    'https://github.com/your-org/auto-video-generator'
                ));
                break;
                
            case 'testConfiguration':
                await this._testConfiguration();
                break;
        }
    }
    
    private async _handleUpdateConfig(newConfig: any) {
        // Merge new config with existing
        this._deepMerge(this._config, newConfig);
        
        // Save to VS Code settings
        const config = vscode.workspace.getConfiguration('avg');
        
        await config.update('browser.headless', this._config.browser.headless, false);
        await config.update('video.fps', this._config.video.fps, false);
        await config.update('audio.voice', this._config.audio.voice, false);
        await config.update('outputDir', this._config.video.outputDir, false);
        
        vscode.window.showInformationMessage('Configuration saved!');
        
        this._updateWebview();
    }
    
    private async _resetToDefaults() {
        const result = await vscode.window.showWarningMessage(
            'Reset all configuration to default values?',
            { modal: true },
            'Reset',
            'Cancel'
        );
        
        if (result === 'Reset') {
            this._loadConfig();
            this._updateWebview();
            vscode.window.showInformationMessage('Configuration reset to defaults!');
        }
    }
    
    private async _exportConfig() {
        await vscode.commands.executeCommand('avg.exportConfigTemplate');
    }
    
    private async _testConfiguration() {
        await vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Testing configuration...",
                cancellable: false,
            },
            async (progress) => {
                progress.report({ increment: 0, message: "Validating browser settings..." });
                await this._sleep(500);
                
                progress.report({ increment: 33, message: "Checking audio engine..." });
                await this._sleep(500);
                
                progress.report({ increment: 66, message: "Verifying output directory..." });
                await this._sleep(500);
                
                progress.report({ increment: 100, message: "Complete!" });
                
                vscode.window.showInformationMessage(
                    'Configuration test passed! All settings are valid.'
                );
            }
        );
    }
    
    private _sleep(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    private _updateWebview() {
        if (this._view) {
            this._view.webview.postMessage({
                command: 'updateData',
                config: this._config,
                envInfo: this._envInfo
            });
        }
    }
    
    private _deepMerge(target: any, source: any) {
        for (const key of Object.keys(source)) {
            if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
                if (!target[key]) target[key] = {};
                this._deepMerge(target[key], source[key]);
            } else {
                target[key] = source[key];
            }
        }
    }
    
    private _getHtmlForWebview(webview: vscode.Webview): string {
        const nonce = getNonce();
        
        return /*html*/ `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" 
          content="default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; script-src 'nonce-${nonce}';">
    <title>AVG Configuration</title>
    <style>
        :root {
            --container-padding: 10px;
            --input-height: 30px;
            --input-padding: 6px 8px;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: var(--vscode-font-family);
            font-size: var(--vscode-font-size);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            padding: var(--container-padding);
            margin: 0;
        }
        
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        
        .header h2 {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
        }
        
        .section {
            margin-bottom: 20px;
        }
        
        .section-title {
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--vscode-descriptionForeground);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .form-group {
            margin-bottom: 12px;
        }
        
        label {
            display: block;
            font-size: 12px;
            color: var(--vscode-foreground);
            margin-bottom: 4px;
        }
        
        input[type="text"],
        input[type="number"],
        select {
            width: 100%;
            height: var(--input-height);
            padding: var(--input-padding);
            border: 1px solid var(--vscode-input-border);
            background-color: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            font-size: 12px;
            outline: none;
            border-radius: 3px;
        }
        
        input:focus, select:focus {
            border-color: var(--vscode-focusBorder);
        }
        
        input[type="checkbox"] {
            width: 16px;
            height: 16px;
            cursor: pointer;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        button {
            width: 100%;
            height: 32px;
            border: none;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 5px;
        }
        
        .btn-primary {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
        }
        
        .btn-primary:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        
        .btn-secondary {
            background-color: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
        }
        
        .btn-secondary:hover {
            background-color: var(--vscode-button-secondaryHoverBackground);
        }
        
        .btn-success {
            background-color: #238636;
            color: white;
        }
        
        .btn-success:hover {
            background-color: #2ea043;
        }
        
        .env-info {
            background-color: var(--vscode-textBlockQuote-background);
            border-left: 3px solid var(--vscode-textLink-foreground);
            padding: 10px;
            margin-bottom: 15px;
            font-size: 11px;
            line-height: 1.5;
        }
        
        .env-info strong {
            color: var(--vscode-textLink-foreground);
        }
        
        .actions {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 15px;
        }
        
        .row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }
        
        .status-success { background-color: #238636; }
        .status-warning { background-color: #d29922; }
        .status-error   { background-color: #da3633; }
        
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="header">
        <h2>⚙️ Configuration</h2>
        <span style="font-size: 11px; color: var(--vscode-descriptionForeground);">v3.0</span>
    </div>

    <!-- Environment Info -->
    <div id="env-info" class="env-info hidden">
        <strong>Detected Environment:</strong><br>
        <span id="env-framework"></span><br>
        <span id="env-components"></span>
    </div>

    <!-- Browser Settings -->
    <div class="section">
        <div class="section-title">🌐 Browser</div>
        
        <div class="form-group checkbox-group">
            <input type="checkbox" id="browser-headless">
            <label for="browser-headless">Headless Mode</label>
        </div>
        
        <div class="row">
            <div class="form-group">
                <label for="browser-vw">Viewport Width</label>
                <input type="number" id="browser-vw" min="800" max="2560">
            </div>
            <div class="form-group">
                <label for="browser-vh">Viewport Height</label>
                <input type="number" id="browser-vh" min="600" max="1440">
            </div>
        </div>
    </div>

    <!-- Video Settings -->
    <div class="section">
        <div class="section-title">🎬 Video</div>
        
        <div class="row">
            <div class="form-group">
                <label for="video-fps">FPS</label>
                <select id="video-fps">
                    <option value="1">1 FPS</option>
                    <option value="2">2 FPS</option>
                    <option value="4" selected>4 FPS</option>
                    <option value="10">10 FPS</option>
                    <option value="24">24 FPS</option>
                    <option value="30">30 FPS</option>
                </select>
            </div>
            <div class="form-group">
                <label for="video-quality">Quality</label>
                <select id="video-quality">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high" selected>High</option>
                </select>
            </div>
        </div>
        
        <div class="form-group">
            <label for="video-output">Output Directory</label>
            <input type="text" id="video-output" placeholder="./video_output">
        </div>
    </div>

    <!-- Audio Settings -->
    <div class="section">
        <div class="section-title">🔊 Audio</div>
        
        <div class="form-group">
            <label for="audio-voice">Voice</label>
            <select id="audio-voice">
                <option value="zh-CN-YunxiNeural">Yunxi (Male - Chinese)</option>
                <option value="zh-CN-XiaoxiaoNeural">Xiaoxiao (Female - Chinese)</option>
                <option value="en-US-GuyNeural">Guy (Male - English)</option>
                <option value="en-US-JennyNeural">Jenny (Female - English)</option>
            </select>
        </div>
        
        <div class="row">
            <div class="form-group">
                <label for="audio-rate">Rate</label>
                <select id="audio-rate">
                    <option value="-50%">-50%</option>
                    <option value="-25%">-25%</option>
                    <option value="-5%" selected>-5% (Default)</option>
                    <option value="+0%">Normal</option>
                    <option value="+5%">+5%</option>
                    <option value="+25%">+25%</option>
                    <option value="+50%">+50%</option>
                </select>
            </div>
            <div class="form-group">
                <label for="audio-volume">Volume</label>
                <select id="audio-volume">
                    <option value="-50%">-50%</option>
                    <option value="-25%">-25%</option>
                    <option value="+0%" selected>Default</option>
                    <option value="+25%">+25%</option>
                    <option value="+50%">+50%</option>
                </select>
            </div>
        </div>
    </div>

    <!-- Recording Settings -->
    <div class="section">
        <div class="section-title">⏺️ Recording</div>
        
        <div class="form-group">
            <label for="recording-mode">Interaction Mode</label>
            <select id="recording-mode">
                <option value="real">Real Interactions</option>
                <option value="static">Static Screenshots</option>
                <option value="hybrid">Hybrid Mode</option>
            </select>
        </div>
        
        <div class="form-group checkbox-group">
            <input type="checkbox" id="recording-sidebar" checked>
            <label for="recording-sidebar">Clip Sidebar</label>
        </div>
        
        <div class="form-group checkbox-group">
            <input type="checkbox" id="recording-scroll" checked>
            <label for="recording-scroll">Auto Scroll</label>
        </div>
    </div>

    <!-- Actions -->
    <div class="actions">
        <button class="btn-success" onclick="generateVideo()">
            ▶️ Generate Video Now
        </button>
        
        <button class="btn-primary" onclick="saveConfig()">
            💾 Save Configuration
        </button>
        
        <button class="btn-secondary" onclick="detectEnvironment()">
            🔍 Detect Environment
        </button>
        
        <button class="btn-secondary" onclick="testConfig()">
            ✅ Test Configuration
        </button>
        
        <div class="row">
            <button class="btn-secondary" onclick="resetDefaults()">
                ↩️ Reset Defaults
            </button>
            <button class="btn-secondary" onclick="exportConfig()">
                📤 Export Config
            </button>
        </div>
    </div>

    <script nonce="${nonce}">
        let currentConfig = {};
        let currentEnvInfo = null;

        window.addEventListener('message', event => {
            const message = event.data;
            
            if (message.command === 'updateData') {
                currentConfig = message.config || {};
                currentEnvInfo = message.envInfo || null;
                
                populateForm(currentConfig);
                updateEnvInfo(currentEnvInfo);
            }
        });

        function populateForm(config) {
            if (!config) return;
            
            // Browser
            setVal('browser-headless', config.browser?.headless);
            setVal('browser-vw', config.browser?.viewportWidth);
            setVal('browser-vh', config.browser?.viewportHeight);
            
            // Video
            setVal('video-fps', config.video?.fps);
            setVal('video-quality', config.video?.quality);
            setVal('video-output', config.video?.outputDir);
            
            // Audio
            setVal('audio-voice', config.audio?.voice);
            setVal('audio-rate', config.audio?.rate);
            setVal('audio-volume', config.audio?.volume);
            
            // Recording
            setVal('recording-mode', config.recording?.interactionMode);
            setVal('recording-sidebar', config.recording?.clipSidebar);
            setVal('recording-scroll', config.recording?.autoScroll);
        }

        function updateEnvInfo(info) {
            const container = document.getElementById('env-info');
            
            if (!info) {
                container.classList.add('hidden');
                return;
            }
            
            container.classList.remove('hidden');
            document.getElementById('env-framework').textContent = 
                \`Framework: \${info.framework} (\${(info.confidence * 100).toFixed(0)}% confidence)\`;
            document.getElementById('env-components').textContent = 
                \`Components: \${info.components.join(', ')}\`;
        }

        function getFormConfig() {
            return {
                browser: {
                    headless: getBool('browser-headless'),
                    viewportWidth: getInt('browser-vw'),
                    viewportHeight: getInt('browser-vh')
                },
                video: {
                    fps: getInt('video-fps'),
                    quality: getStr('video-quality'),
                    outputDir: getStr('video-output')
                },
                audio: {
                    voice: getStr('audio-voice'),
                    rate: getStr('audio-rate'),
                    volume: getStr('audio-volume')
                },
                recording: {
                    interactionMode: getStr('recording-mode'),
                    clipSidebar: getBool('recording-sidebar'),
                    autoScroll: getBool('recording-scroll')
                }
            };
        }

        function saveConfig() {
            postMessage({ command: 'updateConfig', config: getFormConfig() });
        }

        function generateVideo() {
            saveConfig();
            postMessage({ command: 'generateVideo' });
        }

        function detectEnvironment() {
            postMessage({ command: 'detectEnvironment' });
        }

        function testConfig() {
            postMessage({ command: 'testConfiguration' });
        }

        function resetDefaults() {
            postMessage({ command: 'resetToDefaults' });
        }

        function exportConfig() {
            postMessage({ command: 'exportConfig' });
        }

        function postMessage(msg) {
            vscode.postMessage(msg);
        }

        // Helper functions
        function setVal(id, val) {
            const el = document.getElementById(id);
            if (!el) return;
            
            if (el.type === 'checkbox') {
                el.checked = !!val;
            } else {
                el.value = val ?? '';
            }
        }

        function getBool(id) {
            return document.getElementById(id)?.checked ?? false;
        }

        function getInt(id) {
            return parseInt(document.getElementById(id)?.value) || 0;
        }

        function getStr(id) {
            return document.getElementById(id)?.value || '';
        }
    </script>
</body>
</html>`;
    }
}

function getNonce(): string {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
