/* ===== RENDERER: line + dualAxis — Line Charts (multi-series + dual-axis) ===== */

/* line: Multi-series line chart */
registerRenderer('line', function(d, uid){
  return `<div class="chart-card"><canvas id="${uid}"></canvas></div>`;
}, function(d, uid){
  const el=document.getElementById(uid);
  if(!el)return;
  const colors=['#1a73e8','#ea4335','#34a853','#fbbc04','#8e44ad','#e67e22','#00bcd4','#795548'];
  const datasets=(d.datasets||[]).map((ds,i)=>{
    const c=ds.color||colors[i%colors.length];
    return {
      label:ds.label,data:ds.data,spanGaps:true,
      borderColor:c,backgroundColor:c+'22',
      borderWidth:2.5,pointRadius:5,pointHoverRadius:7,
      pointBackgroundColor:'#fff',pointBorderColor:c,
      pointBorderWidth:2,tension:0.3,fill:false,
      datalabels:{display:false}
    };
  });
  new Chart(el,{
    type:'line',
    data:{labels:d.labels||[],datasets},
    plugins:[ChartDataLabels],
    options:{
      responsive:true,maintainAspectRatio:true,
      interaction:{mode:'index',intersect:false},
      plugins:{legend:{position:'bottom',labels:{usePointStyle:true,padding:16,font:{size:12,weight:'bold'}}}},
      scales:{
        y:{beginAtZero:d.yMin!==undefined?undefined:true,min:d.yMin,max:d.yMax,grid:{color:'#f0f0f0'},ticks:{font:{size:11}}},
        x:{grid:{display:false},ticks:{font:{size:11}}}
      }
    }
  });
});

/* dualAxis: Dual-axis line chart */
registerRenderer('dualAxis', function(d, uid){
  return `<div class="chart-card"><canvas id="${uid}"></canvas></div>`;
}, function(d, uid){
  const el=document.getElementById(uid);
  if(!el)return;
  new Chart(el,{
    type:'line',
    data:{
      labels:d.labels||[],
      datasets:[{
        label:d.primaryLabel||'Primary',data:d.primary,
        borderColor:'#1a73e8',backgroundColor:'rgba(26,115,232,.12)',
        borderWidth:3,pointRadius:6,pointBackgroundColor:'#1a73e8',
        pointBorderColor:'#fff',pointBorderWidth:2,tension:0.35,fill:true,
        datalabels:{display:false}
      },{
        label:d.secondaryLabel||'Secondary',data:d.secondary,
        borderColor:'#e74c3c',borderWidth:2,borderDash:[6,3],
        pointRadius:4,pointBackgroundColor:'#e74c3c',pointBorderColor:'#fff',
        pointBorderWidth:1.5,tension:0.35,fill:false,yAxisID:'y1',
        datalabels:{display:false}
      }]
    },
    plugins:[ChartDataLabels],
    options:{
      responsive:true,maintainAspectRatio:true,
      interaction:{mode:'index',intersect:false},
      plugins:{legend:{position:'bottom',labels:{usePointStyle:true,padding:16,font:{size:12,weight:'bold'}}}},
      scales:{
        y:{min:d.yMin||300,max:d.yMax||450,grid:{color:'#f0f0f0'},ticks:{font:{size:11}},title:{display:true,text:d.primaryLabel||'Primary',font:{size:12}}},
        y1:{position:'right',min:d.rMin||40,max:d.rMax||65,grid:{drawOnChartArea:false},ticks:{font:{size:11}},title:{display:true,text:d.secondaryLabel||'Secondary',font:{size:12}}},
        x:{grid:{display:false},ticks:{font:{size:11}}}
      }
    }
  });
});
