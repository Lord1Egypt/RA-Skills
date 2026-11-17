
(function(){
  if(typeof echarts==="undefined"){window.__chartsReady=true;return;}
  var NAVY="#002B5C", GOLD="#C5A572", BLUE="#60A3D9", UP="#C1272D", DOWN="#1E8449";
  var GREY="#9AA5B1", LGREY="#C9D2DA";
  var FONT='"PingFang SC","Helvetica Neue",sans-serif';
  var charts=[];

  function tipItem(){
    return {trigger:"item",backgroundColor:NAVY,borderWidth:0,
      textStyle:{color:"#fff",fontSize:11.5}};
  }
  function titleOpt(main,sub){
    return {text:main,subtext:sub,left:8,top:2,
      textStyle:{fontFamily:FONT,fontSize:13,fontWeight:"bold",color:NAVY},
      subtextStyle:{fontFamily:FONT,fontSize:10.5,color:"#6B7785"}};
  }

  /* ============ 图1：饼图 —— 涨跌家数结构 ============ */
  var el1=document.getElementById("chart1");
  if(el1){
    var c1=echarts.init(el1,null,{renderer:"canvas"});
    c1.setOption({
      animation:false,
      textStyle:{fontFamily:FONT,color:"#3C4854",fontSize:11},
      tooltip:Object.assign(tipItem(),{
        formatter:function(p){return p.name+"<br/>"+p.value+" 家　"+p.percent+"%";}}),
      title:titleOpt("涨跌家数结构","全市场 5,574 只（含停牌 12 只）"),
      series:[{
        type:"pie",
        radius:["40%","64%"],
        center:["50%","52%"],
        avoidLabelOverlap:true,
        startAngle:90,
        minAngle:2,
        itemStyle:{borderColor:"#fff",borderWidth:2},
        label:{show:true,position:"outside",
          formatter:function(p){return p.name+" "+p.percent+"%";},
          fontFamily:FONT,fontSize:11,color:"#3C4854",lineHeight:16},
        labelLine:{length:14,length2:14,lineStyle:{color:"#C9D2DA"}},
        data:[
          {value:4870,name:"下跌",itemStyle:{color:DOWN}},
          {value:643,name:"上涨",itemStyle:{color:UP}},
          {value:49,name:"平盘",itemStyle:{color:GREY}},
          {value:12,name:"停牌",itemStyle:{color:LGREY}}
        ]
      }]
    });
    charts.push(c1);
  }

  /* ============ 图2：横向柱状 —— 行业主力资金净流入/净流出 ============ */
  var el2=document.getElementById("chart2");
  if(el2){
    var inflow=[
      {n:"通信设备",v:51.12},{n:"元件",v:41.01},{n:"地面兵装Ⅱ",v:13.73},{n:"玻璃玻纤",v:7.19},
      {n:"风电设备",v:6.47},{n:"数字媒体",v:6.36},{n:"种植业",v:3.63},{n:"军工电子Ⅱ",v:2.80}
    ];
    var outflow=[
      {n:"半导体",v:-100.66},{n:"工业金属",v:-42.62},{n:"证券Ⅱ",v:-40.63},{n:"自动化设备",v:-27.37},
      {n:"光学光电子",v:-24.05},{n:"电池",v:-23.55},{n:"通用设备",v:-22.05},{n:"化学制品",v:-20.23}
    ];
    var rows=inflow.concat(outflow);
    var c2=echarts.init(el2,null,{renderer:"canvas"});
    c2.setOption({
      animation:false,
      textStyle:{fontFamily:FONT,color:"#3C4854",fontSize:11},
      tooltip:{trigger:"axis",axisPointer:{type:"shadow"},backgroundColor:NAVY,borderWidth:0,
        textStyle:{color:"#fff",fontSize:11.5},
        formatter:function(ps){var p=ps[0];
          return p.name+"<br/>主力净额："+(p.value>0?"+":"")+p.value.toFixed(2)+" 亿元";}},
      title:titleOpt("行业主力资金净流入 / 净流出",
        "单位：亿元　红色＝净流入（上8）　绿色＝净流出（下8）"),
      grid:{left:104,right:74,top:56,bottom:16},
      xAxis:{type:"value",
        axisLabel:{fontFamily:FONT,fontSize:10,color:"#6B7785"},
        splitLine:{lineStyle:{color:"#EEF2F6"}},
        axisLine:{show:false},axisTick:{show:false}},
      yAxis:{type:"category",inverse:true,
        data:rows.map(function(r){return r.n;}),
        axisLabel:{fontFamily:FONT,fontSize:10.8,color:"#3C4854"},
        axisTick:{show:false},
        axisLine:{lineStyle:{color:"#DDE3EA"}}},
      series:[{
        type:"bar",
        barWidth:"56%",
        data:rows.map(function(r){
          var pos=r.v>=0;
          return {
            value:r.v,
            itemStyle:{color:pos?UP:DOWN,
              borderRadius:pos?[0,3,3,0]:[3,0,0,3]},
            label:{show:true,
              position:pos?"right":"left",
              distance:5,
              fontFamily:FONT,fontSize:10,
              color:pos?UP:DOWN,
              fontWeight:"bold",
              formatter:(pos?"+":"")+r.v.toFixed(1)}
          };
        })
      }]
    });
    charts.push(c2);
  }

  /* ============ 图3：横向柱状 —— 概念板块涨跌幅 TOP 16 ============ */
  var el3=document.getElementById("chart3");
  if(el3){
    var con=[
      {n:"覆铜板",v:4.31,g:1},{n:"被动元件概念",v:2.22,g:1},{n:"MLCC",v:1.76,g:1},
      {n:"陶瓷基板",v:1.74,g:1},{n:"电子布",v:1.73,g:1},{n:"中兵系",v:1.61,g:2},
      {n:"印巴冲突概念",v:1.25,g:2},{n:"昨日涨停",v:1.02,g:3},{n:"中国建材集团",v:0.92,g:3},
      {n:"铜缆高速连接器",v:0.83,g:1},{n:"博通概念",v:0.72,g:1},{n:"5.5G",v:0.68,g:1},
      {n:"科特估",v:0.52,g:3},{n:"光纤概念",v:0.48,g:1},{n:"昨日连板",v:0.38,g:3},
      {n:"昨日首板",v:0.31,g:3}
    ];
    var c3=echarts.init(el3,null,{renderer:"canvas"});
    c3.setOption({
      animation:false,
      textStyle:{fontFamily:FONT,color:"#3C4854",fontSize:11},
      tooltip:{trigger:"axis",axisPointer:{type:"shadow"},backgroundColor:NAVY,borderWidth:0,
        textStyle:{color:"#fff",fontSize:11.5},
        formatter:function(ps){var p=ps[0];
          return p.name+"<br/>涨跌幅：+"+p.value.toFixed(2)+"%";}},
      title:titleOpt("概念板块涨跌幅 TOP 16",
        "红色＝PCB/被动元件链　金色＝军工　蓝色＝情绪指标"),
      grid:{left:126,right:74,top:56,bottom:16},
      xAxis:{type:"value",
        min:0,
        axisLabel:{fontFamily:FONT,fontSize:10,color:"#6B7785",
          formatter:function(v){return v+"%";}},
        splitLine:{lineStyle:{color:"#EEF2F6"}},
        axisLine:{show:false},axisTick:{show:false}},
      yAxis:{type:"category",inverse:true,
        data:con.map(function(r){return r.n;}),
        axisLabel:{fontFamily:FONT,fontSize:10.8,color:"#3C4854"},
        axisTick:{show:false},
        axisLine:{lineStyle:{color:"#DDE3EA"}}},
      series:[{
        type:"bar",
        barWidth:"56%",
        data:con.map(function(r){
          var col = r.g===1?UP : (r.g===2?GOLD : BLUE);
          return {
            value:r.v,
            itemStyle:{color:col,borderRadius:[0,3,3,0]},
            label:{show:true,position:"right",distance:5,
              fontFamily:FONT,fontSize:10,color:col,fontWeight:"bold",
              formatter:"+"+r.v.toFixed(2)+"%"}
          };
        })
      }]
    });
    charts.push(c3);
  }

  window.addEventListener("resize",function(){charts.forEach(function(c){c.resize();});});
  requestAnimationFrame(function(){
    charts.forEach(function(c){c.resize();});
    setTimeout(function(){window.__chartsReady=true;},300);
  });
})();
