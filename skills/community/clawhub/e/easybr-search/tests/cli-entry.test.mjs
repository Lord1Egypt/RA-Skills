import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,symlink,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {isCLIEntry} from '../scripts/cli-entry.mjs';

test('global symlink entry points run from an unrelated working directory',async t=>{
 const root=fileURLToPath(new URL('../',import.meta.url));
 const temp=await mkdtemp(path.join(tmpdir(),'easybr-search-global-'));
 t.after(()=>rm(temp,{recursive:true,force:true}));
 const alias=path.join(temp,'easybr-search');
 await symlink(root,alias,process.platform==='win32'?'junction':'dir');
 const run=(script,args)=>execFileSync(process.execPath,[path.join(alias,'scripts',script),...args],{cwd:temp,encoding:'utf8'});
 const version=JSON.parse(readFileSync(new URL('../package.json',import.meta.url),'utf8')).version;
 assert.equal(run('search.mjs',['--version']).trim(),'easybrSearch '+version);
 for(const script of ['search.mjs','benchmark.mjs','platform-check.mjs']){
  assert.ok(run(script,['--help']).trim().length>40,script+' must execute through its alias');
 }
 const imported=execFileSync(process.execPath,['--input-type=module','-e','await import('+JSON.stringify(new URL('../scripts/search.mjs',import.meta.url).href)+')'],{cwd:temp,encoding:'utf8'});
 assert.equal(imported,'','importing the search engine must not start a CLI');
});

test('missing or unrelated entry paths are not CLI entry points',()=>{
 assert.equal(isCLIEntry(import.meta.url,''),false);
 assert.equal(isCLIEntry(import.meta.url,'/nonexistent/easybr-search-entry.mjs'),false);
 assert.equal(isCLIEntry(new URL('../scripts/search.mjs',import.meta.url),fileURLToPath(import.meta.url)),false);
});
