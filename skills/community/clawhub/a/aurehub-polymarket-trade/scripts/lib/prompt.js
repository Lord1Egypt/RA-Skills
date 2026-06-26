import readline from 'readline';

export async function confirm(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    let answered = false;
    rl.question(`${question} `, answer => {
      answered = true;
      rl.close();
      resolve(answer.trim().toLowerCase() === 'yes');
    });
    // Only resolve false on close if the question callback hasn't already answered
    // (handles EOF / stdin closed before user responds).
    // Without this guard, rl.close() in the question callback emits 'close' synchronously,
    // resolving false before the answer-based resolve fires.
    rl.once('close', () => { if (!answered) resolve(false); });
  });
}
