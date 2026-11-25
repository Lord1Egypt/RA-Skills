import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,readFile,writeFile,stat,rm} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {defaultConfig,validateConfig,resolveOptions,loadConfig,initConfig} from '../scripts/config.mjs';
import {parseCLI} from '../scripts/search.mjs';

async function files(t){const root=await mkdtemp(path.join(os.tmpdir(),'easybr-search-config-'));t.after(()=>rm(root,{recursive:true,force:true}));return root}
test('saved platform selection is replaced, not expanded, by an explicit human selection',async t=>{
 const root=await files(t),file=path.join(root,'config.json');await writeFile(file,JSON.stringify({...defaultConfig(),platforms:['baidu','google'],browserMap:{bilibili:'chrome'}}));
 const parsed=parseCLI(['search','--config',file,'--platforms','bilibili','--query','动画']);
 const resolved=await resolveOptions(parsed.options);assert.deepEqual(resolved.platforms,['bilibili']);assert.deepEqual(resolved.queries,['动画']);
 const saved=await resolveOptions({configFile:file});assert.deepEqual(saved.platforms,['baidu','google']);
 const indexed=await resolveOptions(parseCLI(['search','--config',file,'--site','csdn.net']).options);assert.deepEqual(indexed.platforms,['site:csdn.net']);
});
test('config creation is private and refuses to overwrite existing preferences',async t=>{
 const file=path.join(await files(t),'nested','config.json');await initConfig(file);assert.equal((await stat(file)).mode&0o777,0o600);assert.deepEqual(await loadConfig(file),defaultConfig());
 const before=await readFile(file,'utf8');await assert.rejects(initConfig(file),/config_already_exists/);assert.equal(await readFile(file,'utf8'),before);
});
test('explicit missing or malformed configuration fails before any browser work',async t=>{
 const root=await files(t),file=path.join(root,'missing.json');await assert.rejects(resolveOptions({configFile:file}),/config_not_found/);
 assert.deepEqual(await loadConfig(file,{optional:true}),defaultConfig());await writeFile(file,'{');await assert.rejects(loadConfig(file),/config_invalid_json/);
 for(const config of [{platforms:[]},{platforms:['unknown']},{read:11},{timeoutMs:'18000'},{schemaVersion:2},{browserMap:{xhs:'chrome'}},{unexpected:true}])assert.throws(()=>validateConfig(config));
 assert.throws(()=>parseCLI(['search','--platforms','--read','0']),/invalid_platforms/);
});
test('CLI budgets and a replacement browser map override saved preferences',async t=>{
 const root=await files(t),configFile=path.join(root,'config.json'),browserMapFile=path.join(root,'map.json');await writeFile(configFile,JSON.stringify({...defaultConfig(),browserMap:{'*':'old'}}));await writeFile(browserMapFile,JSON.stringify({bilibili:'new'}));
 const resolved=await resolveOptions({configFile,browserMapFile,read:'0',limit:'2',platforms:['bilibili']});assert.equal(resolved.read,'0');assert.deepEqual(resolved.browserMap,{bilibili:'new'});assert.deepEqual(resolved.platforms,['bilibili']);
});
