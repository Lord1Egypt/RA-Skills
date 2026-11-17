// 压缩 rollout 的透明读取。
//
// Codex 会把归档会话压成 `<rollout>.jsonl.zst`（~/.codex/archived_sessions），
// 部分未归档会话也会被就地压缩。压缩过的文件 grep 不到、`readFile` 读出乱码，
// 所以所有按文件读会话的地方都要走这里。
//
// 只用 node:zlib 的 zstd（Node 22.15 起有）。此前还留了一条系统 `zstd` CLI 的
// 回退，现在删了：package.json 的 engines 已收紧到 >=22.15，回退分支永远走不到，
// 留着只让依赖清单多一个外部二进制。
import { createReadStream } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { createInterface } from 'node:readline';
import { createZstdDecompress } from 'node:zlib';

export const isCompressed = (file) => /\.zst$/i.test(file);

function viaZlib(file) {
  if (typeof createZstdDecompress !== 'function') {
    throw new Error(
      'node:zlib 没有 zstd 支持，需要 Node 22.15 以上（当前 ' + process.version + '）'
    );
  }
  return createReadStream(file).pipe(createZstdDecompress());
}

async function collect(stream) {
  const chunks = [];
  for await (const c of stream) chunks.push(c);
  return Buffer.concat(chunks);
}

// 整体读成字符串。只用于小文件；大文件（几十 MB 压缩、解压后可能上 GB）
// 用 lines() 流式走，避免撞上 V8 的字符串长度上限。
export async function readText(file) {
  if (!isCompressed(file)) return readFile(file, 'utf8');
  return (await collect(viaZlib(file))).toString('utf8');
}

async function* readLines(stream) {
  const rl = createInterface({ input: stream, crlfDelay: Infinity });
  try {
    for await (const line of rl) yield line;
  } finally {
    rl.close();
    if (typeof stream.destroy === 'function') stream.destroy();
  }
}

// 逐行异步迭代，普通文件与 .zst 一致。
export async function* lines(file) {
  if (!isCompressed(file)) {
    yield* readLines(createReadStream(file));
    return;
  }
  yield* readLines(viaZlib(file));
}
