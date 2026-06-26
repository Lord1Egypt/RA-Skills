#!/usr/bin/env node

/**
 * 寻梦之旅金句生成器
 * 根据主题随机生成治愈/宿命/诗意风格的结尾金句
 */

class QuoteGenerator {
    constructor() {
        this.quotes = {
            '宿命感': [
                '有些地方，我们先在梦里遇见，然后用 Fly.ai 把它寻成真。',
                '梦不是虚幻，而是灵魂提前抵达的真实。',
                '你梦到的地方，一定在世界的某个角落等你。',
                '每一次梦境，都是潜意识在为你指引方向。',
                '梦与现实的重逢，是命中注定的缘分。',
                '那些反复出现的梦，是心灵在呼唤你前往的地方。',
                '梦境是灵魂的地图，Fly.ai 帮你找到宝藏。',
                '你以为是梦，其实是记忆在召唤。',
                '梦里的风景，终会在现实中与你相遇。',
                '有些相遇，注定要先在梦里发生。'
            ],
            '治愈系': [
                '愿你的每个梦，都能找到回家的路。',
                '梦是心灵的旅行，现实是梦的归宿。',
                '把梦变成现实，是对自己最好的治愈。',
                '当你踏上梦中的土地，所有的不安都会消散。',
                '梦境成真，是宇宙给你最温柔的礼物。',
                '让梦指引方向，让心找到归属。',
                '每一次寻梦，都是一次自我疗愈的旅程。',
                '梦里的光，终会照亮现实的路。',
                '当你找到梦中的地方，心就完整了。',
                '梦与现实相遇的那一刻，一切都值得了。'
            ],
            '诗意浪漫': [
                '梦里寻她千百度，蓦然回首，那地在灯火阑珊处。',
                '一梦一世界，一地一人生。',
                '梦是诗的开始，旅行是诗的延续。',
                '把梦写成诗，把旅行过成诗。',
                '梦里的山水，现实的烟火，都是生命最美的风景。',
                '从梦到现实，不过是一场浪漫的奔赴。',
                '梦是远方的呼唤，旅行是温柔的回应。',
                '梦中有山水，现实有知音。',
                '一场梦，一次旅行，一生的记忆。',
                '梦里花落知多少，现实寻梦正当时。'
            ],
            '冒险探索': [
                '跟着梦走，世界就在脚下。',
                '梦是冒险的开始，Fly.ai 是你的指南针。',
                '不要只做梦，要去寻！',
                '每一个梦，都是一张未使用的机票。',
                '梦境是未知的地图，你是勇敢的探险家。',
                '把梦变成行动，把想象变成体验。',
                '梦有多远，你就能走多远。',
                '寻梦，就是一场最美的冒险。',
                '梦里的地方，值得你用脚步去丈量。',
                '从梦想到现实，只差一次出发的勇气。'
            ],
            '哲理深思': [
                '梦是潜意识的语言，旅行是心灵的对话。',
                '我们不是在寻梦，而是在寻找自己。',
                '梦与现实的边界，比你想象的更模糊。',
                '真正的旅行，是从梦境开始的。',
                '梦不是逃避现实，而是为了更好地回到现实。',
                '每一个梦，都是灵魂的一次彩排。',
                '寻梦的本质，是寻找内心的平静。',
                '梦是时间的折叠，旅行是空间的展开。',
                '当你找到梦中的地方，你就找到了自己。',
                '梦与现实，不过是同一枚硬币的两面。'
            ]
        };
    }

    /**
     * 随机获取一个金句
     */
    getRandomQuote(theme = null) {
        if (theme && this.quotes[theme]) {
            const quotes = this.quotes[theme];
            return quotes[Math.floor(Math.random() * quotes.length)];
        }
        
        // 从所有主题中随机
        const allQuotes = Object.values(this.quotes).flat();
        return allQuotes[Math.floor(Math.random() * allQuotes.length)];
    }

    /**
     * 根据梦境描述智能选择主题
     */
    selectThemeByDream(dreamDescription) {
        const dream = dreamDescription.toLowerCase();
        
        // 检测梦境情感倾向
        if (dream.includes('害怕') || dream.includes('恐惧') || dream.includes('焦虑')) {
            return '治愈系';
        }
        
        if (dream.includes('冒险') || dream.includes('探索') || dream.includes('未知')) {
            return '冒险探索';
        }
        
        if (dream.includes('浪漫') || dream.includes('美') || dream.includes('花')) {
            return '诗意浪漫';
        }
        
        if (dream.includes('反复') || dream.includes('熟悉') || dream.includes('宿命')) {
            return '宿命感';
        }
        
        // 默认随机
        const themes = Object.keys(this.quotes);
        return themes[Math.floor(Math.random() * themes.length)];
    }

    /**
     * 生成金句（支持指定主题或智能选择）
     */
    generate(dreamDescription = null, theme = null) {
        if (!theme && dreamDescription) {
            theme = this.selectThemeByDream(dreamDescription);
        }
        
        const quote = this.getRandomQuote(theme);
        const selectedTheme = theme || '随机';
        
        return {
            quote: quote,
            theme: selectedTheme
        };
    }

    /**
     * 批量生成金句（用于预览）
     */
    generateBatch(count = 10, theme = null) {
        const quotes = [];
        for (let i = 0; i < count; i++) {
            quotes.push(this.getRandomQuote(theme));
        }
        return quotes;
    }

    /**
     * 获取所有主题列表
     */
    getThemes() {
        return Object.keys(this.quotes);
    }

    /**
     * 获取指定主题的金句列表
     */
    getQuotesByTheme(theme) {
        return this.quotes[theme] || [];
    }
}

// CLI 使用方式
if (require.main === module) {
    const args = process.argv.slice(2);
    const generator = new QuoteGenerator();

    if (args.length === 0) {
        // 默认随机生成 10 个金句预览
        console.log('🌙 寻梦之旅金句生成器\n');
        console.log('📋 可用主题:');
        generator.getThemes().forEach((theme, index) => {
            console.log(`  ${index + 1}. ${theme} (${generator.getQuotesByTheme(theme).length}句)`);
        });
        console.log('\n🎲 随机金句预览:');
        const batch = generator.generateBatch(10);
        batch.forEach((quote, index) => {
            console.log(`  ${index + 1}. "${quote}"`);
        });
        console.log('\n💡 使用方法:');
        console.log('  node generate-quote.js                    # 随机生成1个金句');
        console.log('  node generate-quote.js --theme 宿命感      # 指定主题');
        console.log('  node generate-quote.js --dream "我反复梦到..." # 智能选择主题');
        console.log('  node generate-quote.js --batch 10          # 批量生成10个\n');
    } else if (args[0] === '--batch' && args[1]) {
        const count = parseInt(args[1]);
        const theme = args[2] ? args[2] : null;
        const batch = generator.generateBatch(count, theme);
        console.log(`🎲 批量生成 ${count} 个金句${theme ? '（主题：' + theme + '）' : ''}:\n`);
        batch.forEach((quote, index) => {
            console.log(`${index + 1}. "${quote}"`);
        });
    } else if (args[0] === '--theme' && args[1]) {
        const theme = args[1];
        const quote = generator.getRandomQuote(theme);
        console.log(`🎯 主题：${theme}`);
        console.log(`💬 金句："${quote}"`);
    } else if (args[0] === '--dream') {
        const dreamIndex = args.indexOf('--dream');
        const dream = args.slice(dreamIndex + 1).join(' ');
        const result = generator.generate(dream);
        console.log(`🌙 梦境描述：${dream}`);
        console.log(`🎯 智能主题：${result.theme}`);
        console.log(`💬 金句："${result.quote}"`);
    } else {
        const result = generator.generate();
        console.log(`💬 "${result.quote}"`);
        console.log(`🎯 主题：${result.theme}`);
    }
}

module.exports = QuoteGenerator;
