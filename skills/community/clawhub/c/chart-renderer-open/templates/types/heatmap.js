/* ===== RENDERER: heatmap — Matrix Heatmap Table ===== */
registerRenderer('heatmap', function(d){
  const rows=d.rows||[];
  const columns=d.columns||[];
  const totals=d.totals||[];
  const showTotal=totals.length>0;
  function getScoreLevel(rate){
    if(rate<30)return's-lv1';if(rate<45)return's-lv2';if(rate<55)return's-lv3';if(rate<70)return's-lv4';return's-lv5';
  }
  function getRateLevel(rate){
    if(rate>=65)return'high';if(rate>=45)return'mid';return'low';
  }
  let h='<div class="heatmap-wrap"><table class="heatmap"><thead><tr>';
  h+='<th class="subject-col">Item</th>';
  columns.forEach(c=>h+=`<th>${c}</th>`);
  h+='<th>First→Last</th><th>Rate</th><th>Trend</th></tr></thead><tbody>';
  rows.forEach(s=>{
    const first=s.values[0],last=s.values[s.values.length-1];
    const change=Math.round((last-first)*10)/10;
    const changeStr=change>0?'+'+change:change<0?''+change:'-';
    const changeClass=change>0?'pos':change<0?'neg':'neutral';
    const arrow=change>0?'▲':change<0?'▼':'─';
    const trendClass=change>5?'up':change<-5?'down':'flat';
    const trendIcon=change>5?'▲':change<-5?'▼':'─';
    const lastRate=Math.round(last/s.max*1000)/10;
    h+='<tr>';
    h+=`<td class="subject-name">${s.name}</td>`;
    s.values.forEach(sc=>{
      const rate=sc/s.max*100;
      h+=`<td class="score ${getScoreLevel(rate)}">${sc%1===0?sc:sc}</td>`;
    });
    h+=`<td class="change ${changeClass}">${arrow} ${changeStr}</td>`;
    h+=`<td class="rate ${getRateLevel(lastRate)}">${lastRate}%</td>`;
    h+=`<td><span class="trend-badge ${trendClass}">${trendIcon} ${s.trend||''}</span></td>`;
    h+='</tr>';
  });
  if(showTotal){
    const tc=totals[totals.length-1]-totals[0];
    const tcCls=tc>0?'pos':tc<0?'neg':'neutral';
    const tcArr=tc>0?'▲':tc<0?'▼':'─';
    h+='<tr style="background:#f0f4f8;font-weight:700">';
    h+='<td class="subject-name" style="font-size:13px">Total</td>';
    totals.forEach(t=>h+=`<td class="score" style="background:#e8edf3;color:#1a1a2e;font-size:15px">${t}</td>`);
    h+=`<td class="change ${tcCls}" style="font-size:15px">${tcArr} ${tc>0?'+':''}${tc}</td>`;
    h+=`<td class="rate mid">${d.totalRate||''}</td>`;
    h+=`<td><span class="trend-badge ${d.totalTrend==='up'?'up':d.totalTrend==='down'?'down':'flat'}">${d.totalTrend==='up'?'▲':d.totalTrend==='down'?'▼':'─'} ${d.totalTrendLabel||''}</span></td>`;
    h+='</tr>';
  }
  h+='</tbody></table></div>';
  return h;
});
