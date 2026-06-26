#!/usr/bin/env node
/**
 * OpenClaw 文件上传服务器 v2.1
 * - 用户文件独立存储
 * - Web 页面展示文件列表
 * - 支持文件删除
 * - 支持技能包下载
 * - 自动重启支持
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');
const { exec, spawn } = require('child_process');

const PORT = process.env.UPLOAD_PORT || 15170;
const WORKSPACE = process.env.WORKSPACE || '/home/admin/.openclaw/workspace';
const UPLOADS_DIR = path.join(WORKSPACE, 'uploads');
const SKILLS_DIR = path.join(WORKSPACE, 'skills');

// 获取当前技能包目录（用于查找页面文件）
const SKILL_DIR = __dirname; // 当前脚本所在目录

// 从 Gateway 配置读取 Token
function loadGatewayToken() {
    try {
        const configPath = path.join(process.env.HOME || '/home/admin', '.openclaw/openclaw.json');
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        return config.gateway?.auth?.token || '';
    } catch (e) {
        return '';
    }
}

const GATEWAY_TOKEN = loadGatewayToken();

// 确保上传目录存在
if (!fs.existsSync(UPLOADS_DIR)) {
    fs.mkdirSync(UPLOADS_DIR, { recursive: true });
    console.log(`✅ 创建上传目录：${UPLOADS_DIR}`);
}

console.log(`
╔═══════════════════════════════════════════════════════╗
║     OpenClaw 文件上传服务器 v2.1                       ║
╠═══════════════════════════════════════════════════════╣
║  端口：${PORT}                                          ║
║  Workspace: ${WORKSPACE}                          ║
║  上传目录：${UPLOADS_DIR}                        ║
║  Token 认证：${GATEWAY_TOKEN ? '已启用' : '未启用'}                        ║
║  技能包下载：支持                                     ║
╚═══════════════════════════════════════════════════════╝
`);

// 获取文件列表
function getFileList() {
    try {
        const files = fs.readdirSync(UPLOADS_DIR)
            .filter(f => !f.startsWith('.'))
            .map(filename => {
                const filePath = path.join(UPLOADS_DIR, filename);
                const stats = fs.statSync(filePath);
                return {
                    name: filename,
                    size: stats.size,
                    sizeFormatted: formatSize(stats.size),
                    modified: stats.mtime.toISOString(),
                    path: filePath
                };
            })
            .sort((a, b) => b.modified.localeCompare(a.modified));
        return files;
    } catch (e) {
        console.error('获取文件列表失败:', e);
        return [];
    }
}

// 获取技能列表
function getSkillsList() {
    try {
        if (!fs.existsSync(SKILLS_DIR)) return [];
        const skills = fs.readdirSync(SKILLS_DIR)
            .filter(f => !f.startsWith('.'))
            .map(skillName => {
                const skillPath = path.join(SKILLS_DIR, skillName);
                const stats = fs.statSync(skillPath);
                const hasClawhub = fs.existsSync(path.join(skillPath, 'clawhub.json'));
                const hasSkillMd = fs.existsSync(path.join(skillPath, 'SKILL.md'));
                return {
                    name: skillName,
                    modified: stats.mtime.toISOString(),
                    hasClawhub,
                    hasSkillMd,
                    path: skillPath
                };
            })
            .sort((a, b) => a.name.localeCompare(b.name));
        return skills;
    } catch (e) {
        console.error('获取技能列表失败:', e);
        return [];
    }
}

// 格式化文件大小
function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// 解析 multipart/form-data
function parseMultipart(buffer, boundary) {
    const boundaryString = '--' + boundary;
    let content;
    try {
        content = buffer.toString('utf8');
    } catch (e) {
        content = buffer.toString('binary');
    }
    const parts = content.split(boundaryString);
    const result = {};
    
    for (const part of parts) {
        if (part.length === 0 || part.startsWith('--\r\n') || part === '--' || part === '--\r\n') continue;
        
        let cleanPart = part;
        if (cleanPart.startsWith('\r\n')) cleanPart = cleanPart.substring(2);
        
        const headerEndIndex = cleanPart.indexOf('\r\n\r\n');
        if (headerEndIndex === -1) continue;
        
        const headerPart = cleanPart.substring(0, headerEndIndex);
        const body = cleanPart.substring(headerEndIndex + 4);
        const headers = headerPart.split('\r\n');
        const contentDisposition = headers.find(h => h.startsWith('Content-Disposition:'));
        const contentType = headers.find(h => h.startsWith('Content-Type:'));
        
        if (!contentDisposition) continue;
        
        const nameMatch = contentDisposition.match(/name="([^"]+)"/);
        const filenameMatch = contentDisposition.match(/filename="([^"]+)"/);
        
        if (!nameMatch) continue;
        
        const fieldName = nameMatch[1];
        const filename = filenameMatch ? filenameMatch[1] : null;
        
        if (filename) {
            let fileBody = body;
            const lastBoundaryIndex = fileBody.lastIndexOf('--');
            if (lastBoundaryIndex > 0) fileBody = fileBody.substring(0, lastBoundaryIndex);
            fileBody = fileBody.replace(/\r\n$/, '');
            
            const headerEndPos = buffer.indexOf('\r\n\r\n');
            const fileDataStart = headerEndPos + 4;
            let fileDataEnd = buffer.length;
            
            const endBoundaryPos = buffer.lastIndexOf('--' + boundary);
            if (endBoundaryPos > fileDataStart) fileDataEnd = endBoundaryPos - 2;
            
            const fileData = buffer.slice(fileDataStart, fileDataEnd);
            
            result[fieldName] = {
                filename,
                data: fileData,
                contentType: contentType ? contentType.split(': ')[1] : 'application/octet-stream'
            };
        } else {
            result[fieldName] = body.replace(/\r\n$/, '');
        }
    }
    
    return result;
}

// 安全的文件名处理
function sanitizeFilename(filename) {
    const base = path.basename(filename);
    return base.replace(/[^\w.\-\u4e00-\u9fff《》【】()（）]/g, '_');
}

// 打包技能为 zip（使用系统 zip 命令）
function zipSkill(skillName, res) {
    const skillPath = path.join(SKILLS_DIR, skillName);
    const zipPath = path.join(UPLOADS_DIR, `${skillName}-skill.zip`);
    
    if (!fs.existsSync(skillPath)) {
        console.error(`❌ 技能不存在：${skillPath}`);
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Skill not found' }));
        return;
    }
    
    console.log(`📦 开始打包：${skillName}`);
    
    // 使用 zip 命令打包
    const zip = spawn('zip', ['-r', zipPath, skillName], {
        cwd: SKILLS_DIR,
        stdio: ['ignore', 'pipe', 'pipe']
    });
    
    let stderr = '';
    zip.stderr.on('data', (data) => {
        stderr += data.toString();
    });
    
    zip.on('close', (code) => {
        if (code !== 0) {
            console.error(`❌ 打包失败：${stderr}`);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: `zip command failed: ${stderr}` }));
            return;
        }
        
        const stats = fs.statSync(zipPath);
        console.log(`✅ 技能包已创建：${zipPath} (${formatSize(stats.size)})`);
        
        res.setHeader('Content-Type', 'application/zip');
        res.setHeader('Content-Disposition', `attachment; filename="${skillName}-skill.zip"`);
        fs.createReadStream(zipPath).pipe(res);
    });
    
    zip.on('error', (err) => {
        console.error('❌ zip 命令错误:', err);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
    });
}

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    const parsedUrl = new URL(req.url, `http://${req.headers.host}`);
    
    // 提供上传页面
    if (req.method === 'GET' && (parsedUrl.pathname === '/' || parsedUrl.pathname === '/upload.html')) {
        // 优先从技能包目录查找，其次从 workspace 查找
        const htmlPath = path.join(SKILL_DIR, 'upload.html');
        const fallbackPath = path.join(WORKSPACE, 'upload-v2.html');
        
        fs.readFile(htmlPath, (err, data) => {
            if (err) {
                // 尝试 fallback 路径
                fs.readFile(fallbackPath, (err2, data2) => {
                    if (err2) {
                        res.writeHead(404, { 'Content-Type': 'text/plain' });
                        res.end('Upload page not found. Please ensure upload.html exists in the skill directory.');
                        return;
                    }
                    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                    res.end(data2);
                });
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(data);
        });
        return;
    }
    
    // 获取文件列表 API
    if (req.method === 'GET' && parsedUrl.pathname === '/api/files') {
        const tokenParam = parsedUrl.searchParams.get('token');
        
        if (GATEWAY_TOKEN && tokenParam !== GATEWAY_TOKEN) {
            res.writeHead(401, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Invalid token' }));
            return;
        }
        
        const files = getFileList();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, files }));
        return;
    }
    
    // 获取技能列表 API
    if (req.method === 'GET' && parsedUrl.pathname === '/api/skills') {
        const tokenParam = parsedUrl.searchParams.get('token');
        
        if (GATEWAY_TOKEN && tokenParam !== GATEWAY_TOKEN) {
            res.writeHead(401, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Invalid token' }));
            return;
        }
        
        const skills = getSkillsList();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, skills }));
        return;
    }
    
    // 下载技能包 API
    if (req.method === 'GET' && parsedUrl.pathname.startsWith('/api/skills/')) {
        const tokenParam = parsedUrl.searchParams.get('token');
        
        if (GATEWAY_TOKEN && tokenParam !== GATEWAY_TOKEN) {
            res.writeHead(401, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Invalid token' }));
            return;
        }
        
        const skillName = decodeURIComponent(parsedUrl.pathname.replace('/api/skills/', ''));
        const safeSkillName = path.basename(skillName); // 防止路径遍历
        
        console.log(`📦 打包技能：${safeSkillName}`);
        zipSkill(safeSkillName, res);
        return;
    }
    
    // 健康检查
    if (req.method === 'GET' && parsedUrl.pathname === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', workspace: WORKSPACE, uploads: UPLOADS_DIR }));
        return;
    }
    
    // 处理文件上传
    if (req.method === 'POST' && parsedUrl.pathname === '/api/upload') {
        const tokenParam = parsedUrl.searchParams.get('token');
        
        if (GATEWAY_TOKEN && tokenParam !== GATEWAY_TOKEN) {
            console.log(`[${new Date().toISOString()}] ❌ 认证失败：无效 token`);
            res.writeHead(401, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Invalid token' }));
            return;
        }
        
        const contentType = req.headers['content-type'];
        if (!contentType || !contentType.startsWith('multipart/form-data')) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Content-Type must be multipart/form-data' }));
            return;
        }
        
        const boundaryMatch = contentType.match(/boundary=(?:"([^"]+)"|([^;]+))/);
        if (!boundaryMatch) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Invalid boundary' }));
            return;
        }
        const boundary = boundaryMatch[1] || boundaryMatch[2];
        
        const chunks = [];
        req.on('data', chunk => chunks.push(chunk));
        req.on('end', () => {
            try {
                const buffer = Buffer.concat(chunks);
                const parsed = parseMultipart(buffer, boundary);
                
                if (!parsed.file) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'No file provided' }));
                    return;
                }
                
                const file = parsed.file;
                const safeFilename = sanitizeFilename(file.filename);
                const filePath = path.join(UPLOADS_DIR, safeFilename);
                
                fs.writeFileSync(filePath, file.data);
                
                console.log(`[${new Date().toISOString()}] ✅ 文件上传：${safeFilename} (${file.data.length} bytes)`);
                
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    success: true,
                    filename: safeFilename,
                    path: filePath,
                    size: file.data.length,
                    sizeFormatted: formatSize(file.data.length)
                }));
            } catch (error) {
                console.error('上传错误:', error);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: error.message }));
            }
        });
        return;
    }
    
    // 删除文件 API
    if (req.method === 'DELETE' && parsedUrl.pathname.startsWith('/api/files/')) {
        const tokenParam = parsedUrl.searchParams.get('token');
        
        if (GATEWAY_TOKEN && tokenParam !== GATEWAY_TOKEN) {
            res.writeHead(401, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Invalid token' }));
            return;
        }
        
        const filename = decodeURIComponent(parsedUrl.pathname.replace('/api/files/', ''));
        const safeFilename = path.basename(filename);
        const filePath = path.join(UPLOADS_DIR, safeFilename);
        
        if (!fs.existsSync(filePath)) {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'File not found' }));
            return;
        }
        
        try {
            fs.unlinkSync(filePath);
            console.log(`[${new Date().toISOString()}] 🗑️  文件删除：${safeFilename}`);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: true, message: 'File deleted' }));
        } catch (error) {
            console.error('删除失败:', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: error.message }));
        }
        return;
    }
    
    // 404
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
});

server.listen(PORT, '0.0.0.0', () => {
    const os = require('os');
    const interfaces = os.networkInterfaces();
    let ip = '0.0.0.0';
    for (const iface of Object.values(interfaces)) {
        if (!iface) continue;
        for (const alias of iface) {
            if (alias.family === 'IPv4' && !alias.internal) {
                ip = alias.address;
                break;
            }
        }
        if (ip !== '0.0.0.0') break;
    }
    console.log(`📁 上传页面：http://${ip}:${PORT}/`);
    console.log(`📂 文件目录：${UPLOADS_DIR}`);
    console.log(`🎁 技能包下载：http://${ip}:${PORT}/api/skills/<skill-name>?token=xxx`);
    console.log(`🔐 使用 Gateway Token 进行认证`);
});
