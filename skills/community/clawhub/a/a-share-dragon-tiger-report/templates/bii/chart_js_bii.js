/* ═══════════════════════════════════════════════════════════════════════
   BII 双栏范式 · 龙虎榜日更报告 图表配置
   —— 占位符由 gen_bii_2col.py 以双下划线包裹的大写标识注入，禁止直接写死数据
   —— 配色：黑 #000000 + 品牌黄 #FFB500 + 灰阶；涨跌类仍用 A 股红涨绿跌
   —— 所有图表 animation:false + responsive:false + 尺寸写死在 canvas HTML 属性上
   ═══════════════════════════════════════════════════════════════════════ */
var BK='#000000', BY='#FFB500', BYD='#C98A00', GY='#C9C9C4', GY2='#9E9E98';
var AX='#8C8C8C', GRID='rgba(0,0,0,0.07)', UP='#C1272D', DN='#1E8449';
var F={family:'Helvetica Neue,Arial,sans-serif'};

/* ── 注入数据 ── */
var STAGE_L=__STAGE_L__, STAGE_V=__STAGE_V__;
var IND={n:__IND_N__, rank:__IND_RANK__, vr:__IND_VR__, disp:__IND_DISP__};
var RADAR={labels:__RADAR_LABELS__, sets:__RADAR_SETS__};
var SCORE={n:__SCORE_N__, v:__SCORE_V__, act:__SCORE_ACT__};
var FIN={n:__FIN_N__, interim:__FIN_INTERIM__, prior:__FIN_PRIOR__};
var PB={n:__PB_N__, v:__PB_V__};
var DIM={labels:__DIM_LABELS__, sets:__DIM_SETS__};
var ALPHA={used:__ALPHA_USED__, remain:__ALPHA_REMAIN__, max:__ALPHA_MAX__};

/* ── 通用小工具 ── */
function yi(v){return (v<0?'−'+Math.abs(v):v)+' 亿';}
function pct(v){return (v>0?'+':'')+v+'%';}

/* 数值标签插件 */
function labeller(fmt,color,dy){
  return {id:'lb'+Math.random(),afterDatasetsDraw:function(c){
    var ctx=c.ctx; ctx.save();
    ctx.font='700 9.5px Helvetica Neue,Arial,sans-serif';
    ctx.textAlign='center'; ctx.fillStyle=color||'#111111';
    c.data.datasets.forEach(function(ds,di){
      var meta=c.getDatasetMeta(di); if(meta.hidden) return;
      meta.data.forEach(function(el,i){
        var v=ds.data[i]; var s=fmt(v,i); if(s===null) return;
        var off=(typeof dy==='function')?dy(v,i):(dy||-6);
        ctx.fillText(s,el.x,el.y+off);
      });
    });
    ctx.restore();
  }};
}
/* 横向条形末端标签 */
var HBAR_LAB={id:'hbarLab',afterDatasetsDraw:function(c){
  var ctx=c.ctx, meta=c.getDatasetMeta(0), ds=c.data.datasets[0];
  ctx.save(); ctx.font='700 9.5px Helvetica Neue,Arial,sans-serif';
  ctx.textAlign='left'; ctx.fillStyle='#111111';
  meta.data.forEach(function(el,i){
    var v=ds.data[i];
    ctx.fillText((typeof v==='number'? v.toFixed(1) : v), el.x+5, el.y+3.2);
  });
  ctx.restore();
}};
/* L1 门槛虚线（分位 25% / 额比 1.0×） */
var L1_GATE={id:'l1gate',beforeDatasetsDraw:function(c){
  var a=c.chartArea, ctx=c.ctx;
  var x=c.scales.x.getPixelForValue(25), y=c.scales.y.getPixelForValue(1.0);
  ctx.save(); ctx.strokeStyle='rgba(0,0,0,0.30)'; ctx.setLineDash([4,3]); ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(x,a.top); ctx.lineTo(x,a.bottom); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(a.left,y); ctx.lineTo(a.right,y); ctx.stroke();
  ctx.setLineDash([]);
  ctx.font='700 9px Helvetica Neue,Arial,sans-serif'; ctx.fillStyle='#8C8C8C';
  ctx.textAlign='left';  ctx.fillText('低分位 · 高额比（L1 入池区）', a.left+6, a.top+12);
  ctx.textAlign='right'; ctx.fillText('高分位 · 低额比（L1 拦截区）', a.right-6, a.bottom-8);
  ctx.restore();
}};
/* 50% 增速红线 */
var DECEL_LINE={id:'decel',beforeDatasetsDraw:function(c){
  var a=c.chartArea, ctx=c.ctx;
  ctx.save(); ctx.strokeStyle='rgba(193,39,45,0.75)'; ctx.setLineDash([5,3]); ctx.lineWidth=1.2;
  ctx.beginPath(); ctx.moveTo(a.left, a.top+2); ctx.lineTo(a.right, a.top+2); ctx.stroke();
  ctx.setLineDash([]);
  ctx.font='700 9px Helvetica Neue,Arial,sans-serif'; ctx.fillStyle=UP;
  ctx.textAlign='right'; ctx.fillText('增速红线：< 上年度 50% → −15 分', a.right-4, a.top+14);
  ctx.restore();
}};
/* 气泡名称标签 */
var BUB_LAB={id:'bubLab',afterDatasetsDraw:function(c){
  var ctx=c.ctx, meta=c.getDatasetMeta(0), pts=meta.data;
  ctx.save(); ctx.font='700 9px Helvetica Neue,Arial,sans-serif';
  ctx.textAlign='center'; ctx.fillStyle='#111111';
  pts.forEach(function(el,i){ ctx.fillText(IND.n[i], el.x, el.y-el.options.radius-4); });
  ctx.restore();
}};
/* 基础 100 参考线（归一化图用，本报告备用） */
var BASE_LINE={id:'base100',beforeDatasetsDraw:function(ch){
  var a=ch.chartArea, ctx=ch.ctx, y;
  try{ y=ch.scales.y.getPixelForValue(100); }catch(e){ return; }
  ctx.save(); ctx.strokeStyle='rgba(0,0,0,0.45)'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(a.left,y); ctx.lineTo(a.right,y); ctx.stroke();
  ctx.restore();
}};

/* ═══ 图 1：四层漏斗通过数（横向条形，逐层递减） ═══ */
(function(){
  var c=document.getElementById('c1'); if(!c) return;
  new Chart(c,{type:'bar',
    data:{labels:STAGE_L,
      datasets:[{data:STAGE_V,
        backgroundColor:[GY2,GY,BYD,BY,BK],borderRadius:0,barPercentage:0.62}]},
    options:{indexAxis:'y',responsive:false,animation:false,
      layout:{padding:{right:34}},
      plugins:{legend:{display:false},tooltip:{enabled:false}},
      scales:{
        x:{beginAtZero:true,grid:{color:GRID},
           ticks:{color:AX,font:{size:9},stepSize:2,precision:0}},
        y:{grid:{display:false},ticks:{color:'#111111',font:{size:10.5}}}}},
    plugins:[HBAR_LAB]});
})();

/* ═══ 图 2：行业分位 × 额比 气泡矩阵（L1 门槛） ═══ */
(function(){
  var c=document.getElementById('c2'); if(!c) return;
  var pts=IND.n.map(function(n,i){
    return {x:IND.rank[i], y:IND.vr[i], r:Math.max(5, IND.disp[i]/6)};
  });
  new Chart(c,{type:'bubble',
    data:{datasets:[{data:pts, backgroundColor:'rgba(255,181,0,0.55)',
      borderColor:BK, borderWidth:1.4}]},
    options:{responsive:false,animation:false,layout:{padding:{top:14,right:8}},
      plugins:{legend:{display:false},tooltip:{enabled:false}},
      scales:{
        x:{min:0,max:52,grid:{color:GRID},
           title:{display:true,text:'行业年内分位（%）　← 越左越低位',color:AX,font:{size:9.5}},
           ticks:{color:AX,font:{size:9},stepSize:10}},
        y:{min:0.6,max:1.6,grid:{color:GRID},
           title:{display:true,text:'额比（×）　↑ 放量越充分',color:AX,font:{size:9.5}},
           ticks:{color:AX,font:{size:9},stepSize:0.2,precision:1}}}},
    plugins:[L1_GATE, BUB_LAB]});
})();

/* ═══ 图 3：Top 候选五维评分雷达 ═══ */
(function(){
  var c=document.getElementById('c3'); if(!c) return;
  var cols=[BY,BK,'#5A5A5A'], dash=[[],[],[]];
  new Chart(c,{type:'radar',
    data:{labels:RADAR.labels,
      datasets:RADAR.sets.map(function(d,i){
        return {label:d.label,data:d.data,
          borderColor:cols[i%3],backgroundColor:i===0?'rgba(255,181,0,0.16)':'rgba(0,0,0,0.04)',
          borderWidth:i===0?2.6:1.8,pointBackgroundColor:cols[i%3],pointRadius:3,
          borderDash:dash[i%3]};})},
    options:{responsive:false,animation:false,
      plugins:{legend:{position:'bottom',
        labels:{boxWidth:13,boxHeight:2,font:{size:8.5,family:F.family},color:'#444444',padding:9}},
        tooltip:{enabled:false}},
      scales:{r:{min:0,max:100,grid:{color:GRID},angleLines:{color:GRID},
        ticks:{color:'#6E6E6E',font:{size:8.5},backdropColor:'#FFFFFF',
               showLabelBackdrop:true,stepSize:25},
        pointLabels:{color:'#111111',font:{size:10.5,family:F.family}}}}}});
})();

/* ═══ 图 4：综合分横向排行 ═══ */
(function(){
  var c=document.getElementById('c4'); if(!c) return;
  var mx=Math.max.apply(null,SCORE.v);
  new Chart(c,{type:'bar',
    data:{labels:SCORE.n,
      datasets:[{data:SCORE.v,
        backgroundColor:SCORE.v.map(function(v){return v===mx?BY:(v>=60?BYD:GY);}),
        borderRadius:0,barPercentage:0.62}]},
    options:{indexAxis:'y',responsive:false,animation:false,
      layout:{padding:{right:42}},
      plugins:{legend:{display:false},tooltip:{enabled:false}},
      scales:{
        x:{beginAtZero:true,max:100,grid:{color:GRID},
           ticks:{color:AX,font:{size:9},stepSize:20}},
        y:{grid:{display:false},ticks:{color:'#111111',font:{size:10.5}}}}},
    plugins:[{id:'scoreLab',afterDatasetsDraw:function(ch){
      var ctx=ch.ctx, meta=ch.getDatasetMeta(0), ds=ch.data.datasets[0];
      ctx.save(); ctx.font='700 9.5px Helvetica Neue,Arial,sans-serif';
      ctx.textAlign='left';
      meta.data.forEach(function(el,i){
        ctx.fillStyle=(ds.data[i]===mx)?'#8A5A00':'#111111';
        ctx.fillText(ds.data[i].toFixed(1)+'  '+SCORE.act[i], el.x+6, el.y+3.2);
      });
      ctx.restore();
    }}]});
})();

/* ═══ 图 5：中报同比 vs 上年度增速（分组柱 + 50% 红线） ═══ */
(function(){
  var c=document.getElementById('c5'); if(!c) return;
  new Chart(c,{type:'bar',
    data:{labels:FIN.n,
      datasets:[
        {label:'2026 中报归母同比（半年口径）',data:FIN.interim,
          backgroundColor:BY,borderRadius:0,barPercentage:0.72},
        {label:'上一年度（FY）增速',data:FIN.prior,
          backgroundColor:GY,borderRadius:0,barPercentage:0.72}]},
    options:{responsive:false,animation:false,layout:{padding:{top:22}},
      plugins:{legend:{position:'bottom',
        labels:{boxWidth:11,boxHeight:11,font:{size:8.5,family:F.family},color:'#444444',padding:9}},
        tooltip:{enabled:false}},
      scales:{
        x:{grid:{display:false},
           ticks:{color:'#111111',font:{size:9},maxRotation:0,minRotation:0,autoSkip:false}},
        y:{grid:{color:GRID},
           ticks:{color:AX,font:{size:9},
             callback:function(v){return (v>0?'+':'')+Math.round(v*100)+'%';}}}}},
    plugins:[DECEL_LINE, labeller(function(v){
      return (v*100).toFixed(1)+'%';},'#4A4A4A',-6)]});
})();

/* ═══ 图 6：PB 横向柱（低估值排序） ═══ */
(function(){
  var c=document.getElementById('c6'); if(!c) return;
  new Chart(c,{type:'bar',
    data:{labels:PB.n,
      datasets:[{data:PB.v,
        backgroundColor:PB.v.map(function(v){return v<0?UP:(v<=2?BY:GY);}),
        borderRadius:0,barPercentage:0.6}]},
    options:{indexAxis:'y',responsive:false,animation:false,
      layout:{padding:{right:40}},
      plugins:{legend:{display:false},tooltip:{enabled:false}},
      scales:{
        x:{grid:{color:GRID},
           ticks:{color:AX,font:{size:9},stepSize:2,
             callback:function(v){return v+'×';}}},
        y:{grid:{display:false},ticks:{color:'#111111',font:{size:10}}}}},
    plugins:[{id:'pbLab',afterDatasetsDraw:function(ch){
      var ctx=ch.ctx, meta=ch.getDatasetMeta(0), ds=ch.data.datasets[0];
      ctx.save(); ctx.font='700 9.5px Helvetica Neue,Arial,sans-serif';
      ctx.textAlign='left';
      meta.data.forEach(function(el,i){
        var v=ds.data[i], txt=(v<0?'PB 为负 ':'')+v.toFixed(2)+'×';
        ctx.fillStyle = v<0 ? UP : '#111111';
        var xx = v<0 ? el.x+6 : el.x+6;
        ctx.fillText(txt, xx, el.y+3.2);
      });
      ctx.restore();
    }}]});
})();

/* ═══ 图 7：五维评分分组柱（按候选 × tech/flow/fund/cycle/fib） ═══ */
(function(){
  var c=document.getElementById('c7'); if(!c) return;
  var cols=[BK,GY2,GY,'#6B6B66',BY];
  new Chart(c,{type:'bar',
    data:{labels:DIM.labels,
      datasets:DIM.sets.map(function(d,i){
        return {label:d.label,data:d.data,backgroundColor:cols[i%5],borderRadius:0,barPercentage:0.78};})},
    options:{responsive:false,animation:false,
      plugins:{legend:{position:'bottom',
        labels:{boxWidth:11,boxHeight:11,font:{size:8.5,family:F.family},color:'#444444',padding:8}},
        tooltip:{enabled:false}},
      scales:{
        x:{grid:{display:false},
           ticks:{color:'#111111',font:{size:9},maxRotation:0,minRotation:0,autoSkip:false}},
        y:{beginAtZero:true,max:100,grid:{color:GRID},
           ticks:{color:AX,font:{size:9},stepSize:25}}}}});
})();

/* ═══ 图 8：α 账本（已用 vs 剩余，堆叠横向柱） ═══ */
(function(){
  var c=document.getElementById('c8'); if(!c) return;
  new Chart(c,{type:'bar',
    data:{labels:['α 预算使用'],
      datasets:[
        {label:'已用',data:[ALPHA.used],backgroundColor:BY,borderRadius:0,barPercentage:0.36},
        {label:'剩余',data:[ALPHA.remain],backgroundColor:GY,borderRadius:0,barPercentage:0.36}]},
    options:{indexAxis:'y',responsive:false,animation:false,
      layout:{padding:{right:14}},
      plugins:{legend:{position:'bottom',
        labels:{boxWidth:11,boxHeight:11,font:{size:8.5,family:F.family},color:'#444444',padding:8}},
        tooltip:{enabled:false}},
      scales:{
        x:{stacked:true,beginAtZero:true,max:ALPHA.max,grid:{color:GRID},
           ticks:{color:AX,font:{size:9},callback:function(v){return v+' 万';}}},
        y:{stacked:true,grid:{display:false},ticks:{color:'#111111',font:{size:10}}}}},
    plugins:[{id:'alphaLab',afterDatasetsDraw:function(ch){
      var ctx=ch.ctx; ctx.save();
      ctx.font='700 9.5px Helvetica Neue,Arial,sans-serif';
      var meta=ch.getDatasetMeta(0).data[0];
      ctx.fillStyle='#3A2A00'; ctx.textAlign='left';
      ctx.fillText('已用 '+ALPHA.used.toFixed(1)+' 万', meta.x+6, meta.y+3.2);
      ctx.restore();
    }}]});
})();
