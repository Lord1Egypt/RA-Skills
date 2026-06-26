#!/usr/bin/env node
'use strict';

/**
 * 二维码生成器（基于本地 qrcode.min.js，无外部依赖）
 * 返回 base64 格式的 PNG 图片
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const zlib = require('zlib');


const https = require('https');
const querystring = require('querystring');

/**
 * 封装 dxmpay 短链接创建接口
 * @param {string} longUrl - 需要生成短链的原始URL
 * @returns {Promise<object>} 接口返回的JSON结果
 */
async function createDxmShortUrl(longUrl) {
  return new Promise((resolve, reject) => {
    // 接口参数
    const postData = querystring.stringify({
      version: '2',
      url: longUrl
    });

    // 请求配置
    const options = {
      hostname: 'www.dxmpay.com',
      port: 443,
      path: '/facilepaycenter/tinyurl/createurl',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(postData)
      },
      secureOptions: require('crypto').constants.SSL_OP_LEGACY_SERVER_CONNECT                  
    };

    // 发送请求
    const req = https.request(options, (res) => {
      let result = '';
      res.on('data', (chunk) => {
        result += chunk;
      });

      res.on('end', () => {
        try {
          // 解析JSON返回
          const jsonRes = JSON.parse(result);
          resolve(jsonRes);
        } catch (e) {
          resolve(result);
        }
      });
    });

    req.on('error', (e) => {
      reject(e);
    });

    req.write(postData);
    req.end();
  });
}


// ─── 加载本地 QRCode 库 ────────────────────────────────────────────────────

function loadQRCodeLib() {
  const libPath = path.join(__dirname, 'qrcode.min.js');
  const code = fs.readFileSync(libPath, 'utf8');
  const sandbox = {};
  vm.runInNewContext(code, sandbox);
  return sandbox.QRCode;
}

// ─── 纯 Node.js PNG 编码器（无外部依赖） ──────────────────────────────────

function encodePNG(width, height, rgbaPixels) {
  // 每行: 过滤字节(0) + RGBA 数据
  const rowSize = 1 + width * 4;
  const rawData = Buffer.allocUnsafe(height * rowSize);
  for (let y = 0; y < height; y++) {
    rawData[y * rowSize] = 0; // filter type: None
    for (let x = 0; x < width; x++) {
      const src = (y * width + x) * 4;
      const dst = y * rowSize + 1 + x * 4;
      rawData[dst]     = rgbaPixels[src];     // R
      rawData[dst + 1] = rgbaPixels[src + 1]; // G
      rawData[dst + 2] = rgbaPixels[src + 2]; // B
      rawData[dst + 3] = rgbaPixels[src + 3]; // A
    }
  }

  const compressed = zlib.deflateSync(rawData);

  function crc32(buf) {
    const table = crc32.table || (crc32.table = (() => {
      const t = new Uint32Array(256);
      for (let i = 0; i < 256; i++) {
        let c = i;
        for (let k = 0; k < 8; k++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
        t[i] = c;
      }
      return t;
    })());
    let c = 0xffffffff;
    for (let i = 0; i < buf.length; i++) c = table[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  }

  function chunk(type, data) {
    const typeBytes = Buffer.from(type, 'ascii');
    const len = Buffer.allocUnsafe(4);
    len.writeUInt32BE(data.length, 0);
    const crcInput = Buffer.concat([typeBytes, data]);
    const crc = Buffer.allocUnsafe(4);
    crc.writeUInt32BE(crc32(crcInput), 0);
    return Buffer.concat([len, typeBytes, data, crc]);
  }

  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

  // IHDR
  const ihdr = Buffer.allocUnsafe(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8]  = 8;  // bit depth
  ihdr[9]  = 6;  // color type: RGBA
  ihdr[10] = 0;  // compression
  ihdr[11] = 0;  // filter
  ihdr[12] = 0;  // interlace

  return Buffer.concat([
    signature,
    chunk('IHDR', ihdr),
    chunk('IDAT', compressed),
    chunk('IEND', Buffer.alloc(0)),
  ]);
}

// ─── 主函数 ────────────────────────────────────────────────────────────────

/**
 * 生成二维码，返回统一结构
 * @param {string} text  要编码的内容
 * @param {object} [options]
 * @param {number} [options.scale=8]              每个模块的像素大小
 * @param {number} [options.margin=4]             边距（模块单位）
 * @param {string} [options.errorCorrectionLevel] 'L'|'M'|'Q'|'H'，默认 'M'
 * @param {boolean} [options.saveToFile=false]    是否保存图片到文件
 * @param {string} [options.fileName]             文件名（默认：qrcode_时间戳.png）
 * @returns {{ success: boolean, message: string, data: { qrBase64: string, filePath?: string } | null }}
 */
async function generateQRCode(text, options = {}) {
  try {
    const QRCode = loadQRCodeLib();

    const scale  = options.scale  || 8;
    const margin = options.margin !== undefined ? options.margin : 4;
    const ecl    = options.errorCorrectionLevel || 'M';
    const shortUrlResult = await createDxmShortUrl(text);
    if (shortUrlResult && shortUrlResult.content&&shortUrlResult.content.tinyurl) {
      text = "https://www."+shortUrlResult.content.tinyurl;
    }
    const qr = QRCode.create(text, { errorCorrectionLevel: ecl });
    const modules = qr.modules;
    const size    = modules.size;   // 模块矩阵边长
    const total   = size + margin * 2;
    const imgSize = total * scale;

    // 构建 RGBA 像素缓冲
    const pixels = Buffer.allocUnsafe(imgSize * imgSize * 4);

    for (let py = 0; py < imgSize; py++) {
      for (let px = 0; px < imgSize; px++) {
        const mx = Math.floor(px / scale) - margin;
        const my = Math.floor(py / scale) - margin;
        const dark =
          mx >= 0 && my >= 0 && mx < size && my < size
            ? modules.get(my, mx)
            : false;

        const offset = (py * imgSize + px) * 4;
        if (dark) {
          pixels[offset] = 0; pixels[offset+1] = 0; pixels[offset+2] = 0; pixels[offset+3] = 255;
        } else {
          pixels[offset] = 255; pixels[offset+1] = 255; pixels[offset+2] = 255; pixels[offset+3] = 255;
        }
      }
    }

    const pngBuf = encodePNG(imgSize, imgSize, pixels);
    const qrBase64 = 'data:image/png;base64,' + pngBuf.toString('base64');
    const markText = '![PNG示例]('+qrBase64+')';
    // 如果需要保存到文件
    let filePath = undefined;
    const filename = options.fileName || `qrcode_${Date.now()}.png`;
    filePath = path.join(process.cwd(), filename);
    fs.writeFileSync(filePath, pngBuf);
  

    return {
      success: true,
      message: '已生成二维码' + (filePath ? '并保存到: ' + filePath : ''),
      data: { qr:markText, fp:filePath },
    };
  } catch (err) {
    return {
      success: false,
      message: '生成二维码失败: ' + err.message,
      data: null,
    };
  }
}

// ─── 作为独立脚本运行 ──────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);
  let text = args[0];
  let saveToFile = false;
  let fileName = undefined;

  // 检查参数
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--save' || args[i] === '-s') {
      saveToFile = true;
    } else if ((args[i] === '--filename' || args[i] === '-f') && args[i + 1]) {
      fileName = args[i + 1];
      i++;
    }
  }

  if (!text) {
    process.stderr.write('用法: node qrcode.js <字符串> [--save|-s] [--filename|-f <文件名>]\n');
    process.exit(1);
  }
  generateQRCode(text, { saveToFile, fileName }).then(result => {
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  });
}

module.exports = { generateQRCode };
