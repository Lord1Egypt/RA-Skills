import fs from "fs";
import readline from "readline";
import { chain } from 'stream-chain';
import process from 'process';
import { parser } from 'stream-json';
import { streamArray } from 'stream-json/streamers/StreamArray';
import path from 'path';
import { PublicKey } from '@solana/web3.js';
import axios from 'axios';
import JSONStream from 'JSONStream';
import Decimal from 'decimal.js';

export const fsPromises = fs.promises;


type StreamReadCSVCallbackFunc = (line: string, idx: number) => void;
type StreamReadCSVCallbackFuncV2 = (obj: Record<string, string>, srcLine: string) => void;

export function streamReadCSV(
  fileName: string,
  callbackFunc: StreamReadCSVCallbackFunc
) {
  return new Promise((resolve, reject) => {
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
        callbackFunc(line, count)
      } catch (err) {
        console.error(err);
      }
    });

    rl.on('close', () => {
      console.log('');
      console.log('File reading completed.');
      resolve(null);
    });
  })
}

export function isStringNumber(nb: string) {
  if (!nb) {
    return false;
  }

  try {
    if (nb.toLowerCase().includes('e+')) {
      return false;
    }
    if (nb.toLowerCase().includes('e-')) {
      return false;
    }
  } catch (err) {
    throw new Error(`Invalid amount: ${String(err)}, ${nb}`)
  }

  try {
    new Decimal(nb);
    return true;
  } catch (err) {
    return false;
  }
}

export function streamReadCSVUpdated(
  fileName: string,
  callbackFunc: StreamReadCSVCallbackFuncV2
) {
  return new Promise((resolve, reject) => {
    const fileStream = fs.createReadStream(fileName);

    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity,
    });

    let count = 0;
    let headers: string[] = [];

    rl.on('line', (line) => {
      count++;
      process.stdout.write(`${count}\r`);

      if (!line) {
        return;
      }

      const arr = line.split(',');
      if (count === 1) {
        headers = arr.concat([]).map(it => it.trim());
        return;
      }

      const obj: Record<string, string> = {};
      headers.forEach((hdName, idx) => {
        obj[hdName] = arr[idx]?.trim() || '';
      });

      try {
        callbackFunc(obj, line);
      } catch (err) {
        console.error(err);
      }
    });

    rl.on('close', () => {
      console.log('');
      console.log('File reading completed.');
      resolve(null);
    });
  })
}


export function sleep(seconds: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    }, seconds * 1000);
  });
}


export type StreamReadCallbackFunc = (item: any) => any;

export function streamReadJSONArrayFile(
  fPath: string,
  callback: StreamReadCallbackFunc
) {
  return new Promise((resolve, reject) => {
    const pipeline = chain([
      fs.createReadStream(fPath),
      parser(),
      streamArray(),
    ]);

    pipeline.on('data', ({key, value}) => {
      process.stdout.write(`${key}, ${typeof value}\r`);
      try {
        callback(value);
      } catch (err) {
        console.error(err)
      }
    });

    pipeline.on('end', () => {
      console.log('');
      resolve(null);
    });
  })
}


export function streamReadJSONKVFile (
  filePath: string,
  callback: StreamReadCallbackFunc
) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not exist: ${filePath}`);
  }

  return new Promise((resolve, reject) => {
    const stream = fs.createReadStream(filePath, { encoding: 'utf8' });
    const parser = JSONStream.parse('$*');

    let count = 0;
    stream
      .pipe(parser)
      .on('data', (dd: any) => {
        count++;
        process.stdout.write(`${count}\r`);
        const key = dd.key as string;
        const value = dd.value as any;
        const obj: Record<string, unknown> = {};
        obj[key] = value;
        callback(obj);
      })
      .on('end', () => {
        console.log('');
        resolve(null);
      })
      .on('error', (err: any) => {
        console.log('');
        console.log(err);
        resolve(null);
      });
  });
}


export async function getDirFiles(dir: string) {
  let results: string[] = [];
  try {
    const files = await fsPromises.readdir(dir, { withFileTypes: true });
    for (const file of files) {
      const fullPath = path.join(dir, file.name);
      if (file.isDirectory()) {
        const subFiles = await getDirFiles(fullPath);
        results = results.concat(subFiles);
      } else {
        results.push(fullPath);
      }
    }
  } catch (error) {
    console.error(`Error reading directory ${dir}:`, error);
  }
  return results;
}


export async function writeAllocationCSV(
  dataMap: Record<string, string>,
  pathName: string,
  parsedEther?: boolean,
) {
  console.log('Writing CSV: ', pathName);
  fs.writeFileSync(
    pathName,
    'address,allocation\n',
  );
  for (let [address, allocation] of Object.entries(dataMap)) {
    if (parsedEther) {
      allocation = new Decimal(allocation).mul(10**18).toFixed(0);
    }
    fs.appendFileSync(
      pathName,
      `${address},${allocation}\n`,
    );
  }
}


export function isSolanaAddress(address: string): boolean {
  try {
    new PublicKey(address);
    return true;
  } catch (_err) {
    return false;
  }
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
