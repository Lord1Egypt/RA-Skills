import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 配置 - 修改这些参数
const CONFIG = {
  entryPoint: './src/index.ts',  // 入口文件
  compositionId: 'MyVideo',       // Composition ID
  outputDir: './out',             // 输出目录
  outputFile: 'video.mp4',        // 输出文件名
  codec: 'h264',                  // 编码器
  fps: 30,                         // 帧率
  // Chrome 浏览器路径 (可选，留空自动检测)
  browserExecutable: '',
  // 端口配置 (可选，0 表示自动选择)
  port: 0,
};

async function main() {
  console.log('🎬 Edu Video Generator');
  console.log('📦 Bundling...');

  const bundled = await bundle({
    entryPoint: path.join(__dirname, CONFIG.entryPoint),
    outDir: path.join(__dirname, CONFIG.outputDir, 'bundle'),
  });

  console.log('🔍 Getting composition...');
  
  const composition = await selectComposition({
    serveUrl: bundled,
    id: CONFIG.compositionId,
    // 浏览器和端口配置
    ...(CONFIG.browserExecutable && { browserExecutable: CONFIG.browserExecutable }),
    ...(CONFIG.port && { port: CONFIG.port }),
    preferIpv4: true,
  });

  console.log(`📐 Composition: ${composition.id}`);
  console.log(`   Duration: ${composition.durationInFrames} frames (${(composition.durationInFrames / composition.fps).toFixed(1)}s)`);

  console.log('🎥 Rendering...');
  
  await renderMedia({
    composition,
    serveUrl: bundled,
    codec: CONFIG.codec,
    outputLocation: path.join(__dirname, CONFIG.outputDir, CONFIG.outputFile),
    // 浏览器和端口配置
    ...(CONFIG.browserExecutable && { browserExecutable: CONFIG.browserExecutable }),
    ...(CONFIG.port && { port: CONFIG.port + 1 }),
    preferIpv4: true,
    chromiumOptions: {
      disableWebSecurity: true,
    },
  });

  console.log(`✅ Done! Output: ${CONFIG.outputDir}/${CONFIG.outputFile}`);
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
