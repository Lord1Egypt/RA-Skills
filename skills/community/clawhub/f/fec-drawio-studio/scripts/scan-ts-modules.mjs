#!/usr/bin/env node
import{parseArgs as r,printOrWrite as t}from"./studio-core.mjs";import{scanModules as n}from"./scan-js-modules.mjs";const s=r(process.argv.slice(2)),o=n(s._[0]??".",[".ts",".tsx",".mts",".cts",".js",".jsx",".mjs",".cjs"]);t(`${JSON.stringify(o,null,2)}
`,s.output);
