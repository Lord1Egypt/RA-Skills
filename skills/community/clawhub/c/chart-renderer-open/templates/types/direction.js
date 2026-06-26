/* ===== RENDERER: direction — Recommendation Cards ===== */
/*
 * Color and icon mapping is keyword-based.
 * Extend colorMap and iconMap below to support your domain's keywords.
 * Colors: d-azure, d-emerald, d-violet, d-amber, d-rose, d-cyan, d-lime, d-pink, d-teal, d-indigo, d-orange, d-slate
 */
registerRenderer('direction', function(d){
  const colorList=['d-azure','d-emerald','d-violet','d-amber','d-rose','d-cyan','d-lime','d-pink','d-teal','d-indigo','d-orange','d-slate'];
  // Keyword → color class mapping. Add your domain keywords here.
  const colorMap={
    // General
    'tech':'d-azure','science':'d-emerald','medical':'d-rose','education':'d-cyan',
    'legal':'d-indigo','media':'d-violet','finance':'d-amber','marketing':'d-pink',
    'engineering':'d-teal','design':'d-lime','health':'d-rose','environment':'d-teal',
    // Education (legacy compat)
    '生物医学':'d-emerald','医学':'d-rose','医药':'d-emerald','农学':'d-lime','师范':'d-azure',
    '教育':'d-cyan','语言':'d-violet','法学':'d-indigo','新闻':'d-amber','文学':'d-pink',
    '传媒':'d-violet','农林':'d-lime','食品':'d-orange','环境':'d-teal','护理':'d-rose',
    '康复':'d-pink','医学技术':'d-cyan','公共':'d-slate','社会':'d-teal'
  };
  // Keyword → icon mapping. Add your domain keywords here.
  const iconMap={
    // General
    'tech':'💻','science':'🔬','medical':'🩺','education':'📚','legal':'⚖️',
    'media':'📺','finance':'💰','marketing':'📢','engineering':'⚙️','design':'🎨',
    'health':'❤️','environment':'🌍',
    // Education (legacy compat)
    '生物医学':'🧬','医学':'🩺','医药':'💊','农学':'🌾','师范':'🎓','教育':'📚',
    '语言':'🌐','法学':'⚖️','新闻':'📰','文学':'✍️','传媒':'📺','农林':'🌿',
    '食品':'🍎','环境':'🌍','护理':'❤️','康复':'🏥','医学技术':'🔬','公共':'🏛️','社会':'🤝'
  };
  function getColor(title,idx){for(const[k,v]of Object.entries(colorMap))if(title.includes(k))return v;return colorList[idx%colorList.length]}
  function getIcon(title){for(const[k,v]of Object.entries(iconMap))if(title.includes(k))return v;return'📌'}
  let h='<div class="dir-grid">';
  (d.rows||[]).forEach((r,idx)=>{
    const color=getColor(r.title,idx);
    const icon=getIcon(r.title);
    h+=`<div class="dir-card ${color}">
      <div class="dir-card-left">
        <div class="dir-card-icon">${icon}</div>
        <div class="dir-card-name">${r.title}</div>
      </div>
      <div class="dir-card-right">
        <div class="dir-card-reason"><b>Reason</b><span>${r.reason}${r.detail?' — '+r.detail:''}</span></div>
        <div class="dir-card-item threshold"><b>Requirement</b><span>${r.requirement}</span></div>
        <div class="dir-card-item jobs"><b>Outcome</b><span>${r.outcome}</span></div>
      </div>
    </div>`;
  });
  h+='</div>';
  return h;
});
