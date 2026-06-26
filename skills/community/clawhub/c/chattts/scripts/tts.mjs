import { parseArgs } from 'node:util';

async function main() {
  try {
    // 1. 定义命令行参数的解析规则
    const options = {
      seed: { type: 'string' },
      temperature: { type: 'string' },
      top_p: { type: 'string' },
    };

    // 解析 OpenClaw 传过来的参数 (Node.js v18.3.0+ 原生支持)
    const { values, positionals } = parseArgs({
      args: process.argv.slice(2),
      options,
      allowPositionals: true
    });

    const text = positionals[0];
    if (!text) {
      console.error("❌ 错误：请提供需要转换的文本内容。");
      process.exit(1);
    }

    // 2. 获取后台 API 地址，默认指向你的 Python FastAPI 端口
    const apiUrl = process.env.CHATTTS_API_URL || 'http://172.23.252.114:8020';

    // 3. 构造请求负载
    const payload = {
      text: text,
      seed: values.seed ? parseInt(values.seed) : 2048,
      // 注意：如果想让下面这两个参数生效，你的 Python FastAPI 的 TTSRequest 模型里也需要加上这两个字段
      temperature: values.temperature ? parseFloat(values.temperature) : 0.7,
      top_p: values.top_p ? parseFloat(values.top_p) : 0.7
    };

    // 4. 发送请求到 Python 服务端
    const response = await fetch(`${apiUrl}/v1/audio/speech`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    // 5. 将结果输出给 OpenClaw Agent
    if (data.status === 'success') {
      // 成功时，必须输出文件路径，OpenClaw 会捕获这个输出并把音频发给用户
      console.log(data.file_path);
    } else {
      console.error(`❌ 语音生成失败: ${data.message}`);
      process.exit(1);
    }

  } catch (error) {
    console.error(`❌ 无法连接到 ChatTTS 服务，请检查 8080 端口是否在运行: ${error.message}`);
    process.exit(1);
  }
}

main();