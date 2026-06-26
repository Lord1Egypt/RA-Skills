const fs = require('fs');
const path = require('path');

/**
 * Build a VChart pie chart spec showing intent distribution.
 * Title changed to "Activity Breakdown" for non-developer readability.
 */
function buildIntentPieChart(intents) {
    if (!intents) return null;

    const values = [
        { type: 'Innovate', value: intents.innovate || 0 },
        { type: 'Repair', value: intents.repair || 0 },
        { type: 'Optimize', value: intents.optimize || 0 }
    ].filter(v => v.value > 0);

    if (values.length === 0) return null;
    if (values.length === 1) return null;

    return {
        type: 'pie',
        data: [{ id: 'intents', values }],
        valueField: 'value',
        categoryField: 'type',
        color: ['#007AFF', '#FF9500', '#34C759'],
        outerRadius: 0.75,
        innerRadius: 0.45,
        label: {
            visible: true,
            position: 'outside',
            style: { fontSize: 12 }
        },
        legends: { visible: true, orient: 'right' },
        title: { text: 'Activity Breakdown', visible: true }
    };
}

function formatUptime(seconds) {
    const s = typeof seconds === 'number' ? seconds : parseInt(seconds, 10);
    if (!Number.isFinite(s) || s < 0) return String(seconds);
    if (s < 60) return s + 's';
    if (s < 3600) return Math.floor(s / 60) + 'm';
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

function healthLabel(rate) {
    const r = parseFloat(rate);
    if (r >= 80) return { text: 'Healthy', color: 'green' };
    if (r >= 50) return { text: 'Degraded', color: 'orange' };
    return { text: 'Unhealthy', color: 'red' };
}

function headerColorFromRate(rate, loopStatus) {
    if (loopStatus && (loopStatus.includes('STOPPED') || loopStatus.includes('OFF'))) return 'grey';
    const r = parseFloat(rate);
    if (r < 50) return 'red';
    if (r < 80) return 'orange';
    return 'green';
}

/**
 * Compute trend direction by comparing two windows of recent events.
 * @param {Array} recent - array of { status } objects, newest first
 * @returns {{ direction: 'up'|'down'|'stable', recentWin: number, recentLoss: number }}
 */
function computeTrend(recent) {
    if (!recent || recent.length < 2) return { direction: 'stable', recentWin: 0, recentLoss: 0 };

    const half = Math.ceil(recent.length / 2);
    const newer = recent.slice(0, half);
    const older = recent.slice(half);

    const newerRate = newer.filter(e => e.status === 'success').length / newer.length;
    const olderRate = older.length > 0
        ? older.filter(e => e.status === 'success').length / older.length
        : newerRate;

    const recentWin = newer.filter(e => e.status === 'success').length + older.filter(e => e.status === 'success').length;
    const recentLoss = recent.length - recentWin;

    let direction = 'stable';
    if (newerRate - olderRate > 0.05) direction = 'up';
    else if (olderRate - newerRate > 0.05) direction = 'down';

    return { direction, recentWin, recentLoss };
}

function generateDashboardCard(stats, systemInfo, cycleInfo) {
    const { total, successRate, intents, recent } = stats;
    const { uptime, load, loopStatus } = systemInfo;
    const { id, duration } = cycleInfo;

    const alerts = [];
    if (systemInfo.errorAlert) alerts.push(systemInfo.errorAlert);
    if (systemInfo.healthAlert) alerts.push(systemInfo.healthAlert);

    const headerColor = alerts.length > 0
        ? 'red'
        : headerColorFromRate(successRate, loopStatus);

    const health = healthLabel(successRate);
    const uptimeStr = formatUptime(uptime);
    const trend = computeTrend(recent);

    const elements = [];

    if (alerts.length > 0) {
        elements.push({ tag: 'markdown', content: alerts.join('\n\n'), element_id: 'el_alerts' });
        elements.push({ tag: 'hr' });
    }

    elements.push({
        tag: 'column_set',
        flex_mode: 'none',
        background_style: 'default',
        columns: [
            {
                tag: 'column', width: 'weighted', weight: 1, vertical_align: 'center',
                elements: [{
                    tag: 'markdown', text_align: 'center',
                    content: `<font color='${parseFloat(successRate) >= 80 ? 'green' : parseFloat(successRate) >= 50 ? 'orange' : 'red'}'>${successRate}%</font>\nSuccess Rate`
                }]
            },
            {
                tag: 'column', width: 'weighted', weight: 1, vertical_align: 'center',
                elements: [{
                    tag: 'markdown', text_align: 'center',
                    content: `<font color='blue'>${total}</font>\nTotal Cycles`
                }]
            },
            {
                tag: 'column', width: 'weighted', weight: 1, vertical_align: 'center',
                elements: [{
                    tag: 'markdown', text_align: 'center',
                    content: `<font color='blue'>${uptimeStr}</font>\nUptime`
                }]
            }
        ]
    });

    elements.push({ tag: 'hr' });

    const trendArrow = trend.direction === 'up' ? '/\\' : trend.direction === 'down' ? '\\/' : '--';
    const trendWord = trend.direction === 'up' ? 'improving' : trend.direction === 'down' ? 'declining' : 'stable';
    const recentCount = recent ? recent.length : 0;
    elements.push({
        tag: 'markdown',
        content: `Recent ${recentCount} Cycles:  **${trend.recentWin} succeeded**, ${trend.recentLoss} failed\nTrend: ${trendArrow} ${trendWord}`,
        element_id: 'el_trend'
    });

    const pieChart = buildIntentPieChart(intents);
    if (pieChart) {
        elements.push({ tag: 'hr' });
        elements.push({
            tag: 'chart',
            aspect_ratio: '16:9',
            color_theme: 'brand',
            chart_spec: pieChart,
            preview: true,
            element_id: 'el_dash_pie'
        });
    }

    elements.push({
        tag: 'markdown',
        content: `<font color='grey'>Up: ${uptimeStr} | Load: ${load} | #${id} (${duration})</font>`
    });

    if (loopStatus && (loopStatus.includes('STOPPED') || loopStatus.includes('OFF'))) {
        elements.push({
            tag: 'markdown',
            content: `<font color='red'>Evolver loop is stopped. Run "lifecycle.js start" to resume.</font>`
        });
    }

    const headerTags = [
        { text: health.text, color: health.color }
    ];

    return {
        header: {
            template: headerColor,
            title: { tag: 'plain_text', content: 'Evolver Dashboard' },
            text_tag_list: headerTags.map((t, i) => ({
                tag: 'text_tag',
                text: { tag: 'plain_text', content: t.text },
                color: t.color,
                element_id: `el_dtag_${i}`
            }))
        },
        elements
    };
}

module.exports = { generateDashboardCard, buildIntentPieChart, computeTrend, formatUptime };
