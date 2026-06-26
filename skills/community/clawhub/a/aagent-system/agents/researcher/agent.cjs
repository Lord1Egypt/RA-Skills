#!/usr/bin/env node
const {exec} = require('child_process');
const AGENT = 'researcher';
function log(m){console.log(`[${AGENT}] ${m}`);}
function wait(ms){return new Promise(r=>setTimeout(r,ms));}

async function research(){
  try{
    await new Promise((r,e)=>exec('~/aass-scripts/daily_intel.sh 2>&1',{timeout:600000},(ex,out)=>ex?e(ex):r(out)));
    log('研究完成');
  }catch(e){log('err:'+e.message);}
}

async function loop(){
  log('启动');
  while(true){
    await research();
    await wait(3600000+Math.random()*1800000);
  }
}
loop();
