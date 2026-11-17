import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, mkdir, cp, rm, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { loadProfile, createVault, createBrowser, childEnv } from './runtime.mjs';
import { bridge } from './bridge.mjs';
const scripts = dirname(fileURLToPath(import.meta.url));
const skill = dirname(scripts);
const profile = { expectedVaultServerUrl: 'https://vault.example.invalid', expectedVaultEmail: 'fixture@example.invalid' };
const valid = JSON.stringify(profile);
const env = { HOME: '/synthetic-home' };
const cli = (input, extra = {}, cwd = scripts) => spawnSync(process.execPath, [join(cwd,'cli.mjs')], { input: JSON.stringify(input), encoding: 'utf8', env: { ...childEnv(), ...extra } });
const request = { action:'list',origin:'https://login.example.invalid',userId:'AGENT',sessionKey:'agent:AGENT:CONTEXT' };
test('missing profile is sanitized', async () => { await assert.rejects(loadProfile({env,read:async()=>{throw Error('PRIVATE_MARKER');}}),{code:'PROFILE_UNAVAILABLE'}); });
test('missing explicit identity never trusts status', async () => {
  for (const data of [{}, { expectedVaultServerUrl: profile.expectedVaultServerUrl }]) await assert.rejects(loadProfile({env,read:async()=>JSON.stringify(data)}),{code:'VAULT_IDENTITY_REQUIRED'});
  let lookup = false;
  const r = await bridge(request,{vault:{status:async()=>({...profile,status:'unlocked'}),items:async()=>{lookup=true;}}});
  assert.equal(r.code,'VAULT_IDENTITY_REQUIRED'); assert.equal(lookup,false);
});
test('wrong configured identity blocks lookup', async () => {
  for (const patch of [{serverUrl:'https://other.example.invalid'}, {userEmail:'other@example.invalid'}]) {
    let lookup=false;
    const r=await bridge(request,{profile,vault:{status:async()=>({serverUrl:profile.expectedVaultServerUrl,userEmail:profile.expectedVaultEmail,status:'unlocked',...patch}),items:async()=>{lookup=true;}}});
    assert.equal(r.code,'VAULT_IDENTITY_MISMATCH');assert.equal(lookup,false);
  }
});
test('XDG override and state resolution; explicit paths', async () => {
  let observed;
  const read=async p=>{observed=p;return valid;};
  const p=await loadProfile({env:{...env,XDG_CONFIG_HOME:'/xdg',OPENCLAW_STATE_DIR:'/state'},read});
  assert.equal(observed,'/xdg/camofox-vault-login/config.json');assert.equal(p.runtimePath,'/state/extensions/camofox-browser');assert.equal(p.configPath,'/state/openclaw.json');
  await loadProfile({env:{...env,CAMOFOX_VAULT_CONFIG:'/override.json'},read});assert.equal(observed,'/override.json');
  const home=await loadProfile({env,read});assert.equal(observed,'/synthetic-home/.config/camofox-vault-login/config.json');assert.equal(home.configPath,'/synthetic-home/.openclaw/openclaw.json');
  const explicit=await loadProfile({env,read:async()=>JSON.stringify({...profile,camofoxRuntimePath:'/runtime',openclawConfigPath:'/config'})});assert.equal(explicit.runtimePath,'/runtime');assert.equal(explicit.configPath,'/config');
});
test('profile validation rejects unsupported or secret keys and relative paths',async()=>{
  for(const patch of [{password:'PRIVATE_MARKER'},{keychainAccount:'fixture'},{expectedVaultServerUrl:'http://vault.example.invalid'},{camofoxRuntimePath:'relative'},{expectedVaultEmail:42},{expectedVaultEmail:'bad\nvalue'}]) await assert.rejects(loadProfile({env,read:async()=>JSON.stringify({...profile,...patch})}));
  await assert.rejects(loadProfile({env:{CAMOFOX_VAULT_CONFIG:'relative'}}),{code:'PROFILE_PATH_REQUIRED'});
  for(const data of ['null','[]','"PRIVATE_MARKER"','invalid'])await assert.rejects(loadProfile({env,read:async()=>data}));
});
test('locked vault without configured provider fails clearly on any OS',async()=>{
  for(const platform of ['linux','darwin','win32'])await assert.rejects(createVault({platform,profile,run:async()=>{throw Error('must not call');}}).unlock(),{code:'UNLOCK_PROVIDER_MISSING'});
  await assert.rejects(createVault({platform:'linux',profile:{...profile,keychainService:'fixture',keychainAccount:'fixture'}}).unlock(),{code:'UNLOCK_PROVIDER_MISSING'});
});
test('BW_SESSION reuse requires no unlock provider on non-Mac',async()=>{
  const v=createVault({platform:'linux',profile,env:{BW_SESSION:'SESSION_MARKER'},run:async(file,args,env)=>{assert.equal(env.BW_SESSION,'SESSION_MARKER');assert.equal(args[0],'status');return '{}';}});await v.status();
});
test('unsupported runtime build fails before imports',async()=>{
  for(const manifest of [{name:'other',version:'1.18.1'},{name:'@askjo/camofox-browser',version:'0.0.0'}])await assert.rejects(createBrowser({runtimePath:'/runtime',configPath:'/config',userId:'AGENT',sessionKey:'agent:AGENT:CONTEXT',read:async()=>JSON.stringify(manifest)}),{code:'UNSUPPORTED_CAMOFOX_BUILD'});
  await assert.rejects(createBrowser(),{code:'RUNTIME_REQUIRED'});
});
test('actual stdin CLI rejects arguments, missing caller, forbidden profile overrides',()=>{
  assert.equal(JSON.parse(cli({...request,runtimePath:'/PRIVATE_MARKER'}).stdout).code,'UNKNOWN_REQUEST_KEY');
  assert.equal(JSON.parse(cli({action:'list',origin:request.origin}).stdout).code,'CALLER_IDENTITY_REQUIRED');
  const r=spawnSync(process.execPath,[join(scripts,'cli.mjs'),'PRIVATE_MARKER'],{input:'{}',encoding:'utf8',env:childEnv()});assert.equal(JSON.parse(r.stdout).code,'STDIN_ONLY');assert.ok(!r.stdout.includes('PRIVATE_MARKER'));
});
test('actual subprocess config errors never emit profile or path',async()=>{
  const temp=await mkdtemp(join(tmpdir(),'profile-'));
  try{const path=join(temp,'PRIVATE_MARKER.json');await writeFile(path,JSON.stringify({...profile,unknown:'PRIVATE_MARKER'}));const r=cli(request,{CAMOFOX_VAULT_CONFIG:path});assert.equal(r.status,1);assert.equal(JSON.parse(r.stdout).code,'PROFILE_INVALID');assert.ok(!r.stdout.includes('PRIVATE_MARKER'));assert.equal(r.stderr,'');}finally{await rm(temp,{recursive:true,force:true});}
});
test('actual stdin discovery matches configured identity using synthetic bw process',async()=>{
  const temp=await mkdtemp(join(tmpdir(),'discovery-'));
  try{
    const path=join(temp,'config.json');await writeFile(path,valid);
    const executable=join(temp,'bw');await writeFile(executable,"#!/bin/sh\nif [ \"$1\" = \"status\" ]; then echo '{\"serverUrl\":\"https://vault.example.invalid\",\"userEmail\":\"fixture@example.invalid\",\"status\":\"unlocked\"}'; else echo '[]'; fi\n",{mode:0o700});
    const r=cli(request,{CAMOFOX_VAULT_CONFIG:path,PATH:temp});assert.equal(r.status,0);assert.deepEqual(JSON.parse(r.stdout),{ok:true,stage:'listed',items:[]});assert.equal(r.stderr,'');
  }finally{await rm(temp,{recursive:true,force:true});}
});
test('relocated entire skill runs checks and full suite independently',{skip:process.env.CAMOFOX_RELOCATION_CHILD==='1'},async()=>{
  const temp=await mkdtemp(join(tmpdir(),'relocated-'));
  try{const dest=join(temp,'unrelated-skill');await cp(skill,dest,{recursive:true});const cwd=join(dest,'scripts');
    for(const args of [['--check','runtime.mjs'],['--check','cli.mjs'],['--check','bridge.mjs'],['--test','bridge.test.mjs','packaging.test.mjs']]){const r=spawnSync(process.execPath,args,{cwd,encoding:'utf8',env:{...childEnv(),CAMOFOX_RELOCATION_CHILD:'1'},timeout:15000});assert.equal(r.status,0,r.stdout+r.stderr);}
    const r=cli({...request,unknown:true},{},cwd);assert.equal(JSON.parse(r.stdout).code,'UNKNOWN_REQUEST_KEY');
  }finally{await rm(temp,{recursive:true,force:true});}
});
test('export contains no legacy identifying literals or outside relative imports',async()=>{
  const visit=async dir=>{for(const entry of await readdir(dir,{withFileTypes:true})){const path=join(dir,entry.name);if(entry.isDirectory())await visit(path);else{
    const s=await readFile(path,'utf8');
    assert.ok(!/[0-9]{15,}/.test(s),entry.name+' real numeric identity');
    assert.ok(!/from ['"]\.\.\//.test(s),entry.name+' outside import');
    for(const match of s.matchAll(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g))assert.ok(match[0].endsWith('.example.invalid')||match[0].endsWith('@example.invalid'),entry.name+' non-fixture email');
    for(const match of s.matchAll(/https?:\/\/[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+/g)){
      const host=new URL(match[0]).hostname;
      assert.ok(host==='localhost'||host==='127.0.0.1'||host==='example.invalid'||host.endsWith('.example.invalid'),entry.name+' non-fixture host');
    }
  }}};await visit(skill);
});

test('supported synthetic runtime imports fixed contract and enforces loopback config',async()=>{
  const temp=await mkdtemp(join(tmpdir(),'runtime-'));
  try{
    await mkdir(join(temp,'mcp','lib'),{recursive:true});await mkdir(join(temp,'lib'));
    await writeFile(join(temp,'package.json'),JSON.stringify({name:'@askjo/camofox-browser',version:'1.18.1',type:'module'}));
    await writeFile(join(temp,'lib','config.js'),'export const loadConfig=()=>({});');
    await writeFile(join(temp,'mcp','lib','tool-contracts.mjs'),'export async function runTool(name,args,ctx,url){return {payload:name==="camofox_evaluate"?{ok:true,result:{top:true,count:0}}:{ok:true}};}');
    const configPath=join(temp,'config.json');
    const args={runtimePath:temp,configPath,userId:'AGENT',sessionKey:'agent:AGENT:CONTEXT'};
    const config=async settings=>writeFile(configPath,JSON.stringify({plugins:{entries:{'camofox-browser':{config:settings}}}}));
    for(const url of ['https://remote.example.invalid','http://localhost/path','http://u:p@localhost','http://localhost/?query','http://localhost/#fragment']){
      await config({url});await assert.rejects(createBrowser(args),{code:'UNSAFE_CAMOFOX_ENDPOINT'});
    }
    await config({});await assert.rejects(createBrowser(args),{code:'CAMOFOX_URL_MISSING'});
    await writeFile(configPath,'{}');await assert.rejects(createBrowser(args),{code:'CAMOFOX_CONFIG_MISSING'});
    for(const settings of [{port:12345},{url:'http://127.0.0.1:12345'},{url:'http://[::1]:12345'}]){
      await config(settings);const browser=await createBrowser(args);assert.equal((await browser.inspect('tab','#input')).count,0);await browser.type('tab','#input','SYNTHETIC_MARKER');
    }
  }finally{await rm(temp,{recursive:true,force:true});}
});
