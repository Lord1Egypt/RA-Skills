import {createHash} from 'node:crypto';
import {publicURL,shortText} from './results.mjs';
const messages={
 login_required:'在原浏览器环境登录该平台，再只重试这一分支。',
 challenge:'在原浏览器完成人工验证，再只重试这一分支。',
 titles_only:'已取得搜索卡片；打开搜索页手动查看详情，或提供可访问的内容链接。',
 link_unavailable:'该条只有搜索页线索；人工打开详情并复制链接后，可使用 read --url 读取。',
 route_unavailable:'检查私有 browserMap 指定的环境是否唯一且在线，修正后重试；不会自动换账号。',
 result_load_timeout:'打开搜索页检查网络、登录或页面加载，处理后只重试这一平台。',
 unexpected_page:'打开预期搜索页或内容页核对实际跳转，再提供有效链接或重试。',
 content_unavailable:'人工打开来源查看正文，或提供可访问的同一内容链接。',
 unavailable:'检查该平台页面和浏览器连接，处理后只重试这一分支。',
 no_content_links:'搜索页未取得有效内容链接；人工查看页面并提供具体详情链接。',
 read_failed:'检查来源页和浏览器连接，提供可访问链接或重试该来源。'
};
export function handoffTask({platform,status,query,url,id,errorCode}){
 if(['ok','empty','read','not_read'].includes(status))return null;
 const reason=status==='unavailable'&&errorCode==='configured_browser_not_unique_or_online'?'route_unavailable':status;
 const task={platform:shortText(platform,120),status:shortText(reason,80),required:!['titles_only','link_unavailable'].includes(reason),instruction:messages[reason]||messages.unavailable,...(query?{query:shortText(query,500)}:{}),...(id?{sourceId:id}:{}),...(publicURL(url)?{url:publicURL(url)}:{}),...(errorCode?{errorCode:shortText(errorCode,80)}:{})};
 return {taskId:createHash('sha256').update(JSON.stringify(task)).digest('hex').slice(0,14),...task};
}
export function collectHandoffs(searches,results,searchURL){
 const tasks=[];
 for(const row of searches||[]){const task=handoffTask({...row,url:searchURL(row.platform,row.query)});if(task)tasks.push(task)}
 for(const item of results||[]){if(item.readStatus==='not_read'||item.readStatus==='link_unavailable')continue;const task=handoffTask({platform:item.platform,status:item.readStatus,id:item.id,url:item.url,errorCode:item.readError});if(task)tasks.push(task)}
 return [...new Map(tasks.map(t=>[t.taskId,t])).values()];
}
