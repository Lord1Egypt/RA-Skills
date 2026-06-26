/* ===== RENDERER: layered — Tiered Category Cards ===== */
registerRenderer('layered', function(d){
  const tiers=[
    {key:'strong',cls:'l-adv',icon:'✦',label:'Tier 1: Strong',desc:'Top performers'},
    {key:'moderate',cls:'l-pot',icon:'▲',label:'Tier 2: Moderate',desc:'Room for improvement'},
    {key:'weak',cls:'l-risk',icon:'⚠',label:'Tier 3: Weak',desc:'Needs attention'}
  ];
  let h='<div class="layer-grid">';
  tiers.forEach(t=>{
    const items=(d.layers||[])[t.key]||[];
    if(!items.length) return;
    h+=`<div class="layer-card ${t.cls}">
      <div class="layer-header"><span class="icon">${t.icon}</span>${t.label}<span style="font-weight:400;font-size:12px;margin-left:auto;opacity:.7">${t.desc}</span></div>
      <div class="layer-body"><table><thead><tr>
        <th>Item</th><th>Previous</th><th>Current</th><th>Change</th><th>Rate</th><th>Note</th>
      </tr></thead><tbody>`;
    items.forEach(r=>{
      const chg=r.change;
      const chgCls=chg>0?'up':chg<0?'down':'';
      const chgTxt=chg>0?'+'+chg:chg<0?''+chg:'-';
      h+=`<tr>
        <td><b>${r.item}</b></td>
        <td>${r.prev}</td><td><b>${r.current}</b></td>
        <td class="${chgCls}">${chgTxt}</td>
        <td><span class="rate">${r.rate}%</span></td>
        <td class="analysis">${r.note}</td>
      </tr>`;
    });
    h+=`</tbody></table></div></div>`;
  });
  h+='</div>';
  return h;
});
