#!/usr/bin/env node
const {exec} = require('child_process');
const AGENT = process.env.AGENT_NAME || 'scanner';
const INDEX = process.env.AGENT_INDEX || 0;
function log(m){console.log(`[${AGENT}-${INDEX}] ${m}`);}
function wait(ms){return new Promise(r=>setTimeout(r,ms));}

async function scan(){
  try{
    await new Promise((r,e)=>exec('~/aass-dataset/secure_dataset.sh scan 2>&1',{timeout:180000},(ex,out)=>ex?e(ex):r(out)));
    log('扫描完成');
  }catch(e){log('err:'+e.message);}
}

async function loop(){
  log('启动');
  while(true){
    await scan();
    await wait(300000+Math.random()*120000);
  }
}
loop();
