const $=id=>document.getElementById(id);
const labels={not_required:'当前无需验证（不是已通过）',pending:'审核中',approved:'已通过',denied:'审核被拒'};
let lastResult=null;
function node(tag,text,cls){const n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n;}
for(const name of ['kyc','net'])$('tab-'+name).onclick=()=>{for(const n of ['kyc','net']){$(n).hidden=n!==name;$('tab-'+n).setAttribute('aria-pressed',String(n===name));}};
if(!globalThis.chrome?.scripting){$('check').disabled=true;$('message').textContent='请将此文件夹加载为 Chrome 扩展，再从工具栏打开。';}
$('check').onclick=async()=>{$('check').disabled=true;$('copy').disabled=true;$('copy-fallback').hidden=true;lastResult=null;$('results').replaceChildren();$('message').textContent='正在查询，请保持弹窗打开…';try{
 const [tab]=await chrome.tabs.query({active:true,currentWindow:true});if(!tab?.url||new URL(tab.url).origin!=='https://claude.ai')throw Error('请切换到已登录的 https://claude.ai 页面后再检查。');
 const injected=await chrome.scripting.executeScript({target:{tabId:tab.id},func:checkKyc});const data=injected[0]?.result;if(!data||data.error)throw Error(data?.error||'没有收到查询结果，请刷新 Claude 页面后重试。');
 data.rows.forEach((row,i)=>{const card=node('article','');card.append(node('h2',`组织 ${i+1}`),node('p',row.error?'查询失败：'+row.error:labels[row.status]||'未知状态'),node('p',row.status?'原始状态：'+row.status:'','raw'));const detail=node('details','');detail.append(node('summary','显示组织标识'),node('p',[row.name,row.uuid].filter(Boolean).join('\n'),'raw'));card.append(detail);$('results').append(card);});
 const failed=data.rows.filter(r=>r.error).length;$('message').textContent=`已完成 ${data.rows.length-failed} 项，${failed} 项未取得状态。查询时间：${new Date(data.checkedAt).toLocaleString()}${data.incomplete?'；达到查询时间上限，部分组织未查询。':''}`;lastResult=data;$('copy').disabled=false;
 }catch(e){$('message').textContent=e.message;}finally{$('check').disabled=false;}};
$('copy').onclick=async()=>{const text=redactedKyc(lastResult);try{await navigator.clipboard.writeText(text);$('message').textContent='已复制脱敏结果。';}catch{$('copy-fallback').value=text;$('copy-fallback').hidden=false;$('copy-fallback').select();$('message').textContent='自动复制未完成，请从文本框手动复制。';}};
$('net-start').onclick=async()=>{$('net-start').disabled=true;$('net-results').textContent='正在检测…';try{$('net-results').textContent=await browserNetwork();}catch{$('net-results').textContent='检测未完成，请重试。';}finally{$('net-start').disabled=false;}};
$('rtc-start').onclick=()=>{$('rtc-consent').hidden=false;$('rtc-start').disabled=true;};
$('rtc-cancel').onclick=()=>{$('rtc-consent').hidden=true;$('rtc-start').disabled=false;$('rtc-results').textContent='未检测';};
$('rtc-confirm').onclick=async()=>{$('rtc-consent').hidden=true;$('rtc-results').textContent='正在收集候选，最多 5 秒…';try{$('rtc-results').textContent=await rtcCandidates();}finally{$('rtc-start').disabled=false;}};
