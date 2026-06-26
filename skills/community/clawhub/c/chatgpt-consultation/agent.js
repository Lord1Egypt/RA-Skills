#!/usr/bin/env node

// ChatGPT 咨询 Agent
const { execSync } = require('child_process');
const config = require('../config/auto_gpt_config.json');

class ChatGPTConsultAgent {
    
    constructor() {
        this.browserStarted = false;
    }
    
    // 分析是否需要咨询 ChatGPT
    shouldConsultGPT(message) {
        const lowerMessage = message.toLowerCase();
        
        // 用户明确要求
        const explicitTriggers = [
            '咨询chatgpt', '问问chatgpt', '问chatgpt',
            'chatgpt怎么说', '让chatgpt', '用chatgpt',
            '@browser', '使用浏览器'
        ];
        
        if (explicitTriggers.some(trigger => lowerMessage.includes(trigger))) {
            return { shouldConsult: true, reason: '用户明确要求' };
        }
        
        // 问题类型匹配
        const problemPatterns = [
            // 技术问题
            /如何配置|怎么设置|如何安装|怎么部署/,
            /连接失败|错误代码|报错|无法运行/,
            // 专业知识  
            /最新研究|新技术|发展现状|趋势/,
            // 创意建议
            /有什么建议|推荐什么|如何设计|创意/,
            // 复杂问题
            /详细步骤|具体方案|完整流程/
        ];
        
        if (problemPatterns.some(pattern => pattern.test(lowerMessage))) {
            return { shouldConsult: true, reason: '复杂技术问题' };
        }
        
        return { shouldConsult: false, reason: '不需要咨询' };
    }
    
    // 获取问题分类
    getQuestionCategory(question) {
        const lowerQuestion = question.toLowerCase();
        
        if (lowerQuestion.includes('配置') || lowerQuestion.includes('设置') || 
            lowerQuestion.includes('安装') || lowerQuestion.includes('部署')) {
            return 'technical';
        }
        
        if (lowerQuestion.includes('代码') || lowerQuestion.includes('编程') ||
            lowerQuestion.includes('开发') || lowerQuestion.includes('程序')) {
            return 'code';
        }
        
        if (lowerQuestion.includes('研究') || lowerQuestion.includes('技术') ||
            lowerQuestion.includes('最新') || lowerQuestion.includes('趋势')) {
            return 'knowledge';
        }
        
        if (lowerQuestion.includes('创意') || lowerQuestion.includes('设计') ||
            lowerQuestion.includes('建议') || lowerQuestion.includes('推荐')) {
            return 'creative';
        }
        
        return 'general';
    }
    
    // 咨询 ChatGPT
    async consultChatGPT(question, category = 'general') {
        try {
            // 启动浏览器
            if (!this.browserStarted) {
                execSync('openclaw browser start', { stdio: 'inherit' });
                this.browserStarted = true;
            }
            
            // 准备提示词
            const prompt = this.formatPrompt(question, category);
            
            // 执行咨询
            const result = execSync(
                `node scripts/auto_chatgpt.js "${prompt}"`, 
                { encoding: 'utf8', timeout: 30000 }
            );
            
            return {
                success: true,
                answer: result.trim(),
                question: question
            };
            
        } catch (error) {
            return {
                success: false,
                error: error.message,
                question: question,
                answer: '咨询 ChatGPT 时出错，请稍后重试或手动访问 ChatGPT'
            };
        }
    }
    
    // 格式化提示词
    formatPrompt(question, category) {
        const categoryPrompts = {
            technical: `请以专业技术人员的身份，详细解答以下技术配置问题：${question}`,
            code: `请以资深开发者的身份，提供完整的代码解决方案：${question}`,
            knowledge: `请提供最新、最专业的专业知识解答：${question}`,
            creative: `请提供创意性和实用性的建议：${question}`,
            general: `请专业、详细地解答以下问题：${question}`
        };
        
        return categoryPrompts[category] || categoryPrompts.general;
    }
    
    // 生成用户通知
    getConsultationNotice(question, reason, category) {
        const categoryNames = {
            technical: '技术配置',
            code: '编程开发',
            knowledge: '专业知识', 
            creative: '创意建议',
            general: '专业问题'
        };
        
        const notices = [
            `这个问题涉及${categoryNames[category]}，让我为您咨询ChatGPT获取详细指导。`,
            `${categoryNames[category]}方面的问题，让我请教ChatGPT为您提供专业解答。`,
            `为了给您更准确的回答，让我咨询ChatGPT获取${categoryNames[category]}的专业意见。`
        ];
        
        return notices[Math.floor(Math.random() * notices.length)];
    }
}

// 主函数
async function main() {
    const agent = new ChatGPTConsultAgent();
    
    const question = process.argv.slice(2).join(' ');
    if (!question) {
        console.log('使用方法: node agent.js "您的问题"');
        return;
    }
    
    // 分析是否需要咨询
    const analysis = agent.shouldConsultGPT(question);
    if (!analysis.shouldConsult) {
        console.log('❌ 不需要咨询 ChatGPT:', analysis.reason);
        return;
    }
    
    // 获取分类并咨询
    const category = agent.getQuestionCategory(question);
    const notice = agent.getConsultationNotice(question, analysis.reason, category);
    
    console.log(notice);
    
    const result = await agent.consultChatGPT(question, category);
    
    if (result.success) {
        console.log('\n✅ ChatGPT 专业回复:');
        console.log('---');
        console.log(result.answer);
        console.log('---');
    } else {
        console.log('❌ 咨询失败:', result.error);
    }
}

// 执行
if (require.main === module) {
    main().catch(console.error);
}

module.exports = ChatGPTConsultAgent;