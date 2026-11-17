// perplexity.ai/search/<uuid>：必须走浏览器。
// 接口 /rest/thread/<id> 需要登录 cookie，curl 直连拿不到；浏览器页面过 CF 之后可以。
// 参数必须带全 supported_block_use_cases，少了任何一个，回答块（ask_text_0_markdown）就不下发，
// 只会回来问题和元数据 —— 这是踩过的坑，别精简。
import { fmtClock, pickJson } from '../lib/md.mjs';

export const name = 'perplexity.ai';
export const channel = 'browser';
export const match = (url) => /(^|\/\/|\.)perplexity\.ai\/(search|session)\//.test(url);


// 从 Convolvger 的 bookmarklet 抄的完整参数表。少一个 block_use_case 就会丢回答正文。
const QUERY =
  '?with_parent_info=true&with_schematized_response=true&version=2.18&source=default' +
  '&limit=20&offset=0&from_first=false&with_first_entry=true&with_latest_entry=false' +
  '&supported_block_use_cases=answer_modes&supported_block_use_cases=media_items' +
  '&supported_block_use_cases=inline_entity_cards&supported_block_use_cases=place_widgets' +
  '&supported_block_use_cases=finance_widgets&supported_block_use_cases=news_widgets' +
  '&supported_block_use_cases=shopping_widgets&supported_block_use_cases=search_result_widgets' +
  '&supported_block_use_cases=inline_images&supported_block_use_cases=inline_assets' +
  '&supported_block_use_cases=placeholder_cards&supported_block_use_cases=diff_blocks' +
  '&supported_block_use_cases=entity_group_v2&supported_block_use_cases=refinement_filters' +
  '&supported_block_use_cases=canvas_mode&supported_block_use_cases=maps_preview' +
  '&supported_block_use_cases=answer_tabs&supported_block_use_cases=preserve_latex' +
  '&supported_block_use_cases=in_context_suggestions&supported_block_use_cases=pending_followups' +
  '&supported_block_use_cases=inline_claims&supported_block_use_cases=unified_assets' +
  '&supported_block_use_cases=workflow_steps&supported_block_use_cases=workflow_widgets' +
  '&supported_block_use_cases=navigation_results&supported_block_use_cases=background_agents';

export async function read(url, { session, keepOpen = false } = {}) {
  const id = (url.match(/\/(?:search|session)\/([0-9a-f-]{36})/i) || [])[1];
  if (!id) throw new Error('URL 里没有 thread id（应为 36 位 UUID）');

  if (!session) throw new Error('这个站点需要浏览器后端，但调用方没有传入 session');
  await session.open(url);
  try {
    await session.waitReady({ minText: 300, tries: 14, delay: 3000 });

    const code = `
      (async function(){
        var r = await fetch(${JSON.stringify('/rest/thread/' + id + QUERY)}, { credentials: "include" });
        if (!r.ok) return JSON.stringify({ error: "HTTP " + r.status });
        var j = await r.json();
        var pick = function(entry){
          var md = null;
          (entry.blocks || []).forEach(function(b){
            if (b.intended_usage === "ask_text_0_markdown" && b.markdown_block) md = b.markdown_block;
          });
          var text = "";
          if (md) {
            text = md.answer ? String(md.answer) : (md.chunks || []).join("");
          }
          var sources = [];
          (entry.blocks || []).forEach(function(b){
            if (b.intended_usage === "web_results" && b.web_result_block) {
              (b.web_result_block.web_results || []).forEach(function(w){
                // 字段是 name 不是 title
                var title = w.name || w.title || "";
                if (w.url && title) sources.push({ title: title, url: w.url });
              });
            }
          });
          return { query: entry.query_str || "", text: text, created: entry.entry_created_datetime || null, sources: sources };
        };
        var entries = (j.entries || []).slice().sort(function(a, b){
          return String(a.entry_created_datetime).localeCompare(String(b.entry_created_datetime));
        });
        var out = entries.map(pick);
        return JSON.stringify({
          title: (entries[0] || {}).thread_title || "",
          hasNext: !!j.has_next_page,
          entries: out
        });
      })()
    `;

    const raw = await session.eval(code);
    const data = pickJson(raw);
    if (data.error) throw new Error('页面内取 thread 失败：' + data.error);

    const messages = [];
    for (const e of data.entries || []) {
      if (e.query && e.query.trim()) {
        messages.push({ role: '用户', time: fmtClock(e.created), body: e.query });
      }
      if (e.text && e.text.trim()) {
        let body = e.text.trim();
        // 正文里的 [n] 是 Perplexity 自己的编号，与 web_results 的顺序并不一一对应，
        // 所以来源单独列，不冒充编号映射。
        const src = (e.sources || []).slice(0, 20);
        if (src.length) {
          body +=
            '\n\n**参考来源**（编号以原页面为准，未必与正文标记一一对应）\n\n' +
            src.map((s, i) => `${i + 1}. [${s.title}](${s.url})`).join('\n');
        }
        messages.push({ role: 'Perplexity', time: fmtClock(e.created), body });
      }
    }

    if (!messages.length) throw new Error('拿到 thread 但解析不出消息，块结构可能改版了');

    return {
      title: data.title || 'Perplexity 分享',
      messages,
      source: `https://www.perplexity.ai/rest/thread/${id}`,
      note: data.hasNext ? '超过 20 轮，只取到第一页' : '引用标记保留原样，文末附来源清单',
    };
  } finally {
    if (!keepOpen) await session.close();
  }
}
