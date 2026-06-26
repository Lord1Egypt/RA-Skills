const fs = require('fs');
const path = require('path');

// 动态获取用户工作区路径（跨平台支持）
const USER_HOME = process.env.USERPROFILE || process.env.HOME || process.env.HOMEPATH;
const WORKSPACE_DIR = path.join(USER_HOME, '.openclaw', 'workspace');
const SCRIPT_DIR = path.join(WORKSPACE_DIR, 'script', 'apifox');
const outputFile = path.join(USER_HOME, 'Desktop', 'Apifox 接口导出.txt');

// 检查输入目录是否存在，不存在则创建
if (!fs.existsSync(SCRIPT_DIR)) {
    fs.mkdirSync(SCRIPT_DIR, { recursive: true });
    console.log(`✅ 已创建输入目录：${SCRIPT_DIR}`);
    console.log('📝 请将 Apifox 导出的 OpenAPI JSON 文件放到此目录，命名为 source.json 或 source-项目名.json');
}

// 获取命令行参数或默认使用 source.json
let inputFileArg = process.argv[2];
let inputFile;

if (inputFileArg) {
    // 如果指定了项目名，如 "node export.js 商城" 或 "node export.js source-商城.json"
    if (!inputFileArg.endsWith('.json')) {
        inputFileArg = `source-${inputFileArg}.json`;
    }
    inputFile = path.join(SCRIPT_DIR, inputFileArg);
    if (!fs.existsSync(inputFile)) {
        console.error(`❌ 找不到文件：${inputFile}`);
        console.error('可用项目：');
        const files = fs.readdirSync(SCRIPT_DIR).filter(f => f.endsWith('.json'));
        files.forEach(f => console.error(`  - ${f.replace('source-', '').replace('.json', '')}`));
        process.exit(1);
    }
} else {
    // 默认使用 source.json 或最新的 source-*.json
    const defaultFile = path.join(SCRIPT_DIR, 'source.json');
    if (fs.existsSync(defaultFile)) {
        inputFile = defaultFile;
    } else {
        // 找最新的 source-*.json
        const files = fs.readdirSync(SCRIPT_DIR)
            .filter(f => f.startsWith('source-') && f.endsWith('.json'))
            .map(f => ({ name: f, time: fs.statSync(path.join(SCRIPT_DIR, f)).mtimeMs }))
            .sort((a, b) => b.time - a.time);
        
        if (files.length === 0) {
            console.error('❌ 找不到任何 source.json 文件');
            process.exit(1);
        }
        inputFile = path.join(SCRIPT_DIR, files[0].name);
    }
}

const json = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
const schemas = json.components?.schemas || {};

// 递归展开 schema，深挖到最底层
function expandSchema(schemaRef, depth = 0, visited = new Set()) {
    if (depth > 10) return '{ /* 达到最大深度 */ }'; // 防止无限递归
    
    if (!schemaRef) return null;
    
    // 处理 $ref
    if (schemaRef.$ref) {
        const schemaName = schemaRef.$ref.replace('#/components/schemas/', '');
        if (visited.has(schemaName)) {
            return `{ /* ${schemaName} - 循环引用 */ }`;
        }
        visited.add(schemaName);
        
        const schemaDef = schemas[schemaName];
        if (!schemaDef) {
            return `{ /* ${schemaName} - 未找到定义 */ }`;
        }
        return expandSchema(schemaDef, depth, new Set(visited));
    }
    
    // 处理 allOf - 合并所有父 schema
    if (schemaRef.allOf && Array.isArray(schemaRef.allOf)) {
        const result = {};
        for (const sub of schemaRef.allOf) {
            const expanded = expandSchema(sub, depth, new Set(visited));
            if (expanded && typeof expanded === 'object' && !Array.isArray(expanded)) {
                Object.assign(result, expanded);
            }
        }
        return result;
    }
    
    // 处理 object 类型
    if (schemaRef.type === 'object') {
        const result = {};
        if (schemaRef.properties) {
            for (const [propName, propDef] of Object.entries(schemaRef.properties)) {
                result[propName] = expandSchema(propDef, depth + 1, new Set(visited));
            }
        }
        // 处理 additionalProperties
        if (schemaRef.additionalProperties && typeof schemaRef.additionalProperties === 'object') {
            result['[additional]'] = expandSchema(schemaRef.additionalProperties, depth + 1, new Set(visited));
        }
        return result;
    }
    
    // 处理 array 类型 - 展开数组项
    if (schemaRef.type === 'array') {
        const items = expandSchema(schemaRef.items, depth + 1, new Set(visited));
        // 如果 items 是对象，返回数组格式
        if (items && typeof items === 'object') {
            return [items];
        }
        return `[ ${items || 'unknown'} ]`;
    }
    
    // 基础类型 - 返回示例值
    if (schemaRef.type) {
        if (schemaRef.example !== undefined) {
            return schemaRef.example;
        }
        if (schemaRef.default !== undefined) {
            return schemaRef.default;
        }
        const typeMap = {
            'string': schemaRef.enum ? schemaRef.enum[0] : '',
            'integer': 0,
            'number': 0,
            'boolean': false,
            'object': {},
            'array': []
        };
        return typeMap[schemaRef.type] || schemaRef.type;
    }
    
    return schemaRef;
}

// 按模块分组
const modules = {};

for (const [pathName, pathData] of Object.entries(json.paths)) {
    for (const [method, api] of Object.entries(pathData)) {
        const methodName = method.toUpperCase();
        const summary = api.summary || '未命名接口';
        const folder = api['x-apifox-folder'] || '未分类';
        
        if (!modules[folder]) {
            modules[folder] = [];
        }
        
        modules[folder].push({ summary, pathName, methodName, api });
    }
}

let output = [];
let totalCounter = 0;

// 先输出目录
output.push('');
output.push('');
output.push('='.repeat(80));
output.push('目  录');
output.push('='.repeat(80));
output.push('');

for (const [moduleName, apis] of Object.entries(modules)) {
    output.push(`【${moduleName}】 (${apis.length} 个接口)`);
    for (const apiData of apis) {
        totalCounter++;
        output.push(`  ${totalCounter}. ${apiData.summary}`);
    }
    output.push('');
}

totalCounter = 0;

// 按模块输出接口详情
for (const [moduleName, apis] of Object.entries(modules)) {
    output.push('');
    output.push('');
    output.push('═'.repeat(80));
    output.push(`【${moduleName}】 (${apis.length} 个接口)`);
    output.push('═'.repeat(80));
    output.push('');
    
    for (const apiData of apis) {
        totalCounter++;
        const { summary, pathName, methodName, api } = apiData;
        
        output.push(`${totalCounter}. ${summary}`);
        output.push(`   所属模块：${moduleName}`);
        output.push(`   接口地址：${pathName}  ${methodName}`);
        output.push('');
        
        // 请求参数（Query/Header/Path）
        if (api.parameters && api.parameters.length > 0) {
            output.push('请求参数：');
            for (const param of api.parameters) {
                const paramType = param.in;
                const paramName = param.name;
                const required = param.required ? '必填' : '可选';
                const type = param.schema?.type || 'string';
                const desc = param.description || '';
                output.push(`  - ${paramType} 参数：${paramName} (${type}, ${required}) - ${desc}`);
            }
            output.push('');
        }
        
        // 请求 Body
        if (api.requestBody && api.requestBody.content?.['application/json']) {
            const jsonContent = api.requestBody.content['application/json'];
            if (jsonContent.example) {
                output.push('请求参数 application/json：');
                output.push(JSON.stringify(jsonContent.example, null, 2));
                output.push('');
            } else if (jsonContent.schema) {
                const expanded = expandSchema(jsonContent.schema);
                output.push('请求参数 application/json：');
                output.push(JSON.stringify(expanded, null, 2));
                output.push('');
            }
        }
        
        // 响应数据
        if (api.responses?.['200'] && api.responses['200'].content?.['application/json']) {
            const jsonResp = api.responses['200'].content['application/json'];
            if (jsonResp.example) {
                output.push('响应数据：');
                output.push(JSON.stringify(jsonResp.example, null, 2));
                output.push('');
            } else if (jsonResp.schema) {
                const expanded = expandSchema(jsonResp.schema);
                output.push('响应数据：');
                output.push(JSON.stringify(expanded, null, 2));
                output.push('');
            }
        }
        
        output.push('─'.repeat(80));
        output.push('');
    }
}

fs.writeFileSync(outputFile, output.join('\n'), 'utf8');
console.log(`导出完成！共 ${Object.keys(modules).length} 个模块，${totalCounter} 个接口`);
console.log(`文件已保存到：${outputFile}`);
