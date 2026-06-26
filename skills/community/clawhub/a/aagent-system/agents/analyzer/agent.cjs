#!/usr/bin/env node
const {exec} = require('child_process');
const AGENT = 'analyzer';
function log(m){console.log(`[${AGENT}] ${m}`);}
function wait(ms){return new Promise(r=>setTimeout(r,ms));}

async function analyze(){
  try{
    await new Promise((r,e)=>exec('~/aass-scripts/3layer_scheduler.sh analyzer 2>&1',{timeout:300000},(ex,out)=>ex?e(ex):r(out)));
    log('分析完成');
  }catch(e){log('err:'+e.message);}
}

async function loop(){
  log('启动');
  while(true){
    await analyze();
    await wait(600000+Math.random()*300000);
  }
}
loop();
