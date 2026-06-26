#!/usr/bin/env node

/**
 * 寻梦之旅 HTML 报告生成器
 * 将行程数据自动填充到 HTML 模板中，生成沉浸式的寻梦报告
 * 支持命令行调用和模块导入
 */

const fs = require('fs');
const path = require('path');
const QuoteGenerator = require('./generate-quote');

class DreamReportGenerator {
    constructor(templatePath = null) {
        const defaultTemplate = path.join(__dirname, '..', 'assets', 'report-template.html');
        this.templatePath = templatePath || defaultTemplate;
        this.template = this.loadTemplate();
        this.quoteGenerator = new QuoteGenerator();
    }

    /**
     * 加载 HTML 模板
     */
    loadTemplate() {
        if (!fs.existsSync(this.templatePath)) {
            throw new Error(`模板文件不存在: ${this.templatePath}`);
        }
        return fs.readFileSync(this.templatePath, 'utf-8');
    }

    /**
     * 生成时间线 HTML
     */
    generateTimeline(timelineData) {
        return timelineData.map(day => `
            <div class="timeline-item">
                <h4>${day.title}</h4>
                <p>${day.description}</p>
            </div>
        `).join('\n');
    }

    /**
     * 生成照片墙 HTML
     */
    generatePhotoGallery(photos) {
        if (!photos || photos.length === 0) {
            return `
                <div class="photo-item">
                    <div style="width:100%; height:280px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display:flex; align-items:center; justify-content:center; color:white; font-size:1.2em;">
                        📸 照片待添加
                    </div>
                    <div class="caption">上传你的寻梦照片</div>
                </div>
            `;
        }

        return photos.map(photo => {
            // 支持本地图片路径或 URL
            const imgSrc = photo.src || photo.path || '';
            const imgAlt = photo.alt || photo.caption || '寻梦瞬间';
            const caption = photo.caption || '';
            
            if (!imgSrc) {
                return `
                    <div class="photo-item">
                        <div style="width:100%; height:280px; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); display:flex; align-items:center; justify-content:center; color:#333; font-size:1.1em; text-align:center; padding:20px;">
                            📷<br>${imgAlt}
                        </div>
                        ${caption ? `<div class="caption">${caption}</div>` : ''}
                    </div>
                `;
            }
            
            return `
                <div class="photo-item">
                    <img src="${imgSrc}" alt="${imgAlt}">
                    ${caption ? `<div class="caption">${caption}</div>` : ''}
                </div>
            `;
        }).join('\n');
    }

    /**
     * 生成列表项 HTML
     */
    generateListItems(items) {
        return items.map(item => `<li>${item}</li>`).join('\n');
    }

    /**
     * 填充模板数据
     */
    fillTemplate(data) {
        let html = this.template;

        // 基础数据 - 使用 replaceAll 替换所有出现的位置
        html = html.replaceAll('{{title}}', data.title || '寻梦报告');
        html = html.replaceAll('{{dream_quote}}', data.dreamQuote || '梦里寻踪，现实成真');
        html = html.replaceAll('{{dream_description}}', data.dreamDescription || '');
        html = html.replaceAll('{{dream_restoration}}', data.dreamRestoration || '');
        html = html.replaceAll('{{destination_name}}', data.destinationName || '');
        html = html.replaceAll('{{destination_description}}', data.destinationDescription || '');

        // 对比元素
        html = html.replace('{{dream_elements}}', this.generateListItems(data.dreamElements || []));
        html = html.replace('{{reality_elements}}', this.generateListItems(data.realityElements || []));

        // 统计数据
        html = html.replace('{{similarity_score}}', data.similarityScore || '0');
        html = html.replace('{{total_cost}}', data.totalCost || '0');
        html = html.replace('{{days}}', data.days || '0');
        html = html.replace('{{destiny_index}}', data.destinyIndex || '0/100');

        // 时间线
        html = html.replace('{{timeline_items}}', this.generateTimeline(data.timeline || []));

        // 照片墙
        html = html.replace('{{photo_gallery}}', this.generatePhotoGallery(data.photos || []));

        // 情感日记
        html = html.replace('{{emotional_diary}}', data.emotionalDiary || '');

        // 金句 - 支持智能生成或随机生成
        let goldenQuote = data.goldenQuote;
        if (!goldenQuote || goldenQuote === 'auto') {
            const quoteResult = this.quoteGenerator.generate(data.dreamDescription || '');
            goldenQuote = quoteResult.quote;
            console.log(`✨ 金句主题: ${quoteResult.theme}`);
        }
        html = html.replace('{{golden_quote}}', goldenQuote);

        // 生成时间
        html = html.replace('{{generate_time}}', data.generateTime || new Date().toLocaleDateString('zh-CN'));

        return html;
    }

    /**
     * 生成完整的 HTML 报告
     */
    generate(data, outputPath = './dream-report.html') {
        console.log('🌙 正在生成寻梦之旅 HTML 报告...\n');

        const html = this.fillTemplate(data);
        fs.writeFileSync(outputPath, html, 'utf-8');

        console.log(`✅ 报告已生成: ${outputPath}`);
        console.log(`📊 梦境相似度: ${data.similarityScore}%`);
        console.log(`💰 总花费: ${data.totalCost}元`);
        console.log(`📅 行程天数: ${data.days}天`);
        console.log(`✨ 宿命感指数: ${data.destinyIndex}`);
        console.log('\n💡 在浏览器中打开查看完整报告\n');

        return outputPath;
    }

    /**
     * 从 JSON 文件生成报告
     */
    generateFromJSON(jsonPath, outputPath = null) {
        if (!fs.existsSync(jsonPath)) {
            throw new Error(`JSON 文件不存在: ${jsonPath}`);
        }

        const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
        const defaultOutput = outputPath || `./${data.title || 'dream'}-report.html`;
        
        return this.generate(data, defaultOutput);
    }
}

// CLI 使用方式
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('🌙 寻梦之旅 HTML 报告生成器');
        console.log('\n使用方法:');
        console.log('  1. 从 JSON 文件生成:');
        console.log('     node generate-report.js --json data.json');
        console.log('\n  2. 查看示例:');
        console.log('     node generate-report.js --example\n');
        process.exit(0);
    }

    const generator = new DreamReportGenerator();

    if (args[0] === '--json' && args[1]) {
        generator.generateFromJSON(args[1]);
    } else if (args[0] === '--example') {
        // 生成示例报告
        const exampleData = {
            title: '安徽宏村寻梦报告',
            dreamQuote: '梦里寻踪，现实成真',
            dreamDescription: '我反复梦到一个模糊的地方：一座被大雾笼罩的古镇，石板路总是湿的，河边挂着很多红灯笼，远处有座很陡的山，晚上能听到低沉的钟声，感觉既熟悉又陌生。',
            dreamRestoration: '晨雾如纱，轻轻笼罩着一座沉睡千年的古镇。青石板路被昨夜的雨水洗刷得发亮，每一道缝隙都藏着岁月的故事。河岸边，一排排红灯笼在微风中摇曳，倒映在潺潺流水中，像是梦境与现实之间的桥梁。远处的山峰隐没在云雾中，若隐若现，宛如仙境。夜幕降临时，低沉的钟声从山谷传来，一声声敲在心上，既熟悉又陌生，仿佛在召唤你回到某个前世到过的地方。',
            destinationName: '安徽黟县宏村',
            destinationDescription: '宏村，位于安徽省黟县，是中国最具代表性的古村落之一。这里的水系布局独特，被誉为"中国画里的乡村"。雨季的宏村，晨雾中的马头墙、湿漉漉的石板路、河边的红灯笼，完美重现了你的梦境。',
            dreamElements: ['大雾笼罩的古镇', '湿漉漉的石板路', '河边的红灯笼', '远处的陡山', '低沉的钟声', '既熟悉又陌生的感觉'],
            realityElements: ['宏村晨雾中的马头墙', '雨后发亮的青石板路', '南湖岸边的红灯笼装饰', '远处的黄山余脉', '村中古寺的晚钟', '前世到过的宿命感'],
            similarityScore: '92',
            totalCost: '2580',
            days: '3',
            destinyIndex: '95/100',
            timeline: [
                {
                    title: 'Day 1: 初遇宏村',
                    description: '当你踏上石板路的那一刻，梦中的场景几乎完美重现。晨雾中的马头墙若隐若现，南湖的水面倒映着古民居。夜晚，村中传来钟声，和你的梦境一模一样。'
                },
                {
                    title: 'Day 2: 深度寻梦',
                    description: '清晨漫步在月沼边，湿漉漉的石板路反射着晨光。当地老人讲述宏村的故事，你感受到一种莫名的熟悉感，仿佛曾经来过这里。'
                },
                {
                    title: 'Day 3: 梦境验证',
                    description: '登上村外的山丘，俯瞰整个宏村。云雾缭绕中，你的梦境和现实完全重叠。这一刻，你知道梦真的成真了。'
                }
            ],
            photos: [
                { src: 'photo1.jpg', alt: '宏村晨雾', caption: '梦中的晨雾，在这里真实可见' },
                { src: 'photo2.jpg', alt: '石板路', caption: '湿漉漉的石板路，和梦里一模一样' },
                { src: 'photo3.jpg', alt: '红灯笼', caption: '南湖岸边的红灯笼，倒映在水中' }
            ],
            emotionalDiary: '当我踏上宏村的石板路的那一刻，眼泪不自觉地流了下来。这个我在梦里反复出现的地方，竟然真实地存在于这个世界。晨雾中的马头墙、湿漉漉的青石板、河边的红灯笼，每一个细节都和梦境中一模一样。原来，有些地方我们真的会在梦里遇见，然后用一生的时间去寻找它。感谢 Fly.ai，帮我把这个梦寻成真。',
            goldenQuote: 'auto', // 自动生成金句
            generateTime: '2026年4月4日'
        };

        generator.generate(exampleData, './example-dream-report.html');
    }
}

module.exports = DreamReportGenerator;
