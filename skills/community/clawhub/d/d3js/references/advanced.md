# D3 Advanced Modules

## Array Statistics (d3-array)

```js
d3.min/max/extent/mean/median/sum/deviation/variance/count(data)
d3.quantile(data,.25) / .rank(data) / .cumsum(data)
d3.group(data,d=>d.cat)                        // Map
d3.rollup(data,v=>d3.sum(v,d=>d.val),d=>d.cat) // reduce
d3.groupSort(data,g=>d3.sum(g,d=>d.val),d=>d.cat) // sorted keys
d3.sort(data) / .range(0,10,2) / .ticks(0,100,10)
d3.shuffle / .pairs / .permute / .cross / .merge / .zip
d3.union / .intersection / .difference
```

## Interpolators (d3-interpolate)

```js
d3.interpolateNumber(10,20)(0.5)             // 15
d3.interpolateLab("steelblue","brown")(.5)    // color interpolation
d3.interpolate({a:1},{a:2})(0.5)              // objects
d3.interpolateZoom(p0,p1)(0.5)                // zoom
d3.interpolateRgb / .interpolateHsl / .interpolateString
d3.interpolateArray / .interpolateObject
d3.interpolateTransformSvg
```

## Color

```js
const c = d3.color("steelblue");
c.r / .g / .b / .opacity / .darker(.5) / .brighter(.5)
d3.schemeCategory10 / .schemeAccent / .schemePaired / .schemeSet1 / .schemeTableau10
d3.schemePastel1 / .schemePastel2 / .schemeSet2 / .schemeSet3 / .schemeDark2
d3.interpolateViridis / .interpolateMagma / .interpolateInferno / .interpolatePlasma
d3.interpolateBlues / .interpolateReds / .interpolateGreens
d3.interpolateRdBu / .interpolateBrBG / .interpolateRdYlGn / .interpolateSpectral
d3.schemeBlues[3] / .schemeRdYlGn[6]   // multi-level discrete
```

## Random Numbers (d3-random)

```js
d3.randomUniform / .randomInt / .randomNormal / .randomLogNormal
d3.randomBates / .randomIrwinHall / .randomExponential
d3.randomPareto / .randomBernoulli / .randomGeometric / .randomBinomial
d3.randomPoisson / .randomGamma / .randomBeta / .randomWeibull
d3.randomCauchy / .randomLogistic
// reproducible
d3.randomNormal.source(d3.randomLcg(42))(0,1)
```

## Events & Timer

```js
const d = d3.dispatch("start","end");
d.on("start",fn) / .on("start.foo",fn) / .on(".foo",null)  // register/remove
d.call("start") / .call("start",that,arg) / .apply(...)     // fire

d3.timer((elapsed)=>{if(elapsed>200)t.stop()},150)  // repeat
d3.timeout(fn,1000)   // one-shot (like setTimeout)
d3.interval(fn,500)   // interval (like setInterval)
d3.now()              // frame-consistent time
d3.timerFlush()       // immediately fire zero-delay timers
```

## Polygons (d3-polygon)

```js
d3.polygonArea([[1,1],[1.5,0],[2,1]])       // area
d3.polygonCentroid(...)                       // centroid
d3.polygonHull(points)                        // convex hull
d3.polygonContains(poly, point)               // contains
d3.polygonLength(poly)                        // perimeter
```

## Quadtree (d3-quadtree)

```js
d3.quadtree().x(d=>d.x).y(d=>d.y).addAll(points)
tree.add(d) / .remove(d) / .find(x,y,radius)   // nearest neighbor
tree.visit((n,x0,y0,x1,y1)=>{if(cond)return true}) // pre-order
tree.visitAfter / .root / .data / .size / .extent / .copy
```

## Chord (d3-chord)

```js
const chord = d3.chord().padAngle(.05).sortGroups(d3.descending);
const ch = chord(matrix);  // compute chord+group
d3.ribbon().radius(200)(chords)               // ribbon generator
d3.arc().innerRadius(210).outerRadius(220)    // arc segments
```

## Delaunay / Voronoi (d3-delaunay)

```js
const d = d3.Delaunay.from(data, d=>d.x, d=>d.y);
d.voronoi([xmin,ymin,xmax,ymax])  // voronoi diagram
d.find(x,y) / .neighbors(i)       // nearest point/neighbors
d.hull / .triangles / .halfedges  // geometry data
d.render(context)                  // Canvas rendering
```

## Contours (d3-contour)

```js
d3.contourDensity().x(d=>x(d.x)).y(d=>y(d.y)).weight(d=>d.w)
  .size([w,h]).bandwidth(20).thresholds(20)(data)
// returns GeoJSON-format contours, render with d3.geoPath()
```

## Force-Directed Graph (d3-force)

```js
d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d=>d.id).distance(100))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(w/2,h/2))
  .force("collide", d3.forceCollide(30))
  .force("x", d3.forceX(w/2)).force("y", d3.forceY(h/2))
  .on("tick", ()=> {
    link.attr("x1",d=>d.s.x).attr("y1",d=>d.s.y)
        .attr("x2",d=>d.t.x).attr("y2",d=>d.t.y);
    node.attr("cx",d=>d.x).attr("cy",d=>d.y);
  });
sim.restart() / .stop() / .alpha(1).restart()
```

## Hierarchy Layout (d3-hierarchy)

```js
// from nested objects
d3.hierarchy(data).sum(d=>d.value).sort((a,b)=>b.value-a.value)
// from flat table
d3.stratify().id(d=>d.id).parentId(d=>d.parentId)(table)

d3.tree().size([w,h])                          // tree diagram
d3.cluster().size([w,h])                       // dendrogram (same-depth leaves)
d3.treemap().size([w,h]).padding(2)             // treemap
d3.pack().size([w,h]).padding(5)                // circle pack
d3.partition().size([w,h])                      // partition
d3.partition().size([2*Math.PI,radius])         // sunburst

root.descendants() / .links() / .leaves()
root.path(target) / .ancestors() / .each(fn) / .eachAfter(fn)
```

## Geography (d3-geo)

```js
d3.geoMercator().center([104,35]).scale(800)  // Mercator
d3.geoAlbersUsa() / .geoOrthographic() / .geoEqualEarth()
d3.geoNaturalEarth1() / .geoAzimuthalEquidistant()

d3.geoPath().projection(proj)                  // path generator
proj([lng,lat]) / .invert([x,y])               // coordinate conversion

d3.json("us-10m.json").then(d=>{
  svg.selectAll("path").data(topojson.feature(d,d.objects.states).features)
    .join("path").attr("d",d3.geoPath().projection(proj));
})
```

## Zoom (d3-zoom)

```js
d3.zoom().scaleExtent([.5,10]).on("zoom",ev=>{
  g.attr("transform", ev.transform);  // ev.transform: {x,y,k}
});
svg.call(zoom);
svg.call(zoom.transform, d3.zoomIdentity);          // reset
svg.call(zoom.scaleTo, 2);                          // scale to
svg.call(zoom.translateBy, 100, 50);                // translate
const t = d3.zoomTransform(svg.node());              // current transform
svg.on("wheel.zoom", null);                          // disable scroll zoom

// linked axes
.on("zoom", ev=>{ gx.call(d3.axisBottom(ev.transform.rescaleX(x))); })
```

## Brush (d3-brush)

```js
d3.brush().extent([[0,0],[w,h]]).on("end",ev=>{
  if(ev.selection){ const [[x0,y0],[x1,y1]]=ev.selection; /* filter */ }
});
d3.brushX() / .brushY()
svg.call(brush.move, [[50,50],[200,200]])  // set
svg.call(brush.move, null)                 // clear
d3.brushSelection(svg.node())              // get

// Focus+Context
d3.brushX().extent([[0,0],[w,h]]).on("brush",ev=>{
  x.domain((ev.selection||x2.range()).map(x2.invert,x2));
  focus.select(".area").attr("d",area);
});
```

## Drag (d3-drag)

```js
d3.drag()
  .on("start", ev=>{ d3.select(this).raise(); })
  .on("drag", ev=>{ d3.select(this).attr("cx",ev.x).attr("cy",ev.y); })
  .on("end", ev=>{});

// with force simulation
.call(d3.drag()
  .on("start",(ev,d)=>{ if(!ev.active) sim.alphaTarget(.3).restart(); d.fx=d.x;d.fy=d.y; })
  .on("drag",(ev,d)=>{ d.fx=ev.x;d.fy=ev.y; })
  .on("end",(ev,d)=>{ if(!ev.active) sim.alphaTarget(0); d.fx=null;d.fy=null; }));
```