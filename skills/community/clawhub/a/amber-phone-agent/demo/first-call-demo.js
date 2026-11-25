const readline = require('node:readline/promises');

async function main() {
  console.log(`
Amber for OpenClaw · Simulated phone task
This walkthrough uses fictional dialogue. It makes no network requests or phone calls.

You → OpenClaw
“Call Lakeside Auto and ask when my car will be ready and what I need to bring.”

OpenClaw → You
Proposed call: Lakeside Auto (+1 202-555-0142)
Ask for the pickup time and anything you need to bring.
`);
  const terminal = readline.createInterface({ input: process.stdin, output: process.stdout });
  const approval = await terminal.question('Approve this simulated call? [y/N] ');
  terminal.close();
  if (!['y', 'yes'].includes(approval.trim().toLowerCase())) {
    console.log('Call declined.');
    return;
  }

  console.log(`
Simulated call excerpt
Amber: When will the car be ready for pickup, and what should the owner bring?
Shop: It’ll be ready after 4 p.m. today. Please bring a photo ID.
Amber: Is there a cutoff for pickup?
Shop: We close at 6 p.m.

OpenClaw → You
Lakeside Auto confirmed pickup today between 4 and 6 p.m.
Bring a photo ID. The shop didn’t ask you to call back.
`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
