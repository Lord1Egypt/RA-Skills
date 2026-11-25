import { execFileSync } from 'node:child_process';
import { dirname, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const repo = 'TheAngryPit/TheAngrySkills';
const skillPath = 'skills/engineering/openclaw-custom-build-validation';
export function compare({dirty, localTree, remoteTree}) {
  if (dirty) return 'local-modifications';
  if (!localTree || !remoteTree) return 'untracked';
  return localTree === remoteTree ? 'current' : 'source-differs';
}
export function check(run, directory) {
  const git = (...args) => run('git', ['-C', directory, ...args]).trim();
  const result = {source: repo, localCommit: null, canonicalCommit: null, status: 'check-failed'};
  try {
    let root;
    try { root = git('rev-parse','--show-toplevel'); }
    catch (error) {
      if (error.status === 128 && /^fatal: not a git repository(?: \(|:)/m.test(String(error.stderr ?? ''))) {
        return {...result,status:'untracked'};
      }
      throw error;
    }
    const remotes = git('remote','-v').split('\n');
    const expected = /\s(?:https:\/\/github\.com\/|git@github\.com:)TheAngryPit\/TheAngrySkills(?:\.git)?\s/i;
    if (!remotes.some(line => expected.test(line))) return {...result,status:'different-source'};
    // Do not attribute a sibling copy's bytes to the canonical tracked tree.
    if (relative(resolve(root,skillPath),resolve(directory)) !== '') return {...result,status:'untracked'};
    const g = (...args) => run('git',['-C',root,...args]).trim();
    result.localCommit = g('rev-parse','HEAD');
    const dirty = Boolean(g('status','--porcelain','--untracked-files=all','--',skillPath));
    // A draft should not need network access to prove it has local edits.
    if (dirty) return {...result,status:'local-modifications'};
    let localTree;
    try { localTree = g('rev-parse',`HEAD:${skillPath}`); }
    catch { return {...result,status:'untracked'}; }
    const info = JSON.parse(run('gh',['api',`repos/${repo}`]));
    if (info.full_name?.toLowerCase() !== repo.toLowerCase() || typeof info.default_branch !== 'string') throw new Error();
    const commit = JSON.parse(run('gh',['api',`repos/${repo}/commits/${encodeURIComponent(info.default_branch)}`]));
    if (!/^[a-f0-9]{40}$/.test(commit.sha)) throw new Error();
    result.canonicalCommit = commit.sha;
    // Query the parent tree at the fixed commit; a directory entry carries its tree SHA.
    const entries = JSON.parse(run('gh',['api',`repos/${repo}/contents/skills/engineering?ref=${commit.sha}`]));
    if (!Array.isArray(entries)) throw new Error();
    const entry = entries.find(x => x.path === skillPath && x.type === 'dir');
    const remoteTree = entry?.sha;
    if (remoteTree && !/^[a-f0-9]{40}$/.test(remoteTree)) throw new Error();
    return {...result,status:compare({dirty,localTree,remoteTree})};
  } catch { return result; } // No command stderr: it may include private paths/auth detail.
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const run = (bin,args) => execFileSync(bin,args,{encoding:'utf8',timeout:10000,maxBuffer:1000000,stdio:['ignore','pipe','pipe'],env:{...process.env,LC_ALL:'C'}});
  console.log(JSON.stringify(check(run, resolve(dirname(fileURLToPath(import.meta.url)),'..')),null,2));
}
