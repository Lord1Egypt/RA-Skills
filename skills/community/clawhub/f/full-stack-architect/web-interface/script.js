// 全局变量
let prdFiles = [];
let executionLogs = [];
let patterns = [];

// 页面加载完成后执行
window.addEventListener('DOMContentLoaded', function() {
    // 初始化页面
    initPage();
    
    // 模拟数据加载
    loadMockData();
    
    // 每5秒刷新一次数据
    setInterval(loadMockData, 5000);
});

// 初始化页面
function initPage() {
    console.log('初始化页面...');
    // 这里可以添加页面初始化逻辑
}

// 加载模拟数据
function loadMockData() {
    console.log('加载模拟数据...');
    
    // 模拟PRD文件数据
    prdFiles = [
        {
            id: 1,
            name: 'prd-测试电商平台_20260425_140311.md',
            created: '2026-04-25 14:03:11',
            path: 'prd-files/prd-测试电商平台_20260425_140311.md'
        },
        {
            id: 2,
            name: 'prd-测试SaaS平台_20260425_135000.md',
            created: '2026-04-25 13:50:00',
            path: 'prd-files/prd-测试SaaS平台_20260425_135000.md'
        }
    ];
    
    // 模拟执行日志
    executionLogs = [
        '[2026-04-25 14:03:11] 开始生成PRD: 测试电商平台',
        '[2026-04-25 14:03:11] PRD生成完成: prd-测试电商平台_20260425_140311.md',
        '[2026-04-25 13:59:28] 开始更新知识库...',
        '[2026-04-25 13:59:28] 知识库索引已更新',
        '[2026-04-25 13:59:28] 开始创建备份...',
        '[2026-04-25 13:59:28] 备份成功创建: full-stack-architect-backup_20260425_135928.tar.gz'
    ];
    
    // 模拟模式库数据
    patterns = [
        {
            id: 1,
            name: 'JWT认证实现',
            domain: '后端认证',
            description: '使用JWT进行无状态认证的实现方案',
            example: 'const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: "1h" });'
        },
        {
            id: 2,
            name: 'React组件模式',
            domain: '前端开发',
            description: '可复用的React组件设计模式',
            example: 'const Button = ({ children, variant = "primary" }) => <button className={`btn btn-${variant}`}>{children}</button>;'
        }
    ];
    
    // 更新页面
    updateDashboard();
    updatePRDFiles();
    updateExecutionLogs();
    updatePatterns();
}

// 更新仪表盘
function updateDashboard() {
    // 更新PRD文件数量
    document.getElementById('prd-count').textContent = prdFiles.length;
    
    // 更新执行状态
    document.getElementById('execution-status').textContent = '正常';
    
    // 更新模式数量
    document.getElementById('pattern-count').textContent = patterns.length;
    
    // 更新最近执行时间
    if (executionLogs.length > 0) {
        const lastLog = executionLogs[0];
        const timestampMatch = lastLog.match(/\[(.*?)\]/);
        if (timestampMatch) {
            document.getElementById('last-execution').textContent = timestampMatch[1];
        }
    }
}

// 更新PRD文件列表
function updatePRDFiles() {
    const fileList = document.getElementById('prd-file-list');
    
    if (prdFiles.length === 0) {
        fileList.innerHTML = `
            <tr>
                <td colspan="3" class="empty-state">暂无PRD文件</td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    prdFiles.forEach(file => {
        html += `
            <tr>
                <td>${file.name}</td>
                <td>${file.created}</td>
                <td>
                    <div class="action-buttons">
                        <button class="view-button" onclick="viewFile('${file.path}')">查看</button>
                        <button class="download-button" onclick="downloadFile('${file.path}')">下载</button>
                    </div>
                </td>
            </tr>
        `;
    });
    
    fileList.innerHTML = html;
}

// 更新执行日志
function updateExecutionLogs() {
    const logContent = document.getElementById('execution-log-content');
    
    if (executionLogs.length === 0) {
        logContent.textContent = '暂无执行日志';
        return;
    }
    
    logContent.textContent = executionLogs.join('\n');
    
    // 滚动到底部
    logContent.scrollTop = logContent.scrollHeight;
}

// 更新模式库
function updatePatterns() {
    const patternContent = document.getElementById('pattern-content');
    
    if (patterns.length === 0) {
        patternContent.innerHTML = '<p>暂无模式</p>';
        return;
    }
    
    let html = '';
    patterns.forEach(pattern => {
        html += `
            <div class="pattern-item">
                <h3>${pattern.name}</h3>
                <p><strong>领域：</strong>${pattern.domain}</p>
                <p><strong>描述：</strong>${pattern.description}</p>
                <p><strong>示例：</strong></p>
                <pre>${pattern.example}</pre>
            </div>
        `;
    });
    
    patternContent.innerHTML = html;
}

// 查看文件
function viewFile(filePath) {
    console.log('查看文件:', filePath);
    // 这里可以添加文件查看逻辑
    alert('查看文件功能开发中...');
}

// 下载文件
function downloadFile(filePath) {
    console.log('下载文件:', filePath);
    // 这里可以添加文件下载逻辑
    alert('下载文件功能开发中...');
}

// 实际项目中，这里可以添加与后端API的交互代码
// 例如：
// function loadRealData() {
//     // 加载PRD文件
//     fetch('/api/prd-files')
//         .then(response => response.json())
//         .then(data => {
//             prdFiles = data;
//             updatePRDFiles();
//         });
//     
//     // 加载执行日志
//     fetch('/api/execution-logs')
//         .then(response => response.text())
//         .then(data => {
//             executionLogs = data.split('\n').filter(line => line.trim());
//             updateExecutionLogs();
//         });
//     
//     // 加载模式库
//     fetch('/api/patterns')
//         .then(response => response.json())
//         .then(data => {
//             patterns = data;
//             updatePatterns();
//         });
// }
