# ECharts API Reference

## Global Configuration Options

| Option | Type | Default | Description |
|-------|------|-------|------|
| backgroundColor | string | 'transparent' | Canvas background color |
| animation | boolean | true | Enable animation |
| animationDuration | number | 1000 | Animation duration (ms) |
| animationEasing | string | 'cubicOut' | Easing function |

## title

```js
title: {
  text: 'Main Title',
  subtext: 'Subtitle',
  left: 'center',
  textStyle: { color: '#333', fontSize: 18, fontWeight: 'bold' }
}
```

## tooltip

```js
tooltip: {
  trigger: 'axis',
  axisPointer: { type: 'line' },
  backgroundColor: 'rgba(50,50,50,0.9)',
  textStyle: { color: '#fff' }
}
```

## legend

```js
legend: { data: ['Series A','Series B'], left: 'right', orient: 'vertical' }
```

## grid

```js
grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true }
```

## xAxis / yAxis

```js
xAxis: {
  type: 'category',
  data: ['Mon','Tue','Wed'],
  name: 'X Axis Name',
  axisLine: { lineStyle: { color: '#333' } },
  splitLine: { show: false }
}
```

## dataZoom

```js
dataZoom: [
  { type: 'slider', start: 0, end: 100 },
  { type: 'inside', start: 0, end: 100 }
]
```

## visualMap

```js
visualMap: {
  min: 0, max: 100,
  calculable: true,
  inRange: { color: ['#50a3ba','#eac736','#d94e5d'] },
  right: 0, top: 'middle'
}
```

## series Types

### bar

```js
series: [{
  type: 'bar',
  data: [5, 20, 36],
  barWidth: '50%',
  itemStyle: {
    color: new echarts.graphic.LinearGradient(0,0,0,1,[
      { offset: 0, color: '#83bff6' },
      { offset: 1, color: '#188df0' }
    ]),
    borderRadius: [4,4,0,0]
  }
}]
```

### line

```js
series: [{
  type: 'line',
  data: [5, 20, 36],
  smooth: 0.3,
  lineStyle: { width: 2 },
  areaStyle: { color: 'rgba(84,112,198,0.2)' },
  symbol: 'circle', symbolSize: 6
}]
```

### pie

```js
series: [{
  type: 'pie',
  radius: '55%',
  center: ['50%','60%'],
  data: [{ value: 335, name: 'Direct' }],
  label: { show: true, formatter: '{b}: {d}%' }
}]
```

### scatter

```js
series: [{
  type: 'scatter',
  data: [[172,68],[168,62],[177,75]],
  symbolSize: 12,
  itemStyle: { color: 'rgba(84,112,198,0.5)' }
}]
```

### gauge

```js
series: [{
  type: 'gauge',
  startAngle: 180, endAngle: 0,
  min: 0, max: 100, splitNumber: 8,
  axisLine: { lineStyle: { width: 6, color: [[0.25,'#91CC75'],[0.5,'#FAC858'],[1,'#d94e5d']] } },
  pointer: { width: 5, length: '70%' },
  detail: { formatter: '{value}%', fontSize: 28, offsetCenter: [0,'70%'] },
  data: [{ value: 67, name: 'Completion Rate' }]
}]
```

## echarts.init

```js
var chart = echarts.init(document.getElementById('main'));
var chart = echarts.init(dom, 'dark');
var chart = echarts.init(dom, null, { renderer: 'svg' });
```

## Common Methods

```js
chart.setOption(option);
chart.resize();
chart.getDataURL({ type: 'png', pixelRatio: 2 });
chart.clear();
chart.dispose();
echarts.connect('myGroup');
```

## Gradient Configuration

```js
new echarts.graphic.LinearGradient(0,0,0,1,[
  { offset: 0, color: '#83bff6' },
  { offset: 1, color: '#188df0' }
]);
```

## Official References

- Official Documentation: https://echarts.apache.org/handbook/en/get-started/
- Configuration Manual: https://echarts.apache.org/en/option.html
- Examples Gallery: https://echarts.apache.org/examples/en/index.html