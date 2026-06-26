const { fetchWithAuth } = require('../feishu-common/index.js');

var SECRET_PATTERNS = [
    /sk-ant-api03-[a-zA-Z0-9\-_]{20,}/,
    /ghp_[a-zA-Z0-9]{10,}/,
    /xox[baprs]-[a-zA-Z0-9]{10,}/,
    /-----BEGIN [A-Z]+ PRIVATE KEY-----/
];

function scanForSecrets(content) {
    if (!content) return;
    for (var i = 0; i < SECRET_PATTERNS.length; i++) {
        if (SECRET_PATTERNS[i].test(content)) {
            throw new Error('Aborted send to prevent secret leakage.');
        }
    }
}

/**
 * Parse structured status text into key-value pairs.
 * Handles both Chinese and English formats from withOutcomeLine + buildFallbackStatus.
 */
function parseStatusText(text) {
    if (!text) return {};

    const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
    const result = {};

    const fullText = lines.join(' ');

    const zhGoal = fullText.match(/目标[：:]\s*(.+?)(?=[。，]?\s*(?:触发信号|使用基因|影响范围|提交|无可提交|$))/);
    const enGoal = fullText.match(/Goal[：:]\s*(.+?)(?=[.]?\s*(?:Signals|Gene|Blast radius|Committed|No committable|$))/);
    if (zhGoal) { result.goal = zhGoal[1].replace(/[。]$/, '').trim(); result.goalLabel = '目标'; }
    else if (enGoal) { result.goal = enGoal[1].replace(/[.]$/, '').trim(); result.goalLabel = 'Goal'; }

    const zhSig = fullText.match(/触发信号[：:]\s*(.+?)(?=[。]?\s*(?:使用基因|影响范围|提交|无可提交|$))/);
    const enSig = fullText.match(/Signals[：:]\s*(.+?)(?=[.]?\s*(?:Gene|Blast radius|Committed|No committable|$))/);
    if (zhSig) { result.signals = zhSig[1].replace(/[。]$/, '').trim(); result.signalsLabel = '信号'; }
    else if (enSig) { result.signals = enSig[1].replace(/[.]$/, '').trim(); result.signalsLabel = 'Signals'; }

    const zhGene = fullText.match(/使用基因[：:]\s*(.+?)(?=[。]?\s*(?:影响范围|提交|无可提交|$))/);
    const enGene = fullText.match(/Gene[：:]\s*(.+?)(?=[.]?\s*(?:Blast radius|Committed|No committable|$))/);
    if (zhGene) { result.gene = zhGene[1].replace(/[。]$/, '').trim(); result.geneLabel = '基因'; }
    else if (enGene) { result.gene = enGene[1].replace(/[.]$/, '').trim(); result.geneLabel = 'Gene'; }

    const zhBlast = fullText.match(/影响范围[：:]\s*(.+?)(?=[。]?\s*(?:提交|无可提交|$))/);
    const enBlast = fullText.match(/Blast radius[：:]\s*(.+?)(?=[.]?\s*(?:Committed|No committable|$))/);
    if (zhBlast) { result.blast = zhBlast[1].replace(/[。]$/, '').trim(); result.blastLabel = '影响'; }
    else if (enBlast) { result.blast = enBlast[1].replace(/[.]$/, '').trim(); result.blastLabel = 'Blast'; }

    const zhGit = fullText.match(/提交[：:]\s*(.+?)$/);
    const enGit = fullText.match(/Committed\s+(.+?)$/);
    const noGit = fullText.match(/无可提交代码变更|No committable code diff/);
    if (zhGit) { result.git = zhGit[1].replace(/[。]$/, '').trim(); result.gitLabel = 'Git'; }
    else if (enGit) { result.git = enGit[1].replace(/[.]$/, '').trim(); result.gitLabel = 'Git'; }
    else if (noGit) { result.git = noGit[0]; result.gitLabel = 'Git'; }

    return result;
}

function resolveTarget(raw) {
    let target = raw;
    if (!target && process.env.OPENCLAW_MASTER_ID) {
        target = process.env.OPENCLAW_MASTER_ID;
    }
    if (!target) {
        throw new Error("Target ID is required (and OPENCLAW_MASTER_ID env var is not set)");
    }
    return target;
}

function resolveReceiveIdType(target) {
    if (target.startsWith('oc_')) return 'chat_id';
    if (target.startsWith('ou_')) return 'open_id';
    if (target.includes('@')) return 'email';
    return 'open_id';
}

async function postCard(target, cardJson) {
    const receiveIdType = resolveReceiveIdType(target);
    const payload = {
        receive_id: target,
        msg_type: 'interactive',
        content: JSON.stringify(cardJson)
    };

    const res = await fetchWithAuth(
        'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=' + receiveIdType,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }
    );

    const data = await res.json();
    if (data.code !== 0) {
        throw new Error('Feishu API Error: ' + data.msg);
    }
    return data;
}

// v1 card (legacy, kept for backward compat)
async function sendCard({ target: rawTarget, title, text, color, note, cardData }) {
    const target = resolveTarget(rawTarget);

    var processedText = (text || '').replace(/\\n/g, '\n');
    scanForSecrets(processedText);

    var elements = [];

    if (processedText) {
        elements.push({ tag: 'markdown', content: processedText });
    }

    if (note) {
        elements.push({
            tag: 'markdown',
            content: `<font color='grey'>${String(note)}</font>`
        });
    }

    var card = {
        config: { wide_screen_mode: true },
        elements: elements
    };

    if (title) {
        card.header = {
            title: { tag: 'plain_text', content: title },
            template: color || 'blue'
        };
    } else if (cardData && cardData.header) {
        card.header = cardData.header;
    }

    if (cardData && cardData.elements) {
        card.elements = cardData.elements;
    }

    return postCard(target, card);
}

/**
 * Send a v2 structured card for a single evolution cycle report.
 *
 * Layout:
 *   Goal (prominent)
 *   3 columns: Duration | Files Changed | Lines Added
 *   [red error block -- only if failed]
 *   grey footnote: Gene + Signals
 *   grey footer: uptime / load
 *
 * @param {Object} opts
 * @param {string} opts.target - receive_id
 * @param {string} opts.title - card header title (e.g. "Evolution #1234")
 * @param {string} opts.color - header template color
 * @param {Array}  [opts.tags] - header text_tag_list [{text, color}]
 * @param {Object} [opts.summary] - { success, duration, filesChanged, linesAdded, errors, errorCount }
 * @param {string} [opts.status] - raw evolution status text (parsed for goal/gene/signals)
 * @param {string} [opts.footer] - minimal footer text
 */
async function sendStructuredCard(opts) {
    const { title, color, tags, summary, status, footer } = opts;
    const target = resolveTarget(opts.target);

    scanForSecrets(status || '');

    const elements = [];

    let parsed = {};
    if (status) {
        parsed = parseStatusText(status);
    }

    if (parsed.goal) {
        elements.push({
            tag: 'markdown',
            content: `**${parsed.goalLabel || 'Goal'}**: ${parsed.goal}`,
            element_id: 'el_goal'
        });
    } else if (status) {
        const cleanedStatus = status.replace(/^(结果|Result)[:：]\s*(成功|失败|SUCCESS|FAILED)\s*\n?/i, '').trim();
        if (cleanedStatus) {
            elements.push({ tag: 'markdown', content: cleanedStatus, element_id: 'el_status' });
        }
    }

    if (summary) {
        const dur = summary.duration || '?';
        const files = summary.filesChanged != null ? summary.filesChanged : (parsed.blast ? parsed.blast.replace(/[^\d]/g, '') || '0' : '0');
        const lines = summary.linesAdded != null ? summary.linesAdded : '0';

        elements.push({ tag: 'hr' });
        elements.push({
            tag: 'column_set',
            flex_mode: 'none',
            background_style: 'default',
            columns: [
                {
                    tag: 'column', width: 'weighted', weight: 1, vertical_align: 'center',
                    elements: [{
                        tag: 'markdown', text_align: 'center',
                        content: `<font color='blue'>${dur}s</font>\nDuration`
                    }]
                },
                {
                    tag: 'column', width: 'weighted', weight: 1, vertical_align: 'center',
                    elements: [{
                        tag: 'markdown', text_align: 'center',
                        content: `<font color='blue'>${files}</font>\nChanged`
                    }]
                },
                {
                    tag: 'column', width: 'weighted', weight: 1, vertical_align: 'center',
                    elements: [{
                        tag: 'markdown', text_align: 'center',
                        content: `<font color='blue'>+${lines}</font>\nLines`
                    }]
                }
            ]
        });
    }

    if (summary && !summary.success && summary.errors && summary.errors.length > 0) {
        elements.push({
            tag: 'markdown',
            content: `<font color='red'>Error: ${summary.errors[0]}</font>`,
            element_id: 'el_error'
        });
    }

    const footnoteParts = [];
    if (parsed.gene) footnoteParts.push(`Gene: ${parsed.gene}`);
    if (parsed.signals) footnoteParts.push(`Signals: ${parsed.signals}`);
    if (footnoteParts.length > 0) {
        elements.push({
            tag: 'markdown',
            content: `<font color='grey'>${footnoteParts.join(' | ')}</font>`,
            element_id: 'el_footnote'
        });
    }

    if (footer) {
        elements.push({
            tag: 'markdown',
            content: `<font color='grey'>${footer}</font>`
        });
    }

    const header = {
        title: { tag: 'plain_text', content: title || 'Evolution Report' },
        template: color || 'blue'
    };

    if (tags && tags.length > 0) {
        header.text_tag_list = tags.slice(0, 3).map((t, i) => ({
            tag: 'text_tag',
            text: { tag: 'plain_text', content: t.text },
            color: t.color || 'neutral',
            element_id: `el_tag_${i}`
        }));
    }

    const card = {
        schema: '2.0',
        config: {
            update_multi: true,
            width_mode: 'default'
        },
        header,
        body: { elements }
    };

    return postCard(target, card);
}

module.exports = { sendCard, sendStructuredCard, postCard, parseStatusText };
