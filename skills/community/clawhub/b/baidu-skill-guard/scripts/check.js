/**
 * @file Skill安全检查脚本，提供slug查询、目录查询、批量查询等功能
 */
'use strict';

const https = require('https');
const http = require('http');
const {URL} = require('url');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ============================================================
// Configuration
// ============================================================

/**
 * API基础URL
 *
 * @const
 * @type {string}
 */
const API_BASE_URL = 'https://skill-sec.baidu.com';

/**
 * API路径
 *
 * @const
 * @type {string}
 */
const API_PATH = '/v1/skill/security/results';

/**
 * 请求超时时间（毫秒）
 *
 * @const
 * @type {number}
 */
const REQUEST_TIMEOUT = 10000; // 10s

/**
 * 并发请求限制数
 *
 * @const
 * @type {number}
 */
const CONCURRENT_LIMIT = 5;

/**
 * 渠道标识，由打包脚本注入（如 'openclaw-skill'）；null 表示无渠道（通用包）
 *
 * @const
 * @type {string|null}
 */
const _CHANNEL_ID = 'openclaw-skill';

// ============================================================
// Utilities
// ============================================================

/**
 * 构建HTTP请求选项
 *
 * @param {string} slug skill标识
 * @param {string=} version skill版本号
 * @return {Object} HTTP请求选项对象
 */
function buildRequestOptions(slug, version) {
    const queryParams = {slug};
    if (version) {
        queryParams.version = version;
    }

    const queryString = Object.entries(queryParams)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&');

    const url = new URL(`${API_PATH}?${queryString}`, API_BASE_URL);

    const headers = {'Host': url.host};
    if (_CHANNEL_ID) {
        headers['X-Caller'] = _CHANNEL_ID;
    }

    return {
        protocol: url.protocol,
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: `${url.pathname}?${queryString}`,
        method: 'GET',
        headers
    };
}

/**
 * 安全解析JSON字符串
 *
 * @param {string} text 待解析的JSON文本
 * @return {Object} 解析后的对象
 */
function safeJsonParse(text) {
    try {
        return JSON.parse(text);
    }
    catch (e) {
        throw new Error(`响应解析失败（非JSON格式）: ${text.substring(0, 200)}`);
    }
}

/**
 * 创建批量查询结果对象
 *
 * @param {string} code 结果状态码
 * @param {string} msg 结果消息
 * @param {Object=} overrides 覆盖的属性
 * @return {Object} 查询结果对象
 */
function makeQueryFullResult(code, msg, overrides = {}) {
    return {
        code,
        msg,
        ts: Date.now(),
        total: 0,
        safe_count: 0,
        danger_count: 0,
        caution_count: 0,
        error_count: 0,
        results: [],
        ...overrides
    };
}

// ============================================================
// Report Builder
// ============================================================

/**
 * 数据来源映射表
 *
 * @const
 * @type {Object}
 */
const SOURCE_MAP = {
    openclaw: 'ClawdHub',
    github: 'GitHub',
    appbuilder: '百度AppBuilder'
};

/**
 * 置信度等级与判定结果的映射表
 *
 * @const
 * @type {Object}
 */
const CONFIDENCE_MAP = {
    safe: {
        verdict: '✅ 白名单(可信)',
        final_verdict: '✅ 安全安装',
        suggestion: '已通过安全检查，可安全安装'
    },
    caution: {
        verdict: '⚠️ 灰名单，谨慎安装',
        final_verdict: '⚠️ 谨慎安装(需人工确认)',
        suggestion: '存在潜在风险，建议人工审查后再安装'
    },
    dangerous: {
        verdict: '🚫 黑名单，❌ 不建议安装',
        final_verdict: '❌ 不建议安装(需人工确认)',
        suggestion: '发现严重安全风险，建议人工审查后再安装'
    }
};

/**
 * 未收录时的默认置信度判定
 *
 * @const
 * @type {Object}
 */
const CONFIDENCE_DEFAULT = {
    verdict: '❓ 未收录，不建议安装',
    final_verdict: '❌ 不建议安装(需人工确认)',
    suggestion: '尚未被安全系统收录，建议人工审查后再安装'
};

/**
 * 将毫秒时间戳格式化为可读日期字符串
 *
 * @param {number} ms 毫秒时间戳
 * @return {string} 格式化后的日期字符串
 */
function formatTimestamp(ms) {
    if (!ms) {
        ms = Date.now();
    }
    // Force UTC+8
    const d = new Date(ms + 8 * 60 * 60 * 1000);
    const pad = (n) => String(n).padStart(2, '0');
    return '[UTC+8 ' + d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1)
        + '-' + pad(d.getUTCDate()) + ' ' + pad(d.getUTCHours())
        + ':' + pad(d.getUTCMinutes()) + ':' + pad(d.getUTCSeconds()) + ']';
}

/**
 * 根据置信度和检测结果生成概览文本
 *
 * @param {string} confidence 置信度等级
 * @param {number} findingsCount 发现的问题数量
 * @param {number} virusCount 病毒风险数量
 * @return {?string} 概览文本，safe时返回null
 */
function buildOverview(confidence, findingsCount, virusCount) {
    if (confidence === 'safe') {
        return null;
    }
    let text;
    if (confidence === 'dangerous') {
        text = '🚫 Skill存在安全风险';
        if (findingsCount > 0) {
            text += `，发现${findingsCount}项危险行为`;
        }
        if (virusCount > 0) {
            text += `，发现${virusCount}项病毒风险`;
        }
    }
    else if (confidence === 'caution') {
        text = '⚠️ Skill存在潜在风险';
        if (findingsCount > 0) {
            text += `，发现${findingsCount}项可疑行为`;
        }
    }
    else {
        text = '❓ Skill未收录';
    }
    return text;
}

/**
 * 根据安全检查数据构建报告对象
 *
 * @param {Array} data 安全检查结果数据数组
 * @param {number=} ts API响应外层ts毫秒时间戳
 * @return {?Object} 报告对象，无数据时返回null
 */
function buildReport(data, ts) {
    if (!Array.isArray(data) || data.length === 0) {
        return null;
    }

    const item = data[0];
    const detail = item.detail || {};
    const confidence = (item.bd_confidence || '').toLowerCase();
    const mapped = CONFIDENCE_MAP[confidence] || CONFIDENCE_DEFAULT;

    const github = detail.github || {};
    const vt = detail.virustotal || {};
    const oc = detail.openclaw || {};
    const scanner = detail.skillscanner || {};
    const av = detail.antivirus || {};

    const vtStatus = vt.vt_status || null;
    let vtDescribe = null;
    if (vtStatus && vtStatus !== 'Benign'
        && vtStatus !== 'Pending' && vt.vt_describe) {
        vtDescribe = vt.vt_describe;
    }

    const ocStatus = oc.oc_status || null;
    const ocDescribe = (ocStatus && ocStatus !== 'Benign'
        && oc.oc_describe) ? oc.oc_describe : null;

    const findings = Array.isArray(scanner.findings)
        ? scanner.findings.map(f => ({
            severity: f.severity,
            title: f.title,
            description: f.description
        }))
        : [];

    const findingsCount = scanner.findings_count || findings.length;
    const virusCount = av.virus_count || 0;
    const virusList = (virusCount > 0 && Array.isArray(av.virus_details))
        ? av.virus_details.map(v => ({virus_name: v.virus_name, file: v.file}))
        : [];

    return {
        name: item.slug || null,
        version: item.version || null,
        source: SOURCE_MAP[item.source] || '其他',
        author: github.name || null,
        scanned_at: formatTimestamp(ts),
        bd_confidence: confidence || null,
        verdict: mapped.verdict,
        final_verdict: mapped.final_verdict,
        suggestion: mapped.suggestion,
        bd_describe: item.bd_describe || null,
        overview: buildOverview(confidence, findingsCount, virusCount),
        virustotal: {status: vtStatus, describe: vtDescribe},
        openclaw: {status: ocStatus, describe: ocDescribe},
        findings,
        antivirus: {virus_count: virusCount, virus_list: virusList}
    };
}

// ============================================================
// Report Text Formatter
// ============================================================

/**
 * 将单个Skill的report对象渲染为纯文本报告
 *
 * @param {Object} report buildReport()返回的报告对象
 * @return {string} 格式化后的报告纯文本
 */
function formatSingleReportText(report) {
    const lines = [];
    lines.push('🛡️ Skill安全守卫报告');
    lines.push('═══════════════════════════════════════');
    lines.push('📊 守卫摘要');
    lines.push('评估时间：' + (report.scanned_at || '未知'));
    lines.push('Skill名称：' + (report.name || '未知'));
    lines.push('来    源：' + (report.source || '未知'));
    lines.push('作    者：' + (report.author || '未知'));
    lines.push('版    本：' + (report.version || '未知'));
    lines.push('评估结果：' + (report.verdict || '未知'));

    if (report.overview) {
        lines.push('');
        lines.push('───────────────────────────────────────');
        lines.push('📕 评估结果概述');
        lines.push(report.overview);

        lines.push('');
        lines.push('───────────────────────────────────────');
        lines.push('🗒 安全评估详情');
        lines.push(report.bd_describe || 'N/A');

        lines.push('');
        lines.push('评估过程');

        // VirusTotal
        let vtLine = '- VirusTotal：' + (report.virustotal && report.virustotal.status
            ? report.virustotal.status : 'N/A');
        if (report.virustotal && report.virustotal.describe) {
            vtLine += '，' + report.virustotal.describe;
        }
        lines.push(vtLine);

        // OpenClaw
        let ocLine = '- OpenClaw：' + (report.openclaw && report.openclaw.status
            ? report.openclaw.status : 'N/A');
        if (report.openclaw && report.openclaw.describe) {
            ocLine += '，' + report.openclaw.describe;
        }
        lines.push(ocLine);

        // Findings
        if (Array.isArray(report.findings)) {
            for (const f of report.findings) {
                lines.push('- 发现' + (f.severity || '未知')
                    + '行为，' + (f.title || ''));
                if (f.description) {
                    lines.push('   - ' + f.description);
                }
            }
        }

        // Antivirus
        if (report.antivirus && report.antivirus.virus_count > 0
            && Array.isArray(report.antivirus.virus_list)) {
            for (const v of report.antivirus.virus_list) {
                lines.push('- 病毒扫描：发现'
                    + (v.virus_name || '未知病毒') + '，'
                    + (v.file || '未知文件'));
            }
        }
        else {
            lines.push('- 病毒扫描：未检测到病毒');
        }
    }

    lines.push('');
    lines.push('───────────────────────────────────────');
    lines.push('🏁 最终裁决：');
    lines.push(report.final_verdict || '未知');

    if (report.overview) {
        lines.push('');
        lines.push('💡 建议：' + (report.suggestion || ''));
    }
    lines.push('═══════════════════════════════════════');

    return lines.join('\n');
}

/**
 * 为未收录场景生成报告文本
 *
 * @param {string} slug skill标识
 * @return {string} 未收录报告纯文本
 */
function formatNotIndexedReportText(slug) {
    const now = formatTimestamp(Date.now());
    const lines = [];
    lines.push('🛡️ Skill安全守卫报告');
    lines.push('═══════════════════════════════════════');
    lines.push('📊 守卫摘要');
    lines.push('评估时间：' + now);
    lines.push('Skill名称：' + (slug || '未知'));
    lines.push('来    源：未知');
    lines.push('作    者：未知');
    lines.push('版    本：未知');
    lines.push('评估结果：❓ 未收录，不建议安装');
    lines.push('');
    lines.push('───────────────────────────────────────');
    lines.push('🏁 最终裁决：');
    lines.push('❌ 不建议安装(需人工确认)');
    lines.push('');
    lines.push('💡 建议：尚未被安全系统收录，建议人工审查后再安装');
    lines.push('═══════════════════════════════════════');
    return lines.join('\n');
}

/**
 * 为错误场景生成报告文本
 *
 * @param {string} msg 错误消息
 * @return {string} 错误报告纯文本
 */
function formatErrorReportText(msg) {
    const now = formatTimestamp(Date.now());
    const lines = [];
    lines.push('🛡️ Skill安全守卫报告');
    lines.push('═══════════════════════════════════════');
    lines.push('📊 守卫摘要');
    lines.push('评估时间：' + now);
    lines.push('评估结果：❌ 安全检查失败');
    if (msg) {
        lines.push('');
        lines.push('错误信息：' + msg);
    }
    lines.push('');
    lines.push('───────────────────────────────────────');
    lines.push('🏁 最终裁决：');
    lines.push('❌ 暂缓安装(安全检查未完成)');
    lines.push('');
    lines.push('💡 建议：安全检查服务调用失败，建议稍后重试，请勿跳过安全检查直接安装');
    lines.push('═══════════════════════════════════════');
    return lines.join('\n');
}

/**
 * 渲染批量查询结果的单个Skill详情段落
 *
 * @param {Object} report 单个Skill的report对象
 * @return {string} 单个Skill详情段落文本
 */
function formatBatchItemText(report) {
    const lines = [];
    lines.push('───────────────────────────────────────');
    lines.push('📌 ' + (report.name || '未知') + ' v'
        + (report.version || '未知'));
    lines.push('来源：' + (report.source || '未知')
        + ' | 作者：' + (report.author || '未知'));
    lines.push('评估结果：' + (report.verdict || '未知'));

    if (report.overview) {
        lines.push('');
        lines.push('📕 ' + report.overview);

        lines.push('');
        lines.push('🗒 ' + (report.bd_describe || 'N/A'));

        lines.push('');
        lines.push('评估过程');

        let vtLine = '- VirusTotal：' + (report.virustotal && report.virustotal.status
            ? report.virustotal.status : 'N/A');
        if (report.virustotal && report.virustotal.describe) {
            vtLine += '，' + report.virustotal.describe;
        }
        lines.push(vtLine);

        let ocLine = '- OpenClaw：' + (report.openclaw && report.openclaw.status
            ? report.openclaw.status : 'N/A');
        if (report.openclaw && report.openclaw.describe) {
            ocLine += '，' + report.openclaw.describe;
        }
        lines.push(ocLine);

        if (Array.isArray(report.findings)) {
            for (const f of report.findings) {
                lines.push('- 发现' + (f.severity || '未知')
                    + '行为，' + (f.title || ''));
                if (f.description) {
                    lines.push('   - ' + f.description);
                }
            }
        }

        if (report.antivirus && report.antivirus.virus_count > 0
            && Array.isArray(report.antivirus.virus_list)) {
            for (const v of report.antivirus.virus_list) {
                lines.push('- 病毒扫描：发现'
                    + (v.virus_name || '未知病毒') + '，'
                    + (v.file || '未知文件'));
            }
        }
        else {
            lines.push('- 病毒扫描：未检测到病毒');
        }
    }

    lines.push('');
    lines.push('🏁 最终裁决：' + (report.final_verdict || '未知'));
    lines.push('💡 建议：' + (report.suggestion || ''));
    return lines.join('\n');
}

/**
 * 将批量查询结果渲染为纯文本报告
 *
 * @param {Object} batchResult queryFullDirectory()返回的完整结果
 * @return {string} 批量报告纯文本
 */
function formatBatchReportText(batchResult) {
    const now = formatTimestamp(Date.now());
    const dangerAndError = (batchResult.danger_count || 0)
        + (batchResult.error_count || 0);
    const lines = [];

    lines.push('🛡️ Skill安全守卫报告');
    lines.push('═══════════════════════════════════════');
    lines.push('');
    lines.push('📊守卫摘要');
    lines.push('评估时间：' + now);
    lines.push('评估Skills总量：' + (batchResult.total || 0) + '个');
    lines.push(' ✅通过：' + (batchResult.safe_count || 0) + '个');
    lines.push(' 🚫不通过：' + dangerAndError + '个');
    lines.push(' ⚠️需关注：' + (batchResult.caution_count || 0) + '个');
    lines.push('═══════════════════════════════════════');

    // 不通过 Skills
    lines.push('🚫不通过Skills（不建议安装，需人工确认）：');
    lines.push('');

    const results = batchResult.results || [];
    const dangerItems = results.filter(r => {
        if (!r.report) {
            return r.code === 'error'
                || (r.code === 'success'
                    && (!Array.isArray(r.data) || r.data.length === 0));
        }
        const c = (r.report.bd_confidence || '').toLowerCase();
        return c === 'dangerous' || c === '' || c === 'error';
    });

    if (dangerItems.length === 0) {
        lines.push('无');
    }
    else {
        for (const item of dangerItems) {
            if (item.report) {
                lines.push(formatBatchItemText(item.report));
            }
            else {
                lines.push('───────────────────────────────────────');
                lines.push('📌 ' + (item.slug || '未知'));
                lines.push('评估结果：❌ '
                    + (item.msg || '安全检查失败'));
                lines.push('');
                lines.push('🏁 最终裁决：❌ 不建议安装(需人工确认)');
                lines.push('💡 建议：安全检查未通过，建议人工审查');
            }
        }
    }

    lines.push('');
    lines.push('═══════════════════════════════════════');

    // 需关注 Skills
    lines.push('⚠️需关注Skills（需谨慎安装）：');
    lines.push('');

    const cautionItems = results.filter(r => {
        return r.report
            && (r.report.bd_confidence || '').toLowerCase() === 'caution';
    });

    if (cautionItems.length === 0) {
        lines.push('无');
    }
    else {
        for (const item of cautionItems) {
            lines.push(formatBatchItemText(item.report));
        }
    }

    lines.push('');
    lines.push('═══════════════════════════════════════');
    return lines.join('\n');
}

// ============================================================
// HTTP Client (ported from source/api/client.ts)
// ============================================================

/**
 * 发送HTTP请求
 *
 * @param {Object} options HTTP请求选项
 * @param {number} timeout 超时时间（毫秒）
 * @return {Promise.<string>} 响应文本
 */
function makeRequest(options, timeout) {
    return new Promise((resolve, reject) => {
        const protocol = options.protocol === 'https:' ? https : http;

        const req = protocol.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(data);
                }
                else {
                    reject(new Error(
                        `HTTP ${res.statusCode}: ${data.substring(0, 200)}`
                    ));
                }
            });
        });

        req.on('error', (error) => {
            reject(new Error(`请求失败: ${error.message}`));
        });

        req.setTimeout(timeout, () => {
            req.destroy();
            reject(new Error('请求超时'));
        });

        req.end();
    });
}

// ============================================================
// API: checkSkillSecurityFullResponse
// ============================================================

/**
 * 通过slug查询skill安全检查完整响应
 *
 * @param {string} slug skill标识
 * @param {string=} version skill版本号
 * @return {Promise.<Object>} 安全检查响应对象
 */
async function checkSkillSecurityFullResponse(slug, version) {
    const requestOptions = buildRequestOptions(slug, version);
    const responseText = await makeRequest(requestOptions, REQUEST_TIMEOUT);
    return safeJsonParse(responseText);
}

// ============================================================
// Slug Extraction from _meta.json / SKILL.md
// ============================================================

/**
 * 从skill目录提取slug和版本信息
 * 优先读取_meta.json，回退到SKILL.md frontmatter（仅取version），slug兜底为目录名
 *
 * @param {string} dirPath skill目录路径
 * @return {Object} 包含slug和version的对象
 */
function extractSlugFromSkillMd(dirPath) {
    const fallbackSlug = path.basename(dirPath);

    // Step 1: 尝试从 _meta.json 读取
    const metaJsonPath = path.join(dirPath, '_meta.json');
    if (fs.existsSync(metaJsonPath)) {
        try {
            const meta = JSON.parse(fs.readFileSync(metaJsonPath, 'utf8'));
            if (meta.slug) {
                return {
                    slug: meta.slug,
                    version: meta.version || undefined
                };
            }
        }
        catch (e) {
            // _meta.json 解析失败，继续回退
        }
    }

    // Step 2: 回退 - slug使用目录名，从SKILL.md提取version
    const skillMdPath = path.join(dirPath, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) {
        return {slug: fallbackSlug, version: undefined};
    }
    const content = fs.readFileSync(skillMdPath, 'utf8');
    const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!fmMatch) {
        return {slug: fallbackSlug, version: undefined};
    }
    const fm = fmMatch[1];
    const versionMatch = fm.match(/^version:\s*(.+)$/m);
    let version = versionMatch ? versionMatch[1].trim() : undefined;
    // 若顶层未找到，尝试 metadata.version
    if (!version) {
        const metaVersionMatch = fm.match(/^metadata:\s*\r?\n(?:[ \t]+.*\r?\n)*?[ \t]+version:\s*(.+)$/m);
        if (metaVersionMatch) {
            version = metaVersionMatch[1].trim();
        }
    }
    if (version && /^(["']).*\1$/.test(version)) {
        version = version.slice(1, -1);
    }
    return {slug: fallbackSlug, version};
}

// ============================================================
// Content SHA256 (directory-based, matches server-side algorithm)
// ============================================================

/**
 * 计算目录内容的SHA256哈希值
 *
 * @param {string} dirPath 目录路径
 * @return {string} SHA256哈希值，目录为空时返回空字符串
 */
function computeContentSha256(dirPath) {
    const files = [];

    /**
     * 递归遍历目录收集文件路径
     *
     * @param {string} dir 当前目录
     * @param {string} prefix 相对路径前缀
     * @inner
     */
    function walk(dir, prefix) {
        const entries = fs.readdirSync(dir, {withFileTypes: true});
        for (const entry of entries) {
            const rel = prefix
                ? `${prefix}/${entry.name}`
                : entry.name;
            if (entry.isDirectory()) {
                if (entry.name === '__MACOSX') {
                    continue;
                }
                walk(path.join(dir, entry.name), rel);
            }
            else if (entry.isFile()) {
                files.push(rel);
            }
        }
    }

    walk(dirPath, '');

    // Filter out top-level _meta.json, .clawhub/ directory and .DS_Store
    const filtered = files.filter(
        f => f !== '_meta.json' && !f.startsWith('.clawhub/')
            && path.basename(f) !== '.DS_Store'
    );
    if (filtered.length === 0) {
        return '';
    }

    // Normalize paths and sort lexicographically
    const normalized = filtered.map(f => {
        let p = f.replace(/\\/g, '/');
        p = path.posix.normalize(p);
        p = p.replace(/^\/+/, '');
        return p;
    }).sort();

    // Build manifest: "{relativePath}\n{fileSHA256}\n" for each file
    let manifest = '';
    for (const rel of normalized) {
        const abs = path.join(dirPath, rel);
        const hash = crypto.createHash('sha256');
        hash.update(fs.readFileSync(abs));
        manifest += `${rel}\n${hash.digest('hex')}\n`;
    }

    // SHA256 of the entire manifest
    const finalHash = crypto.createHash('sha256');
    finalHash.update(manifest);
    return finalHash.digest('hex');
}

// ============================================================
// API: checkSkillSecurityBySha256
// ============================================================

/**
 * 根据SHA256构建HTTP请求选项
 *
 * @param {string} sha256 内容SHA256哈希值
 * @return {Object} HTTP请求选项对象
 */
function buildSha256RequestOptions(sha256) {
    const queryParams = {sha256};
    const queryString = Object.entries(queryParams)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&');
    const url = new URL(`${API_PATH}?${queryString}`, API_BASE_URL);

    const headers = {'Host': url.host};
    if (_CHANNEL_ID) {
        headers['X-Caller'] = _CHANNEL_ID;
    }

    return {
        protocol: url.protocol,
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: `${url.pathname}?${queryString}`,
        method: 'GET',
        headers
    };
}

/**
 * 通过SHA256查询skill安全检查结果
 *
 * @param {string} sha256 内容SHA256哈希值
 * @return {Promise.<Object>} 安全检查响应对象
 */
async function checkSkillSecurityBySha256(sha256) {
    const requestOptions = buildSha256RequestOptions(sha256);
    const responseText = await makeRequest(requestOptions, REQUEST_TIMEOUT);
    return safeJsonParse(responseText);
}

// ============================================================
// Concurrent execution with limit
// ============================================================

/**
 * 限制并发数执行异步任务列表
 *
 * @param {Array.<Function>} tasks 异步任务函数数组
 * @param {number} limit 最大并发数
 * @return {Promise.<Array>} 所有任务的结果数组
 */
async function parallelLimit(tasks, limit) {
    const results = [];
    let index = 0;

    /**
     * 工作协程，循环消费任务队列
     *
     * @inner
     */
    async function worker() {
        while (index < tasks.length) {
            const i = index++;
            try {
                results[i] = await tasks[i]();
            }
            catch (err) {
                results[i] = {__error: err};
            }
        }
    }

    const workers = Array.from(
        {length: Math.min(limit, tasks.length)},
        () => worker()
    );
    await Promise.all(workers);
    return results;
}

// ============================================================
// QueryFull: Batch query all subdirectories by slug (Scenario C)
// ============================================================

/**
 * 根据响应判定置信度分类
 *
 * @param {Object} response 安全检查响应对象
 * @return {string} 分类结果：safe/dangerous/caution/error
 */
function classifyConfidence(response) {
    if (response.code === 'success'
        && response.data
        && response.data.length > 0) {
        const c = (response.data[0].bd_confidence || '').toLowerCase();
        if (c === 'safe' || c === 'trusted') {
            return 'safe';
        }
        if (c === 'dangerous') {
            return 'dangerous';
        }
        if (c === 'caution') {
            return 'caution';
        }
    }
    return 'error';
}

/**
 * 批量查询目录下所有子目录的skill安全状态
 *
 * @param {string} dirPath skills父目录路径
 * @return {Promise.<Object>} 批量查询结果对象
 */
async function queryFullDirectory(dirPath) {
    if (!dirPath || !fs.existsSync(dirPath)) {
        return makeQueryFullResult(
            'error',
            `❌ 错误：目录路径不存在 -- ${dirPath || '(空)'}`
        );
    }

    const stat = fs.statSync(dirPath);
    if (!stat.isDirectory()) {
        return makeQueryFullResult(
            'error',
            `❌ 错误：路径不是目录 -- ${dirPath}`
        );
    }

    // List immediate subdirectories, skip hidden dirs
    const entries = fs.readdirSync(dirPath).filter(name => {
        if (name.startsWith('.') || name === '__MACOSX') {
            return false;
        }
        return fs.statSync(path.join(dirPath, name)).isDirectory();
    });

    if (entries.length === 0) {
        return makeQueryFullResult(
            'success',
            'queryfull completed, no skill subdirectories found'
        );
    }

    // Build task list for concurrent execution
    const tasks = entries.map(name => {
        const skillDir = path.join(dirPath, name);
        const {slug, version} = extractSlugFromSkillMd(skillDir);

        return async () => {
            try {
                const response = await checkSkillSecurityFullResponse(
                    slug, version
                );
                let result = {slug, ...response};

                // SHA256 fallback: when slug query returns empty data,
                // try content_sha256
                if (response.code === 'success'
                    && Array.isArray(response.data)
                    && response.data.length === 0) {
                    try {
                        const contentSha256 = computeContentSha256(
                            skillDir
                        );
                        const sha256Log = '[sha256-fallback] slug='
                            + slug + ', contentSha256='
                            + (contentSha256 || '(empty)') + '\n';
                        _debugMode && process.stderr.write(sha256Log);
                        if (contentSha256) {
                            const sha256Response
                                = await checkSkillSecurityBySha256(
                                    contentSha256
                                );
                            const dataLen
                                = Array.isArray(sha256Response.data)
                                    ? sha256Response.data.length
                                    : 'N/A';
                            _debugMode && process.stderr.write(
                                '[sha256-fallback] slug=' + slug
                                    + ', sha256 query result: code='
                                    + sha256Response.code
                                    + ', data.length=' + dataLen
                                    + '\n'
                            );
                            if (sha256Response.code === 'success'
                                && Array.isArray(sha256Response.data)
                                && sha256Response.data.length > 0) {
                                result = {slug, ...sha256Response};
                            }
                        }
                    }
                    catch (fallbackErr) {
                        const errMsg = fallbackErr instanceof Error
                            ? fallbackErr.message
                            : fallbackErr;
                        _debugMode && process.stderr.write(
                            '[sha256-fallback] slug=' + slug
                                + ', fallback error: ' + errMsg
                                + '\n'
                        );
                    }
                }

                const report = buildReport(result.data, result.ts);
                if (report) {
                    result.report = report;
                }
                return result;
            }
            catch (error) {
                return {
                    slug,
                    code: 'error',
                    msg: error instanceof Error
                        ? error.message
                        : '未知错误',
                    data: []
                };
            }
        };
    });

    const results = await parallelLimit(tasks, CONCURRENT_LIMIT);

    // Classify results
    let safeCount = 0;
    let dangerCount = 0;
    let cautionCount = 0;
    let errorCount = 0;
    for (const r of results) {
        const category = classifyConfidence(r);
        if (category === 'safe') {
            safeCount++;
        }
        else if (category === 'dangerous') {
            dangerCount++;
        }
        else if (category === 'caution') {
            cautionCount++;
        }
        else {
            errorCount++;
        }
    }

    return makeQueryFullResult('success', 'queryfull completed', {
        total: entries.length,
        safe_count: safeCount,
        danger_count: dangerCount,
        caution_count: cautionCount,
        error_count: errorCount,
        results
    });
}

// ============================================================
// QuerySingle: Query one skill directory by slug (Scenario A2)
// ============================================================

/**
 * 查询单个skill目录的安全状态
 *
 * @param {string} dirPath skill目录路径
 * @return {Promise.<Object>} 安全检查结果（与slug查询格式一致）
 */
async function querySingleDirectory(dirPath) {
    if (!dirPath || !fs.existsSync(dirPath)) {
        return {
            code: 'error',
            msg: `❌ 错误：目录路径不存在 -- ${dirPath || '(空)'}`,
            ts: Date.now(),
            data: []
        };
    }

    const stat = fs.statSync(dirPath);
    if (!stat.isDirectory()) {
        return {
            code: 'error',
            msg: `❌ 错误：路径不是目录 -- ${dirPath}`,
            ts: Date.now(),
            data: []
        };
    }

    const {slug, version} = extractSlugFromSkillMd(dirPath);

    try {
        const response = await checkSkillSecurityFullResponse(
            slug, version
        );
        let result = {...response};

        // SHA256 fallback: when slug query returns empty data
        if (response.code === 'success'
            && Array.isArray(response.data)
            && response.data.length === 0) {
            try {
                const contentSha256 = computeContentSha256(dirPath);
                _debugMode && process.stderr.write(
                    '[sha256-fallback] slug=' + slug
                        + ', contentSha256='
                        + (contentSha256 || '(empty)') + '\n'
                );
                if (contentSha256) {
                    const sha256Response
                        = await checkSkillSecurityBySha256(
                            contentSha256
                        );
                    const dataLen
                        = Array.isArray(sha256Response.data)
                            ? sha256Response.data.length
                            : 'N/A';
                    _debugMode && process.stderr.write(
                        '[sha256-fallback] slug=' + slug
                            + ', sha256 query result: code='
                            + sha256Response.code
                            + ', data.length=' + dataLen
                            + '\n'
                    );
                    if (sha256Response.code === 'success'
                        && Array.isArray(sha256Response.data)
                        && sha256Response.data.length > 0) {
                        result = {...sha256Response};
                    }
                }
            }
            catch (fallbackErr) {
                const errMsg = fallbackErr instanceof Error
                    ? fallbackErr.message
                    : fallbackErr;
                _debugMode && process.stderr.write(
                    '[sha256-fallback] slug=' + slug
                        + ', fallback error: ' + errMsg
                        + '\n'
                );
            }
        }

        const report = buildReport(result.data, result.ts);
        if (report) {
            result.report = report;
        }
        return result;
    }
    catch (error) {
        return {
            code: 'error',
            msg: '🚫 安全检查服务调用失败：'
                + (error instanceof Error
                    ? error.message : '未知错误'),
            ts: Date.now(),
            data: []
        };
    }
}

// ============================================================
// CLI Entry Point
// ============================================================

let _debugMode = false;

/**
 * 解析命令行参数
 *
 * @param {Array.<string>} argv 命令行参数数组
 * @return {Object} 解析后的参数对象
 */
function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        if (argv[i] === '--slug' && i + 1 < argv.length) {
            args.slug = argv[++i];
        }
        else if (argv[i] === '--version' && i + 1 < argv.length) {
            args.version = argv[++i];
        }
        else if (argv[i] === '--action' && i + 1 < argv.length) {
            args.action = argv[++i];
        }
        else if (argv[i] === '--file' && i + 1 < argv.length) {
            args.file = argv[++i];
        }
        else if (argv[i] === '--debug') {
            args.debug = true;
        }
    }
    return args;
}

/**
 * CLI主入口函数
 *
 * @return {Promise} 执行完成的Promise
 */
async function main() {
    const args = parseArgs(process.argv);
    _debugMode = !!args.debug;

    const outputResult = (response) => {
        if (args.debug) {
            console.log(JSON.stringify(response, null, 2));
        } else {
            let compact;
            if (response.results !== undefined) {
                // Scenario D (queryfull): batch summary
                compact = {
                    code: response.code,
                    msg: response.msg,
                    ts: response.ts,
                    total: response.total,
                    safe_count: response.safe_count,
                    danger_count: response.danger_count,
                    caution_count: response.caution_count,
                    error_count: response.error_count,
                    report_text: response.report_text
                };
            } else {
                // Scenario A/C: single query
                const first = Array.isArray(response.data)
                    && response.data.length > 0
                    ? response.data[0] : null;
                compact = {
                    code: response.code,
                    message: response.message,
                    ts: response.ts,
                    bd_confidence: first
                        ? first.bd_confidence : null,
                    final_verdict: response.report
                        ? response.report.final_verdict : null,
                    report_text: response.report_text
                };
            }
            console.log(JSON.stringify(compact, null, 2));
        }
    };
    if (args.action === 'queryfull') {
        // Batch query all subdirectories by slug
        if (!args.file) {
            const output = makeQueryFullResult(
                'error',
                '❌ 错误：--action queryfull 需要提供'
                    + ' --file 参数（skills 父目录）\n'
                    + '用法：node check.js --action queryfull'
                    + ' --file "/path/to/skills"'
            );
            output.report_text = formatErrorReportText(output.msg);
            outputResult(output);
            process.exit(2);
        }

        const response = await queryFullDirectory(args.file);
        response.report_text = formatBatchReportText(response);
        outputResult(response);

        // Exit code: 0 if all safe and total > 0, 1 otherwise
        const allSafe = response.code === 'success'
            && response.total > 0
            && response.safe_count === response.total;
        process.exit(allSafe ? 0 : 1);

    }
    else if (args.action === 'query') {
        // Single directory query
        if (!args.file) {
            const errMsg = '❌ 错误：--action query 需要提供'
                + ' --file 参数（skill 目录路径）\n'
                + '用法：node check.js --action query'
                + ' --file "/path/to/skill-dir"';
            const output = {
                code: 'error',
                msg: errMsg,
                ts: Date.now(),
                data: [],
                report_text: formatErrorReportText(errMsg)
            };
            outputResult(output);
            process.exit(2);
        }

        const response = await querySingleDirectory(args.file);
        if (response.report) {
            response.report_text = formatSingleReportText(
                response.report
            );
        }
        else if (response.code === 'error') {
            response.report_text = formatErrorReportText(
                response.msg
            );
        }
        else {
            response.report_text = formatNotIndexedReportText(
                args.file
            );
        }
        outputResult(response);

        if (response.code === 'success'
            && response.data
            && response.data.length > 0) {
            const bdConfidence
                = (response.data[0].bd_confidence || '').toLowerCase();
            const safe = bdConfidence === 'safe'
                || bdConfidence === 'trusted';
            process.exit(safe ? 0 : 1);
        }
        else {
            process.exit(1);
        }

    }
    else {
        // Slug query flow
        if (!args.slug) {
            const errMsg = '❌ 错误：缺少必填参数 --slug\n'
                + '用法：node check.js --slug'
                + ' \'skill-slug\' [--version \'1.0.0\']';
            const output = {
                code: 'error',
                msg: errMsg,
                ts: Date.now(),
                data: [],
                report_text: formatErrorReportText(errMsg)
            };
            outputResult(output);
            process.exit(2);
        }

        try {
            const response = await checkSkillSecurityFullResponse(
                args.slug, args.version
            );
            const report = buildReport(response.data, response.ts);
            if (report) {
                response.report = report;
                response.report_text = formatSingleReportText(report);
            }
            else {
                response.report_text = formatNotIndexedReportText(
                    args.slug
                );
            }
            outputResult(response);

            // Determine exit code based on bd_confidence
            if (response.code === 'success'
                && response.data
                && response.data.length > 0) {
                const item = response.data[0];
                const bdConfidence
                    = (item.bd_confidence || '').toLowerCase();
                const safe = bdConfidence === 'safe'
                    || bdConfidence === 'trusted';
                process.exit(safe ? 0 : 1);
            }
            else {
                process.exit(1);
            }
        }
        catch (error) {
            const errMsg = '🚫 安全检查服务调用失败：'
                + (error.message || '未知错误');
            const output = {
                code: 'error',
                msg: errMsg,
                ts: Date.now(),
                data: [],
                report_text: formatErrorReportText(errMsg)
            };
            outputResult(output);
            process.exit(2);
        }
    }
}

main().catch((err) => {
    const errMsg = '❌ 脚本执行异常：' + (err.message || '未知错误');
    const output = {
        code: 'error',
        msg: errMsg,
        ts: Date.now(),
        data: [],
        report_text: formatErrorReportText(errMsg)
    };
    // No access to outputResult here; debug flag must be re-parsed
    const debugMode = process.argv.includes('--debug');
    if (debugMode) {
        console.log(JSON.stringify(output, null, 2));
    } else {
        const compact = {
            code: output.code,
            message: output.msg,
            ts: output.ts,
            bd_confidence: null,
            final_verdict: null,
            report_text: output.report_text
        };
        console.log(JSON.stringify(compact, null, 2));
    }
    process.exit(2);
});