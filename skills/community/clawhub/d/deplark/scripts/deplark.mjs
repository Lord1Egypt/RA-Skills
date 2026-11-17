// Official, dependency-free Deplark Skill client. Credentials never enter bundles.
import {createHash, randomBytes, randomUUID} from 'node:crypto';
import {readFile, writeFile, mkdir, lstat, realpath, rename, rm, open, constants} from 'node:fs/promises';
import {resolve, join, dirname} from 'node:path';
import {homedir, tmpdir} from 'node:os';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';

export const sha256 = value => createHash('sha256').update(value).digest('hex');
const names = ['SKILL.md', 'deplark.json', 'scripts/deplark.mjs'];
const keyPattern = /^qd_skill_[A-Za-z0-9_-]{43}$/;
const accountKeyPattern = /^qd_account_[A-Za-z0-9_-]{43}$/;
const tools = ['codex', 'claude'];
function problem(code) { const error = new Error(code); error.code = code; return error; }
export function endpointOrigin(value = 'https://deplark.com') {
  const url = new URL(value);
  if (url.username || url.password || url.search || url.hash || url.pathname !== '/' ||
      (url.protocol !== 'https:' && !(url.protocol === 'http:' && ['127.0.0.1', '[::1]'].includes(url.hostname)))) throw problem('ENDPOINT_INVALID');
  return url.origin;
}
function clientName(value) { if (!tools.includes(value)) throw problem('SKILL_CLIENT_INVALID'); return value; }
function skillName(value) { if (typeof value !== 'string' || value.length > 64 || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value)) throw problem('SKILL_NAME_INVALID'); return value; }
export function bundleIdentity(project, hashes) { return sha256(JSON.stringify({project, hashes: Object.fromEntries(names.map(name => [name, hashes[name]]))})); }
export function accountBundleIdentity(hashes) {return sha256(JSON.stringify({account:true,hashes:Object.fromEntries(names.map(name=>[name,hashes[name]]))}));}
export function validateBundle(bundle) {
  const account=bundle?.schema===2&&bundle.scope==='account';
  if (!bundle || !account&&(bundle.schema !== 1 || !/^[a-f0-9-]{36}$/.test(bundle.project_id || '')) || !bundle.files || Object.keys(bundle.files).length !== 3) throw problem('SKILL_BUNDLE_INVALID');
  skillName(bundle.name);
  const hashes = {};
  for (const name of names) {
    if (typeof bundle.files[name] !== 'string' || Buffer.byteLength(bundle.files[name]) > 512 * 1024) throw problem('SKILL_BUNDLE_INVALID');
    hashes[name] = sha256(bundle.files[name]);
    if (hashes[name] !== bundle.hashes?.[name]) throw problem('SKILL_DIGEST_MISMATCH');
  }
  if ((account?accountBundleIdentity(hashes):bundleIdentity(bundle.project_id, hashes)) !== bundle.id) throw problem('SKILL_DIGEST_MISMATCH');
  let manifest; try { manifest = JSON.parse(bundle.files['deplark.json']); } catch { throw problem('SKILL_BUNDLE_INVALID'); }
  if ((account?(manifest.schema!==2||manifest.scope!=='account'||Object.hasOwn(manifest,'project_id')):(manifest.schema !== 1 || manifest.project_id !== bundle.project_id)) || manifest.name !== bundle.name ||
      !/^[a-f0-9]{64}$/.test(manifest.deploy_client_sha256 || '') ||
      !bundle.files['SKILL.md'].startsWith('---\nname: ' + bundle.name + '\n')) throw problem('SKILL_BUNDLE_INVALID');
  endpointOrigin(manifest.endpoint);
  return {manifest, hashes};
}
async function checkedDirectory(base, segments, create = false) {
  let cursor = await realpath(base);
  for (const segment of segments) {
    cursor = join(cursor, segment);
    if (create) await mkdir(cursor, {mode: 0o700}).catch(error => { if (error.code !== 'EEXIST') throw error; });
    const info = await lstat(cursor);
    if (!info.isDirectory() || info.isSymbolicLink()) throw problem('SKILL_PATH_UNSAFE');
  }
  return cursor;
}
export async function skillDirectory({agent, scope, name, cwd = process.cwd(), home = homedir(), create = false}) {
  clientName(agent); skillName(name);
  if (!['project', 'personal'].includes(scope)) throw problem('SKILL_SCOPE_INVALID');
  const parent = await checkedDirectory(scope === 'project' ? cwd : home, [agent === 'codex' ? '.agents' : '.claude', 'skills'], create);
  return join(parent, name);
}
async function readSafeFile(root, name) {
  const parts = name.split('/'); await checkedDirectory(root, parts.slice(0, -1));
  const file = await open(join(root, name), constants.O_RDONLY | constants.O_NOFOLLOW);
  try { const info = await file.stat(); if (!info.isFile() || info.size > 512 * 1024) throw problem('SKILL_FILE_INVALID'); return await file.readFile('utf8'); }
  finally { await file.close(); }
}
export async function inspectInstallation(options) {
  const directory = await skillDirectory(options), info = await lstat(directory);
  if (info.isSymbolicLink() || !info.isDirectory()) throw problem('SKILL_PATH_UNSAFE');
  const files = {}, hashes = {};
  for (const name of names) { files[name] = await readSafeFile(directory, name); hashes[name] = sha256(files[name]); }
  const manifest = JSON.parse(files['deplark.json']),account=manifest.scope==='account',id = account?accountBundleIdentity(hashes):bundleIdentity(manifest.project_id, hashes);
  validateBundle({schema: manifest.schema,scope:manifest.scope,id,name:manifest.name,project_id:manifest.project_id,hashes,files});
  if (manifest.name !== options.name) throw problem('SKILL_INSTALL_MISMATCH');
  return {directory, manifest, hashes, id, checks: {file: true, discovered: null}, discovery_source: 'user-confirmation-required'};
}
export async function installSkill(bundle, options) {
  validateBundle(bundle);
  const directory = await skillDirectory({...options, name: bundle.name, create: true});
  let existing; try { existing = await lstat(directory); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  if (existing?.isSymbolicLink() || existing && !existing.isDirectory()) throw problem('SKILL_PATH_UNSAFE');
  if(existing&&bundle.scope==='account'){
    try{const current=await inspectInstallation({...options,name:bundle.name});if(current.id===bundle.id)return {status:'already-installed',directory,backup:null,artifact_id:bundle.id,checks:{file:true,discovered:null}};}catch{}
  }
  if (existing && !(options.replace && options.backup)) throw problem('SKILL_EXISTS_USE_REPLACE_AND_BACKUP');
  const staging = join(dirname(directory), '.' + bundle.name + '.install-' + randomUUID());
  const backup = existing ? join(dirname(directory), '.' + bundle.name + '.backup-' + randomUUID()) : null;
  await mkdir(staging, {mode: 0o700}); let moved = false;
  try {
    await mkdir(join(staging, 'scripts'), {mode: 0o700});
    for (const name of names) await writeFile(join(staging, name), bundle.files[name], {flag: 'wx', mode: 0o600});
    if (backup) { await rename(directory, backup); moved = true; }
    try { await rename(staging, directory); }
    catch (error) { if (moved) await rename(backup, directory); throw error; }
    return {status: 'installed', directory, backup, artifact_id: bundle.id, checks: {file: true, discovered: null}};
  } finally { await rm(staging, {recursive: true, force: true}); }
}
export async function uninstallSkill(options) {
  const installed = await inspectInstallation(options);
  if (!options.confirm) throw problem('SKILL_UNINSTALL_REQUIRES_CONFIRM');
  const backup = join(dirname(installed.directory), '.' + options.name + '.removed-' + randomUUID());
  await rename(installed.directory, backup);
  return {status: 'uninstalled', backup, authorization: 'unchanged', cloud_project: 'unchanged'};
}
function nativeCommand(binary, args, input, timeoutMs = 60000) {
  return new Promise((resolveResult, reject) => {
    const child = spawn(binary, args, {stdio: ['pipe', 'pipe', 'pipe']}); let output = '', finished = false;
    const timer = setTimeout(() => { child.kill('SIGTERM'); reject(problem('LOCAL_CLIENT_TIMEOUT')); }, timeoutMs);
    child.stdout.on('data', data => { if (output.length < 16384) output += data.toString(); });
    child.stderr.on('data', () => {}); // Native diagnostics can contain sensitive arguments.
    child.on('error', () => { clearTimeout(timer); if (!finished) { finished = true; reject(problem('LOCAL_CLIENT_UNAVAILABLE')); } });
    child.on('close', code => { clearTimeout(timer); if (!finished) { finished = true; code === 0 ? resolveResult(output) : reject(problem('KEYCHAIN_UNAVAILABLE')); } });
    child.stdin.on('error', () => {}); child.stdin.end(input || '');
  });
}
export function keychainStore({origin, project, agent, accountScope=false, run = nativeCommand, keychain = null} = {}) {
  const account = sha256(endpointOrigin(origin) + '\n' + (accountScope?'account':project) + '\n' + clientName(agent)), service = accountScope?'com.deplark.account-skills':'com.deplark.skills';
  const pattern=accountScope?accountKeyPattern:keyPattern;
  // A custom keychain is only an injected test destination; never alter the search list.
  if (keychain && /[\r\n"\\]/.test(keychain)) throw problem('KEYCHAIN_PATH_INVALID');
  const suffix = keychain ? ` "${keychain}"` : '';
  return {
    async get() {
      try { const value = (await run('/usr/bin/security', ['find-generic-password', '-a', account, '-s', service, '-w', ...(keychain ? [keychain] : [])])).trim(); return pattern.test(value) ? value : null; }
      catch (error) { if (error.code === 'LOCAL_CLIENT_TIMEOUT') throw error; return null; }
    },
    async set(token) {
      if (!pattern.test(token)) throw problem('SKILL_KEY_INVALID');
      // security -i reads commands on stdin. The password never appears in argv.
      await run('/usr/bin/security', ['-i'], `add-generic-password -U -a ${account} -s ${service} -w ${token}${suffix}\n`);
      // Interactive security may exit zero after a failed command; verify the write.
      const saved = await this.get(); if (saved !== token) throw problem('KEYCHAIN_SAVE_FAILED');
    },
    async delete() { try { await run('/usr/bin/security', ['delete-generic-password', '-a', account, '-s', service, ...(keychain ? [keychain] : [])]); } catch {} },
  };
}
function safeConnection(value) {
  if (!value || !/^[a-f0-9-]{36}$/.test(value.id || '') || !tools.includes(value.client) || !Array.isArray(value.permissions)) throw problem('CLIENT_RESPONSE_INVALID');
  return {id: value.id, account: String(value.account || ''), project_id: value.project_id, client: value.client,
    workspace_id: value.workspace_id, permissions: value.permissions.filter(p => ['project:read', 'deployment:read', 'deployment:create'].includes(p)), expires_at: value.expires_at, status: value.status};
}
export function createSkillClient({origin, project, agent, store, fetchImpl = fetch, apiKey, sleep = ms => new Promise(r => setTimeout(r, ms))}) {
  origin = endpointOrigin(origin); clientName(agent);
  if (!/^[a-f0-9-]{36}$/.test(project || '')) throw problem('SKILL_PROJECT_INVALID');
  async function call(path, {token, method = 'GET', body} = {}) {
    let response;
    try { response = await fetchImpl(new URL(path, origin), {method, redirect: 'error', signal: AbortSignal.timeout(30000),
      headers: {...(token ? {Authorization: 'Bearer ' + token} : {}), ...(body ? {'Content-Type': 'application/json'} : {})}, ...(body ? {body: JSON.stringify(body)} : {})}); }
    catch { throw problem('SKILL_NETWORK_UNAVAILABLE'); }
    let data; try { data = await response.json(); } catch { throw problem('CLIENT_RESPONSE_INVALID'); }
    if (!response.ok) {
      const code = /^[A-Z0-9_]{1,80}$/.test(data.error?.code || '') ? data.error.code : 'SKILL_REQUEST_FAILED';
      const error = problem(code); error.status = response.status; throw error;
    }
    return data;
  }
  async function tokenFor() { const token = apiKey || await store.get(); if (!keyPattern.test(token || '')) throw problem('NO_LOCAL_AUTHORIZATION'); return token; }
  async function projectInfo(token) {
    const info = await call('/api/agent/project', {token});
    if (info.project?.id !== project || info.connection?.project_id !== project || info.connection?.client !== agent) throw problem('SKILL_PROJECT_OR_CLIENT_MISMATCH');
    return {...info, connection: safeConnection(info.connection)};
  }
  async function attach(token, verification) {
    const info = await projectInfo(token);
    if (verification) await call('/api/agent/skill-verifications/' + verification + '/connection', {token, method: 'POST', body: {}});
    return {status: 'connected', connection: info.connection};
  }
  return {
    async status() { return {connection: (await projectInfo(await tokenFor())).connection}; },
    async connectExisting(token, verification) {
      if (!keyPattern.test(token || '')) throw problem('SKILL_KEY_INVALID');
      const info = await projectInfo(token);
      await store.set(token);
      if (verification) await call('/api/agent/skill-verifications/' + verification + '/connection', {token, method: 'POST', body: {}});
      return {status: 'connected', connection: info.connection};
    },
    async connectSaved(verification) { return attach(await tokenFor(), verification); },
    async connectBrowser({verification, onAuthorization, signal, maximumMs = 300000} = {}) {
      const verifier = randomBytes(32).toString('base64url'), challenge = createHash('sha256').update(verifier).digest('base64url');
      const start = await call('/api/skill-auth/start', {method: 'POST', body: {project_id: project, client: agent, challenge}});
      const url = new URL(start.verification_url);
      if (url.origin !== origin || url.pathname !== '/app' || url.searchParams.get('skill_connect') !== start.request_id) throw problem('CLIENT_RESPONSE_INVALID');
      await onAuthorization?.({url: url.href, expires_at: start.expires_at});
      const until = Math.min(Date.now() + maximumMs, start.expires_at);
      while (Date.now() < until) {
        if (signal?.aborted) throw problem('SKILL_AUTH_CANCELLED');
        const response = await call('/api/skill-auth/token', {method: 'POST', body: {request_id: start.request_id, verifier}});
        if (response.status === 'connected') {
          if (!keyPattern.test(response.token || '')) throw problem('CLIENT_RESPONSE_INVALID');
          return this.connectExisting(response.token, verification);
        }
        if (response.status !== 'pending') throw problem('CLIENT_RESPONSE_INVALID');
        await sleep(3000);
      }
      throw problem('SKILL_AUTH_EXPIRED');
    },
    async check(installation, verification, scope) {
      const token = await tokenFor(), info = await projectInfo(token);
      if (installation.manifest.project_id !== project || endpointOrigin(installation.manifest.endpoint) !== origin) throw problem('SKILL_INSTALL_MISMATCH');
      const result = await call('/api/agent/skill-verifications/' + verification + '/check', {token, method: 'POST', body: {artifact_id: installation.id, scope, hashes: installation.hashes}});
      return {status: 'checked', artifact_id: installation.id, connection: info.connection, checks: result.checks,
        api: {method: 'GET', path: '/api/agent/project', status: 200}, discovery_source: 'user-confirmation-required'};
    },
    async deploymentGrant() {
      const token = await tokenFor(), info = await projectInfo(token);
      if (!info.connection.permissions.includes('deployment:create')) throw problem('SKILL_PERMISSION_REQUIRED');
      const grant = await call('/api/agent/grants', {token, method: 'POST', body: {project_id: project}});
      if (!/^qd_deploy_[A-Za-z0-9_-]{43}$/.test(grant.token || '') || grant.project_id !== project) throw problem('CLIENT_RESPONSE_INVALID');
      return grant;
    },
    async disconnect() { await store.delete(); return {status: 'disconnected', cloud_authorization: 'not-revoked', skill: 'retained'}; },
  };
}
// Short-lived PKCE state stays outside repositories and Skills, never in argv or logs.
export function pendingAccountAuthorization({origin,agent,home=homedir()}){
  origin=endpointOrigin(origin);clientName(agent);
  const filename=sha256(origin+'\n'+agent)+'.json';
  async function directory(create=false){return checkedDirectory(home,['.config','deplark','authorization'],create);}
  return {
    async get(){
      let file;try{file=await open(join(await directory(),filename),constants.O_RDONLY|constants.O_NOFOLLOW);}catch(error){if(error.code==='ENOENT')return null;throw problem('SKILL_AUTH_STATE_UNAVAILABLE');}
      try{const stat=await file.stat();if(!stat.isFile()||stat.size>8192||(stat.mode&0o077)||process.getuid&&stat.uid!==process.getuid())throw problem('SKILL_AUTH_STATE_UNAVAILABLE');
        const row=JSON.parse(await file.readFile('utf8'));
        if(row.origin!==origin||row.agent!==agent||!/^[A-Za-z0-9_-]{32}$/.test(row.request_id||'')||!/^[A-Za-z0-9_-]{43}$/.test(row.verifier||'')||!Number.isFinite(row.expires_at))throw problem('SKILL_AUTH_STATE_UNAVAILABLE');
        return row;
      }finally{await file.close();}
    },
    async set(row){
      const dir=await directory(true),path=join(dir,filename),temporary=join(dir,'.pending-'+randomUUID());
      try{await writeFile(temporary,JSON.stringify(row),{flag:'wx',mode:0o600});await rename(temporary,path);}finally{await rm(temporary,{force:true});}
    },
    async delete(){try{await rm(join(await directory(),filename),{force:true});}catch(error){if(error.code!=='ENOENT')throw error;}}
  };
}
export function createAccountSkillClient({origin,agent,store,pendingStore,fetchImpl=fetch,apiKey,sleep=ms=>new Promise(r=>setTimeout(r,ms))}){
  origin=endpointOrigin(origin);clientName(agent);
  async function call(path,{token,method='GET',body}={}){
    let r;try{r=await fetchImpl(new URL(path,origin),{method,redirect:'error',signal:AbortSignal.timeout(30000),headers:{...(token?{Authorization:'Bearer '+token}:{}),...(body?{'Content-Type':'application/json'}:{})},...(body?{body:JSON.stringify(body)}:{})});}catch{throw problem('SKILL_NETWORK_UNAVAILABLE');}
    let data;try{data=await r.json();}catch{throw problem('CLIENT_RESPONSE_INVALID');}if(!r.ok){const error=problem(/^[A-Z0-9_]{1,80}$/.test(data.error?.code||'')?data.error.code:'SKILL_REQUEST_FAILED');error.status=r.status;throw error;}return data;
  }
  async function tokenFor(){const token=apiKey||await store.get();if(!accountKeyPattern.test(token||''))throw problem(keyPattern.test(token||'')?'ACCOUNT_KEY_REQUIRED_PROJECT_KEY_IS_SCOPED':'NO_LOCAL_AUTHORIZATION');return token;}
  async function info(token){const data=await call('/api/agent/account',{token}),c=data.connection;if(c?.scope!=='account'||c.client!==agent||c.workspace_id!==data.account?.id||!/^[a-f0-9-]{36}$/.test(c.id||'')||!/^[a-f0-9-]{36}$/.test(data.account?.id||'')||!Array.isArray(c.permissions)||c.status!=='active')throw problem('ACCOUNT_OR_CLIENT_MISMATCH');
    return {account:{id:data.account.id,email:String(data.account.email||'')},connection:{id:c.id,scope:'account',account:String(c.account||''),workspace_id:c.workspace_id,client:c.client,status:c.status,expires_at:c.expires_at,permissions:c.permissions.filter(p=>['projects:read','deployment:read','project:create','deployment:create'].includes(p))}};}
  async function attach(token,verification){const data=await info(token);if(verification)await call('/api/agent/account-skill-verifications/'+verification+'/connection',{token,method:'POST',body:{}});return {status:'connected',...data};}
  async function start(verification){
    const verifier=randomBytes(32).toString('base64url'),result=await call('/api/account-skill/auth/start',{method:'POST',body:{client:agent,challenge:createHash('sha256').update(verifier).digest('base64url'),...(verification?{verification_id:verification}:{})}});
    let url;try{url=new URL(result.verification_url);}catch{throw problem('CLIENT_RESPONSE_INVALID');}
    if(url.origin!==origin||url.username||url.password||url.pathname!=='/app'||url.searchParams.get('account_skill_connect')!==result.request_id||!/^[A-Za-z0-9_-]{32}$/.test(result.request_id||'')||!Number.isFinite(result.expires_at)||result.expires_at<=Date.now()||result.expires_at>Date.now()+360000)throw problem('CLIENT_RESPONSE_INVALID');
    return {origin,agent,request_id:result.request_id,verifier,expires_at:result.expires_at,verification,authorization_url:url.href};
  }
  function pendingView(row){return {status:'authorization-required',authorization_url:new URL('/app?account_skill_connect='+row.request_id,origin).href,expires_at:row.expires_at,consent_required:true,next_action:'Open the authorization URL with your browser tools, review the account and permissions with the user, then run connect --resume. Never ask for a Key on the webpage. Do not wait in a blocking command.'};}
  async function exchange(row,verification=row.verification){
    if(row.expires_at<=Date.now())throw problem('SKILL_AUTH_EXPIRED');
    const result=await call('/api/account-skill/auth/token',{method:'POST',body:{request_id:row.request_id,verifier:row.verifier}});
    if(result.status==='pending')return {...pendingView(row),status:'pending'};
    if(result.status!=='connected'||!accountKeyPattern.test(result.token||''))throw problem('CLIENT_RESPONSE_INVALID');
    await info(result.token);await store.set(result.token);
    // Retain the valid connection even if a separate webpage check has expired.
    if(pendingStore)await pendingStore.delete();
    return {...await attach(result.token,verification),authorization_source:'browser'};
  }
  return {
    async status(){return info(await tokenFor());},
    async connectSaved(verification){return attach(await tokenFor(),verification);},
    async connectExisting(token,verification){if(!accountKeyPattern.test(token||''))throw problem('ACCOUNT_KEY_REQUIRED_PROJECT_KEY_IS_SCOPED');const data=await attach(token,verification);await store.set(token);return data;},
    async startBrowser({verification}={}){
      if(!pendingStore)throw problem('SKILL_AUTH_STATE_UNAVAILABLE');
      let row=await pendingStore.get();if(row?.expires_at<=Date.now()){await pendingStore.delete();row=null;}
      if(!row){row=await start(verification);await pendingStore.set(row);}
      return pendingView(row);
    },
    async resumeBrowser({verification}={}){
      if(!pendingStore)throw problem('SKILL_AUTH_STATE_UNAVAILABLE');const row=await pendingStore.get();if(!row)throw problem('SKILL_AUTH_NO_PENDING_REQUEST');
      try{return await exchange(row,verification||row.verification);}catch(error){if(['SKILL_AUTH_EXPIRED','SKILL_AUTH_DENIED','SKILL_AUTH_USED'].includes(error.code))await pendingStore.delete();throw error;}
    },
    async connectBrowser({verification,onAuthorization=()=>{},signal,maximumMs=300000}={}){
      const row=await start(verification),until=Math.min(Date.now()+maximumMs,row.expires_at);await onAuthorization({url:row.authorization_url,expires_at:row.expires_at});
      while(Date.now()<until){if(signal?.aborted)throw problem('SKILL_AUTH_CANCELLED');const result=await exchange(row);if(result.status==='connected')return result;await sleep(3000);}throw problem('SKILL_AUTH_EXPIRED');
    },
    async projects(){const token=await tokenFor();await info(token);const data=await call('/api/agent/projects',{token});if(!Array.isArray(data.projects)||data.projects.some(p=>!/^[a-f0-9-]{36}$/.test(p.id||'')||!['node','static'].includes(p.kind)))throw problem('CLIENT_RESPONSE_INVALID');return data;},
    async project(id){if(!/^[a-f0-9-]{36}$/.test(id||''))throw problem('SKILL_PROJECT_INVALID');const token=await tokenFor();await info(token);const data=await call('/api/agent/projects/'+id,{token});if(data.project?.id!==id)throw problem('CLIENT_RESPONSE_INVALID');return data;},
    async createProject(body){const token=await tokenFor(),data=await info(token);if(!data.connection.permissions.includes('project:create'))throw problem('ACCOUNT_SKILL_PERMISSION_REQUIRED');return call('/api/agent/projects',{token,method:'POST',body});},
    async deploymentGrant(project,account){const token=await tokenFor(),data=await info(token);if(data.account.id!==account)throw problem('PROJECT_BINDING_ACCOUNT_MISMATCH');if(!data.connection.permissions.includes('deployment:create'))throw problem('ACCOUNT_SKILL_PERMISSION_REQUIRED');const result=await call('/api/agent/grants',{token,method:'POST',body:{project_id:project}});if(!/^qd_deploy_[A-Za-z0-9_-]{43}$/.test(result.token||'')||result.project_id!==project)throw problem('CLIENT_RESPONSE_INVALID');return result;},
    async check(installed,verification,scope){
      if(installed.manifest.scope!=='account'||endpointOrigin(installed.manifest.endpoint)!==origin)throw problem('ACCOUNT_SKILL_INSTALL_REQUIRED');
      const token=await tokenFor(),data=await info(token);await this.projects();
      if(verification)return call('/api/agent/account-skill-verifications/'+verification+'/check',{token,method:'POST',body:{artifact_id:installed.id,scope,hashes:installed.hashes}});
      return {status:'checked',...data,artifact_id:installed.id,scope,checks:{file:true,api:true,authorization:true,deployment_permission:data.connection.permissions.includes('deployment:create'),create_permission:data.connection.permissions.includes('project:create'),discovered:null},discovery_source:'user-confirmation-required'};
    },
    async disconnect(){await store.delete();return {status:'disconnected',cloud_authorization:'not-revoked',skill:'retained'};}
  };
}
export async function readProjectBinding({cwd=process.cwd()}={}){
  let root;try{root=await checkedDirectory(cwd,['.deplark']);}catch(error){if(error.code==='ENOENT')return null;throw error;}
  let text;try{text=await readSafeFile(root,'project.json');}catch(error){if(error.code==='ENOENT')return null;throw error;}
  let row;try{row=JSON.parse(text);}catch{throw problem('PROJECT_BINDING_INVALID');}
  if(row.schema!==1||!/^[a-f0-9-]{36}$/.test(row.account_id||'')||!/^[a-f0-9-]{36}$/.test(row.project_id||'')||!['node','static'].includes(row.kind))throw problem('PROJECT_BINDING_INVALID');endpointOrigin(row.origin);return row;
}
export async function bindAccountProject({origin,account,project,cwd=process.cwd(),replace=false}){
  origin=endpointOrigin(origin);if(!/^[a-f0-9-]{36}$/.test(account||'')||!/^[a-f0-9-]{36}$/.test(project.id||''))throw problem('PROJECT_BINDING_INVALID');
  const root=await checkedDirectory(cwd,['.deplark'],true),lockPath=join(root,'.project.lock');let lock;try{lock=await open(lockPath,constants.O_CREAT|constants.O_EXCL|constants.O_WRONLY|constants.O_NOFOLLOW,0o600);}catch(error){if(error.code==='EEXIST')throw problem('PROJECT_BINDING_BUSY');throw error;}
  let temporary;try{const before=await readProjectBinding({cwd});if(before&&(before.account_id!==account||before.origin!==origin||before.project_id!==project.id)&&!replace)throw problem('PROJECT_BINDING_EXISTS_USE_REPLACE');
    let backup=null;if(before&&replace){backup=join(root,'project.backup-'+randomUUID()+'.json');await writeFile(backup,JSON.stringify(before,null,2)+'\n',{flag:'wx',mode:0o600});}
    const row={schema:1,origin,account_id:account,project_id:project.id,project_name:String(project.name||''),kind:project.kind};temporary=join(root,'.project-'+randomUUID()+'.json');await writeFile(temporary,JSON.stringify(row,null,2)+'\n',{flag:'wx',mode:0o600});await rename(temporary,join(root,'project.json'));return {status:'linked',binding:row,backup};
  }finally{await lock.close();await rm(lockPath,{force:true});if(temporary)await rm(temporary,{force:true});}
}
async function uploadWithGrant(origin,manifest,grant,output){
  const response=await fetch(new URL('/deploy.mjs',origin),{redirect:'error',signal:AbortSignal.timeout(30000)});if(!response.ok)throw problem('DEPLOY_CLIENT_UNAVAILABLE');const source=await response.text();if(sha256(source)!==manifest.deploy_client_sha256)throw problem('DEPLOY_CLIENT_CHANGED_REGENERATE_SKILL');
  const {mkdtemp}=await import('node:fs/promises'),temporary=await mkdtemp(join(tmpdir(),'deplark-upload-'));
  try{const file=join(temporary,'deploy.mjs');await writeFile(file,source,{mode:0o600});const code=await new Promise((done,reject)=>{const child=spawn(process.execPath,[file,'--dir',output,'--endpoint',origin],{stdio:['ignore','inherit','inherit'],env:{...process.env,DEPLARK_API_KEY:'',DEPLARK_DEPLOY_TOKEN:grant.token}});child.on('error',()=>reject(problem('DEPLOY_CLIENT_UNAVAILABLE')));child.on('close',done);});if(code!==0)throw problem('DEPLOYMENT_FAILED');return {status:'deployment-client-completed',project_id:grant.project_id};}finally{await rm(temporary,{recursive:true,force:true});}
}
async function runAccountCLI(command,flags,{origin,agent,scope,manifest,name,runtime={}}){
  const store=runtime.store||(process.platform==='darwin'?keychainStore({origin,agent,accountScope:true}):{get:async()=>process.env.DEPLARK_API_KEY||null,set:async value=>{if(value!==process.env.DEPLARK_API_KEY)throw problem('KEYCHAIN_UNAVAILABLE_USE_DEPLARK_API_KEY');},delete:async()=>{}});
  const client=createAccountSkillClient({origin,agent,store,pendingStore:pendingAccountAuthorization({origin,agent,home:runtime.home}),apiKey:runtime.apiKey??process.env.DEPLARK_API_KEY});
  if(command==='status')return client.status();if(command==='projects')return client.projects();if(command==='disconnect')return client.disconnect();
  if(command==='connect'){
    if(['--api-key','--browser','--resume'].filter(flag=>flags[flag]).length>1)throw problem('CHOOSE_ONE_AUTH_METHOD');
    if(flags['--api-key'])return {...await client.connectExisting(await secretInput(),flags['--verification']),authorization_source:'existing-key'};
    if(flags['--resume'])return client.resumeBrowser({verification:flags['--verification']});
    if(!flags['--browser'])try{return {...await client.connectSaved(flags['--verification']),authorization_source:'saved-key'};}catch(error){if(!['NO_LOCAL_AUTHORIZATION','ACCOUNT_SKILL_KEY_INVALID'].includes(error.code))throw error;}
    if(process.platform!=='darwin')throw problem('KEYCHAIN_UNAVAILABLE_USE_DEPLARK_API_KEY');
    const result=await client.startBrowser({verification:flags['--verification']});
    if(!flags['--no-open']){const child=spawn('/usr/bin/open',[result.authorization_url],{stdio:'ignore'});child.on('error',()=>{});child.unref();}
    return result;
  }
  if(command==='check'){if(flags['--verification']&&!/^[A-Za-z0-9_-]{32}$/.test(flags['--verification']))throw problem('SKILL_VERIFICATION_MISSING');return client.check(await inspectInstallation({agent,scope,name,home:runtime.home}),flags['--verification'],scope);}
  const account=await client.status();
  if(command==='create-project'){
    if(await readProjectBinding())throw problem('PROJECT_ALREADY_LINKED_CREATE_REFUSED');const data=await client.createProject({name:flags['--name'],slug:flags['--slug'],kind:flags['--kind']||'static',entry:flags['--entry']||'server.mjs'});
    try{return {...await bindAccountProject({origin,account:account.account.id,project:data.project}),project:data.project};}catch(error){return {status:'project-created-link-required',project:data.project,link_error:error.code||'PROJECT_BINDING_FAILED'};}
  }
  if(command==='link'){const data=await client.project(flags['--project']);return bindAccountProject({origin,account:account.account.id,project:data.project,replace:flags['--replace']});}
  const binding=await readProjectBinding();if(!binding)throw problem('CHOOSE_NEW_OR_EXISTING_PROJECT_FIRST');if(binding.origin!==origin||binding.account_id!==account.account.id)throw problem('PROJECT_BINDING_ACCOUNT_MISMATCH');const target=await client.project(binding.project_id);
  if(command==='target')return {account:account.account,project:target.project,binding};
  if(command==='deploy'){if(!flags['--dir']||!manifest)throw problem('DEPLOY_REQUIRES_INSTALLED_SKILL_AND_OUTPUT');return uploadWithGrant(origin,manifest,await client.deploymentGrant(binding.project_id,binding.account_id),flags['--dir']);}
  throw problem('SKILL_COMMAND_INVALID');
}
async function secretInput() {
  if (process.env.DEPLARK_API_KEY) return process.env.DEPLARK_API_KEY;
  if (!process.stdin.isTTY) {
    let value = ''; for await (const chunk of process.stdin) { value += chunk; if (value.length > 1024) throw problem('SKILL_KEY_INVALID'); } return value.trim();
  }
  process.stderr.write('Deplark API Key (hidden): '); process.stdin.setRawMode(true); process.stdin.resume();
  try {
    return await new Promise((done, reject) => {
      let value = '';
      const onData = chunk => {
        for (const char of chunk.toString()) {
          if (char === '\u0003') { cleanup(); reject(problem('SKILL_AUTH_CANCELLED')); return; }
          if (char === '\r' || char === '\n') { cleanup(); done(value); return; }
          if (char === '\u007f' || char === '\b') value = value.slice(0, -1);
          else if (char >= ' ' && value.length < 1024) value += char;
        }
      };
      function cleanup() { process.stdin.removeListener('data', onData); }
      process.stdin.on('data', onData);
    });
  } finally { process.stdin.setRawMode(false); process.stdin.pause(); process.stderr.write('\n'); }
}
export async function runSkillCLI(args = process.argv.slice(2),runtime={}) {
  const command = args.shift(), flags = {}, boolean = ['--api-key', '--browser', '--resume', '--replace', '--backup', '--confirm', '--no-open','--account'];
  const values = ['--bundle', '--agent', '--scope', '--name', '--endpoint', '--project', '--verification', '--dir','--slug','--kind','--entry'];
  for (let i = 0; i < args.length; i++) {
    const key = args[i]; if (Object.hasOwn(flags, key)) throw problem('DUPLICATE_OPTION');
    if (boolean.includes(key)) flags[key] = true;
    else if (values.includes(key) && args[i + 1] && !args[i + 1].startsWith('--')) flags[key] = args[++i];
    else throw problem('Usage: install --bundle FILE --agent codex|claude --scope project|personal; connect [--browser|--api-key]; status; check --verification ID; deploy --dir OUTPUT; disconnect; uninstall --confirm');
  }
  const agent = clientName(flags['--agent'] || 'codex');let scope = flags['--scope'] || 'project';
  if (command === 'install') {
    const bundle = JSON.parse(await readFile(resolve(flags['--bundle']), 'utf8'));
    return installSkill(bundle, {agent, scope:flags['--scope']||(bundle.scope==='account'?'personal':'project'), home:runtime.home,replace: flags['--replace'], backup: flags['--backup']});
  }
  const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
  let manifest; try { manifest = JSON.parse(await readFile(join(root, 'deplark.json'), 'utf8')); } catch {}
  const origin = endpointOrigin(flags['--endpoint'] || manifest?.endpoint), project = flags['--project'] || manifest?.project_id;
  const name = flags['--name'] || manifest?.name;
  const account=manifest?.scope==='account'||flags['--account'];if(account&&!flags['--scope'])scope='personal';
  if (command === 'uninstall') return uninstallSkill({agent, scope, name, confirm: flags['--confirm']});
  if(account)return runAccountCLI(command,flags,{origin,agent,scope,manifest,name,runtime});
  const store = process.platform === 'darwin' ? keychainStore({origin, project, agent}) : {
    async get() { return process.env.DEPLARK_API_KEY || null; },
    async set(value) { if (value !== process.env.DEPLARK_API_KEY) throw problem('KEYCHAIN_UNAVAILABLE_USE_DEPLARK_API_KEY'); }, async delete() {},
  };
  const client = createSkillClient({origin, project, agent, store, apiKey: process.env.DEPLARK_API_KEY});
  if (command === 'connect') {
    if (flags['--api-key'] && flags['--browser']) throw problem('CHOOSE_ONE_AUTH_METHOD');
    if (flags['--api-key']) return client.connectExisting(await secretInput(), flags['--verification']);
    if (!flags['--browser']) return client.connectSaved(flags['--verification']);
    if (process.platform !== 'darwin') throw problem('KEYCHAIN_UNAVAILABLE_USE_DEPLARK_API_KEY');
    return client.connectBrowser({verification: flags['--verification'], onAuthorization: async ({url}) => {
      process.stderr.write('Confirm account and project permissions: ' + url + '\n');
      if (!flags['--no-open']) { const child = spawn('/usr/bin/open', [url], {stdio: 'ignore'}); child.on('error', () => {}); child.unref(); }
    }});
  }
  if (command === 'status') return client.status();
  if (command === 'disconnect') return client.disconnect();
  if (command === 'check') {
    if (!/^[A-Za-z0-9_-]{32}$/.test(flags['--verification'] || '')) throw problem('SKILL_VERIFICATION_MISSING');
    return client.check(await inspectInstallation({agent, scope, name}), flags['--verification'], scope);
  }
  if (command === 'deploy') {
    if (!flags['--dir'] || !manifest) throw problem('DEPLOY_REQUIRES_INSTALLED_SKILL_AND_OUTPUT');
    const grant = await client.deploymentGrant();
    const response = await fetch(new URL('/deploy.mjs', origin), {redirect: 'error', signal: AbortSignal.timeout(30000)});
    if (!response.ok) throw problem('DEPLOY_CLIENT_UNAVAILABLE');
    const source = await response.text(); if (sha256(source) !== manifest.deploy_client_sha256) throw problem('DEPLOY_CLIENT_CHANGED_REGENERATE_SKILL');
    const {mkdtemp} = await import('node:fs/promises'), temporary = await mkdtemp(join(tmpdir(), 'deplark-upload-'));
    try {
      const file = join(temporary, 'deploy.mjs'); await writeFile(file, source, {mode: 0o600});
      const code = await new Promise((done, reject) => {
        const child = spawn(process.execPath, [file, '--dir', flags['--dir'], '--endpoint', origin],
          {stdio: ['ignore', 'inherit', 'inherit'], env: {...process.env, DEPLARK_API_KEY: '', DEPLARK_DEPLOY_TOKEN: grant.token}});
        child.on('error', () => reject(problem('DEPLOY_CLIENT_UNAVAILABLE'))); child.on('close', done);
      });
      if (code !== 0) throw problem('DEPLOYMENT_FAILED');
      return {status: 'deployment-client-completed', project_id: project};
    } finally { await rm(temporary, {recursive: true, force: true}); }
  }
  throw problem('SKILL_COMMAND_INVALID');
}
const entryPath=process.argv[1]&&await realpath(process.argv[1]).catch(()=>null);
if (entryPath && import.meta.url === pathToFileURL(entryPath).href) {
  runSkillCLI().then(result => console.log(JSON.stringify(result))).catch(error => { console.error(error.code || 'LOCAL_CLIENT_FAILED'); process.exitCode = 1; });
}
