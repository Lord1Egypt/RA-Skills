import test from 'node:test';import assert from 'node:assert/strict';
import {doctor} from '../scripts/doctor.mjs';
import {backgroundCapability} from '../scripts/runtime.mjs';
function fixture(backgroundExecution=true){return {calls:[],async browsers(){return [{browserId:'private-id',displayName:'chrome',online:true}]},async command(id,action){this.calls.push(action);if(action==='list_tabs')return [];if(action==='capabilities')return {features:{backgroundExecution}};throw Error('must not navigate')}}}
test('doctor verifies readiness without opening pages or returning browser identities',async()=>{
 const bridge=fixture({default:true,ordinaryCommandsNoWindowActivation:true}),report=await doctor({platforms:['baidu','google']},{bridge});assert.equal(report.status,'ready');assert.equal(report.routes.length,2);assert.equal(report.routes[0].backgroundExecution,true);assert.ok(!JSON.stringify(report).includes('private-id'));assert.ok(!bridge.calls.includes('navigate'));
});
test('explicit missing environment and unsupported background execution require attention',async()=>{
 const missing=await doctor({platforms:['baidu'],browserMap:{baidu:'missing'}},{bridge:fixture()});assert.equal(missing.status,'needs_attention');assert.equal(missing.routes[0].online,false);
 const unsupported=await doctor({platforms:['baidu']},{bridge:fixture({default:false})});assert.equal(unsupported.status,'needs_attention');assert.equal(unsupported.checks[0].code,'background_execution_unavailable');
 assert.equal(backgroundCapability(undefined),null);
});
