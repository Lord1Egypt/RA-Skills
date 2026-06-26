// src/core/embedding-worker.js
const { parentPort, workerData } = require('worker_threads');

/**
 * 嵌入计算后台线程
 * 负责：模型下载、初始化、推理计算
 * 避免阻塞主线程（Agent 响应流）
 */
async function initialize() {
    try {
        // 动态导入，减小启动开销
        const { pipeline } = await import('@xenova/transformers');
        
        const modelId = workerData.modelId || 'Xenova/all-MiniLM-L6-v2';
        
        // 初始化进度回调（模拟）
        parentPort.postMessage({ type: 'status', message: 'Loading model...' });

        const extractor = await pipeline('feature-extraction', modelId, {
            progress_callback: (info) => {
                if (info.status === 'progress') {
                    parentPort.postMessage({ 
                        type: 'progress', 
                        file: info.file, 
                        loaded: info.loaded, 
                        total: info.total 
                    });
                }
            }
        });

        parentPort.postMessage({ type: 'ready' });

        // 监听来自主线程的任务请求
        parentPort.on('message', async (task) => {
            if (task.type === 'vectorize') {
                try {
                    const output = await extractor(task.text, {
                        pooling: 'mean',
                        normalize: true
                    });
                    const vector = Array.from(output.data);
                    parentPort.postMessage({ type: 'result', id: task.id, vector });
                } catch (err) {
                    parentPort.postMessage({ type: 'error', id: task.id, message: err.message });
                }
            }
        });

    } catch (err) {
        parentPort.postMessage({ type: 'error', message: `Initialization failed: ${err.message}` });
    }
}

initialize();
