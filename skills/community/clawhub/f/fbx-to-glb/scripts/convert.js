/**
 * FBX → GLB 无损转换工具 (Node.js CLI)
 * 使用 assimpjs (Assimp WASM) 实现高质量转换，完整保留贴图、材质、骨骼、动画。
 *
 * 用法:
 *   node convert.js input.fbx
 *   node convert.js input.fbx -o output.glb
 *   node convert.js input.fbx --embed-textures
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log(`
FBX → GLB 无损转换工具 (基于 assimpjs)

用法:
  node convert.js <input.fbx> [选项]

选项:
  -o, --output <path>   输出文件路径 (默认: 同目录同名 .glb)
  --force               强制覆盖已存在的输出文件
  --help, -h            显示帮助

示例:
  node convert.js model.fbx
  node convert.js model.fbx -o output.glb
  node convert.js model.fbx --force
`);
  process.exit(0);
}

let inputPath = null;
let outputPath = null;
let force = false;

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '-o' || arg === '--output') {
    outputPath = args[++i];
  } else if (arg === '--force') {
    force = true;
  } else if (!arg.startsWith('-')) {
    inputPath = arg;
  }
}

if (!inputPath) {
  console.error('错误: 请指定输入 FBX 文件路径');
  process.exit(1);
}

if (!fs.existsSync(inputPath)) {
  console.error(`错误: 文件不存在: ${inputPath}`);
  process.exit(1);
}

const inputExt = path.extname(inputPath).toLowerCase();
if (inputExt !== '.fbx') {
  console.warn(`警告: 输入文件不是 .fbx 格式 (${inputExt})，将继续尝试...`);
}

if (!outputPath) {
  outputPath = path.join(path.dirname(inputPath), path.basename(inputPath, inputExt) + '.glb');
}

if (fs.existsSync(outputPath) && !force) {
  console.error(`错误: 输出文件已存在: ${outputPath}`);
  console.error('  使用 --force 覆盖');
  process.exit(1);
}

function formatSize(bytes) {
  for (const unit of ['B', 'KB', 'MB', 'GB']) {
    if (bytes < 1024) return `${bytes.toFixed(1)} ${unit}`;
    bytes /= 1024;
  }
  return `${bytes.toFixed(1)} TB`;
}

async function main() {
  console.log(`\n${'='.repeat(60)}`);
  console.log('FBX → GLB 转换器 (assimpjs)');
  console.log(`${'='.repeat(60)}`);

  const inputSize = fs.statSync(inputPath).size;
  console.log(`\n[1/3] 读取文件...`);
  console.log(`  输入: ${inputPath}`);
  console.log(`  大小: ${formatSize(inputSize)}`);

  // Load assimpjs
  console.log(`\n[2/3] 初始化转换引擎...`);
  const t0 = Date.now();

  let ajs;
  try {
    ajs = await require('assimpjs')();
  } catch (err) {
    // Try alternative require paths
    try {
      const assimpjs = require('assimpjs');
      ajs = await assimpjs();
    } catch (err2) {
      console.error(`\n❌ 无法加载 assimpjs: ${err2.message}`);
      console.error('\n请先安装: npm install assimpjs');
      process.exit(1);
    }
  }

  console.log(`  引擎就绪 (${Date.now() - t0}ms)`);
  console.log(`  正在解析 FBX...`);

  // Read input file
  const fileBuffer = fs.readFileSync(inputPath);

  // Create file list and add FBX file
  const fileList = new ajs.FileList();
  const fileName = path.basename(inputPath);
  fileList.AddFile(fileName, new Uint8Array(fileBuffer));

  // Convert to GLB (binary glTF 2.0)
  console.log(`  正在转换...`);
  let result;
  try {
    result = ajs.ConvertFileList(fileList, 'glb2');
  } catch (err) {
    console.error(`\n❌ 转换失败: ${err.message}`);
    process.exit(1);
  }

  if (!result || !result.IsSuccess || !result.IsSuccess()) {
    const errMsg = result ? result.GetErrorCode() : '未知错误';
    console.error(`\n❌ 转换失败: ${errMsg}`);
    if (errMsg && errMsg.includes('format')) {
      console.error('  提示: 文件格式可能不受支持，请检查 FBX 文件是否完整');
    }
    process.exit(1);
  }

  const fileCount = result.FileCount();
  if (fileCount === 0) {
    console.error('\n❌ 转换未生成任何输出文件');
    process.exit(1);
  }

  console.log(`  转换完成，生成 ${fileCount} 个输出文件`);

  // Write output - get the first GLB file
  console.log(`\n[3/3] 写入输出...`);

  for (let i = 0; i < fileCount; i++) {
    const resultFile = result.GetFile(i);
    const resultName = resultFile.GetPath();
    const resultContent = resultFile.GetContent();

    // Determine output path
    let outPath;
    if (fileCount === 1) {
      outPath = outputPath;
    } else {
      // Multiple output files (e.g., textures in separate files)
      const ext = path.extname(resultName) || '.bin';
      const base = path.basename(outputPath, '.glb');
      outPath = path.join(path.dirname(outputPath), `${base}_${i}${ext}`);
    }

    // Ensure directory exists
    const dir = path.dirname(outPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(outPath, Buffer.from(resultContent));
    const outSize = fs.statSync(outPath).size;
    console.log(`  输出: ${outPath}`);
    console.log(`  大小: ${formatSize(outSize)}`);
  }

  const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
  const outputSize = fs.statSync(outputPath).size;

  console.log(`\n${'='.repeat(60)}`);
  console.log(`✅ 转换成功!`);
  console.log(`  耗时: ${elapsed}s`);
  console.log(`  输出: ${outputPath}`);
  console.log(`  大小: ${formatSize(outputSize)}`);
  console.log(`  压缩比: ${(outputSize / inputSize * 100).toFixed(1)}%`);
  console.log(`${'='.repeat(60)}\n`);
}

main().catch(err => {
  console.error(`\n❌ 致命错误: ${err.message}`);
  console.error(err.stack);
  process.exit(1);
});
