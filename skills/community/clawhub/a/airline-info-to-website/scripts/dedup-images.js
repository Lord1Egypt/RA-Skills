#!/usr/bin/env node
/**
 * 图片去重工具
 * 检测并删除重复的图片文件（基于文件哈希）
 * 用法: node dedup-images.js --base-dir "FlightData/航司目录"
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 计算文件 MD5 哈希
function getFileHash(filePath) {
    try {
        const content = fs.readFileSync(filePath);
        return crypto.createHash('md5').update(content).digest('hex');
    } catch (e) {
        return null;
    }
}

// 查找重复图片
function findDuplicates(aircraftDir) {
    const imagesDir = path.join(aircraftDir, 'images');
    if (!fs.existsSync(imagesDir)) {
        return { error: 'no_images_dir' };
    }
    
    const categories = ['1-座椅布局', '2-座椅图片', '3-机上餐食', '4-娱乐设备', '5-其他信息'];
    const fileHashes = new Map();
    const duplicates = [];
    let totalFiles = 0;
    
    for (const category of categories) {
        const catDir = path.join(imagesDir, category);
        if (!fs.existsSync(catDir)) continue;
        
        const files = fs.readdirSync(catDir).filter(f => 
            /\.(jpg|jpeg|png|gif|webp|bmp)$/i.test(f)
        );
        
        for (const file of files) {
            totalFiles++;
            const filePath = path.join(catDir, file);
            const hash = getFileHash(filePath);
            
            if (!hash) continue;
            
            if (fileHashes.has(hash)) {
                const original = fileHashes.get(hash);
                duplicates.push({
                    original: original,
                    duplicate: { path: filePath, name: file, category },
                    hash: hash
                });
            } else {
                fileHashes.set(hash, { path: filePath, name: file, category });
            }
        }
    }
    
    return { totalFiles, duplicates };
}

// 处理单个机型
function processAircraft(aircraftDir, dryRun = false) {
    console.log(`\n==================================================`);
    console.log(`处理机型：${path.basename(aircraftDir)}`);
    console.log(`==================================================`);
    
    const result = findDuplicates(aircraftDir);
    
    if (result.error) {
        console.log(`⚠️  跳过：${result.error}`);
        return { success: false, reason: result.error };
    }
    
    console.log(`\n发现 ${result.duplicates.length} 张重复图片:`);
    
    for (const dup of result.duplicates) {
        console.log(`  🔴 ${dup.duplicate.category}/${dup.duplicate.name}`);
        console.log(`     与 ${dup.original.category}/${dup.original.name} 重复`);
        console.log(`     哈希: ${dup.hash.substring(0, 8)}...`);
        
        if (!dryRun) {
            try {
                fs.unlinkSync(dup.duplicate.path);
                console.log(`     ✅ 已删除`);
            } catch (e) {
                console.log(`     ❌ 删除失败: ${e.message}`);
            }
        }
    }
    
    console.log(`\n总计：发现 ${result.totalFiles} 张图片，删除 ${result.duplicates.length} 张重复项`);
    
    return { 
        success: true, 
        totalFiles: result.totalFiles, 
        removed: result.duplicates.length 
    };
}

function main() {
    const args = process.argv.slice(2);
    let baseDir = null;
    let dryRun = false;
    
    // 解析参数
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--base-dir' && i + 1 < args.length) {
            baseDir = args[i + 1];
        }
        if (args[i] === '--dry-run') {
            dryRun = true;
        }
    }
    
    if (!baseDir) {
        console.log('用法：node dedup-images.js --base-dir "FlightData/航司目录" [--dry-run]');
        process.exit(1);
    }
    
    if (!fs.existsSync(baseDir)) {
        console.log(`❌ 目录不存在：${baseDir}`);
        process.exit(1);
    }
    
    console.log('============================================================');
    console.log('航空公司飞机图片去重工具');
    console.log(`工作目录：${baseDir}`);
    if (dryRun) console.log('🔍 预览模式（不删除文件）');
    console.log('============================================================');
    
    // 查找所有机型目录
    const entries = fs.readdirSync(baseDir);
    const aircraftDirs = entries
        .map(e => path.join(baseDir, e))
        .filter(e => fs.statSync(e).isDirectory());
    
    console.log(`\n检测到 ${aircraftDirs.length} 个机型：${aircraftDirs.map(d => path.basename(d)).join(', ')}`);
    
    const allResults = [];
    for (const aircraftDir of aircraftDirs) {
        const result = processAircraft(aircraftDir, dryRun);
        allResults.push({ name: path.basename(aircraftDir), ...result });
    }
    
    // 生成汇总报告
    const summaryPath = path.join(baseDir, '图片去重报告.md');
    const summaryContent = `# 图片去重报告\n\n航司：${path.basename(baseDir)}\n生成时间：${new Date().toISOString()}\n${dryRun ? '**注意：这是预览报告，未实际删除文件**\n' : ''}\n## 各机型去重统计\n\n| 机型 | 总图片数 | 重复数 | 状态 |\n|------|---------|-------|------|\n${allResults.map(r => {
        if (r.success) {
            return `| ${r.name} | ${r.totalFiles} | ${r.removed} | ${r.removed === 0 ? '✅ 无重复' : '🧹 已清理'} |`;
        } else {
            return `| ${r.name} | - | - | ⚠️ ${r.reason} |`;
        }
    }).join('\n')}\n\n## 统计汇总\n\n- 总机型数：${allResults.length}\n- 有重复机型数：${allResults.filter(r => r.success && r.removed > 0).length}\n- 总删除重复数：${allResults.reduce((sum, r) => sum + (r.success ? r.removed : 0), 0)}\n`;
    
    fs.writeFileSync(summaryPath, summaryContent);
    console.log('\n============================================================');
    console.log('✅ 去重完成!');
    console.log(`\n报告已保存：${summaryPath}`);
}

if (require.main === module) {
    main();
}

module.exports = { findDuplicates, getFileHash };
