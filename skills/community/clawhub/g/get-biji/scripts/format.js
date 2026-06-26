/**
 * Get Notes Formatting Module
 *
 * Handles:
 * - Transcript formatting with chapter heading injection
 * - Summary markdown building
 */

// ============================================================
// Utility
// ============================================================

function formatDuration(ms) {
    const seconds = Math.floor(ms / 1000);
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hours > 0) {
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function stripGoldQuotes(content) {
    if (!content) return '';
    return content.replace(/### ✨ 金句精选[\s\S]*?(?=###\s|##\s|$)/, '').trim();
}

function getDurationMinutes(note) {
    if (note.attachments && note.attachments.length > 0) {
        const audioDuration = note.attachments.find(a => a.duration)?.duration || 0;
        return Math.round(audioDuration / 60000);
    }
    return 0;
}

function safeName(title) {
    return (title || 'Untitled').replace(/[\/\\:*?"<>|]/g, '_').substring(0, 40);
}

// ============================================================
// Smart Classification (ported from original sync-get-notes.js)
// ============================================================

function classifyNote(note) {
    const noteType = note.note_type || '';
    const entryType = note.entry_type || '';
    const content = ((note.content || '') + ' ' + (note.title || '')).toLowerCase();

    const durationMin = getDurationMinutes(note);

    if (noteType === 'recorder_audio' || entryType === 'ai') {
        if (durationMin > 10) {
            if (content.includes('客户') || content.includes('交流') || content.includes('需求') || content.includes('报价')) {
                return '客户';
            }
            return '会议';
        }
        if (durationMin < 3) {
            if (content.includes('待办') || content.includes('记得') || content.includes('要做') || content.includes('明天')) {
                return '待办';
            }
            return '灵感';
        }
    }

    if (content.includes('工作会议') || content.includes('会议纪要') || content.includes('讨论') || content.includes('培训')) {
        return '会议';
    }
    if (content.includes('客户') || content.includes('报价') || content.includes('需求') || content.includes('合作')) {
        return '客户';
    }
    if (content.includes('复盘') || content.includes('反思') || content.includes('总结')) {
        return '复盘';
    }
    if (content.includes('选题') || content.includes('文章') || content.includes('内容') || content.includes('课程')) {
        return '选题';
    }
    if (content.includes('待办') || content.includes('要做') || content.includes('记得')) {
        return '待办';
    }

    return '灵感';
}

// ============================================================
// Chapter Parsing (from note.content markdown)
// ============================================================

/**
 * Parse chapter timestamps and titles from Get Notes' 章节概要 section.
 * Returns [{seconds, title, timestamp}] sorted by seconds.
 */
function parseChapters(content) {
    if (!content) return [];

    const chapters = [];
    // Match patterns like: [00:03:25](https://getnotes.seek:205) **title**
    const regex = /\[(\d{2}:\d{2}:\d{2})\]\(https:\/\/getnotes\.seek:(\d+)\)\s+\*\*(.+?)\*\*/g;
    let match;

    while ((match = regex.exec(content)) !== null) {
        chapters.push({
            timestamp: match[1],         // "00:03:25"
            seconds: parseInt(match[2]),  // 205
            title: match[3].trim(),       // "电影、戏剧与文学的区别"
        });
    }

    chapters.sort((a, b) => a.seconds - b.seconds);
    return chapters;
}

// ============================================================
// Transcript Formatting with Chapter Injection
// ============================================================

/**
 * Build structured transcript from raw sentence data with chapter headings injected.
 *
 * @param {Object} originalData - Raw API response with .content (JSON string containing sentence_list)
 * @param {Array} chapters - Parsed chapters from parseChapters()
 * @returns {string|null} Formatted transcript markdown, or null if no data
 */
function buildTranscript(originalData, chapters) {
    if (!originalData || !originalData.content) return null;

    let contentObj;
    try {
        contentObj = JSON.parse(originalData.content);
    } catch (e) {
        return null;
    }

    const sentences = contentObj.sentence_list || [];
    if (sentences.length === 0) return null;

    // Step 1: Build paragraphs (group sentences by speaker + gap threshold)
    const GAP_THRESHOLD = 5000; // 5 seconds
    const paragraphs = [];
    let currentPara = null;

    for (const sentence of sentences) {
        const speakerId = sentence.speaker_id;
        const text = sentence.text || '';
        const startTime = sentence.start_time || 0;

        if (!currentPara ||
            speakerId !== currentPara.speakerId ||
            startTime - currentPara.endTime > GAP_THRESHOLD) {
            // Start new paragraph
            if (currentPara) paragraphs.push(currentPara);
            currentPara = {
                speakerId,
                startTime,
                endTime: sentence.end_time || startTime,
                texts: [text],
                sentenceStartTimes: [startTime],
            };
        } else {
            currentPara.texts.push(text);
            currentPara.sentenceStartTimes.push(startTime);
            currentPara.endTime = sentence.end_time || startTime;
        }
    }
    if (currentPara) paragraphs.push(currentPara);

    if (paragraphs.length === 0) return null;

    // Step 2: Inject chapter headings
    // For each paragraph, check if any chapter starts within its time range.
    // If a chapter starts mid-paragraph, split the paragraph at the sentence boundary.
    const outputBlocks = []; // Array of {type: 'heading'|'paragraph', ...}
    let chapterIdx = 0;

    for (const para of paragraphs) {
        // Collect chapters that start before or at this paragraph's start
        while (chapterIdx < chapters.length &&
            chapters[chapterIdx].seconds * 1000 <= para.startTime) {
            outputBlocks.push({
                type: 'heading',
                timestamp: formatDuration(chapters[chapterIdx].seconds * 1000),
                title: chapters[chapterIdx].title,
            });
            chapterIdx++;
        }

        // Check if any chapters fall WITHIN this paragraph
        const midChapters = [];
        let tempIdx = chapterIdx;
        while (tempIdx < chapters.length &&
            chapters[tempIdx].seconds * 1000 < para.endTime) {
            midChapters.push({ ...chapters[tempIdx], idx: tempIdx });
            tempIdx++;
        }

        if (midChapters.length === 0) {
            // No chapter splits needed - output whole paragraph
            outputBlocks.push({
                type: 'paragraph',
                startTime: para.startTime,
                speakerId: para.speakerId,
                text: para.texts.join(''),
            });
        } else {
            // Split paragraph at chapter boundaries using sentence timestamps
            let sentenceOffset = 0;

            for (const ch of midChapters) {
                const chapterMs = ch.seconds * 1000;

                // Find the sentence index closest to this chapter's start
                let splitAt = sentenceOffset;
                for (let i = sentenceOffset; i < para.sentenceStartTimes.length; i++) {
                    if (para.sentenceStartTimes[i] >= chapterMs) {
                        splitAt = i;
                        break;
                    }
                    splitAt = i + 1;
                }

                // Output text before the split point
                if (splitAt > sentenceOffset) {
                    const segmentText = para.texts.slice(sentenceOffset, splitAt).join('');
                    if (segmentText.trim()) {
                        outputBlocks.push({
                            type: 'paragraph',
                            startTime: para.sentenceStartTimes[sentenceOffset] || para.startTime,
                            speakerId: para.speakerId,
                            text: segmentText,
                        });
                    }
                }

                // Insert chapter heading
                outputBlocks.push({
                    type: 'heading',
                    timestamp: formatDuration(chapterMs),
                    title: ch.title,
                });

                sentenceOffset = splitAt;
                chapterIdx = ch.idx + 1;
            }

            // Output remaining text after last chapter split
            if (sentenceOffset < para.texts.length) {
                const remainingText = para.texts.slice(sentenceOffset).join('');
                if (remainingText.trim()) {
                    outputBlocks.push({
                        type: 'paragraph',
                        startTime: para.sentenceStartTimes[sentenceOffset] || para.startTime,
                        speakerId: para.speakerId,
                        text: remainingText,
                    });
                }
            }
        }
    }

    // Emit any remaining chapters (after last paragraph)
    while (chapterIdx < chapters.length) {
        outputBlocks.push({
            type: 'heading',
            timestamp: formatDuration(chapters[chapterIdx].seconds * 1000),
            title: chapters[chapterIdx].title,
        });
        chapterIdx++;
    }

    // Step 3: Render to markdown
    let result = '';
    for (const block of outputBlocks) {
        if (block.type === 'heading') {
            result += `\n## [${block.timestamp}] ${block.title}\n\n`;
        } else {
            const ts = formatDuration(block.startTime);
            const label = block.speakerId !== null && block.speakerId !== undefined
                ? `[Speaker ${block.speakerId + 1}]` : '';
            result += `[${ts}] ${label} ${block.text}\n\n`;
        }
    }

    return result.trim();
}

/**
 * Build a plain transcript (no chapter injection) for notes without chapter data.
 */
function buildPlainTranscript(originalData) {
    return buildTranscript(originalData, []);
}

// ============================================================
// Markdown File Building
// ============================================================

const INLINE_THRESHOLD = 50; // lines - below this, inline transcript in summary

/**
 * Build summary markdown content for a note.
 */
function buildSummaryMarkdown(note, transcript, transcriptFilename) {
    const createdDate = note.created_at || '';
    const dateStr = createdDate.split(' ')[0] || 'unknown-date';
    const timeStr = (createdDate.split(' ')[1] || '').substring(0, 5);
    const durationMin = getDurationMinutes(note);
    const category = classifyNote(note);
    const content = note.content || '';

    let md = `---\n`;
    md += `title: "${(note.title || 'Untitled').replace(/"/g, '\\"')}"\n`;
    md += `date: ${dateStr}\n`;
    md += `time: "${timeStr}"\n`;
    md += `note_id: ${note.note_id}\n`;
    md += `category: ${category}\n`;
    if (durationMin > 0) md += `duration_min: ${durationMin}\n`;
    if (transcriptFilename) md += `transcript: "${transcriptFilename}"\n`;
    md += `---\n\n`;

    if (content) md += `${content}\n\n`;

    if (note.attachments && note.attachments.length > 0) {
        md += `## 附件\n\n`;
        note.attachments.forEach(att => {
            const url = att.url || att.attach_url || att.link;
            const duration = att.duration ? ` (${Math.round(att.duration / 60000)} min)` : '';
            if (url) md += `- [audio${duration}](${url})\n`;
        });
        md += `\n`;
    }

    // Inline transcript for short notes
    if (transcript && !transcriptFilename) {
        md += `## 原文\n\n${transcript}\n`;
    }

    return md;
}

/**
 * Build transcript file markdown.
 */
function buildTranscriptMarkdown(note, transcript, summaryFilename) {
    const createdDate = note.created_at || '';
    const dateStr = createdDate.split(' ')[0] || 'unknown-date';

    let md = `---\n`;
    md += `date: ${dateStr}\n`;
    md += `note_id: ${note.note_id}\n`;
    md += `title: "${(note.title || 'Untitled').replace(/"/g, '\\"')}"\n`;
    if (summaryFilename) md += `summary: "${summaryFilename}"\n`;
    md += `---\n\n`;
    md += `${transcript}\n`;

    return md;
}

/**
 * Determine whether a transcript should be in a separate file or inlined.
 * Returns true if separate file needed.
 */
function needsSeparateTranscript(transcript) {
    if (!transcript) return false;
    const lines = transcript.split('\n').length;
    return lines >= INLINE_THRESHOLD;
}

module.exports = {
    formatDuration,
    getDurationMinutes,
    safeName,
    classifyNote,
    parseChapters,
    buildTranscript,
    buildPlainTranscript,
    needsSeparateTranscript,
    buildSummaryMarkdown,
    buildTranscriptMarkdown,
};
