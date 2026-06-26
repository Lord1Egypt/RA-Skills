#!/usr/bin/env node
/**
 * Feishu Upload Skill 使用示例
 * 展示如何集成到OpenClaw工作流中
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 示例1：直接调用上传工具
function exampleDirectCall() {
    console.log('📦 示例1：直接调用上传工具');
    console.log('='.repeat(50));
    
    const filePath = path.join(__dirname, 'test_example.txt');
    
    // 创建测试文件
    fs.writeFileSync(filePath, '这是一个测试文件，用于演示Feishu Upload Skill的使用。\n创建时间：' + new Date().toISOString());
    
    // 假设的聊天ID（实际使用时替换为真实ID）
    const chatId = 'oc_dd899cb1a7846915cdd2d6850bd1dafa';
    
    try {
        // 调用上传工具
        const command = `node ${path.join(__dirname, 'feishu_complete_upload.js')} "${filePath}" "${chatId}"`;
        console.log(`执行命令: ${command}`);
        
        const result = execSync(command, { encoding: 'utf8' });
        console.log('执行结果:', result);
        
        // 解析JSON结果
        const lines = result.trim().split('\n');
        const jsonLine = lines.find(line => line.startsWith('{'));
        if (jsonLine) {
            const data = JSON.parse(jsonLine);
            console.log('\n✅ 上传成功!');
            console.log(`文件Key: ${data.upload.file_key}`);
            console.log(`消息ID: ${data.message_id || 'N/A'}`);
        }
        
    } catch (error) {
        console.error('❌ 执行失败:', error.message);
        if (error.stdout) console.error('输出:', error.stdout);
        if (error.stderr) console.error('错误:', error.stderr);
    }
    
    // 清理测试文件
    fs.unlinkSync(filePath);
    console.log('\n' + '-'.repeat(50));
}

// 示例2：编程式集成
function exampleProgrammatic() {
    console.log('\n💻 示例2：编程式集成');
    console.log('='.repeat(50));
    
    // 在实际的OpenClaw技能中，你可以这样集成：
    const exampleCode = `
// 在你的OpenClaw技能中集成Feishu Upload
const { spawn } = require('child_process');

async function uploadToFeishu(filePath, chatId) {
    return new Promise((resolve, reject) => {
        const uploader = spawn('node', [
            'feishu_complete_upload.js',
            filePath,
            chatId
        ]);
        
        let output = '';
        let error = '';
        
        uploader.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        uploader.stderr.on('data', (data) => {
            error += data.toString();
        });
        
        uploader.on('close', (code) => {
            if (code === 0) {
                try {
                    // 解析JSON输出
                    const lines = output.trim().split('\\n');
                    const jsonLine = lines.find(line => line.startsWith('{'));
                    if (jsonLine) {
                        resolve(JSON.parse(jsonLine));
                    } else {
                        resolve({ success: true, output });
                    }
                } catch (e) {
                    reject(new Error(\`解析失败: \${e.message}\`));
                }
            } else {
                reject(new Error(\`上传失败: \${error}\`));
            }
        });
    });
}

// 使用示例
async function main() {
    try {
        const result = await uploadToFeishu('document.txt', 'oc_xxx');
        console.log('上传结果:', result);
    } catch (error) {
        console.error('上传错误:', error);
    }
}
`;
    
    console.log(exampleCode);
    console.log('-'.repeat(50));
}

// 示例3：批量上传
function exampleBatchUpload() {
    console.log('\n📚 示例3：批量上传多个文件');
    console.log('='.repeat(50));
    
    const batchExample = `
// 批量上传多个文件到飞书
const files = [
    'report.pdf',
    'data.csv',
    'chart.png',
    'summary.txt'
];

async function batchUpload(files, chatId) {
    const results = [];
    
    for (const file of files) {
        if (!fs.existsSync(file)) {
            console.warn(\`文件不存在: \${file}\`);
            continue;
        }
        
        try {
            console.log(\`正在上传: \${file}\`);
            const result = execSync(
                \`node feishu_complete_upload.js "\${file}" "\${chatId}"\`,
                { encoding: 'utf8' }
            );
            
            // 解析结果
            const lines = result.trim().split('\\n');
            const jsonLine = lines.find(line => line.startsWith('{'));
            if (jsonLine) {
                const data = JSON.parse(jsonLine);
                results.push({
                    file,
                    success: true,
                    file_key: data.upload.file_key,
                    message_id: data.message_id
                });
                console.log(\`  ✅ 成功: \${data.upload.file_key}\`);
            }
            
        } catch (error) {
            console.error(\`  ❌ 失败: \${error.message}\`);
            results.push({
                file,
                success: false,
                error: error.message
            });
        }
    }
    
    return results;
}

// 使用示例
const uploadResults = await batchUpload(files, 'oc_xxx');
console.log('批量上传完成:', uploadResults);
`;
    
    console.log(batchExample);
    console.log('-'.repeat(50));
}

// 运行所有示例
function main() {
    console.log('🚀 Feishu Upload Skill 使用示例');
    console.log('='.repeat(50));
    
    exampleDirectCall();
    exampleProgrammatic();
    exampleBatchUpload();
    
    console.log('\n🎉 示例演示完成!');
    console.log('\n📖 更多信息请查看:');
    console.log('  - SKILL.md: 完整技能文档');
    console.log('  - README.md: 使用说明');
    console.log('  - feishu_complete_upload.js: 主工具源码');
}

if (require.main === module) {
    main();
}

module.exports = {
    exampleDirectCall,
    exampleProgrammatic,
    exampleBatchUpload
};