#!/usr/bin/env node
/**
 * 图片语义分类工具
 * 将 0-原始数据 中的图片分类到 1-5 目录
 * 用法: node classify-images.js --base-dir "FlightData/航司目录"
 */

const fs = require('fs');
const path = require('path');

// 分类规则（按文件名关键词匹配）
const CLASSIFICATION_RULES = {
    '1-座椅布局': [
        /seatmap/i, /seat.map/i, /layout/i, /plan/i,
        /座位图/i, /布局/i, /平面图/i,
        /-layout-/, /-plan-/
    ],
    '2-座椅图片': [
        /seat/i, /chair/i, /suite/i,
        /座椅/i, /座位/i, /商务舱/i, /经济舱/i, /头等舱/i,
        /business/i, /economy/i, /first/i, /premium/i,
        /_thumb/i, /-thumb/i
    ],
    '3-机上餐食': [
        /meal/i, /food/i, /dining/i, /menu/i, /catering/i,
        /餐食/i, /餐饮/i, /菜单/i, /食物/i, /美食/i,
        /dish/i, /cuisine/
    ],
    '4-娱乐设备': [
        /ife/i, /entertainment/i, /screen/i, /monitor/i, /wifi/i, /wi-fi/i,
        /娱乐/i, /屏幕/i, /显示器/i, /IFE/i,
        /avod/i, /tv/i, /usb/i, /power/i
    ],
    '5-其他信息': [
        /exterior/i, /logo/i, /badge/i, /other/i, /misc/i,
        /外观/i, /标志/i, /logo/i, /其他/i
    ]
};

function classifyImage(filename) {
    const lowerName = filename.toLowerCase();
    
    for (const [category, patterns] of Object.entries(CLASSIFICATION_RULES)) {
        for (const pattern of patterns) {
            if (pattern.test(lowerName)) {
                return category;
            }
        }
    }
    
    // 默认分类：如果有 "thumb" 关键词，认为是座椅图片
    if (/thumb|thumbnail/.test(lowerName)) {
        return '2-座椅图片';
    }
    
    return '5-其他信息';
}

function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

function processAircraft(aircraftDir) {
    console.log(`\n==================================================`);
    console.log(`处理机型：${path.basename(aircraftDir)}`);
    console.log(`==================================================`);
    
    const imagesDir = path.join(aircraftDir, 'images');
    if (!fs.existsSync(imagesDir)) {
        console.log(`⚠️  未找到 images 目录，跳过`);
        return { success: false, reason: 'no_images_dir' };
    }
    
    const rawDir = path.join(imagesDir, '0-原始数据');
    if (!fs.existsSync(rawDir)) {
        console.log(`⚠️  未找到 0-原始数据 目录，跳过`);
        return { success: false, reason: 'no_raw_data' };
    }
    
    // 确保分类目录存在
    const categories = ['1-座椅布局', '2-座椅图片', '3-机上餐食', '4-娱乐设备', '5-其他信息'];
    for (const cat of categories) {
        ensureDir(path.join(imagesDir, cat));
    }
    
    // 读取原始数据中的文件
    const files = fs.readdirSync(rawDir);
    const imageFiles = files.filter(f => 
        /\.(jpg|jpeg|png|gif|webp|bmp)$/i.test(f)
    );
    
    console.log(`找到 ${imageFiles.length} 张图片`);
    
    const results = {
        '1-座椅布局': 0,
        '2-座椅图片': 0,
        '3-机上餐食': 0,
        '4-娱乐设备': 0,
        '5-其他信息': 0
    };
    
    for (const file of imageFiles) {
        const category = classifyImage(file);
        const srcPath = path.join(rawDir, file);
        const destDir = path.join(imagesDir, category);
        const destPath = path.join(destDir, file);
        
        // 复制文件（保留原始文件）
        try {
            fs.copyFileSync(srcPath, destPath);
            results[category]++;
        } catch (e) {
            console.log(`  ⚠️  复制失败 ${file}: ${e.message}`);
        }
    }
    
    console.log(`\n分类结果:`);
    for (const [cat, count] of Object.entries(results)) {
        console.log(`  ${cat}: ${count} 张`);
    }
    
    // 生成分类报告
    const reportPath = path.join(imagesDir, 'classification-report.md');
    const reportContent = `# 图片分类报告\n\n机型：${path.basename(aircraftDir)}\n生成时间：${new Date().toISOString()}\n\n## 分类统计\n\n| 类别 | 数量 |\n|------|------|\n${Object.entries(results).map(([k, v]) => `| ${k} | ${v} |`).join('\n')}\n\n## 分类规则\n\n- 1-座椅布局：包含 seatmap、layout、plan、座位图、布局等关键词\n- 2-座椅图片：包含 seat、座椅、座位、商务舱、经济舱、头等舱、thumb 等关键词\n- 3-机上餐食：包含 meal、food、menu、餐食、餐饮、菜单等关键词\n- 4-娱乐设备：包含 ife、entertainment、screen、娱乐、屏幕等关键词\n- 5-其他信息：默认分类，包含外观、标志、logo 等关键词\n`;
    
    fs.writeFileSync(reportPath, reportContent);
    console.log(`\n报告已保存：${reportPath}`);
    
    return { success: true, results };
}

function main() {
    const args = process.argv.slice(2);
    let baseDir = null;
    
    // 解析参数
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--base-dir' && i + 1 < args.length) {
            baseDir = args[i + 1];
        }
    }
    
    if (!baseDir) {
        console.log('用法：node classify-images.js --base-dir "FlightData/航司目录"');
        process.exit(1);
    }
    
    if (!fs.existsSync(baseDir)) {
        console.log(`❌ 目录不存在：${baseDir}`);
        process.exit(1);
    }
    
    console.log('============================================================');
    console.log('航空公司飞机图片分类工具');
    console.log(`工作目录：${baseDir}`);
    console.log('分类体系：0-原始数据，1-座椅布局，2-座椅图片，3-机上餐食，4-娱乐设备，5-其他信息');
    console.log('============================================================');
    
    // 查找所有机型目录
    const entries = fs.readdirSync(baseDir);
    const aircraftDirs = entries
        .map(e => path.join(baseDir, e))
        .filter(e => fs.statSync(e).isDirectory());
    
    console.log(`\n检测到 ${aircraftDirs.length} 个机型：${aircraftDirs.map(d => path.basename(d)).join(', ')}`);
    
    const allResults = [];
    for (const aircraftDir of aircraftDirs) {
        const result = processAircraft(aircraftDir);
        allResults.push({ name: path.basename(aircraftDir), ...result });
    }
    
    // 生成汇总报告
    const summaryPath = path.join(baseDir, '图片分类汇总.md');
    const summaryContent = `# 图片分类汇总报告\n\n航司：${path.basename(baseDir)}\n生成时间：${new Date().toISOString()}\n\n## 各机型分类统计\n\n| 机型 | 座椅布局 | 座椅图片 | 机上餐食 | 娱乐设备 | 其他信息 |\n|------|---------|---------|---------|---------|---------|\n${allResults.map(r => {
        if (r.results) {
            return `| ${r.name} | ${r.results['1-座椅布局']} | ${r.results['2-座椅图片']} | ${r.results['3-机上餐食']} | ${r.results['4-娱乐设备']} | ${r.results['5-其他信息']} |`;
        } else {
            return `| ${r.name} | - | - | - | - | ${r.reason} |`;
        }
    }).join('\n')}\n`;
    
    fs.writeFileSync(summaryPath, summaryContent);
    console.log(`\n============================================================`);
    console.log('✅ 所有处理完成!');
    console.log(`\n汇总报告：${summaryPath}`);
}

if (require.main === module) {
    main();
}

module.exports = { classifyImage, CLASSIFICATION_RULES };
