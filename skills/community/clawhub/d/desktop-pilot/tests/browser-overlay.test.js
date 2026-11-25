// Isolated DOM contract test: page UI must not expose cancellation authority.
const {readFileSync} = require('fs');
const {join} = require('path');
const vm = require('vm');
const assert = require('assert/strict');
let markup = '', timerCallback, attached = 0;
const label = {textContent:''};
const root = {set innerHTML(s) {markup=s;}, querySelector:s=>s==='.txt'?label:null};
const window = {};
const context = {window, document:{
  createElement:()=>({setAttribute(){},attachShadow:()=>root,remove(){attached--;}}),
  documentElement:{appendChild(){attached++;}}
},setTimeout:fn=>{timerCallback=fn;return 1;},clearTimeout(){}};
const source=readFileSync(join(__dirname,'../scripts/browser/overlay.js'),'utf8');
vm.runInNewContext(source,context);
const api=window.__dpOverlay;
assert.deepEqual(Object.keys(api),['show','text','hide','visible']);
api.show('Testing');assert.equal(api.visible(),true);assert.equal(label.textContent,'Testing');
api.text('<script>bad()</script>');assert.equal(label.textContent,'<script>bad()</script>');
assert(!markup.includes('class="stop"'));assert(!markup.includes('<script>'));
assert.equal(api.stopped,undefined);assert.equal(api.clear,undefined);
assert(Object.isFrozen(api));assert.equal(Object.getOwnPropertyDescriptor(window,'__dpOverlay').writable,false);
api.show('Again');assert.equal(attached,1);timerCallback();assert.equal(api.visible(),false);
api.text('New');assert.equal(api.visible(),true);api.hide();assert.equal(attached,0);
vm.runInNewContext(source,context);assert.equal(window.__dpOverlay,api);
console.log('PASS: status rendering, text-only updates, repeat injection, watchdog, immutable API; no page-owned cancellation');
