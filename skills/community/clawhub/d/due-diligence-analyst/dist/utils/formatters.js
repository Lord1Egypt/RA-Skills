/**
 * 格式化工具函数
 */
/**
 * 格式化日期
 */
export function formatDate(date) {
    const d = typeof date === 'string' ? new Date(date) : date;
    return d.toISOString().split('T')[0];
}
/**
 * 格式化货币
 */
export function formatCurrency(amount, currency = 'CNY') {
    const symbols = {
        CNY: '¥',
        USD: '$',
        EUR: '€',
    };
    const symbol = symbols[currency] || currency;
    if (amount >= 100000000) {
        return `${symbol}${(amount / 100000000).toFixed(2)}亿`;
    }
    else if (amount >= 10000) {
        return `${symbol}${(amount / 10000).toFixed(2)}万`;
    }
    else {
        return `${symbol}${amount.toLocaleString()}`;
    }
}
/**
 * 格式化百分比
 */
export function formatPercentage(value, decimals = 2) {
    return `${(value * 100).toFixed(decimals)}%`;
}
/**
 * 生成唯一 ID
 */
export function generateId(prefix = 'dd') {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substring(2, 9);
    return `${prefix}-${timestamp}-${random}`;
}
/**
 * 格式化风险等级
 */
export function formatRiskLevel(level) {
    const icons = {
        low: '🟢',
        medium: '🟡',
        high: '🟠',
        critical: '🔴',
    };
    const labels = {
        low: '低',
        medium: '中',
        high: '高',
        critical: '严重',
    };
    return `${icons[level]} ${labels[level]}`;
}
/**
 * 格式化评级
 */
export function formatRating(rating) {
    const descriptions = {
        A: '优秀 - 强烈推荐',
        B: '良好 - 推荐',
        C: '一般 - 需谨慎',
        D: '较差 - 不推荐',
        F: '不合格 - 建议pass',
    };
    return `${rating} (${descriptions[rating]})`;
}
/**
 * 截断文本
 */
export function truncate(text, maxLength) {
    if (text.length <= maxLength)
        return text;
    return text.substring(0, maxLength - 3) + '...';
}
/**
 * 格式化列表为 Markdown
 */
export function formatListMarkdown(items, ordered = false) {
    return items.map((item, index) => {
        const prefix = ordered ? `${index + 1}.` : '-';
        return `${prefix} ${item}`;
    }).join('\n');
}
/**
 * 格式化表格为 Markdown
 */
export function formatTableMarkdown(headers, rows) {
    const headerRow = `| ${headers.join(' | ')} |`;
    const separatorRow = `| ${headers.map(() => '---').join(' | ')} |`;
    const dataRows = rows.map(row => `| ${row.join(' | ')} |`).join('\n');
    return [headerRow, separatorRow, dataRows].join('\n');
}
//# sourceMappingURL=formatters.js.map