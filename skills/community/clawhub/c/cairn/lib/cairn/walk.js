import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, statSync } from 'node:fs';
import { extname, join, relative } from 'node:path';
import { BINARY_EXTS, HARD_IGNORES, MAX_BYTES } from './constants/walk.constants.js';
export const walk = (root, opts) => {
    const rels = existsSync(join(root, '.git')) ? walkGit(root) : walkFs(root);
    return rels.filter((rel) => passesFilter(rel, opts) && acceptable(join(root, rel)));
};
const walkGit = (root) => {
    try {
        const out = execFileSync('git', ['-C', root, 'ls-files'], { encoding: 'utf8' });
        return out.split('\n').filter(Boolean);
    }
    catch {
        return walkFs(root);
    }
};
const walkFs = (root) => {
    const out = [];
    const stack = [root];
    while (stack.length > 0) {
        const dir = stack.pop();
        let entries;
        try {
            entries = readdirSync(dir, { withFileTypes: true });
        }
        catch {
            continue;
        }
        for (const e of entries) {
            if (HARD_IGNORES.has(e.name))
                continue;
            if (e.name.startsWith('.'))
                continue;
            const abs = join(dir, e.name);
            if (e.isDirectory())
                stack.push(abs);
            else if (e.isFile())
                out.push(relative(root, abs));
        }
    }
    return out;
};
const passesFilter = (rel, opts) => {
    if (opts?.include && opts.include.length > 0) {
        if (!opts.include.some((suf) => rel.endsWith(suf)))
            return false;
    }
    if (opts?.exclude && opts.exclude.length > 0) {
        if (opts.exclude.some((sub) => rel.includes(sub)))
            return false;
    }
    return true;
};
const acceptable = (absPath) => {
    const ext = extname(absPath).toLowerCase();
    if (BINARY_EXTS.has(ext))
        return false;
    let st;
    try {
        st = statSync(absPath);
    }
    catch {
        return false;
    }
    if (!st.isFile())
        return false;
    if (st.size > MAX_BYTES)
        return false;
    return true;
};
