#!/usr/bin/env node
/**
 * SQL 加密工具 - 用于将正确 SQL 加密后写入 Cockpit 页面
 * 
 * 使用方式：
 *   node encrypt_for_page.js "SELECT * FROM WSD_PLAN_PROJECT WHERE DEL=0"
 *   node encrypt_for_page.js --decrypt "<ciphertext>" "<iv>"
 *   node encrypt_for_page.js --interactive
 */

const { encrypt, decrypt } = require('../src/security/encryptSql.js');

// ANSI 颜色
const c = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    red: '\x1b[31m',
};

function green(text) { return c.green + text + c.reset; }
function yellow(text) { return c.yellow + text + c.reset; }
function blue(text) { return c.blue + text + c.reset; }
function red(text) { return c.red + text + c.reset; }

// 输出格式化的 JSON 片段
function formatForPage(sql, keyName) {
    const result = encrypt(sql);
    return {
        keyName,
        plainSql: sql,
        placeholderCount: (sql.match(/\?/g) || []).length,
        encrypted: result,
        // 可直接粘贴的格式
        pasteReady: `  "${keyName}": {
    "ciphertext": "${result.ciphertext}",
    "iv": "${result.iv}",
    "algorithm": "AES-256-CBC-HMAC-SHA256"
  }`,
        // SQL_PLAIN 格式
        plainReady: `  "${keyName}": "${sql}"`
    };
}

// 打印结果
function printResult(output, keyName) {
    console.log('\n' + blue('═'.repeat(60)));
    console.log(blue(`SQL Key: ${yellow(keyName)}`));
    console.log(blue('═'.repeat(60)));
    
    console.log('\n' + green('【原文 SQL】'));
    console.log('  ' + output.plainSql);
    console.log(`\n  参数占位符 (?) 数量: ${output.placeholderCount}`);
    
    console.log('\n' + green('【解密验证】'));
    console.log('  用 decrypt() 验证加密后可正确还原');
    
    console.log('\n' + green('【ENCRYPTED_SQL 片段】(直接粘贴到 HTML)'));
    console.log(yellow('  注意：同时更新 SQL_PLAIN 中的对应条目！'));
    console.log('');
    console.log(output.pasteReady);
    
    console.log('\n' + green('【SQL_PLAIN 片段】'));
    console.log('');
    console.log(output.plainReady);
    
    console.log('\n' + blue('═'.repeat(60)) + '\n');
}

// 交互模式
async function interactive() {
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    const ask = (q) => new Promise(r => rl.question(q, r));
    
    console.log(blue('\n╔════════════════════════════════════════╗'));
    console.log(blue('║      Cockpit SQL 加密工具 (交互模式)     ║'));
    console.log(blue('╚════════════════════════════════════════╝\n'));
    
    while (true) {
        const keyName = await ask(yellow('SQL key 名称 (输入 q 退出): '));
        if (keyName === 'q' || keyName === 'Q') break;
        
        const sql = await ask(yellow('SQL 原文 (单行): '));
        if (sql === 'q' || sql === 'Q') break;
        
        try {
            const output = formatForPage(sql, keyName);
            printResult(output, keyName);
        } catch (e) {
            console.log(red(`加密失败: ${e.message}`));
        }
        console.log('');
    }
    
    rl.close();
    console.log(green('\n已退出。'));
}

// 批量处理文件
async function batchFromFile(filePath) {
    const fs = require('fs');
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n').filter(l => l.trim() && !l.startsWith('#'));
    
    console.log(blue(`\n批量处理 ${lines.length} 条 SQL...\n`));
    
    const results = [];
    for (const line of lines) {
        try {
            const [keyName, ...sqlParts] = line.split('|');
            const sql = sqlParts.join('|').trim();
            const output = formatForPage(sql, keyName.trim());
            results.push(output);
            console.log(green('✅ ') + `${output.keyName} (${output.placeholderCount} 个 ?)`);
        } catch (e) {
            console.log(red('❌ ') + `${line.substring(0, 30)}... - ${e.message}`);
        }
    }
    
    console.log(blue('\n═══ 批量结果汇总 ═══\n'));
    
    console.log(green('【ENCRYPTED_SQL】'));
    results.forEach(r => {
        console.log(r.pasteReady + (r !== results[results.length - 1] ? ',' : ''));
    });
    
    console.log('\n' + green('【SQL_PLAIN】'));
    results.forEach(r => {
        console.log(r.plainReady + ',');
    });
}

// 主入口
async function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log(blue('\n╔════════════════════════════════════════╗'));
        console.log(blue('║      Cockpit SQL 加密工具              ║'));
        console.log(blue('╚════════════════════════════════════════╝\n'));
        console.log('用法:');
        console.log('  ' + yellow('node encrypt_for_page.js "<SQL>" [keyName]'));
        console.log('    加密单条 SQL');
        console.log('');
        console.log('  ' + yellow('node encrypt_for_page.js --interactive'));
        console.log('    交互模式');
        console.log('');
        console.log('  ' + yellow('node encrypt_for_page.js --decrypt "<ciphertext>" "<iv>"'));
        console.log('    解密验证');
        console.log('');
        console.log('  ' + yellow('node encrypt_for_page.js --batch <file.txt>'));
        console.log('    批量处理（file.txt 格式: keyName|SQL）');
        console.log('\n');
        return;
    }
    
    if (args[0] === '--interactive' || args[0] === '-i') {
        await interactive();
        return;
    }
    
    if (args[0] === '--decrypt' || args[0] === '-d') {
        const [,, ciphertext, iv] = args;
        if (!ciphertext || !iv) {
            console.log(red('用法: --decrypt "<ciphertext>" "<iv>"'));
            return;
        }
        try {
            const sql = decrypt(ciphertext, iv);
            console.log(green('解密成功:'));
            console.log('  ' + sql);
        } catch (e) {
            console.log(red(`解密失败: ${e.message}`));
        }
        return;
    }
    
    if (args[0] === '--batch' || args[0] === '-b') {
        const filePath = args[1];
        if (!filePath) {
            console.log(red('用法: --batch <file.txt>'));
            return;
        }
        await batchFromFile(filePath);
        return;
    }
    
    // 单条 SQL 加密
    const sql = args[0];
    const keyName = args[1] || 'sqlKey';
    
    try {
        const output = formatForPage(sql, keyName);
        printResult(output, keyName);
    } catch (e) {
        console.log(red(`加密失败: ${e.message}`));
        process.exit(1);
    }
}

main().catch(e => {
    console.error(red(`Error: ${e.message}`));
    process.exit(1);
});
