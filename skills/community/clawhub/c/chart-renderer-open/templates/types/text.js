/* ===== RENDERER: text — 文字提示块 ===== */
registerRenderer('text', function(d){
  const cls=d.level||'warning';
  return `<div class="text-block ${cls}"><h3>${d.title||''}</h3>${d.content||''}</div>`;
});
