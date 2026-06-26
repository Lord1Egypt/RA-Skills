import fs from 'fs';
import path from 'path';

export async function generate_image(args) {
    const endpoint = process.env.COMFYUI_ENDPOINT || "http://127.0.0.1:8188";
    const workflowPath = path.join(process.env.WORKFLOW_PATH, "text2image-1.json");
    
    // 讀取你的 JSON 工作流
    const workflow = JSON.parse(fs.readFileSync(workflowPath, 'utf-8'));
    
    // 修改節點 6 的提示詞
    workflow["6"].inputs.text = prompt;
    // 隨機產生種子避免重複
    workflow["3"].inputs.seed = Math.floor(Math.random() * 1000000000);

    const response = await fetch(`${endpoint}/prompt`, {
        method: 'POST',
        body: JSON.stringify({ prompt: workflow })
    });

    if (response.ok) {
        return "指令已發送至 ComfyUI，開始生成圖片！";
    } else {
        return `發送失敗：${response.statusText}`;
    }
}
