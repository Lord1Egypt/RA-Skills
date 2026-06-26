#!/usr/bin/env node

/**
 * 寻梦之旅短视频脚本生成器
 * 根据梦境和现实目的地，生成抖音/小红书爆款短视频脚本
 * 包含标题、15-30秒脚本、BGM建议、字幕文案
 */

const fs = require('fs');
const path = require('path');

class ShortVideoScriptGenerator {
    constructor() {
        this.videoTemplates = [
            {
                style: '情感治愈',
                titlePattern: '我反复梦到{dream_element}，直到我来到{destination}...',
                hookPattern: '你相信吗？有些地方真的会先在梦里出现',
                bgmSuggestion: '《起风了》纯音乐版 / 《River Flows in You》钢琴版'
            },
            {
                style: '宿命感',
                titlePattern: '梦境相似度{similarity}%！AI帮我找到了梦里的{dream_element}',
                hookPattern: '这个我在梦里见过无数次的地方，竟然真实存在',
                bgmSuggestion: '《星际穿越》原声 / 《Cornfield Chase》'
            },
            {
                style: '反差震撼',
                titlePattern: '把梦变成旅行是什么体验？结局泪目了...',
                hookPattern: '我用AI把梦境变成了现实，结果比梦更美',
                bgmSuggestion: '《追光者》/ 《夜空中最亮的星》'
            },
            {
                style: '冒险探索',
                titlePattern: '跟着梦境去旅行！{destination}寻梦全记录',
                hookPattern: '别人用AI规划旅行，我用AI寻梦',
                bgmSuggestion: '《平凡之路》/ 《蓝莲花》'
            },
            {
                style: '诗意浪漫',
                titlePattern: '梦里寻踪，现实成真 | {destination}寻梦日记',
                hookPattern: '有些地方，我们先在梦里遇见',
                bgmSuggestion: '《贝加尔湖畔》/ 《成都》纯音乐版'
            },
            {
                style: '悬念吸引',
                titlePattern: '我梦到这个地方{dream_element}，结果现实更震撼！',
                hookPattern: '猜猜这是哪里？和我梦里一模一样',
                bgmSuggestion: '《悬疑》类影视原声 / 《Time》汉斯季默'
            },
            {
                style: '数据冲击',
                titlePattern: 'AI说这里和我梦境92%相似！亲测后我信了',
                hookPattern: '梦境相似度92%是什么概念？看完你就懂了',
                bgmSuggestion: '科技感电子音乐 / 《Digital Love》'
            },
            {
                style: '故事叙述',
                titlePattern: '从梦境到现实，我的{destination}寻梦之旅',
                hookPattern: '这是一个关于梦成真的真实故事',
                bgmSuggestion: '《故事》/ 《岁月神偷》'
            },
            {
                style: '视觉震撼',
                titlePattern: '美哭了！梦里的{dream_element}在这里完美重现',
                hookPattern: '当梦境照进现实，每一帧都是壁纸',
                bgmSuggestion: '《大鱼》/ 《光年之外》'
            },
            {
                style: '互动引导',
                titlePattern: '你梦到过哪里？我用AI找到了我的梦中情地',
                hookPattern: '评论区告诉我你反复梦到的场景',
                bgmSuggestion: '轻快流行音乐 / 《小幸运》'
            }
        ];
    }

    /**
     * 提取梦境关键元素
     */
    extractDreamElements(dreamDescription) {
        const elements = [];
        const keywords = {
            '古镇': '古镇', '水乡': '水乡', '小镇': '小镇',
            '山': '山峰', '云海': '云海', '雪山': '雪山',
            '海': '大海', '沙滩': '沙滩', '海岛': '海岛',
            '森林': '森林', '竹林': '竹林', '花海': '花海',
            '星空': '星空', '银河': '银河', '沙漠': '沙漠',
            '雪': '雪景', '雨': '雨景', '雾': '雾景'
        };

        Object.keys(keywords).forEach(keyword => {
            if (dreamDescription.includes(keyword)) {
                elements.push(keywords[keyword]);
            }
        });

        return elements.length > 0 ? elements : ['神秘地方'];
    }

    /**
     * 生成单个视频脚本
     */
    generateSingleScript(template, data, index) {
        const title = template.titlePattern
            .replace('{dream_element}', data.dreamElements[0] || '那个地方')
            .replace('{destination}', data.destination || '目的地')
            .replace('{similarity}', data.similarityScore || '90');

        const hook = template.hookPattern;
        
        const script15s = `【0-3秒】${hook}
【3-8秒】展示梦境描述 + AI还原画面
【8-12秒】现实目的地震撼画面
【12-15秒】梦境vs现实对比 + 引导关注`;

        const script30s = `【0-5秒】${hook}
【5-10秒】"我反复梦到${data.dreamElements[0] || '一个地方'}..."
【10-15秒】展示AI梦境还原过程
【15-20秒】"直到Fly.ai帮我找到了这里——${data.destination}"
【20-25秒】现实美景混剪 + 梦境对比
【25-30秒】"梦境相似度${data.similarityScore || 90}%，梦真的成真了" + 引导互动`;

        const subtitleCopy = `"${hook}
${data.dreamElements[0] || '那个地方'}，${data.destination}
梦境相似度${data.similarityScore || 90}%
有些地方，我们先在梦里遇见
然后用 Fly.ai 把它寻成真
#寻梦之旅 #梦境成真 #FlyAI旅行"`;

        const shootingTips = [
            '使用横屏拍摄，后期可裁剪为竖屏',
            '梦境部分使用滤镜增强梦幻感',
            '现实部分使用自然光，突出真实感',
            '对比画面使用分屏或切换效果',
            '结尾加文字引导关注和评论'
        ];

        return {
            index: index + 1,
            style: template.style,
            title: title,
            hook: hook,
            script15s: script15s,
            script30s: script30s,
            bgm: template.bgmSuggestion,
            subtitleCopy: subtitleCopy,
            shootingTips: shootingTips
        };
    }

    /**
     * 生成10个完整视频脚本
     */
    generateScripts(data) {
        console.log('🎬 正在生成短视频脚本包...\n');

        const dreamElements = this.extractDreamElements(data.dreamDescription || '');
        const fullData = { ...data, dreamElements };

        const scripts = this.videoTemplates.map((template, index) => {
            return this.generateSingleScript(template, fullData, index);
        });

        console.log(`✅ 已生成 ${scripts.length} 个视频脚本\n`);
        console.log('📋 脚本列表:');
        scripts.forEach(script => {
            console.log(`  ${script.index}. [${script.style}] ${script.title}`);
        });
        console.log('');

        return scripts;
    }

    /**
     * 生成 HTML 预览页面
     */
    generateHTMLPreview(scripts, outputPath = './video-scripts.html') {
        const scriptsHTML = scripts.map(script => `
            <div class="script-card">
                <div class="script-header">
                    <span class="script-number">#${script.index}</span>
                    <span class="script-style">${script.style}</span>
                </div>
                <h3>${script.title}</h3>
                <div class="script-section">
                    <h4>🎯 开头钩子</h4>
                    <p>${script.hook}</p>
                </div>
                <div class="script-section">
                    <h4>⏱️ 15秒脚本</h4>
                    <pre>${script.script15s}</pre>
                </div>
                <div class="script-section">
                    <h4>⏱️ 30秒脚本</h4>
                    <pre>${script.script30s}</pre>
                </div>
                <div class="script-section">
                    <h4>🎵 BGM建议</h4>
                    <p>${script.bgm}</p>
                </div>
                <div class="script-section">
                    <h4>📝 字幕文案</h4>
                    <pre class="subtitle">${script.subtitleCopy}</pre>
                </div>
                <div class="script-section">
                    <h4>📸 拍摄技巧</h4>
                    <ul>
                        ${script.shootingTips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
                <button class="copy-btn" onclick="copyScript(${script.index})">📋 复制完整脚本</button>
            </div>
        `).join('');

        const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>寻梦之旅 - 短视频脚本包</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .scripts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
        }
        .script-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .script-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }
        .script-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .script-number {
            font-size: 1.5em;
            font-weight: bold;
            color: #764ba2;
        }
        .script-style {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        .script-card h3 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.2em;
            line-height: 1.5;
        }
        .script-section {
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .script-section h4 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 0.95em;
        }
        .script-section p {
            color: #555;
            line-height: 1.6;
        }
        .script-section pre {
            background: white;
            padding: 15px;
            border-radius: 8px;
            font-size: 0.9em;
            line-height: 1.8;
            color: #333;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .script-section pre.subtitle {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            color: #333;
        }
        .script-section ul {
            margin-left: 20px;
            color: #555;
        }
        .script-section li {
            margin: 8px 0;
        }
        .copy-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1em;
            margin-top: 15px;
            transition: all 0.3s ease;
        }
        .copy-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .tip {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            margin-top: 40px;
        }
        .tip h3 {
            color: #764ba2;
            margin-bottom: 15px;
        }
        .tip ul {
            margin-left: 20px;
            color: #555;
        }
        .tip li {
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 寻梦之旅短视频脚本包</h1>
        
        <div class="scripts-grid">
            ${scriptsHTML}
        </div>

        <div class="tip">
            <h3>💡 使用建议</h3>
            <ul>
                <li>优先拍摄前3个视频，测试数据反馈</li>
                <li>15秒版本适合抖音，30秒版本适合小红书/B站</li>
                <li>BGM选择热门歌曲的纯音乐版，避免版权问题</li>
                <li>发布时添加话题标签：#寻梦之旅 #梦境成真 #FlyAI旅行</li>
                <li>在评论区引导用户分享自己的梦境经历</li>
            </ul>
        </div>
    </div>

    <script>
        const scriptsData = ${JSON.stringify(scripts)};
        
        function copyScript(index) {
            const script = scriptsData.find(s => s.index === index);
            if (!script) return;
            
            const text = \`标题：\${script.title}
风格：\${script.style}

开头钩子：
\${script.hook}

15秒脚本：
\${script.script15s}

30秒脚本：
\${script.script30s}

BGM建议：
\${script.bgm}

字幕文案：
\${script.subtitleCopy}

拍摄技巧：
\${script.shootingTips.join('\\n')}
\`;
            
            navigator.clipboard.writeText(text).then(() => {
                alert('脚本已复制到剪贴板！');
            });
        }
    </script>
</body>
</html>`;

        fs.writeFileSync(outputPath, html, 'utf-8');
        console.log(`✅ HTML 脚本预览已保存: ${outputPath}`);
        return outputPath;
    }

    /**
     * 生成 JSON 格式脚本包
     */
    generateJSON(scripts, outputPath = './video-scripts.json') {
        fs.writeFileSync(outputPath, JSON.stringify(scripts, null, 2), 'utf-8');
        console.log(`✅ JSON 脚本包已保存: ${outputPath}`);
        return outputPath;
    }

    /**
     * 主函数：生成完整的短视频脚本包
     */
    generate(data, outputDir = './') {
        const scripts = this.generateScripts(data);
        
        const htmlPath = path.join(outputDir, 'video-scripts.html');
        const jsonPath = path.join(outputDir, 'video-scripts.json');
        
        this.generateHTMLPreview(scripts, htmlPath);
        this.generateJSON(scripts, jsonPath);
        
        console.log('\n🎉 短视频脚本包生成完成！');
        console.log(`📄 HTML预览: ${htmlPath}`);
        console.log(`📊 JSON数据: ${jsonPath}`);
        console.log('\n💡 在浏览器中打开 HTML 文件查看并复制脚本\n');
        
        return { scripts, htmlPath, jsonPath };
    }
}

// CLI 使用方式
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('🎬 寻梦之旅短视频脚本生成器');
        console.log('\n使用方法:');
        console.log('  node generate-video-scripts.js --dream "梦境描述" --dest "目的地" --score 92');
        console.log('\n示例:');
        console.log('  node generate-video-scripts.js --dream "我梦到古镇" --dest "安徽宏村" --score 92\n');
        process.exit(0);
    }

    // 解析命令行参数
    const params = {};
    for (let i = 0; i < args.length; i += 2) {
        if (args[i].startsWith('--')) {
            const key = args[i].slice(2);
            params[key] = args[i + 1];
        }
    }

    const generator = new ShortVideoScriptGenerator();
    generator.generate({
        dreamDescription: params.dream || '',
        destination: params.dest || '目的地',
        similarityScore: params.score || '90'
    });
}

module.exports = ShortVideoScriptGenerator;
