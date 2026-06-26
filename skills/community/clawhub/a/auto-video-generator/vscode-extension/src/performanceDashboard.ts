import * as vscode from 'vscode';

export class PerformanceDashboardProvider {
    
    private _panel: vscode.WebviewPanel | undefined;
    private _extensionUri: vscode.Uri;
    private _disposables: vscode.Disposable[] = [];
    
    constructor() {}
    
    public async show() {
        if (this._panel) {
            this._panel.reveal(vscode.ViewColumn.One);
            return;
        }
        
        this._panel = vscode.window.createWebviewPanel(
            'avg-perf-dashboard',
            'AVG Performance Dashboard',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: []
            }
        );
        
        this._panel.webview.html = this._getHtmlForWebview();
        
        this._panel.webview.onDidReceiveMessage(
            message => this._handleMessage(message),
            undefined,
            this._disposables
        );
        
        this._panel.onDidDispose(
            () => { this._panel = undefined; },
            undefined,
            this._disposables
        );
        
        // Simulate real-time data updates
        this._startDataSimulation();
    }
    
    private _handleMessage(message: any) {
        switch (message.command) {
            case 'refresh':
                this._refreshData();
                break;
                
            case 'export':
                this._exportMetrics();
                break;
                
            case 'clear':
                this._clearData();
                break;
        }
    }
    
    private _startDataSimulation() {
        if (!this._panel) return;
        
        // Update data every 2 seconds
        setInterval(() => {
            if (this._panel && this._panel.visible) {
                this._refreshData();
            }
        }, 2000);
    }
    
    private _refreshData() {
        // In a real implementation, this would fetch actual metrics
        // For now, we simulate realistic performance data
        const mockData = this._generateMockMetrics();
        
        this._panel?.webview.postMessage({
            command: 'updateMetrics',
            data: mockData,
            timestamp: new Date().toISOString(),
        });
    }
    
    private _generateMockMetrics(): any {
        return {
            overview: {
                totalVideosGenerated: Math.floor(Math.random() * 50) + 10,
                avgGenerationTime: (Math.random() * 30 + 15).toFixed(1),
                successRate: ((Math.random() * 5 + 94)).toFixed(1),
                activeSessions: Math.floor(Math.random() * 3) + 1,
            },
            
            timings: [
                { name: 'Page Navigation', avg: Math.random() * 2000 + 500, p95: Math.random() * 3000 + 1000 },
                { name: 'Screenshot Capture', avg: Math.random() * 300 + 100, p95: Math.random() * 500 + 200 },
                { name: 'Audio Generation', avg: Math.random() * 5000 + 2000, p95: Math.random() * 8000 + 4000 },
                { name: 'Video Encoding', avg: Math.random() * 8000 + 5000, p95: Math.random() * 12000 + 8000 },
                { name: 'Component Interaction', avg: Math.random() * 500 + 200, p95: Math.random() * 1000 + 400 },
            ],
            
            resourceUsage: {
                cpu: Math.random() * 40 + 20,
                memory: Math.random() * 30 + 40,
                diskUsage: Math.random() * 50 + 30,
            },
            
            recentOperations: Array.from({ length: 8 }, (_, i) => ({
                id: i + 1,
                type: ['Page Load', 'Screenshot', 'Audio Gen', 'Encoding'][Math.floor(Math.random() * 4)],
                duration: (Math.random() * 5000 + 200).toFixed(0),
                status: Math.random() > 0.1 ? 'success' : 'error',
                timestamp: new Date(Date.now() - Math.random() * 3600000).toLocaleTimeString(),
            })),
            
            frameworkStats: {
                'Vue + Ant Design': Math.floor(Math.random() * 60) + 20,
                'React + Ant Design': Math.floor(Math.random() * 40) + 15,
                'Element UI': Math.floor(Math.random() * 25) + 10,
                'Vuetify': Math.floor(Math.random() * 15) + 5,
                'Other': Math.floor(Math.random() * 10) + 2,
            },
        };
    }
    
    private async _exportMetrics() {
        const data = this._generateMockMetrics();
        const exportContent = JSON.stringify(data, null, 2);
        
        const uri = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file('metrics-export.json'),
            filters: { 'JSON': ['json'] },
            title: 'Export Performance Metrics'
        });
        
        if (!uri) return;
        
        await vscode.workspace.writeFile(uri, Buffer.from(exportContent));
        vscode.window.showInformationMessage('Metrics exported successfully!');
    }
    
    private _clearData() {
        vscode.window.showWarningMessage(
            'Clear all performance data?',
            { modal: true },
            'Clear'
        ).then(choice => {
            if (choice === 'Clear') {
                this._refreshData();
                vscode.window.showInformationMessage('Performance data cleared!');
            }
        });
    }
    
    private _getHtmlForWebview(): string {
        const nonce = getNonce();
        
        return /*html*/ `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" 
          content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-${nonce}';">
    <title>Performance Dashboard</title>
    <style>
        :root {
            --bg-primary: var(--vscode-editor-background);
            --bg-secondary: var(--vscode-sideBar-background);
            --text-primary: var(--vscode-foreground);
            --text-secondary: var(--vscode-descriptionForeground);
            --border-color: var(--vscode-panel-border);
            --accent-color: var(--vscode-textLink-foreground);
            --success-color: #238636;
            --warning-color: #d29922;
            --error-color: #da3633;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: var(--vscode-font-family);
            background-color: var(--bg-primary);
            color: var(--text-primary);
            padding: 20px;
            line-height: 1.6;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .header h1 {
            font-size: 22px;
            font-weight: 600;
        }
        
        .timestamp {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .grid {
            display: grid;
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .grid-4 { grid-template-columns: repeat(4, 1fr); }
        .grid-2 { grid-template-columns: repeat(2, 1fr); }
        
        @media (max-width: 900px) {
            .grid-4 { grid-template-columns: repeat(2, 1fr); }
        }
        
        .card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 16px;
        }
        
        .card-title {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }
        
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: var(--accent-color);
        }
        
        .metric-unit {
            font-size: 14px;
            color: var(--text-secondary);
            margin-left: 4px;
        }
        
        .bar-chart {
            height: 120px;
            display: flex;
            align-items: flex-end;
            gap: 12px;
            padding-top: 20px;
        }
        
        .bar {
            flex: 1;
            background: linear-gradient(to top, var(--accent-color), rgba(37, 99, 235, 0.3));
            border-radius: 4px 4px 0 0;
            position: relative;
            transition: height 0.3s ease;
            min-height: 4px;
        }
        
        .bar-label {
            position: absolute;
            bottom: -22px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 10px;
            white-space: nowrap;
            color: var(--text-secondary);
        }
        
        .bar-value {
            position: absolute;
            top: -18px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 11px;
            font-weight: 600;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        
        th, td {
            text-align: left;
            padding: 10px 8px;
            border-bottom: 1px solid var(--border-color);
        }
        
        th {
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 11px;
            text-transform: uppercase;
        }
        
        tr:hover td {
            background-color: rgba(255, 255, 255, 0.02);
        }
        
        .status-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }
        
        .status-success {
            background-color: rgba(35, 134, 54, 0.15);
            color: var(--success-color);
        }
        
        .status-error {
            background-color: rgba(218, 54, 51, 0.15);
            color: var(--error-color);
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background-color: var(--border-color);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }
        
        .progress-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        .actions {
            display: flex;
            gap: 8px;
            margin-top: 16px;
        }
        
        button {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background-color: var(--accent-color);
            color: white;
        }
        
        .btn-primary:hover {
            opacity: 0.9;
        }
        
        .btn-secondary {
            background-color: transparent;
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }
        
        .btn-secondary:hover {
            background-color: var(--border-color);
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Performance Dashboard</h1>
        <span class="timestamp" id="last-updated">Loading...</span>
    </div>

    <!-- Overview Cards -->
    <div class="grid grid-4">
        <div class="card">
            <div class="card-title">Videos Generated</div>
            <div class="metric-value" id="total-videos">--</div>
        </div>
        <div class="card">
            <div class="card-title">Avg Generation Time</div>
            <div class="metric-value" id="avg-time">--<span class="metric-unit">s</span></div>
        </div>
        <div class="card">
            <div class="card-title">Success Rate</div>
            <div class="metric-value" id="success-rate">--<span class="metric-unit">%</span></div>
        </div>
        <div class="card">
            <div class="card-title">Active Sessions</div>
            <div class="metric-value" id="active-sessions">--</div>
        </div>
    </div>

    <!-- Performance Metrics -->
    <div class="grid grid-2">
        <div class="card">
            <div class="card-title">⏱️ Operation Timings (ms)</div>
            <table id="timings-table">
                <thead>
                    <tr>
                        <th>Operation</th>
                        <th>Avg</th>
                        <th>P95</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>

        <div class="card">
            <div class="card-title">💻 Resource Usage</div>
            <div style="margin-top: 16px;">
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px;">
                        <span>CPU Usage</span>
                        <span id="cpu-value">--%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="cpu-bar" 
                             style="background-color: #2563eb;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px;">
                        <span>Memory Usage</span>
                        <span id="memory-value">--%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="memory-bar"
                             style="background-color: #7c3aed;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px;">
                        <span>Disk I/O</span>
                        <span id="disk-value">--%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="disk-bar"
                             style="background-color: #059669;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Framework Stats & Recent Operations -->
    <div class="grid grid-2" style="margin-top: 16px;">
        <div class="card">
            <div class="card-title">🎯 Framework Distribution</div>
            <div class="bar-chart" id="framework-chart"></div>
        </div>

        <div class="card">
            <div class="card-title">📋 Recent Operations</div>
            <table id="operations-table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Duration</th>
                        <th>Status</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <!-- Actions -->
    <div class="actions">
        <button class="btn-primary" onclick="refresh()">🔄 Refresh Now</button>
        <button class="btn-secondary" onclick="exportData()">📤 Export Metrics</button>
        <button class="btn-secondary" onclick="clearData()">🗑️ Clear Data</button>
    </div>

    <script nonce="${nonce}">
        let currentData = null;

        window.addEventListener('message', event => {
            const message = event.data;
            
            if (message.command === 'updateMetrics') {
                currentData = message.data;
                updateUI(currentData);
                document.getElementById('last-updated').textContent = 
                    'Updated: ' + new Date(message.timestamp).toLocaleTimeString();
            }
        });

        function updateUI(data) {
            if (!data) return;

            // Overview metrics
            animateValue('total-videos', data.overview.totalVideosGenerated);
            document.getElementById('avg-time').innerHTML = 
                data.overview.avgGenerationTime + '<span class="metric-unit">s</span>';
            document.getElementById('success-rate').innerHTML = 
                data.overview.successRate + '<span class="metric-unit">%</span>';
            document.getElementById('active-sessions').textContent = 
                data.overview.activeSessions;

            // Timings table
            const timingsBody = document.querySelector('#timings-table tbody');
            timingsBody.innerHTML = data.timings.map(t => \`
                <tr>
                    <td>\${t.name}</td>
                    <td>\${t.avg.toFixed(0)}ms</td>
                    <td>\${t.p95.toFixed(0)}ms</td>
                </tr>
            \`).join('');

            // Resource usage
            updateProgressBar('cpu', data.resourceUsage.cpu);
            updateProgressBar('memory', data.resourceUsage.memory);
            updateProgressBar('disk', data.resourceUsage.diskUsage);

            // Framework chart
            renderFrameworkChart(data.frameworkStats);

            // Recent operations
            const opsBody = document.querySelector('#operations-table tbody');
            opsBody.innerHTML = data.recentOperations.map(op => \`
                <tr>
                    <td>\${op.type}</td>
                    <td>\${op.duration}ms</td>
                    <td><span class="status-badge status-\${op.status}">\${op.status}</span></td>
                    <td>\${op.timestamp}</td>
                </tr>
            \`).join('');
        }

        function animateValue(elementId, endValue) {
            const element = document.getElementById(elementId);
            const startValue = parseInt(element.textContent) || 0;
            const duration = 500;
            const startTime = performance.now();

            function update(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const value = Math.floor(startValue + (endValue - startValue) * progress);
                element.textContent = value;

                if (progress < 1) {
                    requestAnimationFrame(update);
                }
            }

            requestAnimationFrame(update);
        }

        function updateProgressBar(name, percentage) {
            const bar = document.getElementById(name + '-bar');
            const value = document.getElementById(name + '-value');
            
            bar.style.width = percentage + '%';
            value.textContent = percentage.toFixed(1) + '%';
        }

        function renderFrameworkChart(stats) {
            const container = document.getElementById('framework-chart');
            const maxValue = Math.max(...Object.values(stats));
            
            container.innerHTML = Object.entries(stats)
                .sort((a, b) => b[1] - a[1])
                .map(([name, value]) => {
                    const height = (value / maxValue) * 80;
                    const displayName = name.length > 12 ? name.substring(0, 10) + '..' : name;
                    
                    return \`
                        <div class="bar" style="height: \${height}px;">
                            <span class="bar-value">\${value}</span>
                            <span class="bar-label">\${displayName}</span>
                        </div>
                    \`;
                }).join('');
        }

        function refresh() {
            vscode.postMessage({ command: 'refresh' });
        }

        function exportData() {
            vscode.postMessage({ command: 'export' });
        }

        function clearData() {
            vscode.postMessage({ command: 'clear' });
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
