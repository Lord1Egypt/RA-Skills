import { CODE_LINES, CODE_OVERLAP, TEXT_BREAK_WINDOW, TEXT_CHARS, TEXT_OVERLAP, } from './constants/chunk.constants.js';
export const chunkCode = (content) => {
    if (content.length === 0)
        return [];
    const lines = content.split('\n');
    const n = lines.length;
    if (n === 0)
        return [];
    const step = CODE_LINES - CODE_OVERLAP;
    const out = [];
    let i = 0;
    while (i < n) {
        const end = Math.min(n, i + CODE_LINES);
        out.push({
            content: lines.slice(i, end).join('\n'),
            start_line: i + 1,
            end_line: end,
        });
        if (end >= n)
            break;
        i += step;
    }
    return out;
};
export const chunkText = (content) => {
    if (content.trim().length === 0)
        return [];
    const len = content.length;
    const out = [];
    let i = 0;
    while (i < len) {
        let end = Math.min(len, i + TEXT_CHARS);
        if (end < len) {
            const breakIdx = content.lastIndexOf('\n\n', end);
            if (breakIdx > i && end - breakIdx < TEXT_BREAK_WINDOW)
                end = breakIdx;
        }
        out.push(toChunk(content, i, end));
        if (end >= len)
            break;
        const next = end - TEXT_OVERLAP;
        i = next > i ? next : i + 1; // guard against zero-progress windows
    }
    return out;
};
const toChunk = (content, start, end) => {
    const slice = content.slice(start, end);
    const before = content.slice(0, start);
    const startLine = countNewlines(before) + 1;
    const endLine = startLine + countNewlines(slice);
    return { content: slice, start_line: startLine, end_line: endLine };
};
const countNewlines = (s) => {
    let n = 0;
    for (let i = 0; i < s.length; i++)
        if (s.charCodeAt(i) === 10)
            n++;
    return n;
};
