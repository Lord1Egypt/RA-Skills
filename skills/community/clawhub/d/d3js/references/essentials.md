# D3 Core Essentials

## Selections

```js
d3.select("div") / .selectAll("circle")   // select
selection.attr("fill","red") / .style("opacity",.8) // attributes
.text("hello") / .classed("active",true)  // text/class
.append("g") / .remove() / .raise()       // structure
.datum(d) / .node()                       // data/native node
```

## Data Join

```js
// enter/update/exit
const c = svg.selectAll("circle").data(data);
c.enter().append("circle").attr("r",d=>d);  // enter
c.attr("r",d=>d);                            // update
c.exit().remove();                           // exit

// join shorthand
svg.selectAll("circle").data(data).join("circle").attr("r",d=>d);

// key function
selection.data(data, d => d.id);
```

## Scales & Color Schemes

```js
d3.scaleLinear().domain([0,100]).range([0,500])       // linear
d3.scaleUtc().domain([d1,d2]).range([0,500])          // time
d3.scaleBand().domain(["A","B"]).range([0,w]).padding(.2) // band
d3.scalePoint().domain(["A","B"]).range([0,w])         // point
d3.scaleOrdinal().domain(["x","y"]).range(["r","b"])   // ordinal
d3.scaleLog() / .scalePow().exponent(.5) / .scaleSymlog()
d3.scaleSequential(d3.interpolateViridis)

// color schemes
d3.schemeCategory10 / .schemeTableau10          // categorical
d3.interpolateViridis / .interpolateBlues       // sequential
d3.interpolateRdBu / .interpolateRdYlGn        // diverging
```

## Axes

```js
d3.axisBottom(x) / .axisLeft(y) / .axisTop(x) / .axisRight(y)
axis.ticks(10) / .tickFormat(d=>d+"%") / .tickValues([0,50,100])
axis.tickSize(6) / .tickPadding(6)
d3.timeMonth.every(3)    // time tick interval
```

## Shapes

```js
d3.line().x(d=>x(d.date)).y(d=>y(d.value)).curve(d3.curveMonotoneX)
d3.area().x(d=>x(d.date)).y0(y(0)).y1(d=>y(d.value))
d3.arc().innerRadius(0).outerRadius(200)    // inner>0=donut
d3.pie().value(d=>d.value).sort(null)
d3.symbol().type(d3.symbolCircle).size(64)  // Circle/Cross/Diamond/Square/Star/Tri/Wye
d3.stack().keys(["a","b"])
// curves: curveLinear/MonotoneX/Cardinal/Basis/Step/Natural/CatmullRom
```

## Transitions & Easing

```js
selection.transition().duration(750).delay((d,i)=>i*20)
  .ease(d3.easeCubicInOut).attr("r",20)
  .on("start",fn).on("end",fn)
// chaining: .transition().attr(...).transition().attr(...)

d3.easeLinear / .easeQuad / .easeCubic / .easeSin
d3.easeExp / .easeCircle / .easeElastic / .easeBack / .easeBounce
// Each has In/Out/InOut variants
d3.easeElastic.amplitude(1.5).period(0.4)  // elastic params
d3.easePoly.exponent(4)                     // polynomial exponent
```

## Path

```js
const p = d3.path(); p.moveTo(10,10); p.lineTo(200,200);
p.arc(80,80,70,0,Math.PI*2); p.rect(10,10,50,50); p.closePath();
p.toString();  // "M10,10L200,200..."
d3.pathRound(3)  // round to 3 decimal places
```

## Margin Convention

```js
const m = {top:20,right:30,bottom:40,left:50};
const w = 800-m.left-m.right, h = 500-m.top-m.bottom;
const svg = d3.select("#chart").append("svg")
  .attr("width", w+m.left+m.right).attr("height", h+m.top+m.bottom)
  .append("g").attr("transform",`translate(${m.left},${m.top})`);
```

## Chart Templates

### Line Chart
```js
svg.append("path").datum(data).attr("fill","none").attr("stroke","steelblue")
  .attr("d", d3.line().x(d=>x(d.date)).y(d=>y(d.value)).curve(d3.curveMonotoneX)(data));
svg.append("g").call(d3.axisBottom(x).ticks(w/80)).attr("transform",`translate(0,${h})`);
svg.append("g").call(d3.axisLeft(y));
```

### Bar Chart
```js
svg.selectAll("rect").data(data).join("rect")
  .attr("x",d=>x(d.name)).attr("y",d=>y(d.value))
  .attr("width",x.bandwidth()).attr("height",d=>h-y(d.value)).attr("fill","steelblue");
```

### Scatter Plot
```js
svg.selectAll("circle").data(data).join("circle")
  .attr("cx",d=>x(d.x)).attr("cy",d=>y(d.y)).attr("r",4).attr("fill","steelblue").attr("opacity",0.7);
```

### Pie Chart
```js
const g = d3.select("#chart").append("svg").attr("w",500).attr("h",500)
  .append("g").attr("transform","translate(250,250)");
g.selectAll("path").data(d3.pie().value(d=>d.value).sort(null)(data)).join("path")
  .attr("d",d3.arc().innerRadius(80).outerRadius(200))
  .attr("fill",(d,i)=>d3.schemeTableau10[i]);
```

## React Integration

```jsx
// declarative (recommended, D3 computation only)
export default function Plot({data}) {
  const x = d3.scaleLinear([0,data.length-1],[40,620]);
  const y = d3.scaleLinear(d3.extent(data),[380,20]);
  const line = d3.line((d,i)=>x(i),y);
  return <svg width={640} height={400}>
    <path fill="none" stroke="currentColor" d={line(data)} />
    {data.map((d,i)=><circle key={i} cx={x(i)} cy={y(d)} r="2.5"/>)}
  </svg>;
}
// useEffect pattern: use ref for d3-selection operations
```

## Svelte Integration

```svelte
<script>
  import * as d3 from 'd3';
  export let data;
  $: x = d3.scaleLinear([0,data.length-1],[40,620]);
  $: y = d3.scaleLinear(d3.extent(data),[380,20]);
  $: line = d3.line((d,i)=>x(i),y);
</script>
<svg width=640 height=400>
  <path fill="none" stroke="currentColor" d={line(data)} />
  {#each data as d,i}<circle cx={x(i)} cy={y(d)} r="2.5"/>{/each}
</svg>
```