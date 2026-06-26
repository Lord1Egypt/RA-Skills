/**
 * Test: Multi-layer Memory System
 */
const { AILoop } = require('./ai_loop_ws.js');
const PLAYER_UID = 'c7c7460c0_10001';
const GOAL = '去新手村找村长';

console.log('=== Start AI Loop Test ===\n');

const ai = new AILoop(PLAYER_UID, 'curious');

console.log('Daily file:', ai.daily.file);
console.log('Curated file:', ai.curated.file);
console.log('Curated summary before:', ai.curated.getSummary());
console.log('');

ai.setGoal(GOAL);
ai.start();

console.log('\nRunning 90s...\n');

setTimeout(() => {
    ai.stop();
    console.log('\n=== After Run ===');
    console.log('Daily events:', ai.daily.getAllEvents().length);
    console.log('Curated:', ai.curated.getDescription());
    process.exit(0);
}, 90000);
