const STUN_URL='stun:stun.l.google.com:19302';
const IP_ENDPOINTS=['https://api.ipify.org?format=json','https://api6.ipify.org?format=json'];
async function browserNetwork(){
  const ips=await Promise.all(IP_ENDPOINTS.map(async url=>{const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),8000);try{const r=await fetch(url,{credentials:'omit',cache:'no-store',redirect:'error',signal:controller.signal});if(!r.ok)throw Error('HTTP '+r.status);const data=await r.json();if(typeof data.ip!=='string'||data.ip.length>45||!(/^[0-9.:a-f]+$/i.test(data.ip)))throw Error('无有效 IP');return data.ip;}catch{return '未取得（可能受网络、服务或浏览器策略影响）';}finally{clearTimeout(timer);}}));
  return `IPv4：${ips[0]}\nIPv6：${ips[1]}\n语言：${navigator.languages.join(', ')}\n时区：${Intl.DateTimeFormat().resolvedOptions().timeZone}\nUTC 偏移（分钟）：${-new Date().getTimezoneOffset()}`;
}
function rtcCandidates(){
 return new Promise(resolve=>{let pc,timer,finished=false;const rows=[];const finish=note=>{if(finished)return;finished=true;clearTimeout(timer);if(pc)pc.close();resolve(rows.length?rows.join('\n'):(note||'未取得候选。可能原因：浏览器策略、网络拦截或 STUN 不可达。'));};
 try{pc=new RTCPeerConnection({iceServers:[{urls:STUN_URL}]});timer=setTimeout(()=>finish(),5000);pc.onicecandidate=e=>{if(!e.candidate){finish();return;}const c=e.candidate;const address=c.address||'未提供';rows.push(`${c.type||'未知类型'} · ${address} · ${c.protocol||'未知协议'}${address.endsWith('.local')?'（浏览器已用 mDNS 隐藏本机地址）':''}`);};pc.createDataChannel('probe');pc.createOffer().then(o=>pc.setLocalDescription(o)).catch(()=>finish('未取得候选，浏览器无法开始收集。'));}catch{finish('此浏览器未提供可用的 WebRTC 检测能力。');}
 });
}
