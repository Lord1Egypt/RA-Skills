import {readFile,mkdir,writeFile,chmod} from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {getPlatform} from './platforms.mjs';

const fail=code=>Object.assign(new Error(code),{code});
export const defaultConfigPath=()=>path.join(os.homedir(),'.config','easybr-search','config.json');
export const defaultConfig=()=>({schemaVersion:1,platforms:['baidu','google'],browserMap:{},limit:5,read:3,timeoutMs:18000,concurrency:3});
export function validateBrowserMap(value){
 if(!value||Array.isArray(value)||typeof value!=='object')throw fail('invalid_browser_map');
 for(const [key,name] of Object.entries(value)){
  if(key!=='*'&&getPlatform(key).id!==key)throw fail('invalid_browser_map_platform');
  if(typeof name!=='string'||!name.trim()||name.length>200)throw fail('invalid_browser_map');
 }
 return value;
}
export function validateConfig(value){
 if(!value||Array.isArray(value)||typeof value!=='object')throw fail('invalid_config');
 const defaults=defaultConfig();
 if(Object.keys(value).some(k=>!Object.hasOwn(defaults,k)))throw fail('unknown_config_field');
 if(value.schemaVersion!==undefined&&value.schemaVersion!==1)throw fail('unsupported_config_version');
 const merged={...defaults,...value};
 if(!Array.isArray(merged.platforms)||!merged.platforms.length||merged.platforms.length>20)throw fail('invalid_platforms');
 merged.platforms=[...new Set(merged.platforms.map(id=>getPlatform(id).id))];
 validateBrowserMap(merged.browserMap);
 for(const [key,low,high] of [['limit',1,20],['read',0,10],['timeoutMs',2000,60000],['concurrency',1,4]]){
  if(!Number.isInteger(merged[key])||merged[key]<low||merged[key]>high)throw fail('invalid_'+key);
 }
 return merged;
}
export async function loadConfig(file,{optional=false}={}){
 try{return validateConfig(JSON.parse(await readFile(path.resolve(file),'utf8')))}
 catch(e){if(optional&&e.code==='ENOENT')return defaultConfig();if(e.code==='ENOENT')throw fail('config_not_found');if(e instanceof SyntaxError)throw fail('config_invalid_json');throw e}
}
export async function resolveOptions(options){
 const file=options.configFile||defaultConfigPath();
 const saved=await loadConfig(file,{optional:!options.configFile});
 // Explicit scope replaces the saved scope; it is never expanded or used as a fallback list.
 const resolved={...saved,...options,platforms:options.platforms??saved.platforms};
 if(options.browserMapFile){
  try{resolved.browserMap=validateBrowserMap(JSON.parse(await readFile(path.resolve(options.browserMapFile),'utf8')))}
  catch(e){if(e.code==='ENOENT')throw fail('browser_map_not_found');if(e instanceof SyntaxError)throw fail('browser_map_invalid_json');throw e}
 }
 return resolved;
}
export async function initConfig(file=defaultConfigPath()){
 const target=path.resolve(file);await mkdir(path.dirname(target),{recursive:true,mode:0o700});
 try{await writeFile(target,JSON.stringify(defaultConfig(),null,2)+'\n',{mode:0o600,flag:'wx'})}
 catch(e){if(e.code==='EEXIST')throw fail('config_already_exists');throw e}
 await chmod(target,0o600);return target;
}
