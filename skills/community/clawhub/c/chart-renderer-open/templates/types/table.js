/* ===== RENDERER: table — 通用美化表格 ===== */
registerRenderer('table', function(d){
  let h='<table class="plain-table"><thead><tr>';
  (d.headers||[]).forEach(th=>h+=`<th>${th}</th>`);
  h+='</tr></thead><tbody>';
  (d.rows||[]).forEach(row=>{
    h+='<tr>';
    row.forEach(cell=>{
      const cls=typeof cell==='string'&&cell.startsWith('↑')?' style="color:var(--green);font-weight:700"':typeof cell==='string'&&cell.startsWith('↓')?' style="color:var(--red);font-weight:700"':'';
      h+=`<td${cls}>${cell}</td>`;
    });
    h+='</tr>';
  });
  h+='</tbody></table>';
  return h;
});
