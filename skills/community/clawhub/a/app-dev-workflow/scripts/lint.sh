#!/bin/bash
# 代码规范检查脚本
# 用法: bash lint.sh <文件路径>

set -e

FILE_PATH="$1"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -z "$FILE_PATH" ]; then
    echo "用法: bash lint.sh <文件路径>"
    echo "示例: bash lint.sh src/services/DIYCoffeeService.ts"
    exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
    echo -e "${RED}❌ 文件不存在: $FILE_PATH${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 检查代码规范: $FILE_PATH${NC}"
echo ""

# 使用Node.js进行检查
node -e "
const fs = require('fs');
const content = fs.readFileSync('$FILE_PATH', 'utf-8');
const lines = content.split('\n');

const issues = [];
let score = 100;

// HOS-001: 使用@ObservedV2
if (content.includes('@Observed') && !content.includes('@ObservedV2')) {
    const lineNum = lines.findIndex(l => l.includes('@Observed')) + 1;
    issues.push({ id: 'HOS-001', severity: 'warning', line: lineNum, message: '建议使用@ObservedV2替代@Observed' });
    score -= 3;
}

// HOS-002: 禁止any类型
const anyMatches = content.match(/:\s*any\b/g);
if (anyMatches) {
    let index = 0;
    for (const match of anyMatches) {
        index = content.indexOf(match, index);
        const lineNum = content.substring(0, index).split('\n').length;
        issues.push({ id: 'HOS-002', severity: 'error', line: lineNum, message: '禁止使用any类型' });
        score -= 10;
        index += match.length;
    }
}

// HOS-003: 硬编码中文
const hardcodedMatches = content.match(/Text\(['\"]([^'\"]*[\u4e00-\u9fa5]+[^'\"]*)['\"]\)/g);
if (hardcodedMatches) {
    let index = 0;
    for (const match of hardcodedMatches) {
        index = content.indexOf(match, index);
        const lineNum = content.substring(0, index).split('\n').length;
        const text = match.match(/['\"](.*)['\"]/)[1];
        issues.push({ id: 'HOS-003', severity: 'error', line: lineNum, message: \`硬编码字符串应使用资源引用: \${text.slice(0, 20)}\` });
        score -= 10;
        index += match.length;
    }
}

// PERF-001: for循环中的await
if (/for\s*\([^)]*\)\s*\{[^}]*await/s.test(content)) {
    const lineNum = lines.findIndex(l => l.includes('for') && l.includes('await')) + 1;
    issues.push({ id: 'PERF-001', severity: 'warning', line: lineNum, message: '避免在for循环中使用await' });
    score -= 3;
}

// PERF-002: ForEach而非LazyForEach
if (content.includes('ForEach') && !content.includes('LazyForEach')) {
    const lineNum = lines.findIndex(l => l.includes('ForEach')) + 1;
    issues.push({ id: 'PERF-002', severity: 'error', line: lineNum, message: '大列表应使用LazyForEach' });
    score -= 10;
}

// SEC-001: 敏感数据存储
if (content.includes('preferences') && !content.includes('SecureStorage')) {
    issues.push({ id: 'SEC-001', severity: 'error', line: 1, message: '敏感数据应使用SecureStorage' });
    score -= 10;
}

// SEC-002: 日志敏感信息
if (/hilog\.[^(]*\([^)]*(password|token|key|secret)/i.test(content)) {
    const lineNum = lines.findIndex(l => l.includes('hilog')) + 1;
    issues.push({ id: 'SEC-002', severity: 'error', line: lineNum, message: '日志禁止输出敏感信息' });
    score -= 10;
}

// ERR-001: async函数错误处理
const asyncFuncRegex = /async\s+\w+\s*\([^)]*\)\s*\{/g;
let match;
while ((match = asyncFuncRegex.exec(content)) !== null) {
    const funcStart = match.index;
    let braceCount = 0;
    let inString = false;
    let stringChar = '';
    let endIndex = funcStart;

    for (let i = funcStart; i < content.length; i++) {
        const char = content[i];
        if (!inString && (char === '\"' || char === \"'\" || char === '\`')) {
            inString = true;
            stringChar = char;
        } else if (inString && char === stringChar && content[i - 1] !== '\\\\') {
            inString = false;
        }

        if (!inString) {
            if (char === '{') braceCount++;
            if (char === '}') {
                braceCount--;
                if (braceCount === 0) {
                    endIndex = i + 1;
                    break;
                }
            }
        }
    }

    const funcContent = content.substring(funcStart, endIndex);
    if (!funcContent.includes('try') && !funcContent.includes('GlobalErrorHandler')) {
        const lineNum = content.substring(0, funcStart).split('\n').length;
        issues.push({ id: 'ERR-001', severity: 'warning', line: lineNum, message: 'async函数应包含错误处理' });
        score -= 3;
    }
}

// ============ 新增规则 ============

// HOS-004: @ObservedV2类中的可变字段应使用@Track
const observedV2Regex = /@ObservedV2[\s\S]*?class\s+\w+/g;
while ((match = observedV2Regex.exec(content)) !== null) {
    const classStart = match.index;
    const classSection = content.substring(classStart, classStart + 2000);
    const classLines = content.substring(0, classStart).split('\n').length;

    // 检查是否有非@Track的可变状态
    const mutableFields = classSection.match(/\b(private\s+)?\w+\s*:\s*(string|number|boolean)\s*[=;]/g);
    if (mutableFields) {
        for (const field of mutableFields) {
            const fieldIndex = classSection.indexOf(field);
            const beforeField = classSection.substring(Math.max(0, fieldIndex - 50), fieldIndex);
            if (!beforeField.includes('@Track') && !beforeField.includes('@Local')) {
                issues.push({ id: 'HOS-004', severity: 'warning', line: classLines + 1, message: '@ObservedV2类中的可变字段建议使用@Track装饰' });
                score -= 3;
                break;
            }
        }
    }
}

// HOS-005: 资源引用格式检查
const resourceRegex = /\$r\s*\(\s*['\"]([^'\"]*)['\"]\s*\)/g;
let resMatch;
while ((resMatch = resourceRegex.exec(content)) !== null) {
    const resRef = resMatch[1];
    const lineNum = content.substring(0, resMatch.index).split('\n').length;

    // 检查格式是否为 app.xxx.name
    if (!/^app\.(string|color|media|float)\.[a-z][a-zA-Z0-9_]*$/.test(resRef)) {
        issues.push({ id: 'HOS-005', severity: 'warning', line: lineNum, message: \`资源引用格式不规范: \${resRef}\` });
        score -= 3;
    }
}

// HOS-006: 避免直接使用全局对象
if (/\bwindow\.|\bdocument\.|\blocalStorage\./.test(content)) {
    const lineNum = lines.findIndex(l => /\bwindow\.|\bdocument\.|\blocalStorage\./.test(l)) + 1;
    issues.push({ id: 'HOS-006', severity: 'error', line: lineNum, message: 'HarmonyOS中避免使用浏览器全局对象' });
    score -= 10;
}

// PERF-003: @Builder参数传递检查
const builderRegex = /@Builder[\s\S]*?\([^)]*\$\$[a-zA-Z_]+\s*:/g;
if (builderRegex.test(content)) {
    const lineNum = lines.findIndex(l => l.includes('@Builder')) + 1;
    issues.push({ id: 'PERF-003', severity: 'warning', line: lineNum, message: '@Builder参数应避免直接使用$$双向绑定，建议传递值或引用' });
    score -= 3;
}

// PERF-004: 图片加载优化检查
const imageRegex = /Image\s*\([^)]*\)/g;
let imgMatch;
while ((imgMatch = imageRegex.exec(content)) !== null) {
    const imgCall = imgMatch[0];
    const lineNum = content.substring(0, imgMatch.index).split('\n').length;

    // 检查是否有.objectFit或.sizingMode
    const afterImg = content.substring(imgMatch.index, imgMatch.index + 300);
    if (!afterImg.includes('.objectFit') && !afterImg.includes('.sizingMode')) {
        issues.push({ id: 'PERF-004', severity: 'info', line: lineNum, message: '图片组件建议设置objectFit属性以优化显示性能' });
        score -= 1;
    }
}

// ERR-002: try-catch必须有finally或至少一个操作
const tryCatchRegex = /try\s*\{/g;
let tryMatch;
while ((tryMatch = tryCatchRegex.exec(content)) !== null) {
    const tryStart = tryMatch.index;
    const trySection = content.substring(tryStart, tryStart + 1000);

    if (!trySection.includes('catch') || trySection.indexOf('catch') > 500) {
        const lineNum = content.substring(0, tryStart).split('\n').length;
        issues.push({ id: 'ERR-002', severity: 'warning', line: lineNum, message: 'try块必须有对应的catch或finally块' });
        score -= 3;
        break;
    }
}

// PERF-005: 组件过度嵌套检查
const buildFuncMatch = content.match(/build\(\)\s*\{[\s\S]*?\n\s*\}/);
if (buildFuncMatch) {
    const buildContent = buildFuncMatch[0];
    const maxDepth = 8;
    let depth = 0;
    let maxFoundDepth = 0;

    for (const char of buildContent) {
        if (char === '(' || char === '{') depth++;
        if (char === ')' || char === '}') depth--;
        maxFoundDepth = Math.max(maxFoundDepth, depth);
    }

    if (maxFoundDepth > maxDepth) {
        const lineNum = lines.findIndex(l => l.includes('build()')) + 1;
        issues.push({ id: 'PERF-005', severity: 'warning', line: lineNum, message: \`组件嵌套深度\${maxFoundDepth}超过建议值\${maxDepth}，考虑拆分组件\` });
        score -= 3;
    }
}

// 输出结果
const errors = issues.filter(i => i.severity === 'error');
const warnings = issues.filter(i => i.severity === 'warning');
const infos = issues.filter(i => i.severity === 'info');

console.log(\`📊 检查报告: $FILE_PATH\`);
console.log(\`   错误: \${errors.length} | 警告: \${warnings.length} | 提示: \${infos.length}\`);

const scoreColor = score >= 90 ? '\x1b[32m' : score >= 70 ? '\x1b[33m' : '\x1b[31m';
const status = score >= 70 ? '✅' : '❌';
console.log(\`   得分: \${scoreColor}\${score}/100\x1b[0m \${status}\`);

if (issues.length > 0) {
    console.log('\n📋 问题列表:');
    issues.forEach(issue => {
        const icon = issue.severity === 'error' ? '🔴' : issue.severity === 'warning' ? '🟡' : '🔵';
        console.log(\`\n\${icon} [\${issue.id}] \${issue.message}\`);
        console.log(\`   位置: 第\${issue.line}行\`);
    });
}

console.log('');

// 更新PROJECT.md中的检查结果
try {
    const projectMd = fs.readFileSync('PROJECT.md', 'utf-8');
    let updated = projectMd;

    // 更新各规范得分
    const hosScore = 100 - issues.filter(i => i.id.startsWith('HOS')).reduce((s, i) => s + (i.severity === 'error' ? 10 : 3), 0);
    const perfScore = 100 - issues.filter(i => i.id.startsWith('PERF')).reduce((s, i) => s + (i.severity === 'error' ? 10 : 3), 0);
    const secScore = 100 - issues.filter(i => i.id.startsWith('SEC')).reduce((s, i) => s + 10, 0);
    const errScore = 100 - issues.filter(i => i.id.startsWith('ERR')).reduce((s, i) => s + 3, 0);

    updated = updated.replace(/\| HOS规范 \| .* \| .+ \|/, \`| HOS规范 | \${hosScore} | \${hosScore >= 80 ? '✅' : '❌'} |\`);
    updated = updated.replace(/\| PERF规范 \| .* \| .+ \|/, \`| PERF规范 | \${perfScore} | \${perfScore >= 80 ? '✅' : '❌'} |\`);
    updated = updated.replace(/\| SEC规范 \| .* \| .+ \|/, \`| SEC规范 | \${secScore} | \${secScore >= 80 ? '✅' : '❌'} |\`);
    updated = updated.replace(/\| ERR规范 \| .* \| .+ \|/, \`| ERR规范 | \${errScore} | \${errScore >= 80 ? '✅' : '❌'} |\`);
    updated = updated.replace(/\*\*总分\*\*: .+/, \`**总分**: \${score}/100\`);

    fs.writeFileSync('PROJECT.md', updated);
    console.log('📝 PROJECT.md 检查结果已更新');
} catch (e) {
    // 忽略更新错误
}

process.exit(score >= 70 ? 0 : 1);
