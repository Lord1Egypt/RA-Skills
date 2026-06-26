// AI Fact Checker - Main verification logic
// Usage: node fact-check.js "text to verify"

const { execSync } = require('child_process');

function extractFactualStatements(text) {
    // Split into sentences
    const sentences = text.split(/(?<=[。.!？!?；;])\s+/g);
    
    // Factual statements: contain verifiable information
    // - Has numbers, dates, specific names, claims that can be checked
    // - Excludes opinions, questions, subjective statements
    const factualPattern = /(\d+|年|月|日|发布于|created by|作者|价格|下载量|星标|地址|网址|http|www|是|位于|成立于|总部在|公司|官方网站)/i;
    const opinionPattern = /(我认为|我觉得|可能|也许|应该|建议|最好|很棒|很糟糕|好看|难用)/i;
    
    return sentences.filter(s => {
        s = s.trim();
        // Must be long enough to contain a fact
        if (s.length < 8) return false;
        // Must have factual keywords
        if (!factualPattern.test(s)) return false;
        // Skip if it's mostly opinion
        if (opinionPattern.test(s) && !factualPattern.test(s)) return false;
        return true;
    });
}

function searchAndVerify(statement) {
    // Use OpenClaw's web_search tool via CLI
    try {
        const cmd = `openclaw tool web_search --query "${statement.replace(/"/g, '\\"')}" --count 5`;
        const result = execSync(cmd, { encoding: 'utf8', maxBuffer: 1024 * 1024 });
        return JSON.parse(result);
    } catch (e) {
        console.error('Search failed:', e.message);
        return null;
    }
}

function calculateConfidence(statement, searchResults) {
    if (!searchResults || searchResults.length === 0) {
        return { score: 30, verdict: '⚠️ 存疑', reason: '未找到相关验证信息' };
    }
    
    let matches = 0;
    const keywords = statement.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    
    for (const result of searchResults) {
        const content = `${result.title} ${result.snippet}`.toLowerCase();
        const matchedKeywords = keywords.filter(k => content.includes(k));
        const matchRate = matchedKeywords.length / keywords.length;
        
        if (matchRate > 0.7) matches += 2;
        else if (matchRate > 0.4) matches += 1;
    }
    
    const score = Math.round((matches / (searchResults.length * 2)) * 100);
    
    let verdict, reason;
    if (score >= 90) {
        verdict = '✅ 可信';
        reason = '多个搜索结果验证一致';
    } else if (score >= 60) {
        verdict = '⚠️ 部分可信';
        reason = '部分信息得到验证';
    } else if (score >= 30) {
        verdict = '⚠️ 存疑';
        reason = '信息不完整或找不到充分验证';
    } else {
        verdict = '❌ 错误';
        reason = '信息与搜索结果矛盾';
    }
    
    return { score, verdict, reason };
}

function generateReport(originalText, results) {
    let report = `# 🧐 AI 事实核查报告\n\n`;
    report += `**原始文本:**\n${originalText}\n\n`;
    report += `---\n\n`;
    
    results.forEach((result, index) => {
        report += `## ${index + 1}. 核查: "${result.statement}"\n\n`;
        report += `- **评分:** ${result.verification.score}/100\n`;
        report += `- **结论:** ${result.verification.verdict}\n`;
        report += `- **原因:** ${result.verification.reason}\n\n`;
        
        if (result.searchResults && result.searchResults.length > 0) {
            report += `**参考来源:**\n`;
            result.searchResults.slice(0, 3).forEach((r, i) => {
                report += `${i + 1}. [${r.title}](${r.url})\n`;
            });
            report += '\n';
        }
    });
    
    // Overall summary
    const avgScore = results.reduce((sum, r) => sum + r.verification.score, 0) / results.length;
    let overall;
    if (avgScore >= 90) overall = '✅ 整体可信';
    else if (avgScore >= 60) overall = '⚠️ 大部分可信，部分需要注意';
    else if (avgScore >= 30) overall = '⚠️ 整体存疑，建议核实';
    else overall = '❌ 整体不可信，存在大量错误';
    
    report += `---\n`;
    report += `**整体评分:** ${Math.round(avgScore)}/100 - ${overall}\n`;
    
    return report;
}

// Main entry point
if (require.main === module) {
    const text = process.argv[2];
    if (!text) {
        console.error('Usage: node fact-check.js "text to verify"');
        process.exit(1);
    }
    
    const statements = extractFactualStatements(text);
    console.log(`Extracted ${statements.length} factual statements`);
    
    const results = statements.map(statement => {
        console.log(`Verifying: ${statement}`);
        const searchResults = searchAndVerify(statement);
        const verification = calculateConfidence(statement, searchResults);
        return { statement, searchResults, verification };
    });
    
    const report = generateReport(text, results);
    console.log(report);
}

module.exports = {
    extractFactualStatements,
    searchAndVerify,
    calculateConfidence,
    generateReport
};
