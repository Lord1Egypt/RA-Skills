import fs from 'fs';
import readline from 'readline';

export function sleep(seconds: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(), seconds * 1000);
  });
}

export function streamReadLines(
  fileName: string,
  callbackFunc: (line: string, idx: number) => void,
) {
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(fileName)) {
      reject(new Error(`File not found: ${fileName}`));
      return;
    }

    const fileStream = fs.createReadStream(fileName);
    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity,
    });

    let count = 0;
    rl.on('line', (line) => {
      if (!line) {
        return;
      }
      count++;
      process.stdout.write(`${count}\r`);
      try {
        callbackFunc(line, count);
      } catch (err) {
        console.error(err);
      }
    });

    rl.on('close', () => {
      console.log('');
      console.log('File reading completed.');
      resolve(null);
    });
  });
}

export async function readFileLastLine(filePath: string) {
  const fd = await fs.promises.open(filePath, 'r');
  const stat = await fd.stat();
  const fileSize = stat.size;

  let buffer = Buffer.alloc(1);
  let lastLine = '';
  let position = fileSize - 1;

  while (position >= 0) {
    await fd.read(buffer, 0, 1, position);
    const char = buffer.toString();

    if (char === '\n' && position !== fileSize - 1) {
      break;
    }
    lastLine = char + lastLine;
    position--;
  }

  await fd.close();
  return lastLine;
}
