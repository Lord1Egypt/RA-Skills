import {Bridge} from './bridge.mjs';
import {getPlatform} from './platforms.mjs';
import {inventory,selectBrowser,safeCode,backgroundCapability} from './runtime.mjs';
export function errorHint(code){return ({bridge_token_missing:'先安装并启动 Easy WebBridge 本机服务，连接浏览器扩展。',bridge_unreachable:'检查 Easy WebBridge 本机服务与扩展连接，再运行 doctor。',no_online_browser:'连接至少一个浏览器扩展，然后运行 browsers 或 doctor。',configured_browser_not_unique_or_online:'核对私有 browserMap 中的环境是否唯一且在线，程序不会替换账号。',config_not_found:'检查 --config 路径，或用 config init 创建自己的配置。',config_already_exists:'现有配置已保留；用 config show 查看，或选择新的文件。',output_directory_not_empty:'使用新的空输出目录，原有成果不会覆盖。',unknown_source_id:'从来源 results.json 选择实际存在的 id。',read_requires_selected_ids:'使用 read --from DIR --ids ID1,ID2 选择来源。',read_requires_from_or_urls:'使用 read --from DIR --ids ... 或 read --url HTTPS_URL。',source_evidence_hash_mismatch:'保存的证据校验失败；核对来源运行，或显式 --refresh 重新访问。',source_evidence_identity_mismatch:'证据与来源身份不一致，不能复用。',unknown_platform:'运行 platforms 查看平台 ID。'})[code]||'运行 --help 查看命令；保留本机错误码用于排查。'}
export async function doctor(options,{bridge}={}){
 const report={status:'ready',nodeVersion:process.version,bridge:'unknown',onlineBrowsers:0,routes:[],checks:[]};
 if(Number(process.versions.node.split('.')[0])<22){report.status='needs_attention';report.checks.push({code:'node_22_required'})}
 try{
  bridge=bridge||await Bridge.connect();const browsers=await inventory(bridge);report.bridge='connected';report.onlineBrowsers=browsers.length;
  const loads=new Map(),capabilities=new Map();
  for(const id of options.platforms||['baidu','google']){
   const profile=getPlatform(id);
   try{
    const selected=selectBrowser(profile,browsers,options.browserMap,loads),browser=selected.browser;loads.set(browser.browserId,(loads.get(browser.browserId)||0)+1);
    if(!capabilities.has(browser.browserId)){try{const c=await bridge.command(browser.browserId,'capabilities',{});capabilities.set(browser.browserId,backgroundCapability(c.features?.backgroundExecution))}catch{capabilities.set(browser.browserId,null)}}
    const backgroundExecution=capabilities.get(browser.browserId);report.routes.push({platform:profile.id,online:true,selectionSource:selected.source,backgroundExecution});
    if(backgroundExecution===false){report.status='needs_attention';report.checks.push({platform:profile.id,code:'background_execution_unavailable'})}
   }catch(e){const code=safeCode(e);report.status='needs_attention';report.routes.push({platform:profile.id,online:false,code});report.checks.push({platform:profile.id,code,hint:errorHint(code)})}
  }
 }catch(e){const code=safeCode(e);report.status='needs_attention';report.bridge='unavailable';report.checks.push({code,hint:errorHint(code)})}
 report.note='仅检查连接和路由；平台登录、验证码及实际搜索结果由本次搜索报告确认。';return report;
}
