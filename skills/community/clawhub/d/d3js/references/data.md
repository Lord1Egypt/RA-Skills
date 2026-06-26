# D3 Data Processing

## CSV/TSV

```js
d3.csv("data.csv", d3.autoType).then(d=>{...})  // auto type inference
d3.csv("data.csv", ({n,v})=>({n,v:+v}))          // manual conversion
d3.csvParse("foo,bar\n1,2")                      // parse string
d3.csvFormat([{foo:1,bar:2}])                    // serialize
d3.dsvFormat("|").parse("foo|bar\n1|2")          // custom delimiter
d3.tsvParse / .tsvFormat / .tsv
```

## Other Loading Methods

```js
d3.json("data.json") / .text("file.txt")
d3.html("page.html") / .xml("data.xml")
d3.image("img.png", {crossOrigin:"anonymous"})
d3.blob("file.bin") / .buffer("file.bin")
```

## Number Formatting

```js
d3.format(",.")(1234.56)      // "1,235"
d3.format("$,")(1234.56)      // "$1,235"
d3.format(".2%")(0.123)       // "12.30%"
d3.format("~s")(1500000)      // "1.5M"
d3.formatPrefix(",.0",1e3)(1500) // "1,500"
// [[fill]align][sign][sym][0][width][,][.prec][~][type]
// type: e/f/g/%/s/d/x
```

## Time Intervals (d3-time)

```js
d3.timeMillisecond / .timeSecond / .timeMinute / .timeHour
d3.timeDay / .timeWeek / .timeMonth / .timeYear
// UTC: d3.utcDay / .utcMonth ...

interval.floor(date) / .ceil(date) / .round(date)
interval.offset(date, n) / .range(start, stop, step)
interval.count(start, end) / .every(step)

d3.timeDay.count(start, end)       // actual days
d3.timeMonth.every(3).range(s, e)  // quarterly
```

## Time Formatting

```js
d3.timeParse("%Y-%m-%d")("2023-01-15")   // parse
d3.utcParse("%Y-%m-%d")("2023-01-15")
d3.timeFormat("%B %d, %Y")(new Date())    // "May 31, 2026"
d3.isoFormat / .isoParse                  // ISO 8601
// directives: %Y/%m/%d/%H/%M/%S/%f/%L/%a/%A/%b/%B/%p/%j
// padding: %0(zero)/%_(space)/%-(none)
```