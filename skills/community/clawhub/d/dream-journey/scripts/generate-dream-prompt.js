#!/usr/bin/env node

/**
 * 梦境视觉 Prompt 生成器
 * 将用户模糊的梦境描述转化为可用于 AI 图像生成的精美视觉 Prompt
 * 支持生成中英文双版本，并输出为 HTML 预览页面
 */

const fs = require('fs');
const path = require('path');

class DreamVisualPromptGenerator {
    constructor() {
        this.stylePresets = {
            '古镇水乡': {
                atmosphere: 'misty morning, soft diffused light, ancient Chinese water town',
                color: 'warm golden hour tones, muted greens and blues',
                mood: 'nostalgic, peaceful, timeless'
            },
            '山林云海': {
                atmosphere: 'sea of clouds, mountain peaks emerging from mist, ethereal light rays',
                color: 'cool blues and whites with warm sunrise accents',
                mood: 'majestic, mystical, transcendent'
            },
            '沙漠星空': {
                atmosphere: 'vast desert under starry sky, Milky Way visible, camping fire glow',
                color: 'deep blues and purples with warm orange firelight',
                mood: 'vast, contemplative, awe-inspiring'
            },
            '雪域高原': {
                atmosphere: 'snow-capped mountains, prayer flags, clear blue sky, altitude light',
                color: 'crisp whites, deep blues, vibrant prayer flag colors',
                mood: 'sacred, pure, spiritual'
            },
            '海岛沙滩': {
                atmosphere: 'turquoise water, white sand, palm trees swaying, golden sunset',
                color: 'tropical blues, warm golds, lush greens',
                mood: 'relaxing, paradise, carefree'
            },
            '古城小巷': {
                atmosphere: 'narrow cobblestone streets, ancient walls, dappled sunlight, local life',
                color: 'warm earth tones, weathered textures, golden hour',
                mood: 'authentic, lived-in, charming'
            }
        };
    }

    /**
     * 分析梦境描述，提取关键元素
     */
    analyzeDream(description) {
        const elements = {
            visual: [],
            auditory: [],
            atmospheric: [],
            emotional: [],
            timeOfDay: '',
            weather: '',
            location: ''
        };

        // 提取视觉元素
        const visualKeywords = {
            '雾': 'mist/fog', '大雾': 'heavy mist', '晨雾': 'morning mist',
            '山': 'mountains', '高山': 'tall mountains', '陡山': 'steep mountains',
            '水': 'water', '河': 'river', '湖': 'lake', '海': 'sea',
            '古镇': 'ancient town', '小镇': 'small town',
            '石板路': 'cobblestone path', '青石板': 'bluestone path',
            '灯笼': 'lanterns', '红灯笼': 'red lanterns',
            '桥': 'bridge', '石桥': 'stone bridge',
            '树': 'trees', '森林': 'forest', '竹林': 'bamboo forest',
            '云': 'clouds', '云海': 'sea of clouds',
            '雪': 'snow', '雪山': 'snow mountain',
            '花': 'flowers', '花海': 'sea of flowers',
            '星空': 'starry sky', '银河': 'Milky Way'
        };

        Object.keys(visualKeywords).forEach(keyword => {
            if (description.includes(keyword)) {
                elements.visual.push(visualKeywords[keyword]);
            }
        });

        // 提取听觉元素
        const auditoryKeywords = {
            '钟声': 'bell tolling', '钟': 'bell sound',
            '流水': 'flowing water', '潺潺': 'babbling brook',
            '鸟鸣': 'birdsong', '鸟叫': 'birds chirping',
            '风声': 'wind howling', '风': 'gentle wind',
            '雨': 'rain', '雨声': 'rainfall sound'
        };

        Object.keys(auditoryKeywords).forEach(keyword => {
            if (description.includes(keyword)) {
                elements.auditory.push(auditoryKeywords[keyword]);
            }
        });

        // 提取氛围元素
        const atmosphericKeywords = {
            '模糊': 'dreamy, ethereal', '朦胧': 'hazy,朦胧 light',
            '安静': 'quiet, serene', '宁静': 'tranquil, peaceful',
            '神秘': 'mysterious, enigmatic', '熟悉': 'familiar, déjà vu',
            '陌生': 'unfamiliar, otherworldly', '温暖': 'warm, cozy',
            '孤独': 'solitary, lonely', '宿命': 'destined, fateful'
        };

        Object.keys(atmosphericKeywords).forEach(keyword => {
            if (description.includes(keyword)) {
                elements.atmospheric.push(atmosphericKeywords[keyword]);
            }
        });

        // 提取情绪元素
        const emotionalKeywords = {
            '害怕': 'slight apprehension', '恐惧': 'fear',
            '安心': 'sense of peace', '平静': 'calm, serene',
            '兴奋': 'excitement, wonder', '感动': 'deeply moved',
            '怀念': 'nostalgic longing', '向往': 'yearning, longing'
        };

        Object.keys(emotionalKeywords).forEach(keyword => {
            if (description.includes(keyword)) {
                elements.emotional.push(emotionalKeywords[keyword]);
            }
        });

        // 判断时间
        if (description.includes('早') || description.includes('晨') || description.includes('日出')) {
            elements.timeOfDay = 'early morning, sunrise, golden hour';
        } else if (description.includes('晚') || description.includes('夜') || description.includes('月亮')) {
            elements.timeOfDay = 'evening, twilight, or night scene';
        } else if (description.includes('黄昏') || description.includes('夕阳')) {
            elements.timeOfDay = 'sunset, golden hour, warm light';
        } else {
            elements.timeOfDay = 'soft morning light, misty atmosphere';
        }

        // 判断天气
        if (description.includes('雨') || description.includes('湿')) {
            elements.weather = 'after rain, wet surfaces, puddles reflecting';
        } else if (description.includes('雾') || description.includes('云')) {
            elements.weather = 'misty, foggy, ethereal atmosphere';
        } else if (description.includes('雪')) {
            elements.weather = 'snowy, winter scene';
        } else {
            elements.weather = 'clear sky, soft light';
        }

        return elements;
    }

    /**
     * 生成中文版视觉 Prompt
     */
    generateChinesePrompt(description, elements) {
        let prompt = `一幅电影级的梦境场景：`;
        
        if (elements.visual.length > 0) {
            prompt += elements.visual.join('、') + '，';
        }
        
        if (elements.weather) {
            prompt += elements.weather + '，';
        }
        
        if (elements.timeOfDay) {
            prompt += elements.timeOfDay + '，';
        }
        
        if (elements.atmospheric.length > 0) {
            prompt += elements.atmospheric.join('、') + '，';
        }
        
        prompt += `柔和的光线，细腻的色调，仿佛记忆与现实交织，充满宿命感和治愈感。`;
        prompt += `超高清画质，电影级构图，氛围感极强。`;

        return prompt;
    }

    /**
     * 生成英文版视觉 Prompt
     */
    generateEnglishPrompt(description, elements) {
        let prompt = `Cinematic dreamy scene: `;
        
        if (elements.visual.length > 0) {
            prompt += elements.visual.join(', ') + ', ';
        }
        
        if (elements.weather) {
            prompt += elements.weather + ', ';
        }
        
        if (elements.timeOfDay) {
            prompt += elements.timeOfDay + ', ';
        }
        
        if (elements.atmospheric.length > 0) {
            prompt += elements.atmospheric.join(', ') + ', ';
        }
        
        prompt += `soft diffused lighting, delicate color grading, where memory and reality intertwine, fateful and healing atmosphere. `;
        prompt += `Ultra HD, cinematic composition, strong atmospheric feeling, photorealistic, 8K resolution.`;

        return prompt;
    }

    /**
     * 生成 HTML 预览页面
     */
    generateHTMLPreview(description, cnPrompt, enPrompt, elements) {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>梦境视觉 Prompt</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        h1 {
            text-align: center;
            color: #764ba2;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .dream-desc {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            border-left: 5px solid #f5576c;
        }
        .dream-desc h3 { color: #f5576c; margin-bottom: 10px; }
        .prompt-box {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            position: relative;
        }
        .prompt-box h3 {
            color: #667eea;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .prompt-text {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            font-size: 1.05em;
            line-height: 1.8;
            color: #333;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .prompt-text:hover {
            border-color: #667eea;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }
        .copy-btn {
            position: absolute;
            top: 25px;
            right: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }
        .copy-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .elements-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .element-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        .element-card h4 {
            color: #764ba2;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .element-card p {
            color: #666;
            font-size: 0.95em;
        }
        .tip {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        .tip h4 { color: #667eea; margin-bottom: 10px; }
        .tip ul { margin-left: 20px; color: #555; }
        .tip li { margin: 8px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 梦境视觉 Prompt</h1>
        
        <div class="dream-desc">
            <h3>你的梦境</h3>
            <p>${description}</p>
        </div>

        <div class="elements-grid">
            <div class="element-card">
                <h4>👁️ 视觉元素</h4>
                <p>${elements.visual.join(', ') || '无'}</p>
            </div>
            <div class="element-card">
                <h4>👂 听觉元素</h4>
                <p>${elements.auditory.join(', ') || '无'}</p>
            </div>
            <div class="element-card">
                <h4>🌫️ 氛围</h4>
                <p>${elements.atmospheric.join(', ') || '无'}</p>
            </div>
            <div class="element-card">
                <h4>💭 情绪</h4>
                <p>${elements.emotional.join(', ') || '无'}</p>
            </div>
        </div>

        <div class="prompt-box">
            <h3>🇨🇳 中文版 Prompt</h3>
            <button class="copy-btn" onclick="copyText('cn-prompt')">📋 复制</button>
            <div class="prompt-text" id="cn-prompt">${cnPrompt}</div>
        </div>

        <div class="prompt-box">
            <h3>🇬🇧 英文版 Prompt</h3>
            <button class="copy-btn" onclick="copyText('en-prompt')">📋 Copy</button>
            <div class="prompt-text" id="en-prompt">${enPrompt}</div>
        </div>

        <div class="tip">
            <h4>💡 使用提示</h4>
            <ul>
                <li>将 Prompt 复制到 AI 图像生成工具（如 Midjourney、DALL-E、Stable Diffusion）</li>
                <li>英文版通常生成效果更好</li>
                <li>可在 Prompt 末尾添加 <code>--v 5 --ar 16:9</code>（Midjourney 参数）</li>
                <li>生成的图片可用于 HTML 报告的梦境展示</li>
            </ul>
        </div>
    </div>

    <script>
        function copyText(id) {
            const text = document.getElementById(id).innerText;
            navigator.clipboard.writeText(text).then(() => {
                alert('已复制到剪贴板！');
            });
        }
    </script>
</body>
</html>`;
    }

    /**
     * 主函数：生成完整的视觉 Prompt 包
     */
    generate(description, outputPath = './dream-visual-prompt.html') {
        console.log('🌙 正在分析梦境描述...\n');
        
        const elements = this.analyzeDream(description);
        const cnPrompt = this.generateChinesePrompt(description, elements);
        const enPrompt = this.generateEnglishPrompt(description, elements);
        
        console.log('✨ 梦境元素提取完成：');
        console.log(`  - 视觉: ${elements.visual.join(', ') || '无'}`);
        console.log(`  - 听觉: ${elements.auditory.join(', ') || '无'}`);
        console.log(`  - 氛围: ${elements.atmospheric.join(', ') || '无'}`);
        console.log(`  - 情绪: ${elements.emotional.join(', ') || '无'}`);
        console.log(`  - 时间: ${elements.timeOfDay}`);
        console.log(`  - 天气: ${elements.weather}\n`);
        
        console.log('🎨 生成视觉 Prompt...\n');
        console.log('中文版:');
        console.log(cnPrompt + '\n');
        console.log('英文版:');
        console.log(enPrompt + '\n');
        
        const html = this.generateHTMLPreview(description, cnPrompt, enPrompt, elements);
        fs.writeFileSync(outputPath, html, 'utf-8');
        
        console.log(`✅ HTML 预览已保存到: ${outputPath}`);
        console.log('💡 在浏览器中打开查看并复制 Prompt\n');
        
        return { cnPrompt, enPrompt, elements, outputPath };
    }
}

// CLI 使用方式
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('🌙 梦境视觉 Prompt 生成器');
        console.log('\n使用方法:');
        console.log('  node generate-dream-prompt.js "你的梦境描述"');
        console.log('\n示例:');
        console.log('  node generate-dream-prompt.js "我梦到一个被雾笼罩的古镇，石板路是湿的，河边有红灯笼"\n');
        process.exit(0);
    }
    
    const description = args.join(' ');
    const generator = new DreamVisualPromptGenerator();
    generator.generate(description);
}

module.exports = DreamVisualPromptGenerator;
